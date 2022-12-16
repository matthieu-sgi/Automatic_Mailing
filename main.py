"""Send emails to a csv file of recipients with an attachment and a "body.html" template"""

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from os import getenv

import smtplib
import ssl
import time

from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm
from unidecode import unidecode


# Add your .env file path
load_dotenv(".env") # load .env file
PASSWORD = getenv("16_DIGIT_PSWD") # App password from gmail
USERNAME = getenv("MAIL_USERNAME") # Gmail address
ATTACHMENT_PATH = getenv("ATTACHMENT_PATH") # Path to the attachment
RECIPIENTS_PATH = getenv("RECIPIENTS_PATH") # Path to the csv file with recipients data

SERVER_NAME = "smtp.gmail.com"
SERVER_PORT = 465

# Pandas column names
CIVILITE = "Salutation"#"civilite" # Mr, Mme, Mlle  #Prenom,Nom,Mail
NOM = "Nom" # Last name
PRENOM = "Prenom" # First name
MAIL = "Mail" # Email address

def write_body(html_path : str, civilite : str, nom: str, prenom : str) -> str:
    """Write the body of the email with the html template and the data from the csv file"""
    with open(html_path, "r",encoding="utf-8") as f:
        body = f.read()
        # print(body.encode("utf-8"))
        if str(civilite) != "nan":
            body = body.replace(r"{civilite}", " " + str(civilite).replace(" ",""))
        else:
            body = body.replace(r"{civilite}","")

        if str(nom) != "nan":
            body = body.replace(r"{nom}", " " + str(nom).replace(" ",""))
        else:
            body = body.replace(r"{nom}","")

        if str(prenom) != "nan" :
            body = body.replace(r"{prenom}", " " + str(prenom).replace(" ",""))
        else:
            body = body.replace(r"{prenom}","")

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
subject : str,
sep : str = ','
) -> None:
    """Send emails to the recipients in the csv file"""
    dests = import_csv(destinataires_path, sep = sep)
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(SERVER_NAME, SERVER_PORT, context=context)
    server.login(USERNAME, PASSWORD)
    for i in tqdm(range(len(dests))):     
        if str(dests[MAIL][i]) != "nan":
            msg = MIMEMultipart()
            body = write_body(body_path,dests[CIVILITE][i],dests[NOM][i],dests[PRENOM][i])
            msg["from"] = USERNAME
            dest_email = str(dests[MAIL][i]).replace(" ","")
            # dest to lower case
            dest_email = dest_email.lower()
            dest_email = unidecode(dest_email)
            msg["to"] = dest_email
            msg["subject"] = subject
            msg.attach(MIMEText(body, "html"))
            msg.attach(import_attachment(attachment_path))
            # print("no mail sent")
            try :
                server.sendmail(USERNAME, dest_email, msg.as_string())
            except smtplib.SMTPRecipientsRefused:
                print("Refused")
            except smtplib.SMTPSenderRefused:
                print("Sender refused")
                time.sleep(140)
                server = smtplib.SMTP_SSL(SERVER_NAME, SERVER_PORT, context=context)
                server.login(USERNAME, PASSWORD)





if __name__ == '__main__':
    subject = "Candidat pour reprise B.SEGUI"

    send_emails(RECIPIENTS_PATH,ATTACHMENT_PATH, body_path= "body.html",subject = subject)
