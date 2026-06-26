#!/usr/bin/env python3
"""List Read AI meetings - quick convenience wrapper.

Usage:
    python list_meetings.py              # Last 7 days
    python list_meetings.py --days 30    # Last 30 days
    python list_meetings.py --today      # Today only
    python list_meetings.py --json       # JSON output
"""

import sys
import os

# Add parent scripts dir to path
sys.path.insert(0, os.path.dirname(__file__))
from readai_client import load_api_key, list_meetings, _fmt_time

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="List Read AI meetings")
    parser.add_argument("--days", type=int, default=7, help="Days to look back")
    parser.add_argument("--today", action="store_true", help="Today only")
    parser.add_argument("--limit", type=int, default=50, help="Max results")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.today:
        args.days = 0

    api_key = load_api_key()
    meetings = list_meetings(api_key, days=args.days, limit=args.limit)

    if not meetings:
        period = "today" if args.today else f"the last {args.days} days"
        print(f"No meetings found for {period}.")
        return

    if args.json:
        print(json.dumps(meetings, indent=2, default=str))
        return

    period = "Today" if args.today else f"Last {args.days} days"
    print(f"\n  Read AI Meetings - {period} ({len(meetings)} found)\n")

    for m in meetings:
        title = m.get("title", m.get("meetingTitle", "Untitled"))
        mid = m.get("id", m.get("meetingId", ""))
        start = m.get("startTime", m.get("start_time", ""))
        duration = m.get("duration", "")
        participants = m.get("participants", m.get("attendees", []))
        n_people = len(participants) if isinstance(participants, list) else 0
        summary = m.get("summary", "")

        print(f"  {title}")
        print(f"    ID: {mid}")
        if start:
            print(f"    When: {_fmt_time(start)}")
        if duration:
            print(f"    Duration: {duration}")
        if n_people:
            print(f"    People: {n_people}")
        if summary:
            # First 120 chars of summary
            preview = summary[:120].replace("\n", " ")
            if len(summary) > 120:
                preview += "..."
            print(f"    Summary: {preview}")
        print()


if __name__ == "__main__":
    main()
