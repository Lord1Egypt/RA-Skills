#!/usr/bin/env python3
"""Search Read AI meetings by keyword, speaker, or date range.

Usage:
    python search_meetings.py "quarterly review"
    python search_meetings.py "budget" --days 30
    python search_meetings.py "action items" --speaker "Brandon"
    python search_meetings.py --speaker "John" --days 14
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(__file__))
from readai_client import load_api_key, list_meetings, get_meeting, _fmt_time, DATA_DIR, INDEX_PATH, TZ


def search_local_index(query: str, speaker: str = None, days: int = 30) -> list[dict]:
    """Search the local meeting index."""
    if not INDEX_PATH.exists():
        return []

    try:
        index = json.loads(INDEX_PATH.read_text())
    except (json.JSONDecodeError, IOError):
        return []

    cutoff = datetime.now(TZ) - timedelta(days=days)
    results = []

    for mid, info in index.items():
        # Date filter
        start = info.get("start", "")
        if start:
            try:
                dt = datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(TZ)
                if dt < cutoff:
                    continue
            except (ValueError, TypeError):
                pass

        # Speaker filter
        if speaker:
            participants = [p.lower() for p in info.get("participants", [])]
            if not any(speaker.lower() in p for p in participants):
                continue

        # Query filter (search title and participants)
        if query:
            title = info.get("title", "").lower()
            all_text = title + " " + " ".join(info.get("participants", []))

            # Also check cached markdown files
            cached_content = ""
            date_str = ""
            if start:
                try:
                    dt = datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(TZ)
                    date_str = dt.strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    pass

            if date_str:
                md_path = DATA_DIR / date_str / f"{mid}.md"
                if md_path.exists():
                    try:
                        cached_content = md_path.read_text().lower()
                    except IOError:
                        pass

            searchable = (all_text + " " + cached_content).lower()
            if query.lower() not in searchable:
                continue

        results.append(info)

    # Sort by start time, newest first
    results.sort(key=lambda x: x.get("start", ""), reverse=True)
    return results


def search_api(api_key: str, query: str, speaker: str = None, days: int = 30) -> list[dict]:
    """Search via API - fetch meetings and filter."""
    meetings = list_meetings(api_key, days=days, limit=100)

    results = []
    for m in meetings:
        # Speaker filter
        if speaker:
            participants = m.get("participants", m.get("attendees", []))
            names = []
            for p in (participants or []):
                if isinstance(p, dict):
                    names.append((p.get("name", "") or p.get("displayName", "")).lower())
                else:
                    names.append(str(p).lower())
            if not any(speaker.lower() in n for n in names):
                continue

        # Query filter
        if query:
            searchable = json.dumps(m, default=str).lower()
            if query.lower() not in searchable:
                continue

        results.append(m)

    return results


def main():
    parser = argparse.ArgumentParser(description="Search Read AI meetings")
    parser.add_argument("query", nargs="?", default="", help="Search query")
    parser.add_argument("--speaker", "-s", help="Filter by speaker/participant name")
    parser.add_argument("--days", type=int, default=30, help="Days to search back (default: 30)")
    parser.add_argument("--local-only", action="store_true", help="Search local cache only (no API)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if not args.query and not args.speaker:
        parser.error("Provide a search query and/or --speaker filter")

    # Try local first
    results = search_local_index(args.query, args.speaker, args.days)

    # Fall back to API if no local results and not local-only
    if not results and not args.local_only:
        try:
            api_key = load_api_key()
            results = search_api(api_key, args.query, args.speaker, args.days)
        except SystemExit:
            pass  # No API key configured

    if not results:
        filters = []
        if args.query:
            filters.append(f'"{args.query}"')
        if args.speaker:
            filters.append(f"speaker: {args.speaker}")
        print(f"No meetings found matching {', '.join(filters)} in the last {args.days} days.")
        return

    if args.json:
        print(json.dumps(results, indent=2, default=str))
        return

    # Display results
    filters = []
    if args.query:
        filters.append(f'"{args.query}"')
    if args.speaker:
        filters.append(f"speaker: {args.speaker}")

    print(f"\n  Search Results: {', '.join(filters)} ({len(results)} found)\n")

    for r in results:
        title = r.get("title", "Untitled")
        mid = r.get("id", r.get("meetingId", ""))
        start = r.get("start", r.get("startTime", r.get("start_time", "")))
        participants = r.get("participants", [])

        print(f"  {title}")
        if mid:
            print(f"    ID: {mid}")
        if start:
            print(f"    When: {_fmt_time(start)}")
        if participants:
            names = participants[:5]
            extras = len(participants) - 5
            display = ", ".join(str(n) for n in names)
            if extras > 0:
                display += f" +{extras} more"
            print(f"    People: {display}")
        print()


if __name__ == "__main__":
    main()
