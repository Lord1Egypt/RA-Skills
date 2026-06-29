#!/usr/bin/env python3
"""
Classify sessions - extract title, message count, timestamps, and last user messages
for session classification.

Usage:
  classify-sessions.py <project_name>

Output: TSV format per session
  session_id | lines | user_msg_count | first_ts | last_ts | title | last_user_messages
"""

import json
import os
import sys
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")


def get_project_dir(project_name: str) -> Path:
    return Path.home() / ".claude" / "projects" / project_name


def extract_session_info(session_file: Path) -> dict:
    session_id = session_file.stem
    lines = 0
    first_user_msg = ""
    custom_title = ""
    first_ts = ""
    last_ts = ""
    user_messages = []
    assistant_count = 0

    try:
        with open(session_file, "r", encoding="utf-8") as f:
            for line in f:
                lines += 1
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg_type = obj.get("type", "")
                ts = obj.get("timestamp", "")

                if ts:
                    if not first_ts:
                        first_ts = ts
                    last_ts = ts

                if msg_type == "custom-title":
                    custom_title = obj.get("customTitle", "")

                elif msg_type == "user":
                    content = obj.get("message", {}).get("content", "")
                    text = ""
                    if isinstance(content, str):
                        text = content[:200]
                    elif isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "text":
                                text = item.get("text", "")[:200]
                                break
                            elif isinstance(item, str):
                                text = item[:200]
                                break

                    # Clean up command tags for display
                    clean_text = text
                    if "<command-message>" in clean_text:
                        import re
                        # Extract command name and args
                        cmd = re.search(r"<command-name>/(\S+)</command-name>", clean_text)
                        args = re.search(r"<command-args>(.*?)</command-args>", clean_text, re.DOTALL)
                        if cmd:
                            clean_text = f"/{cmd.group(1)}"
                            if args and args.group(1).strip():
                                clean_text += f" {args.group(1).strip()[:100]}"
                    elif "<local-command-" in clean_text:
                        clean_text = "(local-command output)"

                    if clean_text:
                        user_messages.append(clean_text)
                        if not first_user_msg:
                            first_user_msg = clean_text

                elif msg_type == "assistant":
                    assistant_count += 1

    except Exception as e:
        return {
            "id": session_id,
            "lines": 0,
            "error": str(e),
        }

    title = custom_title or first_user_msg[:80] or "(empty)"
    last_msgs = user_messages[-3:] if len(user_messages) > 3 else user_messages

    return {
        "id": session_id,
        "lines": lines,
        "user_msg_count": len(user_messages),
        "assistant_count": assistant_count,
        "first_ts": first_ts[:10] if first_ts else "",
        "last_ts": last_ts[:10] if last_ts else "",
        "title": title.replace("\n", " ").replace("\t", " ")[:80],
        "last_user_messages": " | ".join(
            m.replace("\n", " ").replace("\t", " ")[:60] for m in last_msgs
        ),
        "has_custom_title": bool(custom_title),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: classify-sessions.py <project_name>", file=sys.stderr)
        sys.exit(1)

    project_name = sys.argv[1]

    project_dir = get_project_dir(project_name)
    if not project_dir.exists():
        print(f"Error: Project directory not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    sessions = sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)

    if not sessions:
        print("No sessions found.", file=sys.stderr)
        sys.exit(0)

    # Header
    print("ID\tLines\tUserMsgs\tFirstDate\tLastDate\tTitle\tLastMessages")

    for session_file in sessions:
        info = extract_session_info(session_file)
        if "error" in info:
            print(f"{info['id']}\t0\t0\t\t\tERROR: {info['error']}\t", file=sys.stderr)
            continue

        print(
            f"{info['id']}\t"
            f"{info['lines']}\t"
            f"{info['user_msg_count']}\t"
            f"{info['first_ts']}\t"
            f"{info['last_ts']}\t"
            f"{info['title']}\t"
            f"{info['last_user_messages']}"
        )


if __name__ == "__main__":
    main()
