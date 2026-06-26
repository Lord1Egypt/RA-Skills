#!/usr/bin/env python3
"""
sf_sfusd_board.py — SFUSD Board of Education meeting schedule tracker.

Fetches the SFUSD Board of Education meeting schedule from a public Google
Sheets CSV export (full calendar with dates, types, notes). Falls back to
scraping BoardDocs if the spreadsheet is unavailable.

Data sources:
  1. Google Sheets CSV: https://docs.google.com/spreadsheets/d/1ishu0t6lxzrczTkaK2MRE3d9jmj5xKBUO0C6_50gFvc/export?format=csv
  2. BoardDocs portal: https://go.boarddocs.com/ca/sfusd/Board.nsf/vpublic?open
  3. Granicus video: https://sanfrancisco.granicus.com/ViewPublisher.php?view_id=47

Schedule: 2nd and 4th Tuesdays at 5 PM, City Hall or SFUSD HQ (555 Franklin St).

Usage:
    python sf_sfusd_board.py              # upcoming meetings (next 30 days)
    python sf_sfusd_board.py --days 60    # upcoming meetings within 60 days
    python sf_sfusd_board.py --next       # next single meeting only
    python sf_sfusd_board.py --json       # JSON output for orchestrator
    python sf_sfusd_board.py --all        # include past meetings in window
"""

import argparse
import csv
import io
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone, date

try:
    import urllib.request
    import urllib.parse
    import urllib.error
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

GSHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1ishu0t6lxzrczTkaK2MRE3d9jmj5xKBUO0C6_50gFvc/export?format=csv"
)
BOARDDOCS_URL = "https://go.boarddocs.com/ca/sfusd/Board.nsf/vpublic?open"
GRANICUS_URL = "https://sanfrancisco.granicus.com/ViewPublisher.php?view_id=47"

DEFAULT_LOCATION = "555 Franklin St, San Francisco (SFUSD HQ)"
DEFAULT_TIME = "5:00 PM"
SCHEDULE_NOTE = "2nd & 4th Tuesdays, 5 PM"

ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), "sf_sfusd_board_archive.json")
ARCHIVE_MAX = 5000

