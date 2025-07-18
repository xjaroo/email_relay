# 📠 Secure SMTP Email Forwarder for Scanned Documents

This is a lightweight, self-hosted SMTP relay server written in Python using `aiosmtpd`. It is designed to receive scanned documents from a multifunction printer (MFP), and securely forward them to intended recipients via the [Mailgun](https://www.mailgun.com/) email API.

--- 

## ✨ Features

- Accepts incoming emails over SMTP on port `2525`.
- Restricts access to trusted networks (e.g., office IP via firewall).
- Parses and re-wraps incoming emails, preserving attachments.
- Sends emails via Mailgun SMTP with TLS encryption.
- Adds prefix to subject and formats body for clarity.

---

## 🔧 Requirements

- Python 3.7+
- A [Mailgun](https://www.mailgun.com/) account and SMTP credentials.
- An MFP or scanner configured to send email to this server (via SMTP on port 2525).

---

## 📦 Installation

```bash
pip install aiosmtpd
