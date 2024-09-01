import smtplib,os,ssl
import requests
from datetime import datetime

from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv


PORT=465 #465 for ssl
EMAIL_SERVER="smtp.gmail.com"
context=ssl.create_default_context()


current_dir= Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars=current_dir/ ".env"  # name of env file
load_dotenv(envars)

# create env file and fill the required details
email_sender = os.getenv("EMAIL") 
email_password = os.getenv("PASSWORD")
email_receiver="mauryaabhay1213@gmail.com"

def send_email(subject, body):
    msg=EmailMessage()
    msg["Subject"]='subject'
    msg["From"]=formataddr(("Abhay",f'{email_sender}')) # change the title of mail
    msg["To"]=email_receiver
    msg["BCC"]=email_sender

    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_receiver, message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"[{datetime.now()}] {url} is up and running!")
        else:
            message = f"{url} returned status code {response.status_code}"
            print(f"[{datetime.now()}] {message}")
            send_email("Website Down Alert", message)
    except requests.RequestException as e:
        message = f"{url} is down. Error: {e}"
        print(f"[{datetime.now()}] {message}")
        send_email("Website Down Alert", message)

if __name__ == "__main__":
    websites = [                #give the list of your websites here
                                # Note -- website url must be correct for proper working
        "https://www.google.com",
        "https://www.nonexistentwebsite.com"
    ]

    for website in websites:
        check_website(website)