# Meeting type -> relevance tier
TYPE_TIERS = {
    "regular": "high",
    "special": "high",
    "committee": "medium",
    "workshop": "medium",
    "retreat": "low",
    "cancelled": "low",
}


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
    """Merge new records into archive. Dedup by date+type. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_keys = {f"{r['date']}|{r['meeting_type']}" for r in archive["items"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for record in new_records:
        key = f"{record['date']}|{record['meeting_type']}"
        if key not in existing_keys:
            record["scraped_at"] = now
            archive["items"].append(record)
            existing_keys.add(key)
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

def fetch_url(url, timeout=30, accept="text/html"):
    """Fetch a URL and return the content as a string."""
    headers = {
        "Accept": accept,
        "User-Agent": "sf-civic-digest/1.0 (civic monitoring bot)",
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} fetching {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Google Sheets CSV parsing (primary source)
# ---------------------------------------------------------------------------

def _parse_date_flexible(text):
    """Try multiple date formats to parse a date string."""
    text = text.strip()
    if not text:
        return None
    # Try common formats
    for fmt in (
        "%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d",
        "%B %d, %Y", "%b %d, %Y",
        "%m-%d-%Y", "%m-%d-%y",
    ):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def _classify_meeting_type(raw_type):
    """Normalize meeting type string to a canonical form."""
    t = raw_type.strip().lower()
    if "regular" in t or "board meeting" in t:
        return "regular"
    if "special" in t:
        return "special"
    if "committee" in t:
        return "committee"
    if "workshop" in t:
        return "workshop"
    if "retreat" in t:
        return "retreat"
    if "cancel" in t:
        return "cancelled"
    # Default: if it looks like a committee name, mark as committee
    if any(w in t for w in ("curriculum", "budget", "ad hoc", "rules", "audit")):
        return "committee"
    return "regular"


def fetch_from_gsheet():
    """Fetch and parse the SFUSD Board schedule from Google Sheets CSV export."""
    print("Fetching SFUSD Board schedule from Google Sheets...", file=sys.stderr)
    csv_text = fetch_url(GSHEET_CSV_URL, accept="text/csv")
    if not csv_text:
        return None

    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)

    if len(rows) < 2:
        print("Google Sheet has fewer than 2 rows — may be empty.", file=sys.stderr)
        return None

    # Find header row — look for a row containing "date" (case-insensitive)
    header_idx = None
    headers = []
    for i, row in enumerate(rows):
        lower_row = [c.strip().lower() for c in row]
        if "date" in lower_row:
            header_idx = i
            headers = lower_row
            break

    if header_idx is None:
        # Assume first row is header
        header_idx = 0
        headers = [c.strip().lower() for c in rows[0]]

    # Map column indices
    def find_col(*candidates):
        for c in candidates:
            for i, h in enumerate(headers):
                if c in h:
                    return i
        return None

    date_col = find_col("date")
    type_col = find_col("type", "meeting type", "kind")
    time_col = find_col("time")
    location_col = find_col("location", "place", "venue")
    notes_col = find_col("note", "description", "topic", "agenda")

    if date_col is None:
        print("Could not find 'date' column in Google Sheet.", file=sys.stderr)
        return None

    meetings = []
    for row in rows[header_idx + 1:]:
        if not row or all(c.strip() == "" for c in row):
            continue

        def cell(idx):
            if idx is not None and idx < len(row):
                return row[idx].strip()
            return ""

        raw_date = cell(date_col)
        meeting_date = _parse_date_flexible(raw_date)
        if not meeting_date:
            continue

        raw_type = cell(type_col) if type_col is not None else ""
        meeting_type = _classify_meeting_type(raw_type) if raw_type else "regular"

        meeting_time = cell(time_col) if time_col is not None else DEFAULT_TIME
        if not meeting_time:
            meeting_time = DEFAULT_TIME

        location = cell(location_col) if location_col is not None else DEFAULT_LOCATION
        if not location:
            location = DEFAULT_LOCATION

        notes = cell(notes_col) if notes_col is not None else ""

        meetings.append({
            "date": meeting_date.isoformat(),
            "date_obj": meeting_date,
            "meeting_type": meeting_type,
            "meeting_type_raw": raw_type or "Regular Board Meeting",
            "time": meeting_time,
            "location": location,
            "notes": notes,
            "source": "gsheet",
        })

    if meetings:
        print(f"  Parsed {len(meetings)} meetings from Google Sheet.", file=sys.stderr)
    return meetings if meetings else None


# ---------------------------------------------------------------------------
# BoardDocs fallback
# ---------------------------------------------------------------------------

def fetch_from_boarddocs():
    """Fallback: scrape BoardDocs portal for meeting listings."""
    print("Falling back to BoardDocs...", file=sys.stderr)
    html = fetch_url(BOARDDOCS_URL)
    if not html:
        return None

    meetings = []

    # Try to find __NEXT_DATA__ or embedded JSON
    next_data_match = re.search(
        r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL
    )
    if next_data_match:
        try:
            data = json.loads(next_data_match.group(1))
            # Navigate the JSON for meeting data (structure varies)
            props = data.get("props", {}).get("pageProps", {})
            meeting_list = props.get("meetings", props.get("data", []))
            if isinstance(meeting_list, list):
                for m in meeting_list:
                    raw_date = m.get("date", m.get("numberdate", ""))
                    meeting_date = _parse_date_flexible(str(raw_date))
                    if not meeting_date:
                        continue
                    raw_type = m.get("typename", m.get("name", "Regular Board Meeting"))
                    meetings.append({
                        "date": meeting_date.isoformat(),
                        "date_obj": meeting_date,
                        "meeting_type": _classify_meeting_type(raw_type),
                        "meeting_type_raw": raw_type,
                        "time": DEFAULT_TIME,
                        "location": DEFAULT_LOCATION,
                        "notes": "",
                        "source": "boarddocs",
                    })
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

    # Try regex extraction of meeting entries from HTML
    if not meetings:
        # BoardDocs often has entries like: <div class="meeting-name">Regular Meeting - March 25, 2026</div>
        pattern = r'(?:meeting[^>]*>|<td[^>]*>)\s*([^<]*(?:Meeting|Session|Committee|Workshop|Special)[^<]*(?:\d{1,2}[,/]\s*\d{4}|\d{4}))'
        raw_matches = re.findall(pattern, html, re.IGNORECASE)
        for raw in raw_matches:
            # Try to extract date from the text
            date_match = re.search(
                r'(\w+\s+\d{1,2},?\s+\d{4}|\d{1,2}/\d{1,2}/\d{2,4})', raw
            )
            if not date_match:
                continue
            meeting_date = _parse_date_flexible(date_match.group(1))
            if not meeting_date:
                continue
            meetings.append({
                "date": meeting_date.isoformat(),
                "date_obj": meeting_date,
                "meeting_type": _classify_meeting_type(raw),
                "meeting_type_raw": raw.strip(),
                "time": DEFAULT_TIME,
                "location": DEFAULT_LOCATION,
                "notes": "",
                "source": "boarddocs",
            })

    # If nothing found, generate expected dates (2nd/4th Tuesdays)
    if not meetings:
        print("  BoardDocs parsing yielded no results; generating expected schedule.", file=sys.stderr)
        meetings = _generate_expected_schedule(months_ahead=3)

    if meetings:
        print(f"  Found {len(meetings)} meetings from BoardDocs/fallback.", file=sys.stderr)
    return meetings if meetings else None


def _generate_expected_schedule(months_ahead=3):
    """Generate expected meeting dates based on 2nd/4th Tuesday pattern."""
    today = date.today()
    meetings = []

    for month_offset in range(-1, months_ahead + 1):
        m = today.month + month_offset
        y = today.year
        while m < 1:
            m += 12
            y -= 1
        while m > 12:
            m -= 12
            y += 1

        # Find 2nd and 4th Tuesdays
        first_day = date(y, m, 1)
        days_to_tuesday = (1 - first_day.weekday()) % 7
        first_tuesday = first_day + timedelta(days=days_to_tuesday)
        second_tuesday = first_tuesday + timedelta(weeks=1)
        fourth_tuesday = first_tuesday + timedelta(weeks=3)

        for d in [second_tuesday, fourth_tuesday]:
            if d.month != m:
                continue  # Went into next month
            meetings.append({
                "date": d.isoformat(),
                "date_obj": d,
                "meeting_type": "regular",
                "meeting_type_raw": "Regular Board Meeting (projected)",
                "time": DEFAULT_TIME,
                "location": DEFAULT_LOCATION,
                "notes": "Projected from standard schedule",
                "source": "projected",
            })

    return meetings


# ---------------------------------------------------------------------------
# URL builders
# ---------------------------------------------------------------------------

def boarddocs_url_for_date(meeting_date):
    """Build a BoardDocs link. Generic since we can't predict meeting IDs."""
    return BOARDDOCS_URL


