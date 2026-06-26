#!/usr/bin/env python3
"""
SF Rent Board Commission meeting scraper (API-based).

Tracks Rent Board Commission meetings, agendas, and key tenant/landlord info.
Uses the sf.gov Wagtail CMS API — no browser required.

Key facts:
  - Commission meets monthly on Tuesdays at 6pm
  - 25 Van Ness Avenue, Room 610, San Francisco, CA 94102
  - Allowable rent increase changes annually each March 1 — check sf.gov/departments/rent-board
  - Considers appeals of Rent Board ALJ decisions; enacts Rules and Regulations

Sources:
  - https://api.sf.gov/api/v2/pages/?type=sf.Meeting&search=rent+board+commission (Wagtail API)
  - https://www.sf.gov/2026-tentative-rent-board-commission-meeting-dates/

Usage:
  python3 sf_rent_board.py              # upcoming meetings + current rent increase
  python3 sf_rent_board.py --next       # next meeting only
  python3 sf_rent_board.py --json       # JSON output
  python3 sf_rent_board.py --details    # fetch full details for each meeting
"""

import sys
import os
import re
import json
import urllib.request
import urllib.error
from datetime import date, datetime, timezone

WAGTAIL_API = "https://api.sf.gov/api/v2/pages/"
MEETINGS_SEARCH = (
    "https://api.sf.gov/api/v2/pages/"
    "?type=sf.Meeting&search=rent+board+commission&limit=20&order=-id&locale=en&fields=*"
)
COMMISSION_URL = "https://www.sf.gov/departments--rent-board-commission"
EVENTS_URL = "https://www.sf.gov/departments--rent-board-commission/events/upcoming"
MEETING_DATES_URL = "https://www.sf.gov/2026-tentative-rent-board-commission-meeting-dates/"
SFGOV_BASE = "https://www.sf.gov"

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sf_rent_board_archive.json")
ARCHIVE_MAX = 5000

RENT_INCREASE_URL = "https://www.sf.gov/departments/rent-board"

# 2026 full meeting schedule (from the tentative schedule page)
MEETING_DATES_2026 = [
    "January 13, 2026",
    "February 10, 2026",
    "March 10, 2026",
    "April 14, 2026",
    "May 12, 2026",
    "June 9, 2026",
    "July 14, 2026",
    "August 11, 2026",
    "September 8, 2026",
    "October 13, 2026",
    "November 10, 2026",
    "December 8, 2026",
]

MEETING_LOCATION = "25 Van Ness Avenue, Room 610, San Francisco, CA 94102"
MEETING_TIME = "6:00 pm"
MEETING_DAY = "Tuesday"


# -----------------------------------------------------------------
# Archive helpers
# -----------------------------------------------------------------

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

def update_archive(meetings):
    archive = load_archive()
    existing_ids = {r["id"] for r in archive["items"]}
    now = datetime.now(tz=timezone.utc).isoformat()
    added = 0
    for meeting in meetings:
        record = {
            "id": meeting.get("date", meeting.get("title", "")),
            "source": "sf_rent_board",
            "scraped_at": now,
            "title": meeting.get("title", ""),
            "date": meeting.get("date", ""),
            "time": meeting.get("time", ""),
            "location": meeting.get("location", ""),
            "url": meeting.get("url", ""),
            "agenda_pdf": meeting.get("agenda_pdf", ""),
            "items": meeting.get("items", []),
        }
        if record["id"] not in existing_ids:
            archive["items"].append(record)
            existing_ids.add(record["id"])
            added += 1
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new records ({len(archive['items'])} total)", file=sys.stderr)
    return archive


# -----------------------------------------------------------------
# API helpers
# -----------------------------------------------------------------

def api_get(url, timeout=20):
    """Fetch JSON from the sf.gov Wagtail API. Returns parsed dict or None."""
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError) as e:
        print(f"  API error for {url}: {e}", file=sys.stderr)
        return None


def api_get_page(page_id, timeout=20):
    """Fetch a single page by ID from the Wagtail API."""
    url = f"{WAGTAIL_API}{page_id}/"
    return api_get(url, timeout=timeout)


# -----------------------------------------------------------------
# Parsing helpers — extract structured data from API responses
# -----------------------------------------------------------------

def extract_meeting_date(page):
    """Extract (date_obj, start_time_str) from a meeting page's date_time field."""
    date_time = page.get("date_time") or []
    for block in date_time:
        if block.get("type") == "date_time":
            val = block.get("value", {})
            start_date = val.get("start_date", "")
            start_time = val.get("start_time", "")
            if start_date:
                try:
                    d = date.fromisoformat(start_date)
                    return d, start_time or ""
                except ValueError:
                    pass
    return None, ""


