#!/usr/bin/env python3
"""Read AI API client - Fetch meetings, transcripts, action items, and more.

Usage:
    python readai_client.py list                          # List recent meetings
    python readai_client.py get <meeting_id>              # Get meeting details
    python readai_client.py get <meeting_id> --transcript # Include transcript
    python readai_client.py get <meeting_id> --actions    # Action items only
    python readai_client.py export <meeting_id>           # Export as markdown
    python readai_client.py export <meeting_id> --format json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TIMEZONE = "America/Chicago"
TZ = ZoneInfo(TIMEZONE)
API_BASE = "https://api.read.ai/v1"
API_KEY_PATH = os.path.expanduser("~/.config/readai/api-key")
DATA_DIR = Path(os.path.expanduser("~/.readai/meetings"))
INDEX_PATH = DATA_DIR / "index.json"


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
def load_api_key() -> str:
    """Load API key from file."""
    p = Path(API_KEY_PATH)
    if not p.exists():
        print(f"Error: API key not found at {API_KEY_PATH}", file=sys.stderr)
        print("Set up: mkdir -p ~/.config/readai && echo 'YOUR_KEY' > ~/.config/readai/api-key", file=sys.stderr)
        sys.exit(1)
    return p.read_text().strip()


def api_headers(api_key: str) -> dict:
    """Build request headers."""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


# ---------------------------------------------------------------------------
# API Methods
# ---------------------------------------------------------------------------
def list_meetings(api_key: str, days: int = 7, limit: int = 50) -> list[dict]:
    """List meetings from the last N days."""
    headers = api_headers(api_key)
    since = (datetime.now(TZ) - timedelta(days=days)).isoformat()

    params = {
        "since": since,
        "limit": min(limit, 100),
        "order": "desc",
    }

    resp = requests.get(f"{API_BASE}/meetings", headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    meetings = data.get("meetings", data.get("data", data.get("results", [])))
    if isinstance(meetings, dict):
        meetings = meetings.get("meetings", [])

    # Cache to local index
    update_index(meetings)
    return meetings


def get_meeting(api_key: str, meeting_id: str, include_transcript: bool = False) -> dict:
    """Get full meeting details by ID."""
    headers = api_headers(api_key)
    params = {}
    if include_transcript:
        params["include"] = "transcript"

    resp = requests.get(f"{API_BASE}/meetings/{meeting_id}", headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    meeting = resp.json()

    # Cache locally
    cache_meeting(meeting)
    return meeting


def get_meeting_transcript(api_key: str, meeting_id: str) -> list[dict]:
    """Get the full transcript for a meeting."""
    headers = api_headers(api_key)
    resp = requests.get(f"{API_BASE}/meetings/{meeting_id}/transcript", headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("transcript", data.get("entries", data.get("data", [])))


def get_meeting_action_items(api_key: str, meeting_id: str) -> list[dict]:
    """Get action items for a meeting."""
    headers = api_headers(api_key)
    resp = requests.get(f"{API_BASE}/meetings/{meeting_id}/action-items", headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("action_items", data.get("actionItems", data.get("data", [])))


def get_meeting_summary(api_key: str, meeting_id: str) -> dict:
    """Get AI summary for a meeting."""
    headers = api_headers(api_key)
    resp = requests.get(f"{API_BASE}/meetings/{meeting_id}/summary", headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Local Cache
# ---------------------------------------------------------------------------
def cache_meeting(meeting: dict) -> Path:
    """Cache meeting data locally."""
    meeting_id = meeting.get("id", meeting.get("meetingId", "unknown"))
    start = meeting.get("startTime", meeting.get("start_time", ""))

    # Determine date folder
    if start:
        try:
            dt = datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(TZ)
            date_str = dt.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            date_str = datetime.now(TZ).strftime("%Y-%m-%d")
    else:
        date_str = datetime.now(TZ).strftime("%Y-%m-%d")

    day_dir = DATA_DIR / date_str
    day_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON
    json_path = day_dir / f"{meeting_id}.json"
    json_path.write_text(json.dumps(meeting, indent=2, default=str))

    # Save markdown
    md_path = day_dir / f"{meeting_id}.md"
    md_path.write_text(format_meeting_markdown(meeting))

    return json_path


def update_index(meetings: list[dict]):
    """Update the local meeting index for search."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing index
    index = {}
    if INDEX_PATH.exists():
        try:
            index = json.loads(INDEX_PATH.read_text())
        except (json.JSONDecodeError, IOError):
            index = {}

    # Add/update meetings
    for m in meetings:
        mid = m.get("id", m.get("meetingId", ""))
        if not mid:
            continue
        index[mid] = {
            "id": mid,
            "title": m.get("title", m.get("meetingTitle", "Untitled")),
            "start": m.get("startTime", m.get("start_time", "")),
            "end": m.get("endTime", m.get("end_time", "")),
            "duration": m.get("duration", ""),
            "participants": [
                p.get("name", p.get("displayName", str(p)))
                if isinstance(p, dict) else str(p)
                for p in (m.get("participants", m.get("attendees", [])) or [])
            ],
            "indexed_at": datetime.now(TZ).isoformat(),
        }

    INDEX_PATH.write_text(json.dumps(index, indent=2, default=str))


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------
def format_meeting_markdown(meeting: dict) -> str:
    """Format a meeting as markdown."""
    title = meeting.get("title", meeting.get("meetingTitle", "Meeting"))
    lines = [f"# {title}\n"]

    # Time
    start = meeting.get("startTime", meeting.get("start_time", ""))
    end = meeting.get("endTime", meeting.get("end_time", ""))
    duration = meeting.get("duration", meeting.get("meeting_duration", ""))

    if start:
        lines.append(f"**Start:** {_fmt_time(start)}")
    if end:
        lines.append(f"**End:** {_fmt_time(end)}")
    if duration:
        lines.append(f"**Duration:** {duration}")

    # Participants
    participants = meeting.get("participants", meeting.get("attendees", []))
    if participants:
        lines.append("\n## Participants")
        for p in participants:
            if isinstance(p, dict):
                name = p.get("name", p.get("displayName", str(p)))
                email = p.get("email", "")
                engagement = p.get("engagement", p.get("engagementScore", ""))
                detail = f" ({email})" if email else ""
                detail += f" - engagement: {engagement}" if engagement else ""
                lines.append(f"- {name}{detail}")
            else:
                lines.append(f"- {p}")

    # Summary
    summary = meeting.get("summary", meeting.get("meeting_summary", meeting.get("recap", "")))
    if summary:
        lines.append("\n## Summary")
        lines.append(str(summary))

    # Topics
    topics = meeting.get("topics", meeting.get("key_topics", meeting.get("keyTopics", [])))
    if topics:
        lines.append("\n## Key Topics")
        for t in (topics if isinstance(topics, list) else [topics]):
            if isinstance(t, dict):
                lines.append(f"- {t.get('title', t.get('name', str(t)))}")
            else:
                lines.append(f"- {t}")

    # Action Items
    actions = meeting.get("action_items", meeting.get("actionItems", meeting.get("tasks", [])))
    if actions:
        lines.append("\n## Action Items")
        for item in (actions if isinstance(actions, list) else [actions]):
            if isinstance(item, dict):
                text = item.get("text", item.get("description", item.get("title", str(item))))
                assignee = item.get("assignee", item.get("owner", ""))
                due = item.get("dueDate", item.get("due_date", ""))
                suffix = f" (@{assignee})" if assignee else ""
                suffix += f" [due: {due}]" if due else ""
                lines.append(f"- [ ] {text}{suffix}")
            else:
                lines.append(f"- [ ] {item}")

    # Decisions
    decisions = meeting.get("decisions", meeting.get("key_decisions", []))
    if decisions:
        lines.append("\n## Decisions")
        for d in (decisions if isinstance(decisions, list) else [decisions]):
            lines.append(f"- {d}")

    # Transcript excerpt
    transcript = meeting.get("transcript", meeting.get("transcription", []))
    if transcript:
        lines.append("\n## Transcript")
        entries = transcript if isinstance(transcript, list) else []
        if isinstance(transcript, str):
            lines.append(transcript[:3000])
            if len(transcript) > 3000:
                lines.append(f"\n*[Truncated - {len(transcript)} chars total]*")
        else:
            for entry in entries[:30]:
                if isinstance(entry, dict):
                    speaker = entry.get("speaker", entry.get("speakerName", "?"))
                    text = entry.get("text", entry.get("content", ""))
                    ts = entry.get("timestamp", entry.get("time", ""))
                    prefix = f"[{ts}] " if ts else ""
                    lines.append(f"{prefix}**{speaker}:** {text}")
                else:
                    lines.append(str(entry))
            if len(entries) > 30:
                lines.append(f"\n*[Showing 30 of {len(entries)} entries]*")

    return "\n".join(lines)


