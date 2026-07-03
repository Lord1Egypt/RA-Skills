#!/usr/bin/env python3
"""
agentmail-send.py — Send email via iCloud SMTP
==============================================
Reads SMTP credentials from environment variables.
Copy this to your OpenClaw workspace scripts directory:
    ~/.openclaw/workspace/scripts/agentmail-send.py

Environment variables required:
    SMTP_HOST     — SMTP server (e.g. smtp.mail.me.com)
    SMTP_PORT     — Port (587 for STARTTLS, 465 for SSL)
    SMTP_USER     — Your email address
    SMTP_PASSWORD — App-specific password from your email provider
    FROM_NAME     — Display name in "From" (e.g. "Sol AI")

Usage:
    python3 agentmail-send.py \
        --to "recipient@example.com" \
        --subject "Subject line" \
        --body "Email body text" \
        [--attachment "/path/to/file.zip"]

Or import as a module:
    from agentmail_send import send_email
    send_email(to="...", subject="...", body="...")
"""

import os
import sys
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_email(to: str, subject: str, body: str,
               attachments: list = None,
               smtp_host: str = None,
               smtp_port: int = None,
               smtp_user: str = None,
               smtp_password: str = None,
               from_name: str = None) -> dict:
    """
    Send an email via SMTP.

    Args:
        to: Recipient email address
        subject: Email subject line
        body: Email body text (plain text)
        attachments: Optional list of file paths to attach
        smtp_host: SMTP server hostname (env: SMTP_HOST)
        smtp_port: SMTP port (env: SMTP_PORT, default: 587)
        smtp_user: SMTP username / email address (env: SMTP_USER)
        smtp_password: SMTP password / app password (env: SMTP_PASSWORD)
        from_name: Display name for sender (env: FROM_NAME)

    Returns:
        {"success": True} on success, raises on failure
    """
    # Load from environment if not provided
    smtp_host   = smtp_host   or os.environ.get("SMTP_HOST", "smtp.mail.me.com")
    smtp_port   = int(smtp_port or os.environ.get("SMTP_PORT", 587))
    smtp_user   = smtp_user   or os.environ.get("SMTP_USER")
    smtp_password = smtp_password or os.environ.get("SMTP_PASSWORD")
    from_name   = from_name   or os.environ.get("FROM_NAME", "Sol AI")

    if not smtp_user or not smtp_password:
        raise ValueError(
            "SMTP credentials not configured. "
            "Set SMTP_USER and SMTP_PASSWORD environment variables."
        )

    # Build message
    msg = MIMEMultipart()
    msg['From']    = f"{from_name} <{smtp_user}>"
    msg['To']      = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    if attachments:
        for filepath in attachments:
            try:
                with open(filepath, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                filename = os.path.basename(filepath)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{filename}"'
                )
                msg.attach(part)
            except Exception as e:
                print(f"Warning: could not attach {filepath}: {e}", file=sys.stderr)

    # Send
    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=60)
            server.ehlo()
            if smtp_port == 587:
                server.starttls()
                server.ehlo()

        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return {"success": True, "to": to, "subject": subject}

    except smtplib.SMTPAuthenticationError as e:
        raise RuntimeError(
            f"SMTP authentication failed. Check SMTP_USER and SMTP_PASSWORD. "
            f"(App passwords are different from your login password) {e}"
        )
    except smtplib.SMTPException as e:
        raise RuntimeError(f"SMTP error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Send an email via SMTP")
    parser.add_argument("--to",      required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body",    required=True, help="Email body (plain text)")
    parser.add_argument("--attachment", action="append", default=[],
                        help="File path to attach (can be specified multiple times)")
    args = parser.parse_args()

    result = send_email(
        to=args.to,
        subject=args.subject,
        body=args.body,
        attachments=args.attachment if args.attachment else None
    )
    print(f"Sent to {result['to']}: {result['subject']}")


if __name__ == "__main__":
    main()
