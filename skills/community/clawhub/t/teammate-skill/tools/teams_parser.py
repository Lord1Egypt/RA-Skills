#!/usr/bin/env python3
"""
Teams / Outlook Export Parser

Parses Microsoft Teams chat exports and Outlook email exports.

Usage:
    python3 teams_parser.py --file teams_export.json --target "Alex Chen" --output /tmp/teams_out.txt
    python3 teams_parser.py --dir outlook_export/ --target "alex@company.com" --output /tmp/outlook_out.txt
"""

from __future__ import annotations

import json
import argparse
import re
import sys
from pathlib import Path
from typing import Optional


def parse_teams_json(file_path: Path, target: str) -> list:
    """Parse Teams JSON export for target user messages."""
    messages = []

    data = json.loads(file_path.read_text(encoding="utf-8"))

    # Teams export formats can vary
    msg_list = []
    if isinstance(data, list):
        msg_list = data
    elif isinstance(data, dict):
        msg_list = data.get("messages", data.get("value", []))

    for msg in msg_list:
        sender = ""
        if isinstance(msg.get("from"), dict):
            user = msg["from"].get("user", msg["from"].get("application", {}))
            sender = user.get("displayName", user.get("id", ""))
        elif isinstance(msg.get("sender"), str):
            sender = msg["sender"]
        elif isinstance(msg.get("senderDisplayName"), str):
            sender = msg["senderDisplayName"]

        if not sender or target.lower() not in sender.lower():
            continue

        # Extract text content
        body = msg.get("body", {})
        if isinstance(body, dict):
            content = body.get("content", "")
            if body.get("contentType") == "html":
                content = re.sub(r'<[^>]+>', '', content)
        elif isinstance(body, str):
            content = body
        else:
            content = str(msg.get("content", msg.get("text", "")))

        content = content.strip()
        if not content:
            continue

        timestamp = msg.get("createdDateTime", msg.get("timestamp", "unknown"))
        channel = msg.get("channelIdentity", {}).get("channelId", "")
        chat = msg.get("chatId", "")

        messages.append({
            "sender": sender,
            "timestamp": timestamp[:16] if len(timestamp) > 16 else timestamp,
            "content": content[:2000],
            "channel": channel or chat or "direct",
        })

    return messages


def parse_outlook_eml_dir(dir_path: Path, target: str) -> list:
    """Parse directory of .eml files for target sender."""
    # Reuse the email_parser module
    import importlib.util
    email_parser_path = Path(__file__).parent / "email_parser.py"
    if email_parser_path.exists():
        spec = importlib.util.spec_from_file_location("email_parser", email_parser_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        messages = []
        for eml_file in sorted(dir_path.glob("*.eml")):
            msgs = mod.parse_eml(eml_file, target)
            messages.extend(msgs)
        return messages

    return []


def main():
    parser = argparse.ArgumentParser(description="Parse Teams/Outlook exports")
    parser.add_argument("--file", help="Path to Teams JSON export")
    parser.add_argument("--dir", help="Path to directory of .eml files")
    parser.add_argument("--target", required=True, help="Target user name or email")
    parser.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()

    messages = []

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
        messages = parse_teams_json(file_path, args.target)

    if args.dir:
        dir_path = Path(args.dir)
        if not dir_path.is_dir():
            print(f"❌ Directory not found: {dir_path}")
            sys.exit(1)
        messages.extend(parse_outlook_eml_dir(dir_path, args.target))

    if not args.file and not args.dir:
        parser.error("Either --file or --dir is required")

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Teams/Outlook Messages from {args.target}\n")
        f.write(f"# Total: {len(messages)} messages\n\n")

        for msg in messages:
            f.write(f"[{msg['timestamp']}] {msg.get('channel', '')}: {msg['content']}\n")

    print(f"✅ Extracted {len(messages)} messages → {args.output}")


if __name__ == "__main__":
    main()