def _fmt_time(iso_str: str) -> str:
    """Format ISO time to human-readable CT."""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00")).astimezone(TZ)
        return dt.strftime("%b %d, %Y %-I:%M %p CT")
    except (ValueError, TypeError):
        return iso_str


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def cmd_list(args):
    api_key = load_api_key()
    meetings = list_meetings(api_key, days=args.days, limit=args.limit)

    if not meetings:
        print(f"No meetings found in the last {args.days} days.")
        return

    if args.json:
        print(json.dumps(meetings, indent=2, default=str))
        return

    print(f"\n{'='*60}")
    print(f" Read AI Meetings - Last {args.days} days ({len(meetings)} found)")
    print(f"{'='*60}\n")

    for m in meetings:
        mid = m.get("id", m.get("meetingId", "?"))
        title = m.get("title", m.get("meetingTitle", "Untitled"))
        start = m.get("startTime", m.get("start_time", ""))
        duration = m.get("duration", "")
        participants = m.get("participants", m.get("attendees", []))
        n_people = len(participants) if isinstance(participants, list) else 0

        print(f"  {title}")
        print(f"    ID: {mid}")
        if start:
            print(f"    Time: {_fmt_time(start)}")
        if duration:
            print(f"    Duration: {duration}")
        if n_people:
            print(f"    Participants: {n_people}")
        print()


