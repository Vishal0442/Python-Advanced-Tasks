
import smtplib, ssl
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv

# Collecting Sender Email details
sender = input("Type email address of sender press Enter : ",)
password = input("Type your email password and press Enter : ",)

# Add path of Email list file (CSV / Excel)
mail_list_file = ""

# Add path of Attachment file (PDF file for this example)
attachment = ""


def get_contact_list(filename):
    contacts={}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for name, email in reader:
            contacts[name] = email
    return contacts


def mailsender(sender, to, name, password):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = "Attachment Python Test Email"

    text = f"""
    Hi {name}

    This is an test email with attachment sent from Python"""
    html = f"""
    Hi {name}
    <br><br>
    <h3> This is an test email with attachment sent from Python <h3>"""

    # add body to msg
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    # file path
    filepath = attachment
    filename = "Attachment.pdf"

    # open file in read binary mode and add file payload to MIMEBase instance
    with open(filepath, 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())

    # encode file using base64
    encoders.encode_base64(part)

    # add headers as key-val pair to attachment part
    part.add_header("Content-Disposition", f"attachment; filename={filename}")

    # add attachment to msg & convert msg to string
    msg.attach(part)
    content = msg.as_string()

    #create secure connection with ssl context
    context = ssl.create_default_context()

    # login and send mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, to, content)


def main():
    contacts = get_contact_list(mail_list_file)
    for contact in contacts:
        mailsender(sender, contact, contacts[contact], password)

if __name__ == '__main__':
    main()