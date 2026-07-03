r"""
MCP Server - MGC Secure Mail Sender
AI entry point for skill store
"""

import json
import os
import smtplib
import ssl
from typing import Optional, List

try:
    import requests
except ImportError:
    raise ImportError("requests required: pip install requests")

try:
    from fastmcp import FastMCP
except ImportError:
    raise ImportError("fastmcp required: pip install fastmcp")

MGC_BASE_URL = "http://127.0.0.1:57219"
MGC_TOKEN_PATH = os.path.expanduser("~/.mgc/database/mgc_black_box/.mgc_token")
DEFAULT_INFO_TYPE = "config"
DEFAULT_INFO_OWNER = "email_smtp"

mcp = FastMCP("MGC_Secure_Mail_Sender")


def get_mgc_token() -> Optional[str]:
    if not os.path.exists(MGC_TOKEN_PATH):
        return None
    try:
        with open(MGC_TOKEN_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except IOError:
        return None


def get_email_config_from_mgc(token: str, info_type: str = None,
                         info_owner: str = None) -> Optional[dict]:
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


def send_email_smtp(config: dict, to: str, subject: str, body: str) -> tuple:
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

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


@mcp.tool()
def send_email(
    to: str,
    subject: str,
    body: str,
    info_type: str = DEFAULT_INFO_TYPE,
    info_owner: str = DEFAULT_INFO_OWNER
) -> dict:
    """Send email using MGC-stored credentials.

    Args:
        to: Recipient email.
        subject: Email subject.
        body: Email body.
        info_type: MGC info_type (customizable).
        info_owner: MGC info_owner (customizable).
    """
    if not to or not to.strip():
        return {"success": False, "message": "Recipient required"}

    token = get_mgc_token()
    if not token:
        return {"success": False, "message": "MGC not running. Run 'mgc' first."}

    config = get_email_config_from_mgc(token, info_type, info_owner)
    if not config:
        return {"success": False, "message": f"Email config not found. info_type={info_type}, info_owner={info_owner}"}

    success, message = send_email_smtp(config, to, subject, body)
    return {"success": success, "message": message}