"""Send emails to a csv file of recipients with an attachment and a "body.html" template"""
from __future__ import annotations

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from os import getenv

import smtplib
import ssl
import pandas as pd

from tqdm import tqdm
from dotenv import load_dotenv


# Add your .env file path
load_dotenv(".env") # load .env file
PASSWORD = getenv("16_DIGIT_PSWD") # App password from gmail
USERNAME = getenv("MAIL_USERNAME") # Gmail address
ATTACHMENT_PATH = getenv("ATTACHMENT_PATH") # Path to the attachment
RECIPIENTS_PATH = getenv("RECIPIENTS_PATH") # Path to the csv file with recipients data

SERVER_NAME = "smtp.gmail.com"
SERVER_PORT = 465

# Pandas column names
CIVILITE = "civilite"
NOM = "nom"
PRENOM = "prenom"
MAIL = "mail"

def write_body(html_path : str, civilite : str, nom: str, prenom : str) -> str:
    """Write the body of the email with the html template and the data from the csv file"""
    with open(html_path, "r",encoding="utf-8") as f:
        body = f.read()
        body = body.replace(r"{civilite}",civilite)
        body = body.replace(r"{nom}",nom)
        body = body.replace(r"{prenom}",prenom)
        return body

def import_csv(file_name : str, sep : str = ',') -> pd.DataFrame:
    """Import a csv file with recipients data and return a pandas dataframe"""
    df = pd.read_csv(file_name, sep=sep)
    return df

def import_attachment(file_name : str) -> MIMEApplication:
    """Import an attachment and return a MIMEApplication object"""
    with open(file_name, "rb") as f:
        part = MIMEApplication(f.read(), Name=basename(file_name))
        part.add_header('Content-Disposition', 'attachment', filename=file_name)
        return part

def send_emails(
destinataires_path : str,
attachment_path : str,
body_path : str,
subject : str
) -> None:
    """Send emails to the recipients in the csv file"""
    dests = import_csv(destinataires_path, sep = ';')
    for i in tqdm(range(len(dests))):
        msg = MIMEMultipart()
        body = write_body(body_path,dests[CIVILITE][i],dests[NOM][i],dests[PRENOM][i])
        msg["from"] = USERNAME
        msg["to"] = dests[MAIL][i]
        msg["subject"] = subject
        msg.attach(MIMEText(body, "html"))
        msg.attach(import_attachment(attachment_path))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SERVER_NAME, SERVER_PORT, context=context) as server:
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, dests[MAIL][i], msg.as_string())


if __name__ == '__main__':
    subject = "Test publipostage V1"
    print(PASSWORD,USERNAME,ATTACHMENT_PATH,RECIPIENTS_PATH)
    print(type(PASSWORD))
    send_emails(RECIPIENTS_PATH,ATTACHMENT_PATH, body_path= "body.html",subject = subject)
