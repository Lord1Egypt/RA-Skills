#!/usr/bin/env python3
"""
SF.gov meetings scraper — pulls upcoming commission/board meetings from api.sf.gov.
Uses the sf.Meeting Wagtail page type (26k+ records, full agenda data).

Usage:
  python3 sfgov_events.py                  # upcoming civic meetings (14 days)
  python3 sfgov_events.py --days 30        # look ahead N days
  python3 sfgov_events.py --district 5     # meetings relevant to district 5
  python3 sfgov_events.py --all            # all meetings, no relevance filter
  python3 sfgov_events.py --json           # JSON output for digest integration

API: https://api.sf.gov/api/v2/pages/?type=sf.Meeting
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import date, datetime, timedelta, timezone

API_BASE = "https://api.sf.gov/api/v2/pages"
UA = "sf-civic-digest/1.0"

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sfgov_events_archive.json")
ARCHIVE_MAX = 5000

# ---------------------------------------------------------------------------
# Relevance filter
# ---------------------------------------------------------------------------

# Agencies to INCLUDE (high civic value, not already covered by other scrapers)
INCLUDE_AGENCIES = [
    "police commission",
    "small business commission",
    "entertainment commission",
    "human rights commission",
    "commission on the status of women",
    "ethics commission",
    "public utilities commission",
    "port commission",
    "building inspection commission",
    "health commission",
    "fire commission",
    "library commission",
    "arts commission",
    "historic preservation commission",
    "youth commission",
    "elections commission",
    "immigrant rights commission",
    "commission on community investment and infrastructure",
    "treasure island development authority",
    "housing authority commission",
]

# Agencies to SKIP (already covered by dedicated scrapers or low civic value)
SKIP_AGENCIES = [
    "board of supervisors",       # covered by Legistar
    "planning commission",        # covered by sf_planning_commission.py
    "sfmta board",                # covered by sf_sfmta_board.py
    "mta board",                  # alias
    "recreation and park",        # covered by sf_rec_park.py
    "rec and park",               # alias
    "board of appeals",           # covered by sf_board_of_appeals.py
    "civil service commission",   # HR/personnel, rarely relevant
]

# District neighborhood keywords loaded dynamically from config_loader
def _get_district_keywords(district):
    """Return neighborhood keyword list for a given district."""
    try:
        from config_loader import get_district_config
        dc = get_district_config(district)
        neighborhoods = dc.get("neighborhoods", [])
        streets = dc.get("streets", [])
        base = [f"district {district}", f"district-{district}", f"d{district}"]
        return base + [n.lower() for n in neighborhoods] + [s.lower() for s in streets]
    except Exception:
        return [f"district {district}", f"district-{district}", f"d{district}"]


def agency_matches_list(agency_name, agency_list):
    a = agency_name.lower()
    return any(kw in a for kw in agency_list)


def is_relevant_agency(agency_name):
    a = agency_name.lower()
    if any(kw in a for kw in SKIP_AGENCIES):
        return False
    if any(kw in a for kw in INCLUDE_AGENCIES):
        return True
    # Include anything with "commission" or "board" or "authority" not in skip list
    if any(kw in a for kw in ("commission", "board", "authority", "committee")):
        return True
    return False


def matches_district(text, district):
    """Check if text mentions the given district number."""
    if district is None:
        return True
    patterns = _get_district_keywords(district)
    t = text.lower()
    return any(p in t for p in patterns)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_json(url, timeout=20):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


# ---------------------------------------------------------------------------
# Meeting parsing
# ---------------------------------------------------------------------------

def parse_meeting_detail(detail):
    """Parse a sf.Meeting detail response into our standard format."""
    meta = detail.get("meta", {})

    # Title and agency
    title = detail.get("title", "")
    agency_info = detail.get("primary_agency") or {}
    agency_name = agency_info.get("title", "")
    agency_url = (agency_info.get("meta") or {}).get("html_url", "")

    # Date/time
    dt_list = detail.get("date_time") or []
    start_date = ""
    start_time = ""
    end_time = ""
    is_all_day = False
    if dt_list:
        val = dt_list[0].get("value", {})
        start_date = val.get("start_date", "")
        start_time = val.get("start_time", "")
        end_time = val.get("end_time", "")
        is_all_day = val.get("is_all_day", False)

    # Cancelled
    cancelled = detail.get("cancelled", False)

    # Location
    location_blocks = detail.get("meeting_location") or []
    address = ""
    online_link = ""
    phone = ""
    for loc in location_blocks:
        loc_type = loc.get("type", "")
        val = loc.get("value", {})
        if loc_type == "address":
            parts = [val.get("location_name", ""), val.get("line1", ""),
                     val.get("city", "")]
            address = ", ".join(p for p in parts if p)
        elif loc_type == "online":
            link_val = val.get("link", "")
            if isinstance(link_val, dict):
                online_link = link_val.get("url", "")
            else:
                online_link = link_val or ""
            phone_val = val.get("phone", "")
            if isinstance(phone_val, list) and phone_val:
                pv = phone_val[0].get("value", {})
                num = pv.get("phone_number", "")
                details = pv.get("details", "")
                phone = f"{num} ({details})" if details else num
            elif isinstance(phone_val, dict):
                phone = phone_val.get("phone_number", "")
            elif isinstance(phone_val, str):
                phone = phone_val

    # Agenda items (titles only)
    agenda_items = []
    for item in (detail.get("agenda") or []):
        if item.get("type") == "agenda_item":
            val = item.get("value", {})
            tt = val.get("title_and_text") or {}
            atitle = tt.get("title", "")
            if atitle:
                agenda_items.append(atitle)

    # Public comment email (from notices)
    public_comment_email = ""
    for notice in (detail.get("notices") or []):
        val = notice.get("value", {})
        text = val.get("text", "")
        # Look for email addresses in notice text
        emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
        if emails:
            public_comment_email = emails[0]
            break

    # PDF links from related_documents
    pdf_links = []
    for doc_block in (detail.get("related_documents") or []):
        val = doc_block.get("value", {})
        for doc in (val.get("documents") or []):
            doc_val = doc.get("value", {})
            doc_title = doc_val.get("title", "")
            doc_file = doc_val.get("file", "")
            if doc_file:
                pdf_links.append({"title": doc_title, "url": doc_file})

    return {
        "slug": meta.get("slug", ""),
        "title": title,
        "agency": agency_name,
        "agency_url": agency_url,
        "date": start_date,
        "time": start_time[:5] if start_time else "",
        "end_time": end_time[:5] if end_time else "",
        "is_all_day": is_all_day,
        "cancelled": cancelled,
        "address": address,
        "online_link": online_link,
        "phone": phone,
        "agenda_items": agenda_items,
        "public_comment_email": public_comment_email,
        "pdf_links": pdf_links,
        "source_url": meta.get("html_url", ""),
    }


# ---------------------------------------------------------------------------
# Main fetcher
# ---------------------------------------------------------------------------

def get_upcoming_meetings(district=None, days=14, include_all=False):
    """Fetch upcoming sf.Meeting pages, filter by relevance, fetch details.

    Strategy: page through by -id (newest-added first), locale=en to skip
    translations.  Collect meetings whose start_date is in [today, today+days].
    Stop once we see enough consecutive pages with all dates before today.
    """
    today = date.today()
    cutoff = today + timedelta(days=days)
    today_str = today.isoformat()
    cutoff_str = cutoff.isoformat()

    meetings = []
    seen_slugs = set()
    offset = 0
    page_size = 50
    pages_fetched = 0
    max_pages = 30  # safety limit (~1500 records)
    consecutive_old_pages = 0  # stop after 3 pages with all-old dates

    while pages_fetched < max_pages:
        pages_fetched += 1
        url = (
            f"{API_BASE}/?type=sf.Meeting&limit={page_size}&offset={offset}"
            f"&order=-id&locale=en&fields=title,date_time,primary_agency"
        )
        print(f"  Fetching page {pages_fetched} (offset {offset})...",
              file=sys.stderr)
        try:
            data = fetch_json(url, timeout=30)
        except (urllib.error.HTTPError, urllib.error.URLError, Exception) as e:
            print(f"  Error fetching list: {e}", file=sys.stderr)
            break

        items = data.get("items", [])
        if not items:
            break

        found_in_window = False
        for item in items:
            dt_list = item.get("date_time") or []
            if not dt_list:
                continue
            start = dt_list[0].get("value", {}).get("start_date", "")
            if not start:
                continue

            # Skip future-beyond-window and past meetings
            if start < today_str or start > cutoff_str:
                continue

            found_in_window = True

            slug = (item.get("meta") or {}).get("slug", "")
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            # Filter to English (locale=en handles most, but double-check)
            locale = (item.get("meta") or {}).get("locale", "en")
            if locale != "en":
                continue

            agency = (item.get("primary_agency") or {}).get("title", "")

            # Relevance filter
            if not include_all and not is_relevant_agency(agency):
                continue

            detail_url = (item.get("meta") or {}).get("detail_url", "")
            if not detail_url:
                continue

            meetings.append({
                "title": item.get("title", ""),
                "agency": agency,
                "start_date": start,
                "detail_url": detail_url,
            })

        if found_in_window:
            consecutive_old_pages = 0
        else:
            consecutive_old_pages += 1
            if consecutive_old_pages >= 3:
                break

        offset += page_size

    print(f"  Found {len(meetings)} meetings in date range, fetching details...",
          file=sys.stderr)

    # Step 2: fetch detail for each meeting
    results = []
    for i, m in enumerate(meetings):
        try:
            detail = fetch_json(m["detail_url"], timeout=20)
        except Exception as e:
            print(f"  Error fetching detail for '{m['title']}': {e}", file=sys.stderr)
            continue

        parsed = parse_meeting_detail(detail)

        # District filter (check agency + agenda items)
        if district is not None:
            searchable = " ".join([parsed["agency"], parsed["title"]]
                                  + parsed["agenda_items"])
            if not matches_district(searchable, district):
                continue

        results.append(parsed)

        if (i + 1) % 10 == 0:
            print(f"  Fetched {i + 1}/{len(meetings)} details...", file=sys.stderr)

    results.sort(key=lambda x: (x["date"], x["time"]))
    return results


# ---------------------------------------------------------------------------
# Archive
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
    with open(ARCHIVE_FILE, "w") as f:
        json.dump(archive, f, indent=2)


def update_archive(new_meetings):
    """Merge new meetings into archive. Dedup by slug. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_slugs = {a.get("slug") for a in archive["items"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for m in new_meetings:
        slug = m.get("slug", "")
        if not slug or slug in existing_slugs:
            continue
        entry = {
            "slug": slug,
            "source": "sfgov_meetings",
            "scraped_at": now,
            "title": m["title"],
            "agency": m["agency"],
            "date": m["date"],
            "time": m["time"],
            "cancelled": m["cancelled"],
            "address": m["address"],
            "agenda_items": m["agenda_items"],
            "source_url": m["source_url"],
        }
        archive["items"].append(entry)
        existing_slugs.add(slug)
        added += 1
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    archive["updated_at"] = now
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new meetings ({len(archive['items'])} total)",
              file=sys.stderr)


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_meetings(meetings, district=None):
    if not meetings:
        label = f"District {district}" if district else "SF"
        return f"No upcoming meetings found for {label}."

    lines = []
    label = f"District {district} Meetings" if district else "SF Commission & Board Meetings"
    lines.append(f"SF.GOV MEETINGS — {label}")
    lines.append("")

    current_date = None
    for m in meetings:
        if m["date"] != current_date:
            d = datetime.strptime(m["date"], "%Y-%m-%d")
            lines.append(f"  {d.strftime('%A, %B %d').upper()}")
            current_date = m["date"]

        cancelled = " [CANCELLED]" if m["cancelled"] else ""
        time_str = f" {m['time']}" if m["time"] else ""
        lines.append(f"  {m['date']}{time_str}{cancelled} — {m['title']}")

        if m["agency"] and m["agency"] not in m["title"]:
            lines.append(f"       [{m['agency']}]")

        if m["address"]:
            lines.append(f"       Location: {m['address']}")
        if m["online_link"]:
            lines.append(f"       Online: {m['online_link']}")
        if m["phone"]:
            lines.append(f"       Phone: {m['phone']}")

        if m["agenda_items"]:
            lines.append("       Agenda:")
            for ai in m["agenda_items"][:8]:
                lines.append(f"         - {ai[:100]}")
            if len(m["agenda_items"]) > 8:
                lines.append(f"         ... +{len(m['agenda_items']) - 8} more")

        if m["public_comment_email"]:
            lines.append(f"       Public comment: {m['public_comment_email']}")

        if m["pdf_links"]:
            for pdf in m["pdf_links"][:3]:
                lines.append(f"       PDF: {pdf['title']}")

        lines.append(f"       {m['source_url']}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    district = None
    days = 14
    include_all = "--all" in sys.argv
    as_json = "--json" in sys.argv

    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--district" and i + 1 < len(args):
            try:
                district = int(args[i + 1])
            except ValueError:
                pass
        elif arg == "--days" and i + 1 < len(args):
            try:
                days = int(args[i + 1])
            except ValueError:
                pass

    print(f"Fetching sf.gov meetings (next {days} days)...", file=sys.stderr)
    meetings = get_upcoming_meetings(district=district, days=days,
                                     include_all=include_all)
    update_archive(meetings)

    if as_json:
        print(json.dumps(meetings, indent=2))
    else:
        print(format_meetings(meetings, district=district))


if __name__ == "__main__":
    main()
