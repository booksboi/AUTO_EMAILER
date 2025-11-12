# main.py (Upgraded Version)
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(subject: str, body: str, to_addrs: list, attachment_path: str = None):
    """
    Send an email using SMTP credentials from .env.
    Supports multiple recipients and optional attachments.
    """
    if not all([SMTP_HOST, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD, to_addrs]):
        raise SystemExit("❌ Missing SMTP configuration or recipient address.")

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(to_addrs)
    msg["Subject"] = subject
    msg.set_content(body)

    # Add attachment if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
            print(f"📎 Attached file: {file_name}")
    elif attachment_path:
        print(f"⚠️ Attachment not found: {attachment_path}")

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"✅ Email sent successfully to {', '.join(to_addrs)} at {datetime.now().strftime('%H:%M:%S')}")
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Check EMAIL_ADDRESS and EMAIL_PASSWORD (App Password required).")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    print("📧 Python Auto Emailer")
    print("----------------------")

    # Take user inputs
    subject = input("Enter email subject: ").strip() or "Test Email from Auto Emailer"
    body = input("Enter email body: ").strip() or "Hello! This is a test email sent from my Python project."
    recipients = input("Enter recipient email(s), separated by commas: ").split(",")
    recipients = [r.strip() for r in recipients if r.strip()]

    attachment = input("Enter attachment file path (or press Enter to skip): ").strip() or None

    send_email(subject, body, recipients, attachment)

