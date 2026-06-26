#!/usr/bin/env python3
"""
sf_civic_actions.py — Protest, rally, and civic action event tracker for San Francisco.

Fetches upcoming civic action events from two sources:
  1. Mobilize.us public API (rallies, canvasses, phone banks, community events)
  2. Indybay calendar (grassroots protests, marches, demonstrations)

Merges, deduplicates, and classifies events by urgency tier:
  HIGH:   rally, march, protest, demonstration, town hall, public hearing
  MEDIUM: canvass, phone bank, community meeting, training, workshop
  LOW:    fundraiser, social, screening, other

Data sources:
  - https://api.mobilize.us/v1/events (no auth required)
  - https://www.indybay.org/calendar/ (HTML scrape)

Usage:
    # Human-readable output (default 14-day window)
    python sf_civic_actions.py

    # JSON output
    python sf_civic_actions.py --json

    # Custom window (30 days)
    python sf_civic_actions.py --days 30

    # Filter by event type
    python sf_civic_actions.py --type rally
    python sf_civic_actions.py --type protest
    python sf_civic_actions.py --type canvass

    # Combine flags
    python sf_civic_actions.py --json --days 30 --type rally
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from html import unescape

import urllib.request
import urllib.parse
import urllib.error

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

MOBILIZE_BASE = "https://api.mobilize.us/v1/events"
INDYBAY_CALENDAR = "https://www.indybay.org/calendar/"

ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), "sf_civic_actions_archive.json")
ARCHIVE_MAX = 5000

# SF postal code prefixes
SF_ZIP_PREFIXES = ("941",)
SF_LOCALITIES = ("san francisco", "sf")

# Indybay category_id for San Francisco region
INDYBAY_SF_CATEGORY = "36"

# ---------------------------------------------------------------------------
# Event type classification
# ---------------------------------------------------------------------------

# Mobilize.us event_type values mapped to our normalized types
MOBILIZE_TYPE_MAP = {
    "RALLY": "rally",
    "MARCH": "march",
    "PROTEST": "protest",
    "DEMONSTRATION": "demonstration",
    "TOWN_HALL": "town_hall",
    "PUBLIC_HEARING": "public_hearing",
    "COMMUNITY": "community",
    "CANVASS": "canvass",
    "PHONE_BANK": "phone_bank",
    "TEXT_BANK": "phone_bank",
    "TRAINING": "training",
    "MEETING": "community",
    "FUNDRAISER": "fundraiser",
    "HOUSE_PARTY": "social",
    "VOTER_REG": "canvass",
    "DEBATE_WATCH_PARTY": "social",
    "OTHER": "other",
    "PETITION": "canvass",
    "ADVOCACY_CALL": "phone_bank",
    "FRIEND_TO_FRIEND_OUTREACH": "canvass",
}

# Indybay event types mapped to our normalized types
INDYBAY_TYPE_MAP = {
    "protest": "protest",
    "rally": "rally",
    "march": "march",
    "demonstration": "demonstration",
    "meeting": "community",
    "speaker": "community",
    "panel discussion": "community",
    "press conference": "community",
    "conference": "community",
    "class/workshop": "training",
    "fundraiser": "fundraiser",
    "screening": "screening",
    "party/street party": "social",
    "concert/performance": "social",
    "other": "other",
}

HIGH_TYPES = {"rally", "march", "protest", "demonstration", "town_hall", "public_hearing"}
MEDIUM_TYPES = {"canvass", "phone_bank", "community", "training"}
LOW_TYPES = {"fundraiser", "social", "screening", "other"}


def classify_event_type(event_type):
    """Return tier (high/medium/low) based on event type."""
    t = (event_type or "").lower()
    if t in HIGH_TYPES:
        return "high"
    if t in MEDIUM_TYPES:
        return "medium"
    return "low"


def classify_by_title(title):
    """Boost classification if title contains strong keywords."""
    t = (title or "").lower()
    high_kw = ["protest", "rally", "march", "demonstration", "town hall",
               "public hearing", "no kings", "resist", "strike"]
    for kw in high_kw:
        if kw in t:
            return "high"
    return None


# ---------------------------------------------------------------------------
# Scale estimation
# ---------------------------------------------------------------------------

# National/coordinated event names that signal large turnout
BIG_EVENT_KEYWORDS = [
    "no kings", "women's march", "march for", "general strike",
    "national day of", "people's march", "climate march",
]

JOURNALISM_ARCHIVE = os.path.join(os.path.dirname(__file__), "sf_journalism_archive.json")


def estimate_scale(event, all_events):
    """Estimate event scale (big/medium/small) from available signals.

    Signals:
    1. Multiple orgs listing the same event (cross-org duplication)
    2. National/coordinated event keywords in title
    3. "MIRROR" in title (mirroring a national event)
    4. is_coordinated flag on sponsor
    5. Single timeslot (one-time event) vs many (recurring weekly = small)
    6. Cross-reference with journalism archive (press coverage = big)

    Returns: "big", "medium", or "small" with a reason string.
    """
    title = (event.get("title") or "").lower()
    reasons = []
    score = 0

    # Signal 1: Cross-org duplication — count how many events on the same date
    # have similar titles (normalized)
    norm_title = re.sub(r'[^a-z0-9]', '', title)
    same_event_count = 0
    for other in all_events:
        if other["id"] == event["id"]:
            continue
        other_norm = re.sub(r'[^a-z0-9]', '', (other.get("title") or "").lower())
        other_date = other.get("date", "")
        # Check if same date and titles share significant overlap
        if other_date == event.get("date") and (
            norm_title in other_norm or other_norm in norm_title
            or _title_overlap(norm_title, other_norm) > 0.6
        ):
            same_event_count += 1
    if same_event_count >= 2:
        score += 3
        reasons.append(f"{same_event_count + 1} orgs listing this event")
    elif same_event_count == 1:
        score += 2
        reasons.append("2 orgs listing this event")

    # Signal 2: National/coordinated event keywords
    for kw in BIG_EVENT_KEYWORDS:
        if kw in title:
            score += 3
            reasons.append(f"national movement ({kw})")
            break

    # Signal 3: "MIRROR" in title
    if "mirror" in title:
        score += 2
        reasons.append("mirror of national event")

    # Signal 4: is_coordinated flag (from Mobilize sponsor data)
    if event.get("_sponsor_coordinated"):
        score += 1
        reasons.append("coordinated campaign")

    # Signal 5: Recurring vs one-time (many timeslots = recurring weekly = small)
    timeslot_count = event.get("_timeslot_count", 1)
    if timeslot_count > 5:
        score -= 2
        reasons.append(f"recurring ({timeslot_count} timeslots)")
    elif timeslot_count == 1:
        score += 1
        reasons.append("one-time event")

    # Signal 6: Journalism cross-reference
    if os.path.exists(JOURNALISM_ARCHIVE):
        try:
            with open(JOURNALISM_ARCHIVE) as f:
                archive = json.load(f)
            articles = archive if isinstance(archive, list) else archive.get("items", [])
            # Check if any article title mentions this event (fuzzy)
            event_words = set(re.findall(r'[a-z]{4,}', title))
            for article in articles[-500:]:  # check recent 500
                art_title = (article.get("title") or "").lower()
                art_words = set(re.findall(r'[a-z]{4,}', art_title))
                overlap = event_words & art_words
                if len(overlap) >= 3:
                    score += 2
                    reasons.append(f"press coverage ({article.get('outlet_name', 'news')})")
                    break
        except (json.JSONDecodeError, IOError):
            pass

    # Determine scale
    if score >= 4:
        return "big", "; ".join(reasons)
    elif score >= 2:
        return "medium", "; ".join(reasons)
    else:
        return "small", "; ".join(reasons) if reasons else "no scale signals"


def _title_overlap(a, b):
    """Compute character overlap ratio between two normalized titles."""
    if not a or not b:
        return 0
    shorter = min(len(a), len(b))
    if shorter == 0:
        return 0
    # Count shared character bigrams
    bigrams_a = {a[i:i+2] for i in range(len(a)-1)}
    bigrams_b = {b[i:i+2] for i in range(len(b)-1)}
    if not bigrams_a or not bigrams_b:
        return 0
    return len(bigrams_a & bigrams_b) / max(len(bigrams_a), len(bigrams_b))


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
    """Merge new records into archive. Dedup by event URL or ID. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_ids = set()
    for r in archive["items"]:
        existing_ids.add(r.get("id", ""))
        existing_ids.add(r.get("url", ""))
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for record in new_records:
        rid = record.get("id", "")
        rurl = record.get("url", "")
        if rid in existing_ids or rurl in existing_ids:
            continue
        record["scraped_at"] = now
        archive["items"].append(record)
        existing_ids.add(rid)
        existing_ids.add(rurl)
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


