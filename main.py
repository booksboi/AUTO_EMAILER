import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime

# ==========================================
# LOAD CONFIGURATION
# ==========================================
load_dotenv()

# Fetch environment variables
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT", "587")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_ADDRESS = os.getenv("TO_ADDRESS")


# ==========================================
# HELPER FUNCTIONS
# ==========================================
def check_env():
    """Check and prompt for missing environment variables."""
    missing = []
    for key, value in {
        "SMTP_HOST": SMTP_HOST,
        "SMTP_PORT": SMTP_PORT,
        "EMAIL_ADDRESS": EMAIL_ADDRESS,
        "EMAIL_PASSWORD": EMAIL_PASSWORD,
    }.items():
        if not value:
            missing.append(key)

    if missing:
        print(f"⚠️ Missing values in .env file: {', '.join(missing)}")
        for key in missing:
            os.environ[key] = input(f"Enter {key}: ")


def log_email(status, subject, recipients):
    """Log sent email details into a file."""
    with open("email_log.txt", "a") as log:
        log.write(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Status: {status} | Subject: {subject} | To: {recipients}\n"
        )


def attach_files(msg):
    """Attach files to the email."""
    attachments = input("Enter file paths to attach (comma separated) or leave blank: ").strip()
    if attachments:
        paths = [path.strip() for path in attachments.split(",")]
        for path in paths:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    msg.add_attachment(
                        f.read(),
                        maintype="application",
                        subtype="octet-stream",
                        filename=os.path.basename(path),
                    )
                    print(f"📎 Attached: {os.path.basename(path)}")
            else:
                print(f"⚠️ Skipped (file not found): {path}")


# ==========================================
# MAIN EMAIL FUNCTION
# ==========================================
def send_email():
    """Send an email with optional HTML and attachments."""
    check_env()

    # Get details interactively
    subject = input("\nEnter Email Subject: ")
    body = input("Enter Email Body (plain text): ")
    recipients = input("Enter recipient emails (comma separated): ").strip() or TO_ADDRESS

    # Ask if HTML email
    is_html = input("Send as HTML email? (y/n): ").lower().startswith("y")

    # Create message
    msg = EmailMessage()
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = recipients
    msg["Subject"] = subject

    if is_html:
        msg.add_alternative(body, subtype="html")
    else:
        msg.set_content(body)

    # Attach files
    attach_files(msg)

    # Send email
    try:
        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)
            print("\n✅ Email sent successfully!")
            log_email("SUCCESS", subject, recipients)
    except Exception as e:
        print(f"\n❌ Failed to send email: {e}")
        log_email("FAILED", subject, recipients)


# ==========================================
# MAIN APP ENTRY
# ==========================================
if __name__ == "__main__":
    print("📬 ================================")
    print("         AUTO EMAILER 2.0")
    print("==================================")

    send_email()
    print("\n📝 Email details logged in email_log.txt")
