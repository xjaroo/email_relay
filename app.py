import time
import smtplib
from aiosmtpd.controller import Controller
from email.parser import BytesParser
from email.policy import default
from email.message import EmailMessage

# === Mailgun SMTP Config ===
MAILGUN_SMTP_SERVER = "smtp.mailgun.org"
MAILGUN_SMTP_PORT = 587
MAILGUN_USER = "scanner@mg.abc.com"  # or postmaster@mg.abc.com
MAILGUN_PASS = "......"
MAILGUN_FROM = "scanner@mg.abc.io"

class ForwardSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        print("\n📨 Email received!")
        print(f"👤 From: {envelope.mail_from}")
        print(f"📬 To: {envelope.rcpt_tos}")

        # Parse incoming message
        original = BytesParser(policy=default).parsebytes(envelope.content)
        subject = original.get('Subject', '(No Subject)')

        # Build a new email to forward
        fwd = EmailMessage()
        fwd['Subject'] = f"📠 Scan: {subject}"
        fwd['From'] = MAILGUN_FROM
        fwd['To'] = envelope.rcpt_tos
        fwd.set_content("Forwarded scan from FUJIFILM printer.")

        # Copy attachments and plain text body
        if original.is_multipart():
            for part in original.walk():
                ctype = part.get_content_type()
                disposition = part.get_content_disposition()
                if disposition == 'attachment':
                    fwd.add_attachment(
                        part.get_payload(decode=True),
                        maintype=part.get_content_maintype(),
                        subtype=part.get_content_subtype(),
                        filename=part.get_filename()
                    )
                elif ctype == 'text/plain' and not fwd.get_content():
                    fwd.set_content(part.get_content())
        else:
            fwd.set_content(original.get_content())

        # Send via Mailgun
        try:
            with smtplib.SMTP(MAILGUN_SMTP_SERVER, MAILGUN_SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(MAILGUN_USER, MAILGUN_PASS)
                smtp.send_message(fwd)
            print("✅ Forwarded to Mailgun successfully!")
        except Exception as e:
            print("❌ Failed to send:", e)

        return "250 Message accepted and forwarded"

def run_mailgun_forwarder():
    handler = ForwardSMTPHandler()
    controller = Controller(handler, hostname="0.0.0.0", port=2525)
    controller.start()
    print("📡 SMTP forwarder running on port 2525... (Ctrl+C to stop)")

if __name__ == "__main__":
    run_mailgun_forwarder()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 SMTP forwarder stopped.")