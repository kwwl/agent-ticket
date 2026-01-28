from __future__ import print_function
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def send_mail(subject, message):
    creds = None
    # token.pickle contient les jetons d'accès
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(message)
    message["to"] = "ticketmailclass@gmail.com"
    message["subject"] = subject

    create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    send_message = (
        service.users().messages().send(userId="me", body=create_message).execute()
    )

    print("Email envoyé :", send_message)


if __name__ == "__main__":
    send_mail(subject="Test Gmail API", message="Ceci est un email automatique.")
