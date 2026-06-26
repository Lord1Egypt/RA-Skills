#!/usr/bin/env python3
"""
sf_rec_park.py — SF Recreation and Park Commission meeting/agenda tracker.

Scrapes the Granicus publisher page for Rec & Park (view_id=91) to get
meeting dates and clip IDs, then fetches agenda items from each meeting's
AgendaViewer page.

Data source: https://sanfrancisco.granicus.com/ViewPublisher.php?view_id=91

Meeting schedule:
  Full Commission: 3rd Thursday of each month, 10am, City Hall Room 416
  Capital Committee: 1st Wednesday
  Operations Committee: 1st Thursday
  Joint Zoo Committee: 3rd Thursday, 9am
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

try:
    import urllib.request
    import urllib.error
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PUBLISHER_URL = "https://sanfrancisco.granicus.com/ViewPublisher.php?view_id=91"
AGENDA_URL_TEMPLATE = "https://sanfrancisco.granicus.com/AgendaViewer.php?view_id=91&clip_id={clip_id}"
STATE_FILE = os.path.join(os.path.dirname(__file__), "sf_rec_park_state.json")
ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), "sf_rec_park_archive.json")
ARCHIVE_MAX = 5000

# Load district config for location-specific keywords
try:
    from config_loader import get_district_config as _get_district_config
    _DISTRICT_CFG = _get_district_config()
except ImportError:
    _DISTRICT_CFG = {"district": 5, "neighborhoods": [], "streets": []}

def _build_high_keywords():
    """Build HIGH interest keywords from district config + universal park terms."""
    cfg = _DISTRICT_CFG
    district = cfg.get("district", 5)
    # Universal park/outdoor terms (relevant for any district)
    universal = [
        "golden gate park", "ggp", "playground", "play area", "trail", "path",
        "bike", "bicycle", "pedestrian", "walking", "tree removal",
        "tree planting", "urban forest", "oak woodlands",
    ]
    # District-specific terms from config
    district_kw = [
        f"d{district}", f"district {district}",
    ]
    district_kw.extend(n.lower() for n in cfg.get("neighborhoods", []))
    district_kw.extend(s.lower() for s in cfg.get("streets", []))
    return universal + district_kw

HIGH_KEYWORDS = _build_high_keywords()

# Keywords for MEDIUM interest — capital projects, budget, policy
MEDIUM_KEYWORDS = [
    "capital", "budget", "bond", "renovation", "improvement project",
    "master plan", "community garden", "dog play", "athletic field",
    "concession", "lease", "contract award", "grant",
    "equity", "access", "ada", "accessibility",
    "open space", "natural areas", "recreation center",
]

# Keywords for LOW interest (routine/admin/zoo)
LOW_KEYWORDS = [
    "zoo", "zoological", "roll call", "adjournment", "minutes",
    "closed session", "commissioners' matters", "new business",
    "communications", "general public comment",
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
    return {"seen_meetings": {}, "seen_items": {}}


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
# Fetch helpers
# ---------------------------------------------------------------------------

def fetch_url(url, timeout=30):
    """Fetch a URL and return the response body as a string."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; sf-civic-digest/1.0)",
            "Accept": "text/html,application/xhtml+xml",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"HTTP error fetching {url}: {e.code} {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Parse publisher page — extract meetings with dates and clip_ids
# ---------------------------------------------------------------------------

def parse_meetings(html):
    """
    Parse the Granicus ViewPublisher page to extract meeting rows.
    Each row has: date, clip_id (from agenda/video link), body name (from headers attr).
    """
    meetings = []

    # Match table rows: each <tr> contains date and clip_id
    # Date pattern: <td ...><span style="display:none;">TIMESTAMP</span>MM/DD/YY</td>
    # Clip ID pattern: AgendaViewer.php?view_id=91&clip_id=NNNNN
    # Body name: headers="Date Recreation-and-Park-Commission" or similar

    row_pattern = re.compile(
        r'<tr\s+class="(?:odd|even)"[^>]*>(.*?)</tr>',
        re.DOTALL
    )

    for row_match in row_pattern.finditer(html):
        row_html = row_match.group(1)

        # Extract date: MM/DD/YY after the hidden timestamp span
        date_match = re.search(
            r'<span style="display:none;">\d+</span>\s*(\d{2}/\d{2}/\d{2})',
            row_html
        )
        if not date_match:
            continue
        date_str = date_match.group(1)

        # Parse date
        try:
            meeting_date = datetime.strptime(date_str, "%m/%d/%y")
        except ValueError:
            continue

        # Extract clip_id from AgendaViewer link
        clip_match = re.search(r'AgendaViewer\.php\?view_id=91&(?:amp;)?clip_id=(\d+)', row_html)
        clip_id = clip_match.group(1) if clip_match else None

        # Extract body name from headers attribute
        body_match = re.search(r'headers="Date\s+([^"]+)"', row_html)
        body_name = body_match.group(1).replace("-", " ") if body_match else "Recreation and Park Commission"

        meetings.append({
            "date": meeting_date.strftime("%Y-%m-%d"),
            "date_obj": meeting_date,
            "clip_id": clip_id,
            "body": body_name,
            "has_agenda": clip_id is not None,
        })

    return meetings


