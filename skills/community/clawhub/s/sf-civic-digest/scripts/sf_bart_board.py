#!/usr/bin/env python3
"""
sf_bart_board.py — BART Board of Directors meeting tracker via Legistar API.

Fetches upcoming and recent BART Board meetings from the Legistar API.
Classifies meetings by body relevance: Board of Directors (HIGH),
Police Citizen Review Board / Accessibility / Bicycle Advisory (MEDIUM),
subcommittees (LOW).

Data source: https://webapi.legistar.com/v1/bart/Events
No authentication required.

Usage:
    # Human-readable output (default 30-day window)
    python sf_bart_board.py

    # JSON output
    python sf_bart_board.py --json

    # Next meeting only
    python sf_bart_board.py --next

    # Custom window (60 days)
    python sf_bart_board.py --days 60

    # Combine flags
    python sf_bart_board.py --json --days 14
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

import urllib.request
import urllib.parse
import urllib.error

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

LEGISTAR_BASE = "https://webapi.legistar.com/v1/bart"
EVENTS_URL = f"{LEGISTAR_BASE}/Events"

ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), "sf_bart_board_archive.json")
ARCHIVE_MAX = 5000

# Bodies we care about, mapped to relevance tier
HIGH_BODIES = [
    "Board of Directors",
]

MEDIUM_BODIES = [
    "Police Citizen Review Board",
    "Accessibility Task Force",
    "Bicycle Advisory Task Force",
]

# Everything else is LOW


# ---------------------------------------------------------------------------
# Archive management
# ---------------------------------------------------------------------------

def load_archive():
    if os.path.exists(ARCHIVE_FILE):
        try:
            with open(ARCHIVE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"items": []}


def save_archive(archive):
    archive["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(ARCHIVE_FILE, "w") as f:
        json.dump(archive, f, indent=2)


def update_archive(new_records):
    """Merge new records into archive. Dedup by EventId. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_ids = {r["id"] for r in archive["items"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for record in new_records:
        if record["id"] not in existing_ids:
            record["scraped_at"] = now
            archive["items"].append(record)
            existing_ids.add(record["id"])
            added += 1
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new records ({len(archive['items'])} total)", file=sys.stderr)
    return archive


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_json(url, timeout=30):
    """Fetch a URL and return parsed JSON."""
    headers = {
        "Accept": "application/json",
        "User-Agent": "sf-civic-digest/1.0 (civic monitoring bot)",
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode("utf-8", errors="replace")
            return json.loads(data)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} fetching {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Legistar API
# ---------------------------------------------------------------------------

def fetch_events(days=30):
    """Fetch BART events from Legistar API within a date window."""
    start_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = (datetime.now(timezone.utc) + timedelta(days=days)).strftime("%Y-%m-%d")

    params = {
        "$top": "100",
        "$orderby": "EventDate desc",
        "$filter": f"EventDate ge datetime'{start_date}' and EventDate le datetime'{end_date}'",
    }
    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    url = f"{EVENTS_URL}?{query}"

    print(f"Fetching BART events ({days}-day window)...", file=sys.stderr)
    data = fetch_json(url)
    if data is None:
        return []

    if not isinstance(data, list):
        print(f"Unexpected response type: {type(data)}", file=sys.stderr)
        return []

    return data


def classify_body(body_name):
    """Classify a meeting body by relevance tier."""
    if not body_name:
        return "low"
    for name in HIGH_BODIES:
        if name.lower() in body_name.lower():
            return "high"
    for name in MEDIUM_BODIES:
        if name.lower() in body_name.lower():
            return "medium"
    return "low"


def parse_event(event):
    """Parse a Legistar event into our normalized format."""
    event_id = event.get("EventId")
    body_name = event.get("EventBodyName", "")
    raw_date = event.get("EventDate", "")
    event_time = event.get("EventTime", "")
    location = event.get("EventLocation", "")
    agenda_url = event.get("EventAgendaFile", "")
    meeting_url = event.get("EventInSiteURL", "")
    agenda_status = event.get("EventAgendaStatusName", "")

    # Parse date — Legistar returns "2026-03-26T00:00:00"
    event_date = ""
    if raw_date:
        try:
            dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            event_date = dt.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            event_date = raw_date[:10] if len(raw_date) >= 10 else raw_date

    tier = classify_body(body_name)

    return {
        "id": event_id,
        "body_name": body_name,
        "date": event_date,
        "time": event_time or "",
        "location": location or "",
        "agenda_url": agenda_url or "",
        "meeting_url": meeting_url or "",
        "agenda_status": agenda_status or "",
        "tier": tier,
    }


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

TIER_MARKERS = {"high": "[!!!]", "medium": "[**]", "low": "[.]"}


def format_event_text(event):
    """Format a single event for human-readable output."""
    lines = []
    marker = TIER_MARKERS.get(event["tier"], "[.]")

    # Parse date for display
    try:
        dt = datetime.strptime(event["date"], "%Y-%m-%d")
        date_str = dt.strftime("%A, %B %-d, %Y")
    except (ValueError, TypeError):
        date_str = event["date"]

    # Timing relative to today
    today = datetime.now(timezone.utc).date()
    try:
        event_dt = datetime.strptime(event["date"], "%Y-%m-%d").date()
        if event_dt > today:
            delta = (event_dt - today).days
            timing = f"in {delta} day{'s' if delta != 1 else ''}"
        elif event_dt == today:
            timing = "TODAY"
        else:
            delta = (today - event_dt).days
            timing = f"{delta} day{'s' if delta != 1 else ''} ago"
    except (ValueError, TypeError):
        timing = ""

    lines.append(f"  {marker} {event['body_name']} -- {date_str} ({timing})")
    if event["time"]:
        lines.append(f"      Time: {event['time']}")
    if event["location"]:
        lines.append(f"      Location: {event['location']}")
    if event["agenda_url"]:
        lines.append(f"      Agenda: {event['agenda_url']}")
    if event["meeting_url"]:
        lines.append(f"      Meeting: {event['meeting_url']}")
    if event["agenda_status"]:
        lines.append(f"      Status: {event['agenda_status']}")

    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="BART Board of Directors meeting tracker (Legistar API)"
    )
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON for orchestrator integration")
    parser.add_argument("--next", action="store_true",
                        help="Show only the next upcoming meeting")
    parser.add_argument("--days", type=int, default=30,
                        help="Lookback/lookahead window in days (default: 30)")
    parser.add_argument("--all", action="store_true",
                        help="Include LOW-tier subcommittee meetings")
    args = parser.parse_args()

    # Fetch events
    raw_events = fetch_events(days=args.days)
    if not raw_events:
        print("No BART events found.", file=sys.stderr)
        if args.json:
            print(json.dumps({"meetings": [], "error": "No events found"}))
        else:
            print("No BART Board meetings found in the date range.")
        return

    # Parse and classify
    events = [parse_event(e) for e in raw_events]

    # Filter: unless --all, drop LOW tier
    if not args.all:
        events = [e for e in events if e["tier"] != "low"]

    # Sort by date ascending
    events.sort(key=lambda e: e["date"])

    print(f"Found {len(events)} relevant BART meetings.", file=sys.stderr)

    # --next: find next future meeting (prefer HIGH tier)
    if args.next:
        today_str = datetime.now(timezone.utc).date().isoformat()
        future = [e for e in events if e["date"] >= today_str]
        if future:
            # Prefer the next Board of Directors meeting
            high_future = [e for e in future if e["tier"] == "high"]
            events = [high_future[0]] if high_future else [future[0]]
        elif events:
            events = [events[-1]]  # fallback to most recent

    # Archive
    archive_records = []
    for e in events:
        archive_records.append({
            "id": e["id"],
            "source": "sf_bart_board",
            "body_name": e["body_name"],
            "date": e["date"],
            "time": e["time"],
            "location": e["location"],
            "agenda_url": e["agenda_url"],
            "meeting_url": e["meeting_url"],
            "agenda_status": e["agenda_status"],
            "tier": e["tier"],
        })
    update_archive(archive_records)

    # Output
    if args.json:
        output = []
        for e in events:
            output.append({
                "id": e["id"],
                "body_name": e["body_name"],
                "date": e["date"],
                "time": e["time"],
                "location": e["location"],
                "agenda_url": e["agenda_url"],
                "meeting_url": e["meeting_url"],
                "agenda_status": e["agenda_status"],
                "tier": e["tier"],
            })
        print(json.dumps(output, indent=2))
    else:
        print()
        print("=" * 60)
        print("  BART BOARD OF DIRECTORS")
        print("  Legistar: bart.legistar.com")
        print("=" * 60)
        print()

        # Group by tier
        high = [e for e in events if e["tier"] == "high"]
        medium = [e for e in events if e["tier"] == "medium"]
        low = [e for e in events if e["tier"] == "low"]

        if high:
            print(f"  -- BOARD OF DIRECTORS ({len(high)}) --")
            for e in high:
                lines = format_event_text(e)
                print("\n".join(lines))
            print()

        if medium:
            print(f"  -- ADVISORY BODIES ({len(medium)}) --")
            for e in medium:
                lines = format_event_text(e)
                print("\n".join(lines))
            print()

        if low:
            print(f"  -- SUBCOMMITTEES ({len(low)}) --")
            for e in low:
                lines = format_event_text(e)
                print("\n".join(lines))
            print()

        if not events:
            print("  No meetings found in the date range.")
            print()


if __name__ == "__main__":
    main()
