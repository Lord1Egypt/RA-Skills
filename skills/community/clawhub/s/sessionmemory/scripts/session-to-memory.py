#!/usr/bin/env python3
"""
session-to-memory.py - Convert OpenClaw JSONL session logs to searchable Markdown.

Reads all session JSONL files, converts them to clean Markdown transcripts,
saves them to memory/sessions/, and triggers re-indexing by OpenClaw's
memory vector store (which auto-watches memory/*.md files).

Usage:
    python3 scripts/session-to-memory.py [--force]  # Convert all sessions
    python3 scripts/session-to-memory.py --new       # Only new/changed sessions
"""

import json
import glob
import os
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path

SESSIONS_DIR = os.path.expanduser("~/.openclaw/agents/main/sessions")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory/sessions")
STATE_FILE = os.path.join(MEMORY_DIR, ".state.json")
MIN_MESSAGES = 5  # Skip tiny sessions (system-only, heartbeats)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"processed": {}}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def file_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def parse_session(jsonl_path):
    messages = []
    metadata = {}
    with open(jsonl_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            role = entry.get("role", "")
            content = entry.get("content", "")

            # Extract text from content (can be string or list)
            if isinstance(content, list):
                text_parts = []
                for part in content:
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            text_parts.append(part.get("text", ""))
                    elif isinstance(part, str):
                        text_parts.append(part)
                text = "\n".join(text_parts)
            elif isinstance(content, str):
                text = content
            else:
                text = str(content) if content else ""

            if not text.strip():
                continue

            # Skip tool calls and system messages for readability
            if role == "tool":
                continue

            # Extract sender info from metadata
            sender = ""
            if role == "user":
                # Try to find sender name in the text
                if "Sender (untrusted metadata)" in text:
                    try:
                        sender_match = text.split('"name": "')[1].split('"')[0]
                        sender = sender_match
                    except (IndexError, KeyError):
                        pass

                # Clean up the text - remove metadata blocks
                clean_text = text
                # Remove JSON metadata blocks
                import re
                clean_text = re.sub(r'Conversation info \(untrusted metadata\):.*?```\n', '', clean_text, flags=re.DOTALL)
                clean_text = re.sub(r'Sender \(untrusted metadata\):.*?```\n', '', clean_text, flags=re.DOTALL)
                clean_text = clean_text.strip()
                if not clean_text:
                    continue
                text = clean_text

            messages.append({
                "role": role,
                "sender": sender,
                "text": text[:5000],  # Truncate very long messages
            })

            # Track session metadata
            if not metadata.get("first_timestamp"):
                # Try to extract timestamp
                if "timestamp" in text:
                    try:
                        ts = text.split('"timestamp": "')[1].split('"')[0]
                        metadata["first_timestamp"] = ts
                    except (IndexError, KeyError):
                        pass

    return messages, metadata

def convert_to_markdown(messages, session_id, metadata):
    lines = []
    ts = metadata.get("first_timestamp", "unknown")
    lines.append(f"# Session: {session_id}")
    lines.append(f"_Started: {ts}_\n")

    for msg in messages:
        role = msg["role"]
        sender = msg.get("sender", "")
        text = msg["text"]

        if role == "user":
            label = f"**{sender}**" if sender else "**User**"
        elif role == "assistant":
            label = "**Assistant**"
        elif role == "system":
            label = "**System**"
        else:
            label = f"**{role}**"

        lines.append(f"{label}: {text}\n")

    return "\n".join(lines)

def main():
    force = "--force" in sys.argv
    new_only = "--new" in sys.argv

    os.makedirs(MEMORY_DIR, exist_ok=True)
    state = load_state()

    if not os.path.isdir(SESSIONS_DIR):
        print(f"Sessions directory not found: {SESSIONS_DIR}")
        sys.exit(1)

    jsonl_files = glob.glob(os.path.join(SESSIONS_DIR, "*.jsonl"))
    print(f"Found {len(jsonl_files)} session files")

    converted = 0
    skipped = 0

    for jsonl_path in sorted(jsonl_files):
        session_id = os.path.basename(jsonl_path).replace(".jsonl", "")
        output_path = os.path.join(MEMORY_DIR, f"session-{session_id[:30]}.md")

        # Check if already processed (unless force)
        if not force:
            current_hash = file_hash(jsonl_path)
            if state["processed"].get(session_id) == current_hash:
                skipped += 1
                continue

        messages, metadata = parse_session(jsonl_path)

        if len(messages) < MIN_MESSAGES:
            skipped += 1
            continue

        markdown = convert_to_markdown(messages, session_id, metadata)

        with open(output_path, "w") as f:
            f.write(markdown)

        state["processed"][session_id] = file_hash(jsonl_path)
        converted += 1

    save_state(state)
    print(f"Converted: {converted}, Skipped: {skipped}")

if __name__ == "__main__":
    main()
