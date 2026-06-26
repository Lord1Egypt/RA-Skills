#!/usr/bin/env python3
"""
sf_sfmta_board.py — SFMTA Board of Directors meeting & agenda tracker.

Scrapes sfmta.com/calendar for upcoming Board meetings, then parses each
meeting page for agenda items. Classifies items by relevance to transit
riders (service changes, bike infra, fare decisions, pedestrian safety).

Data source: https://www.sfmta.com/calendar  (curl-friendly, Drupal)
Meeting pages: https://www.sfmta.com/calendar/board-directors-meeting-{slug}
Agenda PDFs: https://www.sfmta.com/media/{id}/download?inline

Schedule: 1st and 3rd Tuesdays, 1 PM, City Hall Room 400.
"""

import argparse
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

BASE_URL = "https://www.sfmta.com"
CALENDAR_URL = f"{BASE_URL}/calendar"
STATE_FILE = os.path.join(os.path.dirname(__file__), "sf_sfmta_board_state.json")
ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), "sf_sfmta_board_archive.json")
ARCHIVE_MAX = 5000

# Keywords for relevance classification — transit rider perspective
HIGH_KEYWORDS = [
    # Service changes
    "service change", "service reduc", "service restor", "route change",
    "muni service", "service equity", "service plan", "frequency",
    "headway", "line eliminat", "line restor", "rapid network",
    # Bike infrastructure
    "bike", "bicycle", "cycl", "protected lane", "bike lane",
    "bike share", "bikeway", "bike network",
    # Fare decisions
    "fare", "clipper", "free muni", "youth pass", "senior pass",
    "low income pass", "lifeline pass", "pricing",
    # Pedestrian safety
    "pedestrian", "vision zero", "crosswalk", "signal timing",
    "walk", "daylighting", "speed limit", "traffic calm",
    "speed reduction", "school zone", "slow street",
    # Major transit projects
    "bus rapid", "brt", "subway", "central subway", "light rail",
    "geary", "van ness", "quick-build", "transit lane",
    "transit-only", "red lane", "bus lane", "transit priority",
]

MEDIUM_KEYWORDS = [
    # Capital projects & fleet
    "capital", "fleet", "battery electric", "zero emission",
    "trolleybus", "lrv", "vehicle procure", "potrero yard",
    "kirkland", "woods", "bus yard", "moderniz",
    # Budget (affects service levels)
    "budget", "financial", "revenue", "deficit",
    # Safety general
    "safety", "collision", "crash", "fatality", "injury",
    "enforcement", "red light", "speed camera",
    # Accessibility
    "accessib", "ada", "paratransit", "wheel", "elevator",
    # Streets
    "street design", "roadway", "shared space", "slow street",
    "open street", "car-free", "jfk", "great highway",
]

LOW_KEYWORDS = [
    # Parking (explicitly de-prioritized)
    "parking", "meter", "garage", "residential permit",
    # Administrative
    "claim", "contract", "agreement", "procurement",
    "closed session", "litigation", "personnel",
    "calpers", "retirement", "insurance",
    "minutes", "cac report",
]

# Items with these keywords are always noise
SKIP_KEYWORDS = [
    "closed session",
]


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"seen_items": {}, "last_check": None}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


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
    """Merge new records into archive. Dedup by id. Cap at ARCHIVE_MAX."""
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

