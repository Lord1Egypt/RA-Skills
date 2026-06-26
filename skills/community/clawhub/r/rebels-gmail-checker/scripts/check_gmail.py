#!/usr/bin/env python3
"""Gmail Checker — fetches unread inbox emails, filters out noise, outputs a prioritized digest.

Usage:
    python3 check_gmail.py [hours]         # default: 24 hours
    python3 check_gmail.py --json [hours]  # structured JSON output

Credentials (required): <DATA_DIR>/gmail.json
Config (optional):      <DATA_DIR>/gmail-config.json

DATA_DIR resolution order:
  1. $SKILL_DATA_DIR          (set by agent platform)
  2. ~/.config/gmail-checker   (XDG default)
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# --- Path resolution ---
# Agent platforms set SKILL_DATA_DIR to their preferred credential store.
# Falls back to ~/.config/gmail-checker (XDG-compliant, works everywhere).
DATA_DIR = os.path.expanduser(
    os.environ.get("SKILL_DATA_DIR", "~/.config/gmail-checker")
)
CREDS_PATH = os.path.join(DATA_DIR, "gmail.json")
CONFIG_PATH = os.path.join(DATA_DIR, "gmail-config.json")

DEFAULT_CONFIG = {
    "hours": 24,
    "max_results": 50,
    "high_priority_domains": [],
    "high_priority_keywords": [
        "security", "vulnerability", "alert", "urgent",
        "action required", "suspended", "billing",
    ],
    "labels_skip": [
        "CATEGORY_PROMOTIONS", "CATEGORY_UPDATES",
        "CATEGORY_FORUMS", "CATEGORY_SOCIAL",
    ],
}


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            user_config = json.load(f)
        merged = {**DEFAULT_CONFIG, **user_config}
        for key in ("high_priority_keywords", "labels_skip"):
            if key in user_config:
                merged[key] = user_config[key]
        return merged
    return DEFAULT_CONFIG


def get_credentials():
    with open(CREDS_PATH) as f:
        data = json.load(f)

    creds = Credentials(
        token=None,
        refresh_token=data["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=data["client_id"],
        client_secret=data["client_secret"],
    )
    creds.refresh(Request())
    return creds


def fetch_unread_emails(service, config):
    hours = config["hours"]
    query = f"is:unread in:inbox newer_than:{hours}h"

    results = service.users().messages().list(
        userId="me", q=query, maxResults=config["max_results"]
    ).execute()
    messages = results.get("messages", [])

    skip_labels = set(config["labels_skip"])
    high_domains = set(d.lower() for d in config["high_priority_domains"])
    high_keywords = [kw.lower() for kw in config["high_priority_keywords"]]

    emails = []
    for msg in messages:
        detail = service.users().messages().get(
            userId="me", id=msg["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date", "LabelIds"],
        ).execute()

        headers = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
        labels = set(detail.get("labelIds", []))

        if labels & skip_labels:
            continue

        sender = headers.get("From", "Unknown")
        subject = headers.get("Subject", "(no subject)")
        date_str = headers.get("Date", "")

        if "<" in sender and ">" in sender:
            email_addr = sender.split("<")[1].split(">")[0].strip().lower()
        else:
            email_addr = sender.strip().lower()

        domain = email_addr.split("@")[-1] if "@" in email_addr else ""
        subject_lower = subject.lower()

        if domain in high_domains:
            priority = "HIGH"
        elif any(kw in subject_lower for kw in high_keywords):
            priority = "HIGH"
        elif "CATEGORY_PERSONAL" in labels:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        emails.append({
            "sender": sender,
            "email": email_addr,
            "subject": subject,
            "date": date_str,
            "priority": priority,
        })

    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    emails.sort(key=lambda e: priority_order.get(e["priority"], 3))
    return emails


def format_text(emails, hours):
    if not emails:
        return f"No unread emails in the last {hours}h."

    lines = [f"Unread Inbox (last {hours}h)\n"]
    by_priority = {"HIGH": [], "MEDIUM": [], "LOW": []}
    for e in emails:
        by_priority[e["priority"]].append(e)

    icons = {"HIGH": "🔴 HIGH", "MEDIUM": "🟡 MED", "LOW": "🟢 LOW"}

    for p in ("HIGH", "MEDIUM", "LOW"):
        if not by_priority[p]:
            continue
        lines.append(f"[{icons[p]}]")
        for e in by_priority[p]:
            lines.append(f"  {e['subject']}")
            lines.append(f"  from: {e['sender']}")
        lines.append("")

    total = len(emails)
    lines.append(f"{total} unread email{'s' if total != 1 else ''}")
    return "\n".join(lines)


def format_json(emails, hours):
    output = {"hours": hours, "total": len(emails), "emails": emails}
    return json.dumps(output, indent=2, ensure_ascii=False)


def main():
    args = sys.argv[1:]
    as_json = False

    if args and args[0] == "--json":
        as_json = True
        args = args[1:]

    hours = int(args[0]) if args else None
    config = load_config()
    if hours:
        config["hours"] = hours

    try:
        creds = get_credentials()
        service = build("gmail", "v1", credentials=creds)
        emails = fetch_unread_emails(service, config)
        if as_json:
            print(format_json(emails, config["hours"]))
        else:
            print(format_text(emails, config["hours"]))
    except FileNotFoundError as e:
        print(f"Missing file: {e}", file=sys.stderr)
        print(f"Expected credentials at: {CREDS_PATH}", file=sys.stderr)
        print("Run the setup script first. See references/setup.md for instructions.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error checking Gmail: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
