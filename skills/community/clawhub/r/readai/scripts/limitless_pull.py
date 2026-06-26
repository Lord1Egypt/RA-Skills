#!/usr/bin/env python3
"""Pull meeting/conversation data from Limitless AI pendant.

Usage:
    python limitless_pull.py --today           # Today's data
    python limitless_pull.py 2026-02-19        # Specific date
    python limitless_pull.py --today --ai      # With AI summary
    python limitless_pull.py --days 7          # Last 7 days
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

TIMEZONE = os.environ.get("READAI_TIMEZONE", "America/Chicago")
TZ = ZoneInfo(TIMEZONE)
API_BASE = "https://api.limitless.ai/v1"
API_KEY_PATH = os.path.expanduser("~/.config/readai/api-key")
DATA_DIR = Path(os.path.expanduser("~/.readai/lifelogs"))
PAGE_LIMIT = 10


def load_api_key() -> str:
    p = Path(API_KEY_PATH)
    if not p.exists():
        # Fallback to limitless-specific path
        alt = Path(os.path.expanduser("~/.config/limitless/api-key"))
        if alt.exists():
            return alt.read_text().strip()
        print(f"Error: API key not found at {API_KEY_PATH}", file=sys.stderr)
        sys.exit(1)
    return p.read_text().strip()


def fetch_lifelogs(api_key: str, date_str: str) -> list[dict]:
    """Fetch all lifelogs for a date, with pagination."""
    headers = {"X-API-Key": api_key}
    all_logs = []
    cursor = None

    while True:
        params = {
            "timezone": TIMEZONE,
            "date": date_str,
            "limit": PAGE_LIMIT,
            "includeMarkdown": "true",
            "includeHeadings": "true",
        }
        if cursor:
            params["cursor"] = cursor

        resp = requests.get(f"{API_BASE}/lifelogs", headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        logs = data.get("data", {}).get("lifelogs", [])
        if not logs:
            break

        all_logs.extend(logs)
        cursor = data.get("data", {}).get("cursor")
        if not cursor:
            break

    return all_logs


def extract_info(lifelog: dict) -> dict:
    """Extract key info from a lifelog entry."""
    contents = lifelog.get("contents", [])
    parts = []
    speakers = set()

    for block in contents:
        btype = block.get("type", "")
        content = block.get("content", "")
        speaker = block.get("speakerName")

        if speaker and speaker.lower() != "unknown":
            speakers.add(speaker)

        if btype == "heading1":
            parts.append(f"## {content}")
        elif btype == "heading2":
            parts.append(f"### {content}")
        elif btype == "blockquote":
            name = speaker or "Unknown"
            parts.append(f"> **{name}:** {content}")
        elif btype == "list-item":
            parts.append(f"- {content}")
        elif content:
            parts.append(content)

    return {
        "id": lifelog.get("id", "unknown"),
        "title": lifelog.get("title", "Untitled"),
        "start_time": lifelog.get("startTime", ""),
        "end_time": lifelog.get("endTime", ""),
        "speakers": sorted(speakers),
        "content": "\n".join(parts),
    }


def fmt_time(iso_str: str) -> str:
    if not iso_str:
        return "?"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00")).astimezone(TZ)
        return dt.strftime("%-I:%M %p")
    except (ValueError, TypeError):
        return iso_str


def save_data(date_str: str, lifelogs: list[dict], entries: list[dict], summary: str = None):
    """Save to disk."""
    day_dir = DATA_DIR / date_str
    day_dir.mkdir(parents=True, exist_ok=True)

    (day_dir / "raw_lifelogs.json").write_text(json.dumps(lifelogs, indent=2, default=str))
    (day_dir / "entries.json").write_text(json.dumps(entries, indent=2, default=str))

    if summary:
        (day_dir / "digest.md").write_text(summary)


def basic_summary(date_str: str, entries: list[dict]) -> str:
    """Generate basic text summary."""
    lines = [f"## Daily Digest - {date_str}\n"]

    all_speakers = set()
    for e in entries:
        all_speakers.update(e["speakers"])

    if all_speakers:
        lines.append("### People")
        for s in sorted(all_speakers):
            lines.append(f"- {s}")
        lines.append("")

    lines.append("### Conversations")
    for e in entries:
        t = f"{fmt_time(e['start_time'])} - {fmt_time(e['end_time'])}"
        who = ", ".join(e["speakers"]) if e["speakers"] else "Solo"
        lines.append(f"- **{e['title']}** ({t}) - {who}")

    lines.append(f"\n*{len(entries)} entries on {date_str}*")
    return "\n".join(lines)


def ai_summary(date_str: str, entries: list[dict]) -> str:
    """Generate AI-powered summary via Claude CLI."""
    entry_texts = []
    for e in entries:
        t = f"{fmt_time(e['start_time'])} - {fmt_time(e['end_time'])}"
        who = ", ".join(e["speakers"]) if e["speakers"] else "Solo"
        entry_texts.append(f"### {e['title']}\n**Time:** {t}\n**With:** {who}\n\n{e['content'][:3000]}\n")

    prompt = f"""Summarize Brandon's day from Limitless pendant recordings for {date_str}.

{chr(10).join(entry_texts)}

Sections: People talked to, Key conversations, Action items, Notable decisions, Quick 2-3 sentence summary.
Keep it concise and actionable."""

    try:
        result = subprocess.run(
            ["claude", "-p", "--model", "sonnet"],
            input=prompt, capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return basic_summary(date_str, entries)


def run(date_str: str, use_ai: bool = False) -> str:
    api_key = load_api_key()
    lifelogs = fetch_lifelogs(api_key, date_str)

    if not lifelogs:
        return f"No data found for {date_str}."

    entries = [extract_info(ll) for ll in lifelogs]
    summary = ai_summary(date_str, entries) if use_ai else basic_summary(date_str, entries)
    save_data(date_str, lifelogs, entries, summary)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Pull Limitless pendant data")
    parser.add_argument("date", nargs="?", help="YYYY-MM-DD (default: yesterday)")
    parser.add_argument("--today", action="store_true")
    parser.add_argument("--days", type=int, help="Pull last N days")
    parser.add_argument("--ai", action="store_true", help="AI-powered summary")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    now = datetime.now(TZ)

    if args.days:
        for i in range(args.days):
            d = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            print(f"\n{'='*40}\n{d}\n{'='*40}")
            print(run(d, args.ai))
    else:
        if args.date:
            date_str = args.date
        elif args.today:
            date_str = now.strftime("%Y-%m-%d")
        else:
            date_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")

        print(run(date_str, args.ai))


if __name__ == "__main__":
    main()