def fetch_page(url, timeout=30):
    """Fetch a URL and return the HTML as a string."""
    headers = {
        "Accept": "text/html,application/xhtml+xml",
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
# Calendar scraping
# ---------------------------------------------------------------------------

def parse_meeting_date_from_slug(slug):
    """Extract a date from a slug like 'board-directors-meeting-april-7-2026'."""
    m = re.search(r'meeting-(\w+)-(\d+)-(\d{4})', slug)
    if not m:
        return None
    month_str, day_str, year_str = m.group(1), m.group(2), m.group(3)
    try:
        dt = datetime.strptime(f"{month_str} {day_str} {year_str}", "%B %d %Y")
        return dt.date()
    except ValueError:
        return None


def _probe_past_meetings(n_months=2):
    """
    The SFMTA calendar page only shows future meetings. To find recent past
    meetings, we probe known URL patterns (1st and 3rd Tuesdays) going back
    n_months. This is fast — just HEAD requests to check which pages exist.
    """
    today = date.today()
    candidates = []

    for month_offset in range(0, n_months + 1):
        # Go back month_offset months
        probe_month = today.month - month_offset
        probe_year = today.year
        while probe_month < 1:
            probe_month += 12
            probe_year -= 1

        # Find 1st and 3rd Tuesdays of this month
        first_day = date(probe_year, probe_month, 1)
        # Find first Tuesday (weekday 1)
        days_to_tuesday = (1 - first_day.weekday()) % 7
        first_tuesday = first_day + timedelta(days=days_to_tuesday)
        third_tuesday = first_tuesday + timedelta(weeks=2)

        for d in [first_tuesday, third_tuesday]:
            if d >= today:
                continue  # Skip future dates (handled by calendar page)
            month_name = d.strftime("%B").lower()
            slug = f"/calendar/board-directors-meeting-{month_name}-{d.day}-{d.year}"
            candidates.append((slug, d))

    # Check which URLs exist (lightweight HEAD-like check via fetch_page)
    found = []
    for slug, d in candidates:
        url = BASE_URL + slug
        try:
            req = urllib.request.Request(url, method="HEAD", headers={
                "User-Agent": "sf-civic-digest/1.0",
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    found.append({
                        "slug": slug,
                        "url": url,
                        "date": d.isoformat(),
                        "date_obj": d,
                    })
        except Exception:
            pass  # 404 or error — meeting doesn't exist at this date

    return found


def fetch_meeting_list(include_past=0):
    """Fetch the SFMTA calendar and extract Board of Directors meeting links.

    The calendar page only lists future meetings. If include_past > 0, we
    also probe recent past meeting URLs (1st/3rd Tuesdays pattern).
    """
    html = fetch_page(CALENDAR_URL)
    if not html:
        return []

    # Extract board-directors-meeting links from calendar page (future)
    pattern = r'href="(/calendar/board-directors-meeting-[^"]+)"'
    slugs = list(set(re.findall(pattern, html)))

    meetings = []
    seen_dates = set()
    for slug in slugs:
        meeting_date = parse_meeting_date_from_slug(slug)
        if meeting_date:
            meetings.append({
                "slug": slug,
                "url": BASE_URL + slug,
                "date": meeting_date.isoformat(),
                "date_obj": meeting_date,
            })
            seen_dates.add(meeting_date.isoformat())

    # Probe past meetings if requested
    if include_past > 0:
        past_probed = _probe_past_meetings(n_months=2)
        for pm in past_probed:
            if pm["date"] not in seen_dates:
                meetings.append(pm)
                seen_dates.add(pm["date"])

    # Sort by date
    meetings.sort(key=lambda m: m["date_obj"])

    # Remove internal date_obj before returning
    for m in meetings:
        del m["date_obj"]

    return meetings


# ---------------------------------------------------------------------------
# Meeting page parsing
# ---------------------------------------------------------------------------

def fetch_meeting_items(meeting_url):
    """Fetch a meeting detail page and extract agenda items from report links."""
    html = fetch_page(meeting_url)
    if not html:
        return [], None

    items = []

    # Extract agenda items from report links: /reports/DATE-mtab-item-NUM-TITLE
    pattern = r'href="(/reports/[^"]*mtab-item[^"]*)"[^>]*>([^<]*)<'
    matches = re.findall(pattern, html)

    seen_urls = set()
    for report_url, raw_title in matches:
        if report_url in seen_urls:
            continue
        seen_urls.add(report_url)

        title = raw_title.strip()
        # Parse item number from title: "3-17-26 MTAB Item 10.2 Traffic Modifications"
        item_match = re.search(r'Item\s+([\d.]+[A-Za-z]?)\s+(.*)', title)
        if item_match:
            item_num = item_match.group(1)
            item_title = item_match.group(2).strip()
        else:
            item_num = ""
            item_title = title

        # Determine if consent calendar (item 10.x) or regular
        is_consent = item_num.startswith("10.")
        category = "consent" if is_consent else "regular"

        items.append({
            "item_number": item_num,
            "title": item_title,
            "category": category,
            "report_url": BASE_URL + report_url,
        })

    # Extract the agenda PDF link
    agenda_pdf = None
    pdf_match = re.search(r'href="(/reports/[^"]*mtab-agenda[^"]*)"', html)
    if pdf_match:
        agenda_pdf = BASE_URL + pdf_match.group(1)
    # Also look for direct media download
    if not agenda_pdf:
        media_match = re.search(r'href="(/media/\d+/download[^"]*)"', html)
        if media_match:
            agenda_pdf = BASE_URL + media_match.group(1)

    return items, agenda_pdf


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_item(item):
    """
    Classify an agenda item by relevance to a car-free transit enthusiast.
    Returns: 'high', 'medium', 'low', or 'skip'
    """
    text = (item.get("title", "") + " " + item.get("item_number", "")).lower()

    # Skip noise
    for kw in SKIP_KEYWORDS:
        if kw in text:
            return "skip"

    # High: service changes, bike infra, fare, pedestrian safety
    for kw in HIGH_KEYWORDS:
        if kw in text:
            return "high"

    # Medium: capital projects, budget, safety, accessibility
    for kw in MEDIUM_KEYWORDS:
        if kw in text:
            return "medium"

    # Low: parking, administrative, contracts
    for kw in LOW_KEYWORDS:
        if kw in text:
            return "low"

    # Default: medium (Board items are generally significant)
    return "medium"


def is_new_item(item, state):
    """Check if we've seen this item before."""
    key = f"{item.get('item_number', '')}|{item.get('title', '')}"
    return key not in state.get("seen_items", {})


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

TIER_MARKERS = {"high": "[!!!]", "medium": "[**]", "low": "[.]"}


def format_meeting_text(meeting, items, show_low=False):
    """Format a meeting and its items for human-readable output."""
    lines = []
    meeting_date = meeting.get("date", "?")
    url = meeting.get("url", "")

    # Parse date for display
    try:
        dt = datetime.strptime(meeting_date, "%Y-%m-%d")
        date_str = dt.strftime("%A, %B %-d, %Y")
    except (ValueError, TypeError):
        date_str = meeting_date

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

    lines.append(f"SFMTA Board of Directors -- {date_str} ({timing})")
    lines.append(f"  1:00 PM | City Hall Room 400")
    lines.append(f"  {url}")
    lines.append("")

    if not items:
        lines.append("  Agenda not yet published.")
        return lines

    high_items = [i for i in items if i["tier"] == "high"]
    medium_items = [i for i in items if i["tier"] == "medium"]
    low_items = [i for i in items if i["tier"] == "low"]

    if high_items:
        lines.append(f"  -- TRANSIT RIDER IMPACT ({len(high_items)}) --")
        for item in high_items:
            new_tag = " [NEW]" if item.get("new") else ""
            num = f"Item {item['item_number']}: " if item["item_number"] else ""
            cat = f" [{item['category']}]" if item["category"] == "consent" else ""
            lines.append(f"    {TIER_MARKERS['high']} {num}{item['title']}{cat}{new_tag}")
        lines.append("")

    if medium_items:
        lines.append(f"  -- NOTABLE ({len(medium_items)}) --")
        for item in medium_items:
            new_tag = " [NEW]" if item.get("new") else ""
            num = f"Item {item['item_number']}: " if item["item_number"] else ""
            cat = f" [{item['category']}]" if item["category"] == "consent" else ""
            lines.append(f"    {TIER_MARKERS['medium']} {num}{item['title']}{cat}{new_tag}")
        lines.append("")

    if low_items and show_low:
        lines.append(f"  -- LOW PRIORITY ({len(low_items)}) --")
        for item in low_items:
            num = f"Item {item['item_number']}: " if item["item_number"] else ""
            lines.append(f"    {TIER_MARKERS['low']} {num}{item['title']}")
        lines.append("")
    elif low_items:
        lines.append(f"  ({len(low_items)} low-priority items hidden: parking, admin, contracts)")
        lines.append("")

    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="SFMTA Board of Directors meeting & agenda tracker"
    )
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON for orchestrator integration")
    parser.add_argument("--next", action="store_true",
                        help="Show only the next upcoming meeting")
    parser.add_argument("--all", action="store_true",
                        help="Include low-priority items (parking, admin)")
    parser.add_argument("--no-state", action="store_true",
                        help="Don't load/save state (for testing)")
    parser.add_argument("--mark-seen", action="store_true",
                        help="Mark fetched items as seen in state")
    parser.add_argument("--past", type=int, default=0,
                        help="Also include N most recent past meetings")
    args = parser.parse_args()

    # State
    state = load_state() if not args.no_state else {"seen_items": {}, "last_check": None}

    # Fetch meeting list
    print("Fetching SFMTA Board meeting calendar...", file=sys.stderr)
    meetings = fetch_meeting_list(include_past=args.past)

    if not meetings:
        print("No meetings found on calendar.", file=sys.stderr)
        if args.json:
            print(json.dumps({"meetings": [], "error": "No meetings found on calendar"}))
        else:
            print("No SFMTA Board meetings found on the calendar.")
        return

    print(f"Found {len(meetings)} Board meetings on calendar.", file=sys.stderr)

    # Split into past and future
    today = date.today().isoformat()
    future = [m for m in meetings if m["date"] >= today]
    past = [m for m in meetings if m["date"] < today]

    # Select which meetings to show
    selected = []
    if args.next:
        if future:
            selected = [future[0]]
        elif past:
            # No future meetings on calendar; show most recent past
            selected = [past[-1]]
    else:
        selected = list(future)
        if args.past > 0 and past:
            selected = past[-args.past:] + selected

    if not selected:
        selected = meetings[-1:]  # fallback: show the most recent

    # Fetch agenda items for each selected meeting
    all_results = []
    for meeting in selected:
        print(f"  Fetching agenda for {meeting['date']}...", file=sys.stderr)
        items, agenda_pdf = fetch_meeting_items(meeting["url"])

        classified = []
        for item in items:
            tier = classify_item(item)
            if tier == "skip":
                continue
            new = is_new_item(item, state)
            classified.append({
                **item,
                "tier": tier,
                "new": new,
            })

        # Sort: high first, then medium, then low
        tier_order = {"high": 0, "medium": 1, "low": 2}
        classified.sort(key=lambda x: tier_order.get(x["tier"], 9))

        all_results.append({
            "meeting": meeting,
            "agenda_pdf": agenda_pdf,
            "items": classified,
            "item_count": len(classified),
            "high_count": sum(1 for i in classified if i["tier"] == "high"),
        })

    # Archive results
    archive_records = []
    for r in all_results:
        archive_records.append({
            "id": r["meeting"]["url"],
            "source": "sf_sfmta_board",
            "date": r["meeting"]["date"],
            "url": r["meeting"]["url"],
            "agenda_pdf": r.get("agenda_pdf"),
            "item_count": r["item_count"],
            "high_count": r["high_count"],
            "items": [
                {
                    "item_number": i["item_number"],
                    "title": i["title"],
                    "category": i["category"],
                    "tier": i["tier"],
                    "report_url": i["report_url"],
                }
                for i in r["items"]
            ],
        })
    update_archive(archive_records)

    # Output
    if args.json:
        output = []
        for r in all_results:
            output.append({
                "date": r["meeting"]["date"],
                "url": r["meeting"]["url"],
                "agenda_pdf": r["agenda_pdf"],
                "item_count": r["item_count"],
                "high_count": r["high_count"],
                "items": [
                    {
                        "item_number": i["item_number"],
                        "title": i["title"],
                        "category": i["category"],
                        "tier": i["tier"],
                        "new": i["new"],
                        "report_url": i["report_url"],
                    }
                    for i in r["items"]
                    if args.all or i["tier"] != "low"
                ],
            })
        print(json.dumps(output, indent=2))
    else:
        if not all_results:
            print("No SFMTA Board meetings to display.")
        else:
            print()
            print("=" * 60)
            print("  SFMTA BOARD OF DIRECTORS")
            print("  Meets 1st & 3rd Tuesdays, 1 PM, City Hall Room 400")
            print("  Watch: sfgovtv.org/sfmtaLIVE")
            print("  Comment: MTABoard@sfmta.com (by noon day before)")
            print("=" * 60)
            print()

            for r in all_results:
                lines = format_meeting_text(
                    r["meeting"], r["items"], show_low=args.all
                )
                print("\n".join(lines))

    # Update state
    if not args.no_state and args.mark_seen:
        for r in all_results:
            for item in r["items"]:
                key = f"{item.get('item_number', '')}|{item.get('title', '')}"
                state.setdefault("seen_items", {})[key] = {
                    "meeting_date": r["meeting"]["date"],
                    "title": item["title"],
                    "tier": item["tier"],
                    "seen_at": datetime.now(timezone.utc).isoformat(),
                }
        state["last_check"] = datetime.now(timezone.utc).isoformat()
        save_state(state)
        total_seen = len(state["seen_items"])
        print(f"State updated: {total_seen} items tracked.", file=sys.stderr)

    return all_results


if __name__ == "__main__":
    main()
