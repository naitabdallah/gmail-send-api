# Email Sender Application

## Overview
The Email Sender Application is a Python-based desktop tool designed to send personalized emails to a list of recipients using Gmail's API. It offers functionality to select recipient data from a CSV file, compose email content, and send emails efficiently. Additionally, the application provides the capability to create user accounts using the Gmail API.

## Features
- Browse and select CSV files containing recipient data and user information.
- Input sender email address, email subject, and email body.
- Specify the number of emails to send per batch.
- Select credentials JSON file for Gmail API authentication.
- Create new user accounts using CSV file inputs.
- Utilizes Selenium and requests libraries for Gmail API integration.

## Installation and Setup
### Prerequisites
- Python 3.x installed on your system.
- Ensure `pip` is installed for Python package management.
- WebDriver for your browser (e.g., Chrome WebDriver) in your system PATH.
- Gmail API credentials JSON file.

### Installation Steps
1. Clone or download the repository to your local machine:
    ```bash
    cd  gmail-api
    ```
2. Install required Python packages using `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
3. Ensure your WebDriver is installed and accessible.

## Usage
1. Launch the application by executing `main.py`:
    ```bash
    python main.py
    ```
2. Browse and select the necessary CSV files for recipient data, user information, and credentials.
3. Enter the sender's email address, email subject, and compose the email body.
4. Specify the number of emails to send per batch using the spinner.
5. Click on the "Create Users" button to create new user accounts if required.
6. Click on the "Send Emails" button to initiate the email sending process.

## Important Notes
- Ensure that your Gmail account from which you're sending emails allows access to less secure apps or uses the OAuth 2.0 protocol for authentication.
- Be cautious with sharing and storing credentials and user data files.

## Contributions and Issues
Contributions to enhance the application's functionality or address issues are welcome. Please feel free to open a pull request or submit an issue detailing any problems you encounter.
