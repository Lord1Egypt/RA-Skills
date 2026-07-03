r"""
Example - Send Email via MGC
Manual test script for users
"""

import argparse
import json
import os
import smtplib
import ssl
import sys

try:
    import requests
except ImportError:
    print("Error: requests required. Install: pip install requests")
    sys.exit(1)

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MGC_BASE_URL = "http://127.0.0.1:57219"
MGC_TOKEN_PATH = os.path.expanduser("~/.mgc/database/mgc_black_box/.mgc_token")
DEFAULT_INFO_TYPE = "config"
DEFAULT_INFO_OWNER = "email_smtp"


def get_mgc_token():
    if not os.path.exists(MGC_TOKEN_PATH):
        return None
    try:
        with open(MGC_TOKEN_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except IOError:
        return None


def get_email_config_from_mgc(token, info_type=None, info_owner=None):
    info_type = info_type or DEFAULT_INFO_TYPE
    info_owner = info_owner or DEFAULT_INFO_OWNER

    try:
        resp = requests.post(
            f"{MGC_BASE_URL}/api/mgc/sensitive/get",
            headers={"X-MGC-Token": token, "Content-Type": "application/json"},
            json={"info_type": info_type, "info_owner": info_owner},
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == 200:
                content = data.get("data", {})
                if isinstance(content, str):
                    return json.loads(content)
                elif isinstance(content, dict) and content.get("content"):
                    return json.loads(content["content"])
        return None
    except requests.exceptions.RequestException:
        return None
    except json.JSONDecodeError:
        return None


def send_email_smtp(config, to, subject, body):
    msg = MIMEMultipart('mixed')
    msg['From'] = config["address"]
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    recipients = [to]
    # smtp_port dynamically fetched from config
    try:
        smtp_port = int(config["smtp_port"])
    except (ValueError, TypeError):
        return False, "SMTP port must be a number"
    smtp_server = config["smtp_server"]
    address = config["address"]
    password = config["password"]

    try:
        if smtp_port == 465:
            ctx = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ctx) as server:
                server.login(address, password)
                server.sendmail(address, recipients, msg.as_string())
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(address, password)
                server.sendmail(address, recipients, msg.as_string())
        return True, "Email sent"
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Send email via MGC")
    parser.add_argument("-t", "--to", required=True, help="Recipient email")
    parser.add_argument("-s", "--subject", required=True, help="Email subject")
    parser.add_argument("-b", "--body", required=True, help="Email body")
    parser.add_argument("--info-type", default=DEFAULT_INFO_TYPE, help="MGC info_type")
    parser.add_argument("--info-owner", default=DEFAULT_INFO_OWNER, help="MGC info_owner")
    args = parser.parse_args()

    token = get_mgc_token()
    if not token:
        print("Error: MGC not running. Run 'mgc' first.")
        sys.exit(1)

    config = get_email_config_from_mgc(token, args.info_type, args.info_owner)
    if not config:
        print(f"Error: Email config not found in MGC")
        print(f"Save: mgc_save info_type={args.info_type} info_owner={args.info_owner} < config.json")
        sys.exit(1)

    success, message = send_email_smtp(config, args.to, args.subject, args.body)
    if success:
        print(f"Success: {message}")
    else:
        print(f"Error: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()