def granicus_url():
    """Granicus video archive page for SFUSD."""
    return GRANICUS_URL


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_meeting(meeting):
    """Assign a relevance tier based on meeting type."""
    mt = meeting.get("meeting_type", "regular")
    return TYPE_TIERS.get(mt, "medium")


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

TYPE_LABELS = {
    "regular": "Regular Board Meeting",
    "special": "Special Meeting",
    "committee": "Committee Meeting",
    "workshop": "Workshop",
    "retreat": "Board Retreat",
    "cancelled": "CANCELLED",
}

TIER_MARKERS = {"high": "[!!!]", "medium": "[**]", "low": "[.]"}


def format_meeting_text(meeting):
    """Format a single meeting for human-readable output."""
    lines = []
    meeting_date = meeting.get("date", "?")
    meeting_type = meeting.get("meeting_type", "regular")
    tier = meeting.get("tier", "medium")

    # Parse date for display
    try:
        dt = datetime.strptime(meeting_date, "%Y-%m-%d")
        date_str = dt.strftime("%A, %B %-d, %Y")
    except (ValueError, TypeError):
        date_str = meeting_date

    # Timing relative to today
    today = date.today()
    try:
        meeting_dt = datetime.strptime(meeting_date, "%Y-%m-%d").date()
        if meeting_dt > today:
            days_until = (meeting_dt - today).days
            timing = f"in {days_until} day{'s' if days_until != 1 else ''}"
        elif meeting_dt == today:
            timing = "TODAY"
        else:
            days_ago = (today - meeting_dt).days
            timing = f"{days_ago} day{'s' if days_ago != 1 else ''} ago"
    except (ValueError, TypeError):
        timing = ""

    label = TYPE_LABELS.get(meeting_type, meeting.get("meeting_type_raw", "Meeting"))
    marker = TIER_MARKERS.get(tier, "")

    lines.append(f"  {marker} {label} -- {date_str} ({timing})")
    lines.append(f"      {meeting.get('time', DEFAULT_TIME)} | {meeting.get('location', DEFAULT_LOCATION)}")
    lines.append(f"      BoardDocs: {boarddocs_url_for_date(meeting_date)}")
    lines.append(f"      Video: {granicus_url()}")

    notes = meeting.get("notes", "")
    if notes:
        lines.append(f"      Notes: {notes}")

    if meeting.get("source") == "projected":
        lines.append("      (projected from standard schedule -- check BoardDocs for confirmation)")

    lines.append("")
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="SFUSD Board of Education meeting schedule tracker"
    )
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON for orchestrator integration")
    parser.add_argument("--next", action="store_true",
                        help="Show only the next upcoming meeting")
    parser.add_argument("--days", type=int, default=30,
                        help="Show meetings within N days (default 30)")
    parser.add_argument("--all", action="store_true",
                        help="Include past meetings in the date window too")
    args = parser.parse_args()

    # Fetch meetings: try Google Sheet first, then BoardDocs
    meetings = fetch_from_gsheet()
    if meetings is None:
        meetings = fetch_from_boarddocs()
    if meetings is None:
        # Last resort: projected schedule
        print("All sources failed. Using projected schedule.", file=sys.stderr)
        meetings = _generate_expected_schedule(months_ahead=3)

    if not meetings:
        if args.json:
            print(json.dumps({"meetings": [], "error": "No meetings found"}))
        else:
            print("No SFUSD Board meetings found.")
        return

    # Filter by date window
    today = date.today()
    window_start = today if not args.all else today - timedelta(days=args.days)
    window_end = today + timedelta(days=args.days)

    filtered = []
    for m in meetings:
        try:
            md = datetime.strptime(m["date"], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            continue
        if window_start <= md <= window_end:
            filtered.append(m)

    # Sort by date
    filtered.sort(key=lambda m: m["date"])

    # --next: pick only the next upcoming meeting
    if args.next:
        upcoming = [m for m in filtered if m["date"] >= today.isoformat()]
        if upcoming:
            filtered = [upcoming[0]]
        elif filtered:
            filtered = [filtered[-1]]  # fallback to most recent

    # Classify and add tier
    for m in filtered:
        m["tier"] = classify_meeting(m)

    # Archive
    archive_records = []
    for m in filtered:
        archive_records.append({
            "date": m["date"],
            "meeting_type": m.get("meeting_type", "regular"),
            "meeting_type_raw": m.get("meeting_type_raw", ""),
            "time": m.get("time", DEFAULT_TIME),
            "location": m.get("location", DEFAULT_LOCATION),
            "notes": m.get("notes", ""),
            "tier": m.get("tier", "medium"),
            "source": m.get("source", "unknown"),
            "boarddocs_url": boarddocs_url_for_date(m["date"]),
            "granicus_url": granicus_url(),
        })
    if archive_records:
        update_archive(archive_records)

    # Output
    if args.json:
        output = []
        for m in filtered:
            rec = {
                "date": m["date"],
                "meeting_type": m.get("meeting_type", "regular"),
                "meeting_type_raw": m.get("meeting_type_raw", ""),
                "time": m.get("time", DEFAULT_TIME),
                "location": m.get("location", DEFAULT_LOCATION),
                "notes": m.get("notes", ""),
                "tier": m.get("tier", "medium"),
                "source": m.get("source", "unknown"),
                "boarddocs_url": boarddocs_url_for_date(m["date"]),
                "granicus_url": granicus_url(),
            }
            # Remove internal fields
            output.append(rec)
        print(json.dumps(output, indent=2))
    else:
        if not filtered:
            print(f"No SFUSD Board meetings in the next {args.days} days.")
            return

        print()
        print("=" * 64)
        print("  SFUSD BOARD OF EDUCATION")
        print(f"  Meets {SCHEDULE_NOTE}")
        print(f"  BoardDocs: {BOARDDOCS_URL}")
        print(f"  Video archives: {GRANICUS_URL}")
        print("=" * 64)
        print()

        high = [m for m in filtered if m.get("tier") == "high"]
        medium = [m for m in filtered if m.get("tier") == "medium"]
        low = [m for m in filtered if m.get("tier") == "low"]

        if high:
            print(f"  -- FULL BOARD ({len(high)}) --")
            for m in high:
                lines = format_meeting_text(m)
                print("\n".join(lines))

        if medium:
            print(f"  -- COMMITTEES / WORKSHOPS ({len(medium)}) --")
            for m in medium:
                lines = format_meeting_text(m)
                print("\n".join(lines))

        if low:
            print(f"  ({len(low)} low-priority meetings: retreats, cancelled)")
            for m in low:
                lines = format_meeting_text(m)
                print("\n".join(lines))

    # Clean up internal fields from returned data
    for m in filtered:
        m.pop("date_obj", None)

    return filtered


if __name__ == "__main__":
    main()
