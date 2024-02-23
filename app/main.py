import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QSpinBox
import csv
from gmail import GmailAPI

class EmailSender(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.user_data = []
        self.data_data = []
        self.dataFile = None
        self.userFile = None
        self.credentialsFile = None
        self.numEmails = None
        self.userCreationFile = None

    def initUI(self):
        self.setGeometry(200, 200, 800, 700)
        self.setWindowTitle('Email Sender')
        self.setFixedSize(700, 700)

        self.lblData = QLabel('Select data.csv file:', self)
        self.lblData.move(20, 20)

        self.btnData = QPushButton('Browse', self)
        self.btnData.move(150, 15)
        self.btnData.clicked.connect(self.browseData)

        self.lblUser = QLabel('Select user.csv file:', self)
        self.lblUser.move(20, 60)

        self.btnUser = QPushButton('Browse', self)
        self.btnUser.move(150, 55)
        self.btnUser.clicked.connect(self.browseUser)

        self.lblSenderEmail = QLabel('Sender Email:', self)
        self.lblSenderEmail.move(20, 100)

        self.txtSenderEmail = QLineEdit(self)
        self.txtSenderEmail.move(150, 95)

        self.lblSubject = QLabel('Email Subject:', self)
        self.lblSubject.move(20, 140)

        self.txtSubject = QLineEdit(self)
        self.txtSubject.move(150, 135)

        self.lblBody = QLabel('Email Body:', self)
        self.lblBody.move(20, 180)

        self.txtBody = QTextEdit(self)
        self.txtBody.setGeometry(150, 175, 400, 150)

        self.lblNumEmails = QLabel('Number of Emails:', self)
        self.lblNumEmails.move(20, 340)

        self.spinNumEmails = QSpinBox(self)
        self.spinNumEmails.move(150, 335)
        self.spinNumEmails.setMinimum(1)
        self.spinNumEmails.setMaximum(100000000)

        self.lblCredentials = QLabel('Select credentials.json file:', self)
        self.lblCredentials.move(20, 380)

        self.btnCredentials = QPushButton('Browse', self)
        self.btnCredentials.move(180, 375)
        self.btnCredentials.clicked.connect(self.browseCredentials)

        self.btnSend = QPushButton('Send Emails', self)
        self.btnSend.setGeometry(350, 420, 200, 40)
        self.btnSend.clicked.connect(self.sendEmails)

        # New widgets for user information and user creation
        self.lblUserCreation = QLabel('Create Users from CSV:', self)
        self.lblUserCreation.move(20, 460)

        self.btnUserCreation = QPushButton('Browse', self)
        self.btnUserCreation.move(180, 455)
        self.btnUserCreation.clicked.connect(self.browseUserCreation)

        self.btnCreateUsers = QPushButton('Create Users', self)
        self.btnCreateUsers.setGeometry(350, 455, 200, 40)
        self.btnCreateUsers.clicked.connect(self.createUsers)


        self.show()

    
    def browseData(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open Data File', '', 'CSV Files (*.csv)')
        if fileName:
            self.dataFile = fileName

    def browseUser(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open User File', '', 'CSV Files (*.csv)')
        if fileName:
            self.userFile = fileName

    def browseCredentials(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open Credentials File', '', 'JSON Files (*.json)')
        if fileName:
            self.credentialsFile = fileName

    def browseUserCreation(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open User Creation File', '', 'CSV Files (*.csv)')
        if fileName:
            self.userCreationFile = fileName

    def createUsers(self):
        print('create user function')
        with open(self.userFile, 'r') as user_file:
                user_reader = csv.reader(user_file)
                next(user_reader)  # Skip header
                for row in user_reader:
                    self.user_data.append(row)

        for user in self.user_data:
            gmail_api = GmailAPI(self.credentialsFile)
            access_token = gmail_api.auth(user[0], user[1])
            try:
                with open(self.userCreationFile, 'r') as user_creation_file:
                    user_creation_reader = csv.reader(user_creation_file)
                    next(user_creation_reader)  # Skip header
                    i = 0
                    for row in user_creation_reader:
                        i+=1
                        print(row,"_",i) 
                        new_user_data = {
                            "name": {
                                "givenName":  row[2],
                                "familyName":  row[3],
                            },
                            "password": row[1],
                            "primaryEmail": row[0],
                            "changePasswordAtNextLogin": False
                        }
                        gmail_api.create_user(access_token=access_token,user_data=new_user_data)
            except Exception as e:
                print("An error occurred during user creation:", e)


    def sendEmails(self):
        try:
            with open(self.userFile, 'r') as user_file:
                user_reader = csv.reader(user_file)
                next(user_reader)  # Skip header
                for row in user_reader:
                    self.user_data.append(row)

            # Read data file and store data in self.data_data list
            with open(self.dataFile, 'r') as data_file:
                data_reader = csv.reader(data_file)
                next(data_reader)  # Skip header
                for row in data_reader:
                    self.data_data.append(row[0])
            
            sender = self.txtSenderEmail.text()
            subject = self.txtSubject.text()
            message_html = self.txtBody.toPlainText()
            
            num_emails = self.spinNumEmails.value()

            start_index = 0
            end_index = start_index+num_emails

            for user in self.user_data:
                gmail_api = GmailAPI(self.credentialsFile)
                access_token = gmail_api.auth(user[0], user[1])
                to_list = self.data_data[start_index:end_index]
                gmail_api.send_emails_(access_token, sender, to_list, subject, message_html)
                start_index += num_emails
                end_index = start_index+num_emails
                
        except Exception as e:
            print("An error occurred app :", e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmailSender()
    sys.exit(app.exec_())
    
