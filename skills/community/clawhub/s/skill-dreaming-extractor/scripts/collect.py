#!/usr/bin/env python3
"""
Dreaming v2 — Session Collector

Reads yesterday's raw session JSONL files, filters out dreaming noise
and system sessions, outputs a clean text file for extraction.

Usage: python3 collect.py [--date YYYY-MM-DD] [--agents-dir DIR] [--output FILE]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

AGENTS_DIR = Path(os.environ.get("OPENCLAW_AGENTS_DIR", os.path.expanduser("~/.openclaw/agents")))
OUTPUT_DIR = Path(os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))) / "memory" / ".dreams" / "extraction-input"

# Patterns in first user message that indicate dreaming/system noise
NOISE_PATTERNS = [
    "write a dream diary entry",
    "dream diary entry from these memory fragments",
    "continue where you left off. the previous model attempt failed",
    "run your session startup sequence",
]

# Max characters per session to include (prevent one massive session from dominating)
MAX_CHARS_PER_SESSION = 15000
# Max total output chars (~50k tokens worth at ~4 chars/token)
MAX_TOTAL_CHARS = 200000


def is_noise_session(first_user_text: str) -> bool:
    lower = first_user_text.lower()
    return any(p in lower for p in NOISE_PATTERNS)


def extract_messages(jsonl_path: Path) -> list[dict]:
    """Extract user/assistant text messages from a session JSONL."""
    messages = []
    session_date = None

    try:
        with open(jsonl_path) as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)

                if entry.get("type") == "session":
                    session_date = entry.get("timestamp", "")[:10]

                if entry.get("type") != "message":
                    continue

                msg = entry.get("message", {})
                role = msg.get("role")
                if role not in ("user", "assistant"):
                    continue

                content = msg.get("content", [])
                if isinstance(content, str):
                    texts = [content]
                elif isinstance(content, list):
                    texts = [c.get("text", "") for c in content if c.get("type") == "text" and c.get("text")]
                else:
                    continue

                for text in texts:
                    if text.strip():
                        messages.append({
                            "role": role,
                            "text": text.strip(),
                            "timestamp": entry.get("timestamp", ""),
                        })
    except (json.JSONDecodeError, OSError) as e:
        print(f"  WARN: failed to read {jsonl_path.name}: {e}", file=sys.stderr)
        return []

    return messages


def collect_sessions(target_date: str, agents_dir: Path) -> list[dict]:
    """Collect all real (non-noise) sessions for a given date."""
    sessions = []

    for agent_dir in sorted(agents_dir.iterdir()):
        sessions_dir = agent_dir / "sessions"
        if not sessions_dir.is_dir():
            continue

        for jsonl_file in sorted(sessions_dir.glob("*.jsonl")):
            # Skip checkpoint files
            if ".checkpoint." in jsonl_file.name:
                continue

            # Check file modification date matches target
            mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime, tz=timezone.utc)
            if mtime.strftime("%Y-%m-%d") != target_date:
                # Also check session start date from first line
                try:
                    with open(jsonl_file) as f:
                        first = json.loads(f.readline())
                        sess_date = first.get("timestamp", "")[:10]
                        if sess_date != target_date:
                            continue
                except (json.JSONDecodeError, OSError):
                    continue

            messages = extract_messages(jsonl_file)
            if not messages:
                continue

            # Check if first user message is noise
            first_user = next((m for m in messages if m["role"] == "user"), None)
            if first_user and is_noise_session(first_user["text"]):
                continue

            # Filter to text messages only, truncate
            text_parts = []
            char_count = 0
            for m in messages:
                chunk = f"[{m['role']}] {m['text']}"
                if char_count + len(chunk) > MAX_CHARS_PER_SESSION:
                    text_parts.append(f"[... truncated at {MAX_CHARS_PER_SESSION} chars ...]")
                    break
                text_parts.append(chunk)
                char_count += len(chunk)

            sessions.append({
                "session_id": jsonl_file.stem,
                "agent": agent_dir.name,
                "messages": text_parts,
                "message_count": len(messages),
                "char_count": char_count,
            })

    return sessions


def format_output(sessions: list[dict], target_date: str) -> str:
    """Format collected sessions into extraction input."""
    lines = [
        f"# Session Extraction Input — {target_date}",
        f"# Collected: {datetime.now(timezone.utc).isoformat()[:19]}Z",
        f"# Sessions: {len(sessions)} (after noise filtering)",
        f"# Total conversations: {sum(s['message_count'] for s in sessions)}",
        "",
    ]

    total_chars = 0
    for i, sess in enumerate(sessions, 1):
        header = f"--- SESSION {i}/{len(sessions)} [{sess['agent']}:{sess['session_id'][:8]}] ({sess['message_count']} messages) ---"
        lines.append(header)

        for msg in sess["messages"]:
            if total_chars + len(msg) > MAX_TOTAL_CHARS:
                lines.append(f"[... total output truncated at {MAX_TOTAL_CHARS} chars ...]")
                return "\n".join(lines)
            lines.append(msg)
            total_chars += len(msg)

        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Collect sessions for dreaming extraction")
    parser.add_argument("--date", default=None, help="Target date YYYY-MM-DD (default: yesterday)")
    parser.add_argument("--agents-dir", default=str(AGENTS_DIR), help="Agents directory")
    parser.add_argument("--output", default=None, help="Output file path")
    parser.add_argument("--stats-only", action="store_true", help="Print stats without writing")
    args = parser.parse_args()

    if args.date:
        target_date = args.date
    else:
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        target_date = yesterday.strftime("%Y-%m-%d")

    agents_dir = Path(args.agents_dir)
    if not agents_dir.exists():
        print(f"ERROR: agents dir not found: {agents_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Collecting sessions for {target_date}...", file=sys.stderr)
    sessions = collect_sessions(target_date, agents_dir)

    if not sessions:
        print(f"No real sessions found for {target_date}", file=sys.stderr)
        sys.exit(0)

    total_msgs = sum(s["message_count"] for s in sessions)
    total_chars = sum(s["char_count"] for s in sessions)
    print(f"Found {len(sessions)} sessions, {total_msgs} messages, ~{total_chars:,} chars", file=sys.stderr)

    if args.stats_only:
        for s in sessions:
            print(f"  {s['agent']}:{s['session_id'][:8]} — {s['message_count']} msgs, {s['char_count']:,} chars")
        sys.exit(0)

    output_text = format_output(sessions, target_date)

    output_dir = OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = output_dir / f"{target_date}.txt"

    output_path.write_text(output_text)
    print(f"Written to {output_path} ({len(output_text):,} chars)", file=sys.stderr)
    print(str(output_path))


if __name__ == "__main__":
    main()