def extract_location(page):
    """Extract address string from meeting_location field."""
    locations = page.get("meeting_location") or []
    for block in locations:
        if block.get("type") == "address":
            val = block.get("value", {})
            parts = [val.get("line1", ""), val.get("line2", "")]
            city = val.get("city", "")
            state = val.get("state", "")
            zipcode = val.get("zip", "")
            addr = ", ".join(p for p in parts if p)
            if city:
                addr += f", {city}"
            if state:
                addr += f", {state}"
            if zipcode:
                addr += f" {zipcode}"
            if addr.strip(", "):
                return addr.strip(", ")
    return MEETING_LOCATION


def extract_agenda_pdf(page):
    """Extract first agenda PDF URL from agenda or related_documents fields."""
    # Try agenda field first
    agenda_blocks = page.get("agenda") or []
    for block in agenda_blocks:
        val = block.get("value", {})
        docs = val.get("documents") or val.get("title_and_text", {}).get("documents") or []
        if not isinstance(docs, list):
            # Sometimes documents is nested inside title_and_text
            docs = []
        for doc in docs:
            doc_val = doc.get("value", {}) if isinstance(doc, dict) else {}
            file_url = doc_val.get("file", "")
            if file_url:
                return file_url

    # Try related_documents
    related = page.get("related_documents") or []
    for block in related:
        val = block.get("value", {})
        docs = val.get("documents") or []
        for doc in docs:
            doc_val = doc.get("value", {}) if isinstance(doc, dict) else {}
            title = doc_val.get("title", "").lower()
            file_url = doc_val.get("file", "")
            if file_url and "agenda" in title:
                return file_url

    # Return first related_documents file as fallback
    for block in related:
        val = block.get("value", {})
        docs = val.get("documents") or []
        for doc in docs:
            doc_val = doc.get("value", {}) if isinstance(doc, dict) else {}
            file_url = doc_val.get("file", "")
            if file_url:
                return file_url

    return ""


def extract_agenda_items(page):
    """Extract agenda item titles from agenda field."""
    items = []
    agenda_blocks = page.get("agenda") or []
    for block in agenda_blocks:
        val = block.get("value", {})
        tt = val.get("title_and_text", {})
        title = tt.get("title", "")
        if title:
            items.append({"text": title, "type": "agenda_item"})
        # Also pick up document links
        docs = val.get("documents") or []
        for doc in docs:
            doc_val = doc.get("value", {}) if isinstance(doc, dict) else {}
            doc_title = doc_val.get("title", "")
            file_url = doc_val.get("file", "")
            if doc_title and file_url:
                items.append({"text": doc_title, "href": file_url, "type": "attachment"})
    return items


def extract_all_attachments(page):
    """Extract all document attachments from agenda + related_documents."""
    attachments = []
    seen = set()

    for block in (page.get("agenda") or []):
        val = block.get("value", {})
        for doc in (val.get("documents") or []):
            doc_val = doc.get("value", {}) if isinstance(doc, dict) else {}
            file_url = doc_val.get("file", "")
            title = doc_val.get("title", "")
            if file_url and file_url not in seen:
                seen.add(file_url)
                attachments.append({"text": title, "href": file_url, "type": "attachment"})

    for block in (page.get("related_documents") or []):
        val = block.get("value", {})
        for doc in (val.get("documents") or []):
            doc_val = doc.get("value", {}) if isinstance(doc, dict) else {}
            file_url = doc_val.get("file", "")
            title = doc_val.get("title", "")
            if file_url and file_url not in seen:
                seen.add(file_url)
                attachments.append({"text": title, "href": file_url, "type": "attachment"})

    return attachments


def format_time_12h(time_str):
    """Convert 'HH:MM:SS' or 'HH:MM' to '6:00 pm' style."""
    if not time_str:
        return MEETING_TIME
    try:
        parts = time_str.split(":")
        h = int(parts[0])
        m = int(parts[1]) if len(parts) > 1 else 0
        suffix = "am" if h < 12 else "pm"
        if h > 12:
            h -= 12
        elif h == 0:
            h = 12
        return f"{h}:{m:02d} {suffix}"
    except (ValueError, IndexError):
        return MEETING_TIME


# -----------------------------------------------------------------
# Data fetchers
# -----------------------------------------------------------------

