#!/usr/bin/env python3
"""
Slack Export Parser

Parses Slack workspace export JSON to extract messages from a target user.

Usage:
    python3 slack_parser.py --file slack_export.zip --target "Alex Chen" --output /tmp/slack_out.txt
    python3 slack_parser.py --dir slack_export_dir/ --target "alex.chen" --output /tmp/slack_out.txt
"""

from __future__ import annotations

import json
import argparse
import os
import sys
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


def load_users(export_dir: Path) -> dict:
    """Load user ID to name/username mapping."""
    users_file = export_dir / "users.json"
    if not users_file.exists():
        return {}
    users = json.loads(users_file.read_text(encoding="utf-8"))
    mapping = {}
    for u in users:
        uid = u.get("id", "")
        name = u.get("real_name", u.get("name", ""))
        username = u.get("name", "")
        mapping[uid] = {"name": name, "username": username}
    return mapping


def find_target_user(users: dict, target: str) -> Optional[str]:
    """Find user ID matching the target name or username."""
    target_lower = target.lower()
    for uid, info in users.items():
        if (target_lower in info["name"].lower() or
            target_lower in info["username"].lower() or
            target_lower == uid.lower()):
            return uid
    return None


def parse_channel_messages(channel_dir: Path, target_uid: str, users: dict) -> list:
    """Parse all JSON files in a channel directory for target user messages."""
    messages = []
    if not channel_dir.is_dir():
        return messages

    for json_file in sorted(channel_dir.glob("*.json")):
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        for msg in data:
            if not isinstance(msg, dict):
                continue
            if msg.get("user") != target_uid:
                continue
            if msg.get("subtype") in ("channel_join", "channel_leave", "bot_message"):
                continue

            text = msg.get("text", "").strip()
            if not text:
                continue

            # Replace user mentions with names
            for uid, info in users.items():
                text = text.replace(f"<@{uid}>", f"@{info['name']}")

            ts = msg.get("ts", "0")
            try:
                dt = datetime.fromtimestamp(float(ts), tz=timezone.utc)
                timestamp = dt.strftime("%Y-%m-%d %H:%M")
            except (ValueError, OSError):
                timestamp = "unknown"

            messages.append({
                "channel": channel_dir.name,
                "timestamp": timestamp,
                "text": text,
                "thread_ts": msg.get("thread_ts"),
                "reply_count": msg.get("reply_count", 0),
                "reactions": [r["name"] for r in msg.get("reactions", [])],
            })

    return messages


def parse_export(export_path: str, target: str, output: str):
    """Parse a Slack export (directory or zip) for target user messages."""

    export = Path(export_path)

    # Handle zip file
    if export.suffix == ".zip":
        tmp_dir = tempfile.mkdtemp(prefix="slack_export_")
        with zipfile.ZipFile(export, "r") as zf:
            zf.extractall(tmp_dir)
        export_dir = Path(tmp_dir)
        # Find the actual export root (might be nested)
        if (export_dir / "users.json").exists():
            pass
        else:
            subdirs = [d for d in export_dir.iterdir() if d.is_dir()]
            if subdirs and (subdirs[0] / "users.json").exists():
                export_dir = subdirs[0]
    else:
        export_dir = export

    # Load users
    users = load_users(export_dir)
    if not users:
        print("⚠️  No users.json found in export. Will match by raw user field.")

    # Find target user
    target_uid = find_target_user(users, target)
    if not target_uid:
        print(f"⚠️  Could not find user matching '{target}'. Available users:")
        for uid, info in list(users.items())[:20]:
            print(f"   {info['name']} (@{info['username']}) — {uid}")
        sys.exit(1)

    target_info = users[target_uid]
    print(f"Found target: {target_info['name']} (@{target_info['username']})")

    # Parse all channels
    all_messages = []
    channels_file = export_dir / "channels.json"
    if channels_file.exists():
        channels = json.loads(channels_file.read_text(encoding="utf-8"))
        channel_names = [c["name"] for c in channels]
    else:
        channel_names = [d.name for d in export_dir.iterdir() if d.is_dir() and d.name != "__MACOSX"]

    for channel_name in channel_names:
        channel_dir = export_dir / channel_name
        messages = parse_channel_messages(channel_dir, target_uid, users)
        all_messages.extend(messages)

    # Sort by timestamp
    all_messages.sort(key=lambda m: m["timestamp"])

    # Write output
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Slack Messages from {target_info['name']}\n")
        f.write(f"# Total: {len(all_messages)} messages\n")
        f.write(f"# Channels: {len(set(m['channel'] for m in all_messages))}\n\n")

        current_channel = None
        for msg in all_messages:
            if msg["channel"] != current_channel:
                current_channel = msg["channel"]
                f.write(f"\n## #{current_channel}\n\n")

            thread_marker = " [thread]" if msg.get("thread_ts") else ""
            reactions_str = f" [{', '.join(msg['reactions'])}]" if msg["reactions"] else ""
            f.write(f"[{msg['timestamp']}]{thread_marker}{reactions_str} {msg['text']}\n")

    print(f"✅ Extracted {len(all_messages)} messages → {output}")


def main():
    parser = argparse.ArgumentParser(description="Parse Slack export for target user")
    parser.add_argument("--file", "--dir", dest="export_path", required=True, help="Path to Slack export (zip or directory)")
    parser.add_argument("--target", required=True, help="Target user name or username")
    parser.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()
    parse_export(args.export_path, args.target, args.output)


if __name__ == "__main__":
    main()
