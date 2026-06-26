#!/usr/bin/env python3
"""
sf_sfcta.py — SF County Transportation Authority meeting & agenda tracker.

Scrapes sfcta.org/events for upcoming SFCTA meetings (Board, CAC, committees),
then parses each meeting detail page for agenda items and document PDFs.
Classifies items by relevance to transit/bike/ped infrastructure.

Data source: https://www.sfcta.org/events  (Drupal, curl-friendly)
Detail pages: https://www.sfcta.org/events/{slug}
Agenda PDFs: https://www.sfcta.org/sites/default/files/...

Schedule: Transportation Authority Board meets 2nd and 4th Tuesdays, 10 AM,
          City Hall Room 250 (Legislative Chamber).
          Community Advisory Committee meets 4th Wednesday, 6 PM,
          1455 Market St, 22nd Floor.

The SFCTA handles: Prop L sales tax revenue allocation, congestion pricing,
major transit capital projects, Muni Forward, freeway removals, bike/ped
infrastructure funding.

Usage:
  python3 sf_sfcta.py                   # upcoming meetings (next 30 days)
  python3 sf_sfcta.py --json            # JSON output
  python3 sf_sfcta.py --next            # next meeting only
  python3 sf_sfcta.py --days 60         # look ahead 60 days
  python3 sf_sfcta.py --all             # include low-priority items
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone, date
from html import unescape

try:
    import urllib.request
    import urllib.parse
    import urllib.error
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_URL = "https://www.sfcta.org"
EVENTS_URL = f"{BASE_URL}/events"
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sf_sfcta_archive.json")
ARCHIVE_MAX = 5000

# Meeting type classification
MEETING_TYPES = {
    "transportation authority board": {
        "type": "Board",
        "relevance": "HIGH",
        "time": "10:00 AM",
        "location": "Legislative Chamber, Room 250, City Hall",
    },
    "community advisory committee": {
        "type": "CAC",
        "relevance": "MEDIUM",
        "time": "6:00 PM",
        "location": "1455 Market St, 22nd Floor",
    },
    "treasure island": {
        "type": "Committee",
        "relevance": "MEDIUM",
        "time": "9:00 AM",
        "location": "Legislative Chamber, Room 250, City Hall",
    },
    "citizens advisory committee": {
        "type": "CAC",
        "relevance": "MEDIUM",
        "time": "6:00 PM",
        "location": "1455 Market St, 22nd Floor",
    },
    "plans and programs": {
        "type": "Committee",
        "relevance": "MEDIUM",
        "time": "10:00 AM",
        "location": "Legislative Chamber, Room 250, City Hall",
    },
    "finance": {
        "type": "Committee",
        "relevance": "MEDIUM",
        "time": "10:00 AM",
        "location": "Legislative Chamber, Room 250, City Hall",
    },
}

# Keywords for agenda item relevance classification
HIGH_KEYWORDS = [
    # Congestion pricing
    "congestion pric", "downtown toll", "cordon", "traffic pric",
    "demand management",
    # Muni Forward / transit
    "muni forward", "transit performance", "transit effectiveness",
    "rapid network", "bus rapid", "brt", "transit lane",
    "transit-only", "transit priority",
    # Bike/ped infrastructure
    "bike", "bicycle", "cycl", "protected lane", "bike lane",
    "bike network", "bikeway", "pedestrian", "walk", "vision zero",
    "traffic calm", "slow street", "safe routes", "school zone",
    # Sales tax allocation
    "prop l", "prop k", "sales tax", "expenditure plan",
    "strategic plan", "revenue alloc",
    # Freeway removals / major projects
    "freeway", "i-280", "highway removal", "boulevard",
    "central subway", "geary", "van ness",
    # Service changes
    "service change", "service reduc", "service restor",
    "fare", "free muni", "clipper",
]

MEDIUM_KEYWORDS = [
    # Capital projects
    "capital", "appropriat", "funding", "grant", "allocation",
    "project delivery", "project update",
    # Major transit systems
    "caltrain", "bart", "ferry", "golden gate", "samtrans",
    "regional", "mtc", "plan bay area",
    # Budget
    "budget", "financial", "revenue", "deficit", "audit",
    # Safety
    "safety", "collision", "crash", "fatality",
    # Streets
    "street design", "roadway", "car-free", "jfk", "great highway",
    # Policy
    "legislation", "autonomous vehicle", "tnc", "uber", "lyft",
    "equity", "environmental",
]

LOW_KEYWORDS = [
    # Administrative
    "minutes", "roll call", "adjournment", "public comment",
    "new items", "chair's report", "closed session",
    "appointment", "appoint",
    # Routine
    "personnel", "contract", "procurement",
]

# Items that are always procedural noise
SKIP_TITLES = [
    "roll call", "adjournment", "public comment",
    "end of consent", "other items",
    "during this segment",
]


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
        print(f"  Archive: +{added} new records ({len(archive['items'])} total)",
              file=sys.stderr)
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
# Event listing scraping
# ---------------------------------------------------------------------------

def classify_meeting_type(title):
    """Classify a meeting by its title. Returns (type, relevance) tuple."""
    title_lower = title.lower()
    for key, info in MEETING_TYPES.items():
        if key in title_lower:
            return info["type"], info["relevance"]
    # Default: treat unknown SFCTA meetings as medium-relevance committees
    return "Other", "MEDIUM"


def get_default_info(title):
    """Get default time/location for a meeting type based on title."""
    title_lower = title.lower()
    for key, info in MEETING_TYPES.items():
        if key in title_lower:
            return info["time"], info["location"]
    return "", ""


def fetch_meeting_list(days=30):
    """
    Fetch upcoming SFCTA meetings from the events page.
    Returns list of meeting dicts with title, date, time, location, url.
    """
    html = fetch_page(f"{EVENTS_URL}?status=upcoming")
    if not html:
        return []

    meetings = []
    today = date.today()
    cutoff = today + timedelta(days=days)

    # Parse event cards from HTML
    # Each card has: event-card_title, time datetime="...", event-card_time,
    # event-card_location, and a detail link
    cards = re.split(r'<div class="event-card\s*">', html)

    for card in cards[1:]:  # skip content before first card
        # Title
        title_m = re.search(r'event-card_title">([^<]+)', card)
        if not title_m:
            continue
        title = unescape(title_m.group(1).strip())

        # Date from <time datetime="...">
        dt_m = re.search(r'<time datetime="([^"]+)"', card)
        if not dt_m:
            continue
        dt_str = dt_m.group(1)

        # Parse the datetime
        try:
            # Format: 2026-04-14T09:00:00-0700
            # Strip timezone for parsing, handle both +/-HHMM and Z
            clean = re.sub(r'[+-]\d{4}$', '', dt_str).replace('Z', '')
            dt_obj = datetime.strptime(clean, "%Y-%m-%dT%H:%M:%S")
            meeting_date = dt_obj.date()
        except ValueError:
            continue

        # Skip meetings outside our window
        if meeting_date < today or meeting_date > cutoff:
            continue

        # Time from event-card_time
        time_m = re.search(r'event-card_time">([^<]+)', card)
        time_str = time_m.group(1).strip() if time_m else ""

        # Location from event-card_location
        loc_m = re.search(r'event-card_location">([^<]+)', card)
        location = loc_m.group(1).strip() if loc_m else ""

        # Detail URL
        url_m = re.search(r'href="(https://www\.sfcta\.org/events/[^"]+)"', card)
        detail_url = url_m.group(1) if url_m else ""

        # Fill in defaults if missing
        if not time_str or not location:
            def_time, def_loc = get_default_info(title)
            if not time_str:
                time_str = def_time
            if not location:
                location = def_loc

        meeting_type, relevance = classify_meeting_type(title)

        meetings.append({
            "title": title,
            "type": meeting_type,
            "relevance": relevance,
            "date": meeting_date.isoformat(),
            "date_display": meeting_date.strftime("%A, %B %-d, %Y"),
            "time": time_str,
            "location": location,
            "url": detail_url,
        })

    # Sort by date
    meetings.sort(key=lambda m: m["date"])
    return meetings


# ---------------------------------------------------------------------------
# Meeting detail page parsing
# ---------------------------------------------------------------------------

def fetch_agenda_items(detail_url):
    """
    Fetch a meeting detail page and extract agenda items and PDFs.
    Returns (items, agenda_pdf_url, packet_pdf_url).

    SFCTA numbers agenda items sequentially including procedural ones
    (Roll Call=1, Chair's Report=2, ED Report=3, Minutes=4, etc.).
    PDFs use this same numbering in filenames: Item3_..., Item5_..., etc.
    We preserve the SFCTA item number so PDF matching works correctly.
    """
    html = fetch_page(detail_url)
    if not html:
        return [], "", ""

    # Extract main agenda PDF and packet PDF (top-level attachments)
    agenda_pdf = ""
    packet_pdf = ""
    all_pdfs = re.findall(
        r'href="(/sites/default/files/[^"]+)"[^>]*>\s*([^<]+)',
        html
    )
    for href, label in all_pdfs:
        label_lower = label.strip().lower()
        if "agenda" in label_lower and "agenda" in href.lower() and not agenda_pdf:
            agenda_pdf = BASE_URL + href
        elif "packet" in label_lower and not packet_pdf:
            packet_pdf = BASE_URL + href

    # Extract agenda items from field__item divs inside the Agenda section
    items = []
    agenda_section = re.search(r'Agenda</div>(.*?)(?:Participation|<footer)', html, re.DOTALL)
    if agenda_section:
        agenda_html = agenda_section.group(1)
        raw_items = re.findall(r'field__item">\s*([^<]+?)\s*</div>', agenda_html)

        # SFCTA numbers items sequentially starting from 1.
        # We track the SFCTA item number for all entries (including skipped ones)
        # so that PDF matching stays aligned.
        sfcta_item_num = 0
        in_consent = False
        for raw in raw_items:
            text = unescape(raw.strip())
            if not text:
                continue

            text_lower = text.lower()

            # Track consent agenda boundaries (not numbered items themselves)
            if text_lower.startswith("consent agenda"):
                in_consent = True
                continue
            if text_lower.startswith("end of consent"):
                in_consent = False
                continue

            # Skip sub-items (indented detail lines, not numbered)
            if text_lower.startswith("positions:") or text_lower.startswith("during this"):
                continue

            # This is a numbered agenda item — increment the SFCTA number
            sfcta_item_num += 1

            # Skip procedural noise from output, but still count them
            if any(skip in text_lower for skip in SKIP_TITLES):
                continue

            is_info = "information" in text_lower
            is_action = "action" in text_lower

            # Determine action type
            if is_action:
                action_type = "ACTION"
            elif is_info:
                action_type = "INFORMATION"
            else:
                action_type = ""

            # Clean title: remove trailing "— ACTION*", "- INFORMATION", etc.
            clean_title = re.sub(
                r'\s*[—–-]\s*(ACTION\*?|INFORMATION)\s*$', '', text
            ).strip()
            # Also remove leading [Final Approval] etc. for display but keep track
            is_final = "[final approval]" in text_lower
            display_title = re.sub(
                r'^\[Final Approval\]\s*', '', clean_title, flags=re.IGNORECASE
            ).strip()

            # Find associated PDF links using the SFCTA item number
            item_pdfs = []
            item_pdf_pattern = rf'href="(/sites/default/files/[^"]*Item{sfcta_item_num}[_][^"]*\.pdf)"'
            for pdf_href in re.findall(item_pdf_pattern, html, re.IGNORECASE):
                item_pdfs.append(BASE_URL + pdf_href)

            items.append({
                "number": sfcta_item_num,
                "title": display_title,
                "action_type": action_type,
                "consent": in_consent,
                "final_approval": is_final,
                "pdfs": item_pdfs,
            })

    return items, agenda_pdf, packet_pdf


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_item(item):
    """Classify an agenda item by relevance. Returns 'high', 'medium', or 'low'."""
    text = item.get("title", "").lower()

    for kw in HIGH_KEYWORDS:
        if kw in text:
            return "high"

    for kw in MEDIUM_KEYWORDS:
        if kw in text:
            return "medium"

    for kw in LOW_KEYWORDS:
        if kw in text:
            return "low"

    # Default: medium for SFCTA (transportation policy is generally significant)
    return "medium"


def flag_key_topics(item):
    """Return list of key topic tags for an item."""
    text = item.get("title", "").lower()
    topics = []
    topic_map = {
        "congestion pricing": ["congestion pric", "downtown toll", "cordon"],
        "Muni Forward": ["muni forward", "transit effectiveness"],
        "bike/ped": ["bike", "bicycle", "cycl", "pedestrian", "vision zero",
                     "walk", "safe routes"],
        "sales tax (Prop L)": ["prop l", "sales tax", "expenditure plan"],
        "freeway removal": ["freeway", "i-280", "highway removal"],
        "Caltrain": ["caltrain"],
        "BART": ["bart"],
        "autonomous vehicles": ["autonomous vehicle"],
        "safety": ["safety study", "vision zero", "traffic calm"],
    }
    for topic, keywords in topic_map.items():
        if any(kw in text for kw in keywords):
            topics.append(topic)
    return topics


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

TIER_MARKERS = {"high": "[!!!]", "medium": "[**]", "low": "[.]"}
RELEVANCE_MARKERS = {"HIGH": "[!!!]", "MEDIUM": "[**]", "LOW": "[.]"}


def format_meeting_text(meeting, items, show_low=False):
    """Format a meeting and its items for human-readable output."""
    lines = []
    meeting_date = meeting.get("date", "?")
    title = meeting.get("title", "SFCTA Meeting")
    meeting_type = meeting.get("type", "")
    relevance = meeting.get("relevance", "MEDIUM")
    url = meeting.get("url", "")
    agenda_pdf = meeting.get("agenda_pdf", "")

    # Timing info
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

    marker = RELEVANCE_MARKERS.get(relevance, "")
    lines.append(f"{marker} {title} -- {meeting.get('date_display', meeting_date)} ({timing})")
    lines.append(f"  {meeting.get('time', '')} | {meeting.get('location', '')}")
    if url:
        lines.append(f"  {url}")
    if agenda_pdf:
        lines.append(f"  Agenda PDF: {agenda_pdf}")
    lines.append("")

    if not items:
        lines.append("  Agenda not yet published.")
        lines.append("")
        return lines

    high_items = [i for i in items if i["tier"] == "high"]
    medium_items = [i for i in items if i["tier"] == "medium"]
    low_items = [i for i in items if i["tier"] == "low"]

    if high_items:
        lines.append(f"  -- KEY TRANSPORTATION ITEMS ({len(high_items)}) --")
        for item in high_items:
            num = f"Item {item['number']}: " if item.get("number") else ""
            action = f" [{item['action_type']}]" if item.get("action_type") else ""
            consent = " [consent]" if item.get("consent") else ""
            final = " [FINAL]" if item.get("final_approval") else ""
            topics = item.get("topics", [])
            topic_str = f" ({', '.join(topics)})" if topics else ""
            lines.append(f"    {TIER_MARKERS['high']} {num}{item['title']}{action}{consent}{final}{topic_str}")
        lines.append("")

    if medium_items:
        lines.append(f"  -- NOTABLE ({len(medium_items)}) --")
        for item in medium_items:
            num = f"Item {item['number']}: " if item.get("number") else ""
            action = f" [{item['action_type']}]" if item.get("action_type") else ""
            consent = " [consent]" if item.get("consent") else ""
            topics = item.get("topics", [])
            topic_str = f" ({', '.join(topics)})" if topics else ""
            lines.append(f"    {TIER_MARKERS['medium']} {num}{item['title']}{action}{consent}{topic_str}")
        lines.append("")

    if low_items and show_low:
        lines.append(f"  -- LOW PRIORITY ({len(low_items)}) --")
        for item in low_items:
            num = f"Item {item['number']}: " if item.get("number") else ""
            lines.append(f"    {TIER_MARKERS['low']} {num}{item['title']}")
        lines.append("")
    elif low_items:
        lines.append(f"  ({len(low_items)} low-priority items hidden: admin, appointments)")
        lines.append("")

    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="SFCTA meeting & agenda tracker"
    )
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON for orchestrator integration")
    parser.add_argument("--next", action="store_true",
                        help="Show only the next upcoming meeting")
    parser.add_argument("--days", type=int, default=30,
                        help="Look-ahead window in days (default: 30)")
    parser.add_argument("--all", action="store_true",
                        help="Include low-priority items")
    parser.add_argument("--no-agenda", action="store_true",
                        help="Skip fetching detail pages (faster, list only)")
    args = parser.parse_args()

    # Fetch meeting list
    print("Fetching SFCTA meeting calendar...", file=sys.stderr)
    meetings = fetch_meeting_list(days=args.days)

    if not meetings:
        print("No upcoming SFCTA meetings found.", file=sys.stderr)
        if args.json:
            print(json.dumps({"meetings": [], "error": "No meetings found"}))
        else:
            print("No upcoming SFCTA meetings found.")
        return

    print(f"Found {len(meetings)} upcoming meetings.", file=sys.stderr)

    # If --next, keep only the first meeting
    if args.next:
        meetings = meetings[:1]

    # Fetch agenda items for each meeting
    all_results = []
    for meeting in meetings:
        items = []
        agenda_pdf = ""
        packet_pdf = ""

        if not args.no_agenda and meeting.get("url"):
            print(f"  Fetching agenda for {meeting['title']} ({meeting['date']})...",
                  file=sys.stderr)
            raw_items, agenda_pdf, packet_pdf = fetch_agenda_items(meeting["url"])

            for item in raw_items:
                tier = classify_item(item)
                topics = flag_key_topics(item)
                items.append({
                    **item,
                    "tier": tier,
                    "topics": topics,
                })

            # Sort: high first, then medium, then low
            tier_order = {"high": 0, "medium": 1, "low": 2}
            items.sort(key=lambda x: tier_order.get(x["tier"], 9))

        result = {
            **meeting,
            "agenda_pdf": agenda_pdf,
            "packet_pdf": packet_pdf,
            "items": items,
            "item_count": len(items),
            "high_count": sum(1 for i in items if i["tier"] == "high"),
        }
        all_results.append(result)

    # Archive
    archive_records = []
    for r in all_results:
        archive_records.append({
            "id": r.get("url", r["date"]),
            "source": "sf_sfcta",
            "title": r["title"],
            "type": r["type"],
            "relevance": r["relevance"],
            "date": r["date"],
            "time": r["time"],
            "location": r["location"],
            "url": r.get("url", ""),
            "agenda_pdf": r.get("agenda_pdf", ""),
            "packet_pdf": r.get("packet_pdf", ""),
            "item_count": r["item_count"],
            "high_count": r["high_count"],
            "items": [
                {
                    "number": i["number"],
                    "title": i["title"],
                    "action_type": i.get("action_type", ""),
                    "consent": i.get("consent", False),
                    "tier": i["tier"],
                    "topics": i.get("topics", []),
                }
                for i in r["items"]
            ],
        })
    update_archive(archive_records)

    # Output
    if args.json:
        output = []
        for r in all_results:
            entry = {
                "title": r["title"],
                "type": r["type"],
                "relevance": r["relevance"],
                "date": r["date"],
                "date_display": r["date_display"],
                "time": r["time"],
                "location": r["location"],
                "url": r.get("url", ""),
                "agenda_pdf": r.get("agenda_pdf", ""),
                "packet_pdf": r.get("packet_pdf", ""),
                "item_count": r["item_count"],
                "high_count": r["high_count"],
                "items": [
                    {
                        "number": i["number"],
                        "title": i["title"],
                        "action_type": i.get("action_type", ""),
                        "consent": i.get("consent", False),
                        "final_approval": i.get("final_approval", False),
                        "tier": i["tier"],
                        "topics": i.get("topics", []),
                        "pdfs": i.get("pdfs", []),
                    }
                    for i in r["items"]
                    if args.all or i["tier"] != "low"
                ],
            }
            output.append(entry)
        print(json.dumps(output, indent=2))
    else:
        if not all_results:
            print("No upcoming SFCTA meetings to display.")
        else:
            print()
            print("=" * 65)
            print("  SF COUNTY TRANSPORTATION AUTHORITY (SFCTA)")
            print("  Board meets 2nd & 4th Tuesdays, 10 AM, City Hall Room 250")
            print("  CAC meets 4th Wednesday, 6 PM, 1455 Market St 22nd Fl")
            print("  Comment: clerk@sfcta.org | Watch: sfgovtv.org")
            print("=" * 65)
            print()

            for r in all_results:
                lines = format_meeting_text(r, r["items"], show_low=args.all)
                print("\n".join(lines))

    return all_results


if __name__ == "__main__":
    main()
