import os
import smtplib
import ssl
from dotenv import load_dotenv

load_dotenv()

sender = os.getenv("EMAIL_SENDER")
password = os.getenv("EMAIL_PASSWORD")
receiver = os.getenv("EMAIL_RECEIVER")

subject = "Test Email"
body = "This is a test message from Kyrgyz Horizont."

email_text = f"Subject: {subject}\n\n{body}"

context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, email_text.encode("utf-8"))

    print("✔ Email sent successfully!")

except Exception as e:
    print("❌ Error:", e)