def fetch_upcoming_meetings():
    """
    Fetch upcoming Rent Board Commission meetings from the sf.gov Wagtail API.
    Returns list of dicts: {title, date_str, date, time, location, url, agenda_pdf, items}.
    """
    print("Fetching upcoming meetings from sf.gov API...", file=sys.stderr)
    data = api_get(MEETINGS_SEARCH)

    today = date.today()
    meetings = []

    if data and "items" in data:
        print(f"  API returned {len(data['items'])} meeting pages", file=sys.stderr)
        for page in data["items"]:
            title = page.get("title", "")
            cancelled = page.get("cancelled", False)

            meeting_date, start_time = extract_meeting_date(page)

            # Skip past meetings
            if meeting_date and meeting_date < today:
                continue

            # Extract location (use API data, fallback to constant)
            location = extract_location(page)
            time_str = format_time_12h(start_time)

            # Extract page URL (API returns http://api.sf.gov/..., fix to https://www.sf.gov/...)
            meta = page.get("meta", {})
            url = meta.get("html_url", "")
            url = re.sub(r'^https?://api\.sf\.gov/', 'https://www.sf.gov/', url)

            # Extract agenda PDF
            agenda_pdf = extract_agenda_pdf(page)

            # Extract agenda items / attachments
            items = extract_all_attachments(page)

            meeting = {
                "title": title,
                "date_str": meeting_date.strftime("%-d %B %Y") if meeting_date else title,
                "date": meeting_date.isoformat() if meeting_date else "",
                "time": time_str,
                "location": location,
                "url": url,
                "agenda_pdf": agenda_pdf,
                "items": items,
                "cancelled": cancelled,
            }
            meetings.append(meeting)
    else:
        print("  API returned no results", file=sys.stderr)

    # If we got nothing from the API, fall back to hardcoded 2026 schedule
    if not meetings:
        print("  No meetings from API, using 2026 schedule fallback", file=sys.stderr)
        meetings = build_from_schedule_2026(today)

    meetings.sort(key=lambda m: m.get("date", ""))
    return meetings


def fetch_meeting_details(meeting):
    """
    Fetch full details for a single meeting by loading its page from the API.
    Updates the meeting dict in-place with agenda PDF and items.

    The page ID can be extracted from the URL or we search by title.
    """
    url = meeting.get("url", "")
    if not url:
        return

    # Try to find this meeting's page by searching for it
    title = meeting.get("title", "")
    if not title:
        return

    print(f"  Fetching meeting details: {title}", file=sys.stderr)

    # Search for this specific meeting
    search_term = urllib.request.quote(title[:60])
    search_url = (
        f"{WAGTAIL_API}?type=sf.Meeting&search={search_term}&limit=5&locale=en&fields=*"
    )
    data = api_get(search_url)

    if not data or "items" not in data:
        return

    # Find the matching page
    for page in data["items"]:
        page_url = page.get("meta", {}).get("html_url", "")
        if page_url == url or page.get("title", "") == title:
            meeting["agenda_pdf"] = extract_agenda_pdf(page) or meeting.get("agenda_pdf", "")
            meeting["items"] = extract_all_attachments(page) or meeting.get("items", [])
            return


# -----------------------------------------------------------------
# Utility helpers
# -----------------------------------------------------------------

def parse_date_from_url(url):
    """
    Parse date from sf.gov meeting URL patterns:
      meeting--april-14-2026--...
      meeting-20260414-...
    """
    # Pattern: meeting--<month-name>-<day>-<year>
    m = re.search(
        r'meeting--'
        r'(january|february|march|april|may|june|july|august|september|october|november|december)'
        r'-(\d{1,2})-(\d{4})',
        url, re.IGNORECASE
    )
    if m:
        try:
            return datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%B %d %Y").date()
        except ValueError:
            pass

    # Pattern: meeting-YYYYMMDD-...
    m = re.search(r'meeting-(\d{8})-', url)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y%m%d").date()
        except ValueError:
            pass

    return None


def parse_date_from_text(text):
    """Parse a date from text like 'April 14, 2026 Rent Board Commission Meeting'."""
    m = re.search(
        r'(January|February|March|April|May|June|July|August|September|October|November|December)'
        r'\s+(\d{1,2}),\s+(\d{4})',
        text
    )
    if m:
        try:
            return datetime.strptime(m.group(0), "%B %d, %Y").date()
        except ValueError:
            pass
    return None


def build_from_schedule_2026(today=None):
    """Build meeting list from the hardcoded 2026 schedule."""
    today = today or date.today()
    meetings = []
    for date_str in MEETING_DATES_2026:
        try:
            d = datetime.strptime(date_str, "%B %d, %Y").date()
        except ValueError:
            continue
        if d < today:
            continue
        url = date_to_sfgov_url(d, date_str)
        meetings.append({
            "title": f"{date_str} Rent Board Commission Meeting",
            "date_str": d.strftime("%-d %B %Y"),
            "date": d.isoformat(),
            "time": MEETING_TIME,
            "location": MEETING_LOCATION,
            "url": url,
            "agenda_pdf": "",
            "items": [],
        })
    return meetings


