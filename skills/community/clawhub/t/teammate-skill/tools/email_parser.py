#!/usr/bin/env python3
"""
Email Parser

Parses .eml and .mbox email files to extract messages from a target sender.

Usage:
    python3 email_parser.py --file emails.mbox --target "Alex Chen" --output /tmp/email_out.txt
    python3 email_parser.py --file message.eml --target "alex@company.com" --output /tmp/email_out.txt
"""

from __future__ import annotations

import email
import email.policy
import mailbox
import argparse
import sys
from pathlib import Path
from typing import Optional


def extract_text(msg) -> str:
    """Extract plain text body from an email message."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="replace")
                except Exception:
                    continue
    else:
        try:
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset() or "utf-8"
            return payload.decode(charset, errors="replace")
        except Exception:
            pass
    return ""


def matches_target(sender: str, target: str) -> bool:
    """Check if sender matches target (name or email)."""
    if not sender or not target:
        return False
    target_lower = target.lower()
    sender_lower = sender.lower()
    return target_lower in sender_lower


def parse_eml(file_path: Path, target: str) -> list:
    """Parse a single .eml file."""
    messages = []
    with open(file_path, "rb") as f:
        msg = email.message_from_binary_file(f, policy=email.policy.default)

    sender = str(msg.get("From", ""))
    if not matches_target(sender, target):
        return messages

    subject = str(msg.get("Subject", "(no subject)"))
    date = str(msg.get("Date", "unknown"))
    to = str(msg.get("To", ""))
    body = extract_text(msg)

    if body.strip():
        messages.append({
            "from": sender,
            "to": to,
            "subject": subject,
            "date": date,
            "body": body.strip()[:5000],
        })

    return messages


def parse_mbox(file_path: Path, target: str) -> list:
    """Parse an .mbox file."""
    messages = []
    mbox = mailbox.mbox(str(file_path))

    for msg in mbox:
        sender = str(msg.get("From", ""))
        if not matches_target(sender, target):
            continue

        subject = str(msg.get("Subject", "(no subject)"))
        date = str(msg.get("Date", "unknown"))
        to = str(msg.get("To", ""))
        body = extract_text(msg)

        if body.strip():
            messages.append({
                "from": sender,
                "to": to,
                "subject": subject,
                "date": date,
                "body": body.strip()[:5000],
            })

    return messages


def main():
    parser = argparse.ArgumentParser(description="Parse email files for target sender")
    parser.add_argument("--file", required=True, help="Path to .eml or .mbox file")
    parser.add_argument("--target", required=True, help="Target sender name or email")
    parser.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    # Detect format
    if file_path.suffix.lower() == ".eml":
        messages = parse_eml(file_path, args.target)
    elif file_path.suffix.lower() == ".mbox":
        messages = parse_mbox(file_path, args.target)
    else:
        # Try mbox first, then eml
        try:
            messages = parse_mbox(file_path, args.target)
        except Exception:
            messages = parse_eml(file_path, args.target)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Emails from {args.target}\n")
        f.write(f"# Total: {len(messages)} emails\n\n")

        for msg in messages:
            f.write(f"## {msg['subject']}\n")
            f.write(f"From: {msg['from']}\n")
            f.write(f"To: {msg['to']}\n")
            f.write(f"Date: {msg['date']}\n\n")
            f.write(f"{msg['body']}\n")
            f.write("\n---\n\n")

    print(f"✅ Extracted {len(messages)} emails → {args.output}")


if __name__ == "__main__":
    main()
