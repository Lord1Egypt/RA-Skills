# Zero-Exposure SMTP Email Script Template (MGC 1.4.10)
# Store this script in MGC via mgc_save; AI invokes it via mgc_run.
# Users should customize SMTP_CREDENTIAL_NAME / EMAIL_CONTENT_NAME.

import smtplib
import os
import json
import argparse
import requests
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ========== Configuration ==========
# Replace these with your credential names (info_owner).
SMTP_CREDENTIAL_NAME = "smtp_gmail"           # SMTP credentials
EMAIL_CONTENT_NAME = "email_template_001"     # (Optional) Email content stored in MGC


def get_credential(cred_name):
    """Read credential from MGC local API. Script-internal only; AI never calls this."""
    token_path = os.path.expanduser("~/.mgc/database/mgc_black_box/.mgc_token")
    if not os.path.exists(token_path):
        return None
    with open(token_path) as f:
        token = f.read().strip()

    resp = requests.post(
        "http://127.0.0.1:57219/api/mgc/sensitive/get",
        headers={"X-MGC-Token": token, "Content-Type": "application/json"},
        json={"info_type": "config", "info_owner": cred_name, "action": "run"},
        timeout=10,
    )
    if resp.status_code == 200:
        data = resp.json()
        data_field = data.get("data")
        if isinstance(data_field, str):
            return json.loads(data_field)
        elif isinstance(data_field, dict):
            content = data_field.get("content", "")
            if content:
                return json.loads(content)
    return None


def get_email_content(content_name):
    """Read email content from MGC (optional privacy feature)."""
    token_path = os.path.expanduser("~/.mgc/database/mgc_black_box/.mgc_token")
    if not os.path.exists(token_path):
        return None
    with open(token_path) as f:
        token = f.read().strip()

    resp = requests.post(
        "http://127.0.0.1:57219/api/mgc/sensitive/get",
        headers={"X-MGC-Token": token, "Content-Type": "application/json"},
        json={"info_type": "config", "info_owner": content_name, "action": "run"},
        timeout=10,
    )
    if resp.status_code == 200:
        data = resp.json()
        data_field = data.get("data")
        if isinstance(data_field, str):
            return data_field
        elif isinstance(data_field, dict):
            return data_field.get("content", "")
    return None


def send_email(to_address, subject, body, use_stored_content=False):
    """Send email via SMTP."""
    cred = get_credential(SMTP_CREDENTIAL_NAME)
    if not cred:
        return {"success": False, "error": "Failed to get SMTP credentials"}

    if use_stored_content:
        stored_content = get_email_content(EMAIL_CONTENT_NAME)
        if stored_content:
            try:
                content_data = json.loads(stored_content)
                subject = content_data.get("subject", subject)
                body = content_data.get("body", body)
            except Exception:
                body = stored_content

    try:
        msg = MIMEMultipart()
        msg['From'] = cred['address']
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        with smtplib.SMTP(cred["smtp_server"], cred["smtp_port"]) as server:
            server.starttls()
            server.login(cred["address"], cred["password"])
            server.sendmail(cred["address"], [to_address], msg.as_string())
        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    # ✅ Literal defaults only — MGC 1.4.10 auto-parses into ext02
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", default="")
    parser.add_argument("--subject", default="")
    parser.add_argument("--body", default="")
    parser.add_argument("--use_stored_content", action="store_true")
    args, _ = parser.parse_known_args()  # ✅ parse_known_args avoids exit on unknown params

    result = send_email(
        to_address=args.to,
        subject=args.subject,
        body=args.body,
        use_stored_content=args.use_stored_content,
    )

    # Write result to file so AI can read it (mgc_run returns pid+status, not stdout).
    out_dir = os.path.expanduser("~/mgc_outputs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(
        out_dir, f"email_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"RESULT_FILE:{out_path}")


if __name__ == "__main__":
    main()