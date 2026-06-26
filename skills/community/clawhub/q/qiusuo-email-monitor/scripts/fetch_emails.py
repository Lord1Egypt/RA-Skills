#!/usr/bin/env python3
"""
fetch_emails.py - Fetch new emails via IMAP since last run.

Usage:
    python3 fetch_emails.py --config <path-to-config.json>

Config JSON fields:
    email       : Gmail address (or other IMAP address)
    password    : App password or IMAP password
    imap_host   : IMAP server (default: imap.gmail.com)
    imap_port   : IMAP port (default: 993)
    mailbox     : Mailbox to check (default: INBOX)
    state_file  : Path to state file tracking last UID (default: ./email_state.json)
    max_emails  : Max emails to fetch per run (default: 20)
    fetch_attachments : Whether to download attachments (default: false)
    attachment_dir    : Directory to save attachments (default: ./attachments)

Output: JSON array of new email objects printed to stdout.
        Returns exit code 0 always; prints [] if no new emails.
"""

import imaplib
import email
from email.header import decode_header
import json
import argparse
import os
import sys
from datetime import datetime

DEFAULT_CONFIG = {
    "imap_host": "imap.gmail.com",
    "imap_port": 993,
    "mailbox": "INBOX",
    "state_file": "./email_state.json",
    "max_emails": 20,
    "fetch_attachments": False,
    "attachment_dir": "./attachments"
}


def decode_str(s):
    if s is None:
        return ""
    parts = decode_header(s)
    result = ""
    for part, enc in parts:
        if isinstance(part, bytes):
            result += part.decode(enc or "utf-8", errors="replace")
        else:
            result += part
    return result.strip()


def get_body_and_attachments(msg, fetch_attachments=False, attachment_dir="./attachments"):
    body = ""
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get("Content-Disposition") or "")
            if "attachment" in cd:
                if fetch_attachments:
                    filename = decode_str(part.get_filename() or "attachment")
                    os.makedirs(attachment_dir, exist_ok=True)
                    filepath = os.path.join(attachment_dir, filename)
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    attachments.append(filepath)
                else:
                    filename = decode_str(part.get_filename() or "attachment")
                    attachments.append(filename)
            elif ct == "text/plain" and not body:
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")
    return body[:800], attachments


def load_state(state_file):
    if os.path.exists(state_file):
        with open(state_file) as f:
            return json.load(f)
    return {"last_uid": 0, "last_checked": None}


def save_state(state_file, state):
    os.makedirs(os.path.dirname(os.path.abspath(state_file)), exist_ok=True)
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to config JSON file")
    args = parser.parse_args()

    with open(args.config) as f:
        cfg = json.load(f)

    # Merge with defaults
    for k, v in DEFAULT_CONFIG.items():
        cfg.setdefault(k, v)

    # Expand ~ in paths
    cfg["state_file"] = os.path.expanduser(cfg["state_file"])
    cfg["attachment_dir"] = os.path.expanduser(cfg["attachment_dir"])

    state = load_state(cfg["state_file"])
    last_uid = int(state.get("last_uid", 0))

    mail = imaplib.IMAP4_SSL(cfg["imap_host"], cfg["imap_port"])
    mail.login(cfg["email"], cfg["password"])
    mail.select(cfg["mailbox"])

    if last_uid > 0:
        _, data = mail.uid("search", None, f"UID {last_uid + 1}:*")
    else:
        _, data = mail.uid("search", None, "ALL")

    uids = data[0].split() if data[0] else []
    uids = uids[-cfg["max_emails"]:]  # cap

    results = []
    max_uid = last_uid

    for uid_bytes in uids:
        uid = int(uid_bytes)
        if uid <= last_uid:
            continue
        _, msg_data = mail.uid("fetch", uid_bytes, "(RFC822)")
        if not msg_data or not msg_data[0]:
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        body, attachments = get_body_and_attachments(
            msg,
            fetch_attachments=cfg["fetch_attachments"],
            attachment_dir=cfg["attachment_dir"]
        )
        results.append({
            "uid": uid,
            "from": decode_str(msg["From"]),
            "subject": decode_str(msg["Subject"]),
            "date": msg["Date"],
            "snippet": body,
            "attachments": attachments
        })
        if uid > max_uid:
            max_uid = uid

    mail.logout()

    # Update state
    if max_uid > last_uid:
        state["last_uid"] = max_uid
    state["last_checked"] = datetime.utcnow().isoformat() + "Z"
    save_state(cfg["state_file"], state)

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