def fetch_html(url, timeout=30):
    """Fetch a URL and return raw HTML string."""
    headers = {
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
# Mobilize.us API
# ---------------------------------------------------------------------------

def is_sf_event(event):
    """Check if a Mobilize.us event is in San Francisco."""
    loc = event.get("location")
    if not loc:
        # Virtual events without location — include if zipcode query returned them
        return event.get("is_virtual", False)
    locality = (loc.get("locality") or "").lower()
    postal = loc.get("postal_code") or ""
    if locality in SF_LOCALITIES:
        return True
    for prefix in SF_ZIP_PREFIXES:
        if postal.startswith(prefix):
            return True
    return False


def fetch_mobilize_events(days=14):
    """Fetch upcoming civic action events from Mobilize.us API."""
    params = {
        "zipcode": "94103",
        "timeslot_start": "gte_now",
        "per_page": "50",
    }
    query = urllib.parse.urlencode(params)
    url = f"{MOBILIZE_BASE}?{query}"

    print("Fetching Mobilize.us events...", file=sys.stderr)
    data = fetch_json(url)
    if data is None:
        return []

    events_data = data.get("data", [])
    if not events_data:
        print("No Mobilize.us events found.", file=sys.stderr)
        return []

    cutoff = datetime.now(timezone.utc) + timedelta(days=days)
    results = []

    for event in events_data:
        if not is_sf_event(event):
            continue

        timeslots = event.get("timeslots", [])
        if not timeslots:
            continue

        # Use the first upcoming timeslot
        ts = timeslots[0]
        start_ts = ts.get("start_date", 0)
        end_ts = ts.get("end_date", 0)

        try:
            start_dt = datetime.fromtimestamp(start_ts, tz=timezone.utc)
            end_dt = datetime.fromtimestamp(end_ts, tz=timezone.utc)
        except (OSError, ValueError):
            continue

        if start_dt > cutoff:
            continue

        raw_type = event.get("event_type", "OTHER")
        event_type = MOBILIZE_TYPE_MAP.get(raw_type, "other")

        # Build location string
        loc = event.get("location") or {}
        venue = loc.get("venue", "")
        addr_lines = loc.get("address_lines", [])
        address = ", ".join(line for line in addr_lines if line)
        locality = loc.get("locality", "")
        region = loc.get("region", "")
        loc_parts = [p for p in [venue, address, locality, region] if p]
        location_str = ", ".join(loc_parts)

        if event.get("is_virtual") and not location_str:
            location_str = "Virtual"

        description = event.get("description") or event.get("summary") or ""
        description_snippet = description[:200].strip()
        if len(description) > 200:
            description_snippet += "..."

        # Determine tier
        tier = classify_event_type(event_type)
        title_tier = classify_by_title(event.get("title", ""))
        if title_tier == "high" and tier != "high":
            tier = "high"

        sponsor = event.get("sponsor") or {}
        tags = [t.get("name", "") for t in (event.get("tags") or [])]

        results.append({
            "id": f"mobilize-{event.get('id', '')}",
            "source": "mobilize",
            "title": event.get("title", ""),
            "date": start_dt.strftime("%Y-%m-%d"),
            "time": start_dt.strftime("%H:%M") + " - " + end_dt.strftime("%H:%M") + " UTC",
            "start_ts": start_ts,
            "event_type": event_type,
            "event_type_raw": raw_type,
            "tier": tier,
            "organizer": sponsor.get("name", ""),
            "location": location_str,
            "url": event.get("browser_url", ""),
            "description": description_snippet,
            "tags": tags,
            "is_virtual": event.get("is_virtual", False),
            # Extra signals for scale estimation
            "_sponsor_coordinated": sponsor.get("is_coordinated", False),
            "_timeslot_count": len(timeslots),
        })

    print(f"  Mobilize.us: {len(results)} SF events within {days} days.", file=sys.stderr)
    return results


# ---------------------------------------------------------------------------
# Indybay calendar scraper
# ---------------------------------------------------------------------------

def parse_indybay_calendar(html, days=14):
    """Parse Indybay calendar HTML for SF events."""
    if not html:
        return []

    results = []
    today = datetime.now(timezone.utc).date()
    cutoff = today + timedelta(days=days)
    current_year = today.year

    # Parse day sections: <div id="week-day-N" class="day-events">
    # Each contains a day-title with date, then <event> tags
    day_pattern = re.compile(
        r'<div\s+id="week-day-\d+"\s+class="day-events">'
        r'<div\s+class="day-title">.*?'
        r'<span\s+class="day-title-date-textfull">(.*?)</span>'
        r'.*?</div>\s*(.*?)</div>(?=<div\s+id="week-day-|</div>\s*$)',
        re.DOTALL
    )

    event_pattern = re.compile(
        r'<event\s+class="event event-listing"\s+(.*?)>'
        r'<div class="event-listing-title"><a href="(.*?)">(.*?)</a></div>'
        r'<div class="event-listing-type">(.*?)</div>'
        r'<div class="event-listing-categories">(.*?)</div>'
        r'<div class="event-listing-time">(.*?)</div>'
        r'</event>',
        re.DOTALL
    )

    for day_match in day_pattern.finditer(html):
        date_text = day_match.group(1).strip()  # e.g., "March 27"
        events_html = day_match.group(2)

        # Parse date
        try:
            event_date = datetime.strptime(f"{date_text} {current_year}", "%B %d %Y").date()
            # Handle year boundary: if parsed date is far in the past, try next year
            if event_date < today - timedelta(days=180):
                event_date = datetime.strptime(f"{date_text} {current_year + 1}", "%B %d %Y").date()
        except ValueError:
            continue

        if event_date > cutoff:
            continue

        for ev_match in event_pattern.finditer(events_html):
            attrs = ev_match.group(1)
            link = ev_match.group(2).strip()
            title = unescape(ev_match.group(3).strip())
            event_type_raw = unescape(ev_match.group(4).strip())
            categories = unescape(ev_match.group(5).strip())
            time_str = ev_match.group(6).strip()

            # Filter to SF events: check if "San Francisco" is in categories
            # or if category_id="36" is in attributes
            cat_list = [c.strip().lower() for c in categories.split("|")]
            is_sf = ("san francisco" in cat_list
                     or f'category_id="{INDYBAY_SF_CATEGORY}"' in attrs)

            if not is_sf:
                continue

            # Normalize event type
            event_type = INDYBAY_TYPE_MAP.get(event_type_raw.lower(), "other")

            # Determine tier
            tier = classify_event_type(event_type)
            title_tier = classify_by_title(title)
            if title_tier == "high" and tier != "high":
                tier = "high"

            full_url = f"https://www.indybay.org{link}" if link.startswith("/") else link

            results.append({
                "id": f"indybay-{link}",
                "source": "indybay",
                "title": title,
                "date": event_date.strftime("%Y-%m-%d"),
                "time": time_str,
                "start_ts": 0,
                "event_type": event_type,
                "event_type_raw": event_type_raw,
                "tier": tier,
                "organizer": "",
                "location": "San Francisco",
                "url": full_url,
                "description": f"Categories: {categories}",
                "tags": [c.strip() for c in categories.split("|") if c.strip()],
                "is_virtual": False,
            })

    print(f"  Indybay: {len(results)} SF events within {days} days.", file=sys.stderr)
    return results


def fetch_indybay_events(days=14):
    """Fetch and parse Indybay calendar for SF civic action events."""
    print("Fetching Indybay calendar...", file=sys.stderr)
    html = fetch_html(INDYBAY_CALENDAR)
    if not html:
        return []
    return parse_indybay_calendar(html, days=days)


# ---------------------------------------------------------------------------
# Merge & dedup
# ---------------------------------------------------------------------------

def normalize_for_dedup(title):
    """Normalize a title for fuzzy dedup comparison."""
    return re.sub(r'[^a-z0-9]', '', title.lower())


def deduplicate_events(events):
    """Remove duplicate events by URL and by title+date similarity."""
    seen_urls = set()
    seen_title_dates = set()
    deduped = []

    for event in events:
        url = event.get("url", "")
        if url and url in seen_urls:
            continue
        seen_urls.add(url)

        norm_title = normalize_for_dedup(event.get("title", ""))
        date = event.get("date", "")
        key = f"{norm_title}_{date}"

        if key in seen_title_dates:
            continue
        seen_title_dates.add(key)

        deduped.append(event)

    return deduped


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

    type_label = event["event_type"].upper().replace("_", " ")
    scale = event.get("scale", "small")
    scale_tag = {"big": " [LARGE]", "medium": " [MEDIUM]", "small": ""}[scale]
    scale_reason = event.get("scale_reason", "")

    lines.append(f"  {marker} {event['title']}{scale_tag}")
    lines.append(f"      Date: {date_str} ({timing})")
    if event["time"]:
        lines.append(f"      Time: {event['time']}")
    lines.append(f"      Type: {type_label}")
    if scale_reason:
        lines.append(f"      Scale: {scale} — {scale_reason}")
    if event["organizer"]:
        lines.append(f"      Organizer: {event['organizer']}")
    if event["location"]:
        lines.append(f"      Location: {event['location']}")
    if event["url"]:
        lines.append(f"      URL: {event['url']}")
    if event["description"]:
        lines.append(f"      Info: {event['description']}")
    lines.append(f"      Source: {event['source']}")

    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Protest, rally, and civic action event tracker for San Francisco"
    )
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON for orchestrator integration")
    parser.add_argument("--days", type=int, default=14,
                        help="Lookahead window in days (default: 14)")
    parser.add_argument("--type", type=str, default=None,
                        help="Filter by event type (rally, protest, march, canvass, phone_bank, community, etc.)")
    args = parser.parse_args()

    # Fetch from both sources
    mobilize_events = fetch_mobilize_events(days=args.days)
    indybay_events = fetch_indybay_events(days=args.days)

    # Merge and deduplicate
    all_events = mobilize_events + indybay_events
    all_events = deduplicate_events(all_events)

    # Estimate scale for each event (needs the full list for cross-org detection)
    for event in all_events:
        scale, scale_reason = estimate_scale(event, all_events)
        event["scale"] = scale
        event["scale_reason"] = scale_reason

    # Filter by type if requested
    if args.type:
        filter_type = args.type.lower().replace(" ", "_")
        all_events = [e for e in all_events if e["event_type"] == filter_type]

    # Sort: big events first within each date, then by tier
    scale_order = {"big": 0, "medium": 1, "small": 2}
    tier_order = {"high": 0, "medium": 1, "low": 2}
    all_events.sort(key=lambda e: (e["date"], scale_order.get(e.get("scale", "small"), 3), tier_order.get(e["tier"], 3)))

    print(f"Found {len(all_events)} civic action events.", file=sys.stderr)

    # Archive all events
    update_archive(all_events)

    # Output
    if args.json:
        output = []
        for e in all_events:
            output.append({
                "id": e["id"],
                "source": e["source"],
                "title": e["title"],
                "date": e["date"],
                "time": e["time"],
                "event_type": e["event_type"],
                "event_type_raw": e["event_type_raw"],
                "tier": e["tier"],
                "organizer": e["organizer"],
                "location": e["location"],
                "url": e["url"],
                "description": e["description"],
                "tags": e["tags"],
                "is_virtual": e.get("is_virtual", False),
                "scale": e.get("scale", "small"),
                "scale_reason": e.get("scale_reason", ""),
            })
        print(json.dumps(output, indent=2))
    else:
        print()
        print("=" * 68)
        print("  SF CIVIC ACTIONS — Protests, Rallies & Community Events")
        print(f"  Sources: Mobilize.us, Indybay | {args.days}-day window")
        print("=" * 68)
        print()

        # Group by tier
        high = [e for e in all_events if e["tier"] == "high"]
        medium = [e for e in all_events if e["tier"] == "medium"]
        low = [e for e in all_events if e["tier"] == "low"]

        if high:
            print(f"  -- RALLIES, MARCHES & PROTESTS ({len(high)}) --")
            for e in high:
                lines = format_event_text(e)
                print("\n".join(lines))
                print()

        if medium:
            print(f"  -- CANVASSES, PHONE BANKS & COMMUNITY ({len(medium)}) --")
            for e in medium:
                lines = format_event_text(e)
                print("\n".join(lines))
                print()

        if low:
            print(f"  -- FUNDRAISERS, SOCIALS & OTHER ({len(low)}) --")
            for e in low:
                lines = format_event_text(e)
                print("\n".join(lines))
                print()

        if not all_events:
            print("  No civic action events found in the date range.")
            print()


if __name__ == "__main__":
    main()
