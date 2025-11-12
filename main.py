import os
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch credentials
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT", "587")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_ADDRESS = os.getenv("TO_ADDRESS")

def check_env():
    """Check and prompt for missing environment variables"""
    missing = []
    for key, value in {
        "SMTP_HOST": SMTP_HOST,
        "SMTP_PORT": SMTP_PORT,
        "EMAIL_ADDRESS": EMAIL_ADDRESS,
        "EMAIL_PASSWORD": EMAIL_PASSWORD,
        "TO_ADDRESS": TO_ADDRESS,
    }.items():
        if not value:
            missing.append(key)

    if missing:
        print(f"⚠️ Missing values in .env file: {', '.join(missing)}")
        for key in missing:
            os.environ[key] = input(f"Enter {key}: ")

def send_email(subject: str, body: str):
    """Send an email using SMTP credentials"""
    check_env()

    msg = EmailMessage()
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = os.getenv("TO_ADDRESS")
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)
            print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    print("📧 Auto Emailer Started")
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")
    send_email(subject, body)
