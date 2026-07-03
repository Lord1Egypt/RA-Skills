#!/usr/bin/env python3
"""
agentmail-inbox.py — Read recent emails from local himalaya mail store
=============================================================
Reads email from a local Maildir-style store managed by himalaya CLI.
Requires himalaya to be installed and configured.

This script reads from the local mail store, NOT from IMAP directly.
This is more reliable for automation because it doesn't require
a persistent IMAP connection.

For iCloud/himalaya setup, see the SolEmail README.

Usage:
    python3 agentmail-inbox.py [--limit 10] [--unread-only]
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime, timezone
from pathlib import Path


HIMALAYA_CONFIG_PATH = os.environ.get(
    "HIMALAYA_CONFIG_PATH",
    os.path.expanduser("~/.config/himalaya/config.toml")
)


def run_himalaya(args: list) -> str:
    """Run himalaya CLI and return output."""
    result = subprocess.run(
        ["himalaya"] + args,
        capture_output=True,
        text=True,
        env={**os.environ, "HIMALAYA_CONFIG_PATH": HIMALAYA_CONFIG_PATH}
    )
    if result.returncode != 0:
        print(f"himalaya error: {result.stderr}", file=sys.stderr)
        return ""
    return result.stdout


def list_emails(limit: int = 20, unread_only: bool = False) -> list:
    """
    List recent emails using himalaya envelope.

    Returns a list of dicts with keys:
        id, from, to, subject, date, flags
    """
    args = ["envelope", "-w", "200"]
    if unread_only:
        args = ["envelope", "-w", "200", "--unread"]
    args += ["--", str(limit)]

    output = run_himalaya(args)
    emails = []

    for line in output.strip().split("\n"):
        if not line.strip():
            continue
        # himalaya envelope format is pipe-delimited:
        # id|flags|from|from_name|to|subject|date_internal|date_parsed|size|attachments
        parts = line.split("|")
        if len(parts) >= 9:
            try:
                emails.append({
                    "id":       parts[0].strip(),
                    "flags":    parts[1].strip(),
                    "from":     parts[2].strip(),
                    "from_name": parts[3].strip(),
                    "to":       parts[4].strip(),
                    "subject":  parts[5].strip(),
                    "date":     parts[7].strip() if len(parts) > 7 else "",
                })
            except IndexError:
                continue

    return emails


def read_email(email_id: str) -> dict:
    """
    Read a single email body using himalaya.

    Returns dict with keys: id, from, from_name, to, subject, date, body, flags
    """
    # Get full email output
    output = run_himalaya(["read", "--", email_id])

    # Parse first line as headers, rest as body
    lines = output.split("\n")
    header_line = lines[0] if lines else ""

    # Parse pipe-delimited header
    parts = header_line.split("|")
    if len(parts) < 8:
        return {"id": email_id, "raw": output}

    email = {
        "id":        parts[0].strip(),
        "flags":     parts[1].strip(),
        "from":      parts[2].strip(),
        "from_name": parts[3].strip(),
        "to":        parts[4].strip(),
        "subject":   parts[5].strip(),
        "date":      parts[7].strip(),
        "body":      "\n".join(lines[1:]).strip(),
    }
    return email


def format_email_short(e: dict) -> str:
    """One-line summary for display."""
    date = e.get("date", "")[:10]
    sender = e.get("from_name") or e.get("from", "?")
    subject = e.get("subject", "(no subject)")
    return f"[{date}] {sender}: {subject}"


def main():
    parser = argparse.ArgumentParser(description="List recent emails from local himalaya store")
    parser.add_argument("--limit",      type=int, default=10, help="Max emails to show (default: 10)")
    parser.add_argument("--unread-only", action="store_true", help="Show only unread")
    parser.add_argument("--json",        action="store_true", help="Output as JSON")
    parser.add_argument("--read",        type=str, metavar="ID", help="Read a specific email by ID")
    args = parser.parse_args()

    if args.read:
        email = read_email(args.read)
        if args.json:
            print(json.dumps(email, indent=2, default=str))
        else:
            print(f"From:    {email.get('from_name')} <{email.get('from')}>")
            print(f"To:      {email.get('to')}")
            print(f"Subject: {email.get('subject')}")
            print(f"Date:    {email.get('date')}")
            print(f"Flags:   {email.get('flags')}")
            print()
            print(email.get("body", "(no body)"))
        return

    emails = list_emails(limit=args.limit, unread_only=args.unread_only)

    if args.json:
        print(json.dumps(emails, indent=2, default=str))
        return

    if not emails:
        print("No emails found.")
        return

    print(f"=== {len(emails)} recent email{'s' if len(emails) != 1 else ''} ===\n")
    for e in emails:
        print(format_email_short(e))


if __name__ == "__main__":
    main()