def cmd_get(args):
    api_key = load_api_key()

    if args.actions:
        actions = get_meeting_action_items(api_key, args.meeting_id)
        if args.json:
            print(json.dumps(actions, indent=2, default=str))
        else:
            print("\n## Action Items\n")
            for item in actions:
                if isinstance(item, dict):
                    text = item.get("text", item.get("description", str(item)))
                    assignee = item.get("assignee", "")
                    suffix = f" (@{assignee})" if assignee else ""
                    print(f"- [ ] {text}{suffix}")
                else:
                    print(f"- [ ] {item}")
        return

    meeting = get_meeting(api_key, args.meeting_id, include_transcript=args.transcript)

    if args.json:
        print(json.dumps(meeting, indent=2, default=str))
    else:
        print(format_meeting_markdown(meeting))


def cmd_export(args):
    api_key = load_api_key()
    meeting = get_meeting(api_key, args.meeting_id, include_transcript=True)

    if args.format == "json":
        output = json.dumps(meeting, indent=2, default=str)
    else:
        output = format_meeting_markdown(meeting)

    if args.output:
        Path(args.output).write_text(output)
        print(f"Exported to {args.output}")
    else:
        print(output)


def main():
    parser = argparse.ArgumentParser(description="Read AI API Client")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = sub.add_parser("list", help="List recent meetings")
    p_list.add_argument("--days", type=int, default=7, help="Days to look back (default: 7)")
    p_list.add_argument("--limit", type=int, default=50, help="Max meetings (default: 50)")
    p_list.add_argument("--today", action="store_true", help="Today only")
    p_list.add_argument("--json", action="store_true", help="JSON output")
    p_list.set_defaults(func=cmd_list)

    # get
    p_get = sub.add_parser("get", help="Get meeting details")
    p_get.add_argument("meeting_id", help="Meeting ID")
    p_get.add_argument("--transcript", action="store_true", help="Include full transcript")
    p_get.add_argument("--actions", action="store_true", help="Action items only")
    p_get.add_argument("--json", action="store_true", help="JSON output")
    p_get.set_defaults(func=cmd_get)

    # export
    p_export = sub.add_parser("export", help="Export meeting")
    p_export.add_argument("meeting_id", help="Meeting ID")
    p_export.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p_export.add_argument("--output", "-o", help="Output file path")
    p_export.set_defaults(func=cmd_export)

    args = parser.parse_args()

    # Handle --today for list
    if args.command == "list" and hasattr(args, "today") and args.today:
        args.days = 0

    args.func(args)


if __name__ == "__main__":
    main()