def date_to_sfgov_url(d, date_str):
    """
    Generate the sf.gov meeting URL from a date.
    Pattern: https://www.sf.gov/meeting--{month}-{day}-{year}--{month}-{day}-{year}-rent-board-commission-meeting/
    """
    month = d.strftime("%B").lower()
    day = str(d.day)
    year = str(d.year)
    slug = f"{month}-{day}-{year}"
    return f"{SFGOV_BASE}/meeting--{slug}--{slug}-rent-board-commission-meeting/"


# -----------------------------------------------------------------
# Output formatters
# -----------------------------------------------------------------

def format_meetings(meetings, next_only=False):
    """Format meetings as human-readable text."""
    lines = []
    lines.append("")
    lines.append("🏠  SF RENT BOARD COMMISSION")
    lines.append("=" * 55)

    lines.append(f"\n💰 Current allowable rent increase: check {RENT_INCREASE_URL}")
    lines.append(f"   (Updated annually each March 1, based on 60% of Bay Area CPI)")
    lines.append("")

    if not meetings:
        lines.append("No upcoming meetings found.")
        return "\n".join(lines)

    display = meetings[:1] if next_only else meetings

    lines.append("📅 UPCOMING MEETINGS")
    lines.append("─" * 55)

    for m in display:
        cancelled = m.get("cancelled", False)
        d = m.get("date", "")
        if d:
            try:
                dt = date.fromisoformat(d)
                day_name = dt.strftime("%A")
                formatted_date = dt.strftime("%B %-d, %Y")
                label = f"\n  📌 {day_name}, {formatted_date}  {m.get('time', MEETING_TIME)}"
                if cancelled:
                    label += "  [CANCELLED]"
                lines.append(label)
            except ValueError:
                lines.append(f"\n  📌 {m.get('date_str', d)}  {m.get('time', MEETING_TIME)}")
        else:
            lines.append(f"\n  📌 {m.get('title', 'Meeting')}  {m.get('time', MEETING_TIME)}")

        lines.append(f"     📍 {m.get('location', MEETING_LOCATION)}")

        url = m.get("url", "")
        if url:
            lines.append(f"     🌐 {url}")

        agenda = m.get("agenda_pdf", "")
        if agenda:
            lines.append(f"     📄 Agenda: {agenda}")
        else:
            lines.append(f"     📄 Agenda: (not yet posted)")

        items = m.get("items", [])
        if items:
            lines.append(f"     📎 Attachments:")
            for item in items[:5]:
                lines.append(f"        • {item.get('text', '')} — {item.get('href', '')}")

    return "\n".join(lines)


def format_json(meetings, news=None):
    """Format output as JSON."""
    out = {
        "body": "Rent Board Commission",
        "rent_increase_source": RENT_INCREASE_URL,
        "meetings": meetings,
        "news": news or [],
        "sources": {
            "commission_page": COMMISSION_URL,
            "events": EVENTS_URL,
            "meeting_dates_2026": MEETING_DATES_URL,
        }
    }
    return json.dumps(out, indent=2)


# -----------------------------------------------------------------
# Main
# -----------------------------------------------------------------

def main():
    args = sys.argv[1:]
    next_only = "--next" in args
    as_json = "--json" in args
    fetch_details_flag = "--details" in args

    today = date.today()

    # Fetch upcoming meetings from the Wagtail API
    meetings = fetch_upcoming_meetings()

    if not meetings:
        print("No upcoming meetings found from API.", file=sys.stderr)
        # Fall back to hardcoded schedule
        meetings = build_from_schedule_2026(today)
        print(f"Using hardcoded 2026 schedule: {len(meetings)} upcoming meetings", file=sys.stderr)

    # Archive meetings
    update_archive(meetings)

    # If --details requested, re-fetch individual meeting pages for fuller data
    if fetch_details_flag:
        limit = 1 if next_only else 3
        for m in meetings[:limit]:
            if m.get("url") and not m.get("agenda_pdf"):
                fetch_meeting_details(m)

    # Output
    if as_json:
        # For JSON, fetch details for meetings missing agenda info
        for m in meetings[:5]:
            if m.get("url") and not m.get("agenda_pdf"):
                fetch_meeting_details(m)
        print(format_json(meetings))
    else:
        print(format_meetings(meetings, next_only=next_only))

        if not next_only:
            print(f"\n📋 2026 Full Schedule (all months):")
            print(f"   {', '.join(d.split(',')[0].replace(' 2026', '') for d in MEETING_DATES_2026)}")
            print(f"\n   Source: {COMMISSION_URL}")


if __name__ == "__main__":
    main()
