from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import requests
import time
import json

class GmailAPI:
    def __init__(self, credentials_file):
        with open(credentials_file) as f:
            self.credentials = json.load(f)

        self.CLIENT_ID = self.credentials['web']['client_id']
        self.CLIENT_SECRET = self.credentials['web']['client_secret']
        self.REDIRECT_URI = self.credentials['web']['redirect_uris'][0]
        self.SCOPES = ['https://mail.google.com/','https://www.googleapis.com/auth/admin.directory.user']
    
    def auth(self, email, password):
        driver = webdriver.Chrome()
        authorization_url = f'https://accounts.google.com/o/oauth2/auth?client_id={self.CLIENT_ID}&redirect_uri={self.REDIRECT_URI}&scope={"%20".join(self.SCOPES)}&response_type=code&access_type=offline'
        driver.get(authorization_url)

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'identifierId'))
        )
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'Passwd'))
        )

        WebDriverWait(driver, 10).until(EC.visibility_of(password_input))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'Passwd')))

        password_input.send_keys(password, Keys.RETURN)

        allow_button = WebDriverWait(driver, 500).until(
            EC.element_to_be_clickable((By.ID, 'submit_approve_access'))
        )
        allow_button.click()

        time.sleep(5)  

        authorization_code = driver.current_url.split('code=')[1]
        driver.quit()

        token_url = 'https://oauth2.googleapis.com/token'
        payload = {
            'code': authorization_code,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'redirect_uri': self.REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        response = requests.post(token_url, data=payload)
        tokens = response.json()
        return tokens['access_token']
    
    def send_emails_(self, access_token, sender, to_list, subject, message_html):
        if not access_token:
            raise ValueError("Access token is required.")
        if not sender:
            raise ValueError("Sender email address is required.")
        if not to_list:
            raise ValueError("Recipient list is empty.")
        if not subject:
            raise ValueError("Email subject is required.")
        if not message_html:
            raise ValueError("Email message content is required.")

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        email_address = ''
        try:
            profile_response = requests.get(
                'https://gmail.googleapis.com/gmail/v1/users/me/profile',
                headers=headers
            )
            profile_response.raise_for_status()
            profile_data = profile_response.json()
            email_address = profile_data['emailAddress']
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching user profile: {e}")
            return

        batch_size = 100 
        num_batches = (len(to_list) + batch_size - 1) // batch_size 

        emails_sent = 0
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(to_list))
            bcc_list = to_list[start_idx:end_idx]

            bcc_header = f"Bcc: {', '.join(bcc_list)}\n"
            raw_message = (
                f"From: {sender} <{email_address}>\n"
                f"{bcc_header}"
                f"Subject: {subject}\n"
                f"MIME-Version: 1.0\n"
                f"Content-Type: text/html; charset=utf-8\n\n"
                f"{message_html}"
            )
            message = {
                'raw': base64.urlsafe_b64encode(raw_message.encode()).decode()
            }
            
            try:
                response = requests.post(
                    'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
                    headers=headers,
                    json={"raw": message['raw']}
                )
                response.raise_for_status()
                emails_sent += len(bcc_list)
                print(f"{len(bcc_list)} Emails sent successfully!")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while sending email: {e}")

        print(f"Total {emails_sent} emails sent successfully!")

        
    def create_user(self, access_token, user_data):
        # Construct the request URL
        create_user_url = f"https://www.googleapis.com/admin/directory/v1/users?access_token={access_token}"

        # Send a POST request to create a new user
        response = requests.post(create_user_url, json=user_data)

        if response.status_code == 200:
            print("User created successfully.")
            return response.json()
        else:
            print("Error creating user:", response.text)
            return None
        
    import requests

    def delete_all_users(self, access_token, domain):
        if not access_token:
            raise ValueError("Access token is required.")

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        print(f"delete users {domain} access token : {access_token}")
        try:
            next_page_token = None
            while True:
                url = f"https://www.googleapis.com/admin/directory/v1/users?domain={domain}"
                if next_page_token:
                    url += f"&pageToken={next_page_token}"

                response = requests.get(url,headers)
                response.raise_for_status()
                data = response.json()
                users = data.get('users', [])
                print("Users found in this page:", len(users))

                for user in users:
                    user_key = user['id']
                    delete_user_url = f"https://www.googleapis.com/admin/directory/v1/users/{user_key}"
                    delete_response = requests.delete(delete_user_url, headers=headers)
                    
                    if delete_response.status_code == 204:
                        print(f"User {user_key} deleted successfully.")
                    else:
                        print(f"Error deleting user {user_key}: {delete_response.text}")

                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    break

        except requests.exceptions.RequestException as e:
            print("Error listing or deleting users:", e)