# ---------------------------------------------------------------------------
# Parse agenda viewer page — extract agenda items
# ---------------------------------------------------------------------------

def parse_agenda(html):
    """
    Parse the Granicus AgendaViewer page to extract agenda items.
    Items are in <div class="agenda agendaN"> tags where N is the nesting level.
    """
    items = []

    # Match agenda divs: <div class="agenda agenda0">TEXT</div> or with <a> inside
    pattern = re.compile(
        r'<div\s+class="agenda\s+agenda(\d+)"[^>]*>'
        r'(?:<a[^>]*>)?\s*(.*?)\s*(?:</a>)?</div>',
        re.DOTALL
    )

    for m in pattern.finditer(html):
        level = int(m.group(1))
        title = m.group(2).strip()

        # Clean up HTML entities
        title = title.replace("&rsquo;", "'")
        title = title.replace("&ldquo;", '"')
        title = title.replace("&rdquo;", '"')
        title = title.replace("&amp;", "&")
        title = title.replace("&nbsp;", " ")
        title = re.sub(r'<[^>]+>', '', title)  # strip any remaining tags
        title = title.strip()

        if not title:
            continue

        items.append({
            "title": title,
            "level": level,
        })

    return items


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_item(item):
    """
    Classify an agenda item as HIGH, MEDIUM, or LOW interest.
    Returns the tier string.
    """
    title_lower = item["title"].lower()

    # Check LOW first (routine items we want to skip in display)
    for kw in LOW_KEYWORDS:
        if kw.lower() in title_lower:
            return "low"

    # Check HIGH (D5/NOPA relevant, trails, trees, playgrounds)
    for kw in HIGH_KEYWORDS:
        if kw.lower() in title_lower:
            return "high"

    # Check MEDIUM (capital, budget, policy)
    for kw in MEDIUM_KEYWORDS:
        if kw.lower() in title_lower:
            return "medium"

    # Sub-items (level > 0) that didn't match anything are low
    if item["level"] > 0:
        return "low"

    # Top-level items that didn't match anything: medium by default
    # (General Calendar items are usually substantive)
    return "medium"


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_meeting_text(meeting, items_by_tier):
    """Format a single meeting with its classified agenda items for human display."""
    lines = []
    date_str = meeting["date"]
    body = meeting["body"]

    lines.append(f"  {body} -- {date_str}")

    if not any(items_by_tier.values()):
        if meeting["has_agenda"]:
            lines.append("    (no substantive agenda items parsed)")
        else:
            lines.append("    (agenda not yet posted)")
        return lines

    high = items_by_tier.get("high", [])
    medium = items_by_tier.get("medium", [])

    if high:
        for item in high:
            prefix = f"  {item['title'][:3]}" if re.match(r'^\d', item['title']) else ""
            lines.append(f"    !!! {item['title'][:100]}")

    if medium:
        for item in medium[:5]:
            lines.append(f"    ** {item['title'][:100]}")
        remaining = len(medium) - 5
        if remaining > 0:
            lines.append(f"    + {remaining} more items")

    low_count = len(items_by_tier.get("low", []))
    if low_count:
        lines.append(f"    ({low_count} routine/admin items not shown)")

    return lines


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def fetch_and_parse(days_back=30, days_forward=60, past_count=0, next_only=False):
    """
    Fetch meetings from Granicus and parse agendas.
    Returns list of meeting dicts with classified items.
    """
    print("Fetching Rec & Park meetings from Granicus...", file=sys.stderr)
    html = fetch_url(PUBLISHER_URL)
    if not html:
        print("Failed to fetch publisher page", file=sys.stderr)
        return []

    meetings = parse_meetings(html)
    print(f"Found {len(meetings)} meetings on publisher page", file=sys.stderr)

    now = datetime.now()
    cutoff_past = now - timedelta(days=days_back)
    cutoff_future = now + timedelta(days=days_forward)

    # Filter to relevant date range
    relevant = []
    for m in meetings:
        d = m["date_obj"]
        if cutoff_past <= d <= cutoff_future:
            relevant.append(m)

    # Sort by date ascending
    relevant.sort(key=lambda x: x["date"])

    if next_only:
        # Find the next upcoming meeting (or most recent if none upcoming)
        upcoming = [m for m in relevant if m["date_obj"] >= now - timedelta(days=1)]
        if upcoming:
            relevant = [upcoming[0]]
        elif relevant:
            relevant = [relevant[-1]]

    if past_count and not next_only:
        # Show only the N most recent past meetings
        past = [m for m in relevant if m["date_obj"] < now]
        future = [m for m in relevant if m["date_obj"] >= now]
        relevant = past[-past_count:] + future

    # Fetch agendas for each meeting
    results = []
    for meeting in relevant:
        items = []
        items_by_tier = {"high": [], "medium": [], "low": []}

        if meeting["clip_id"]:
            agenda_url = AGENDA_URL_TEMPLATE.format(clip_id=meeting["clip_id"])
            print(f"  Fetching agenda for {meeting['date']} (clip {meeting['clip_id']})...", file=sys.stderr)
            agenda_html = fetch_url(agenda_url)
            if agenda_html:
                raw_items = parse_agenda(agenda_html)
                for item in raw_items:
                    tier = classify_item(item)
                    item["tier"] = tier
                    items.append(item)
                    items_by_tier[tier].append(item)
                print(f"    {len(raw_items)} items: {len(items_by_tier['high'])} high, "
                      f"{len(items_by_tier['medium'])} medium, {len(items_by_tier['low'])} low",
                      file=sys.stderr)

        # Clean up date_obj (not serializable)
        result = {
            "date": meeting["date"],
            "body": meeting["body"],
            "clip_id": meeting["clip_id"],
            "has_agenda": meeting["has_agenda"],
            "agenda_url": AGENDA_URL_TEMPLATE.format(clip_id=meeting["clip_id"]) if meeting["clip_id"] else None,
            "items": items,
            "items_by_tier": items_by_tier,
            "high_count": len(items_by_tier["high"]),
            "medium_count": len(items_by_tier["medium"]),
            "low_count": len(items_by_tier["low"]),
        }
        results.append(result)

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="SF Rec & Park Commission tracker")
    parser.add_argument("--days", type=int, default=30,
                        help="Look back N days for past meetings (default: 30)")
    parser.add_argument("--forward", type=int, default=60,
                        help="Look forward N days for future meetings (default: 60)")
    parser.add_argument("--past", type=int, default=0,
                        help="Show only N most recent past meetings (0=all in range)")
    parser.add_argument("--next", action="store_true",
                        help="Show only the next upcoming meeting")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON (for orchestrator)")
    parser.add_argument("--no-state", action="store_true",
                        help="Don't load/save state file")
    parser.add_argument("--mark-seen", action="store_true",
                        help="Mark fetched meetings as seen in state")
    args = parser.parse_args()

    state = load_state() if not args.no_state else {"seen_meetings": {}, "seen_items": {}}

    # Auto-expand lookback window when --past is set, since Rec & Park meets
    # monthly (3rd Thursday). 30 days only catches ~1 meeting.
    days_back = args.days
    if args.past and args.past > 1 and days_back < args.past * 35:
        days_back = args.past * 35  # ~35 days per monthly meeting

    results = fetch_and_parse(
        days_back=days_back,
        days_forward=args.forward,
        past_count=args.past,
        next_only=args.next,
    )

    # Archive results
    archive_records = []
    for meeting in results:
        archive_records.append({
            "id": f"{meeting['date']}|{meeting.get('clip_id', '')}",
            "source": "sf_rec_park",
            "date": meeting["date"],
            "body": meeting["body"],
            "clip_id": meeting.get("clip_id"),
            "agenda_url": meeting.get("agenda_url"),
            "high_count": meeting.get("high_count", 0),
            "medium_count": meeting.get("medium_count", 0),
            "items": [
                {"title": item["title"], "tier": item["tier"], "level": item["level"]}
                for item in meeting.get("items", [])
            ],
        })
    update_archive(archive_records)

    if args.json:
        # Output for orchestrator: list of meetings with items
        output = []
        for meeting in results:
            m = {
                "date": meeting["date"],
                "body": meeting["body"],
                "clip_id": meeting["clip_id"],
                "agenda_url": meeting["agenda_url"],
                "high_count": meeting["high_count"],
                "medium_count": meeting["medium_count"],
                "items": [
                    {
                        "title": item["title"],
                        "tier": item["tier"],
                        "level": item["level"],
                    }
                    for item in meeting["items"]
                    if item["tier"] != "low"
                ],
            }
            output.append(m)
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        if not results:
            print("No Rec & Park Commission meetings found in the specified range.")
        else:
            print()
            print("RECREATION & PARK COMMISSION")
            print("  Full Commission: 3rd Thursday, 10am, City Hall Room 416")
            print(f"  Source: sanfrancisco.granicus.com (view_id=91)")
            print()

            for meeting in results:
                lines = format_meeting_text(meeting, meeting["items_by_tier"])
                for line in lines:
                    print(line)
                print()

    # Update state
    if not args.no_state and args.mark_seen:
        for meeting in results:
            key = f"{meeting['date']}_{meeting['clip_id']}"
            state.setdefault("seen_meetings", {})[key] = {
                "date": meeting["date"],
                "body": meeting["body"],
                "high_count": meeting["high_count"],
                "seen_at": datetime.now(timezone.utc).isoformat(),
            }
            for item in meeting["items"]:
                if item["tier"] in ("high", "medium"):
                    item_key = f"{meeting['date']}_{item['title'][:60]}"
                    state.setdefault("seen_items", {})[item_key] = {
                        "title": item["title"],
                        "tier": item["tier"],
                        "meeting_date": meeting["date"],
                        "seen_at": datetime.now(timezone.utc).isoformat(),
                    }
        save_state(state)
        print(f"State updated: {len(state['seen_meetings'])} meetings, "
              f"{len(state['seen_items'])} items tracked.", file=sys.stderr)

    return results


if __name__ == "__main__":
    main()
