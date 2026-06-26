#!/usr/bin/env python3
"""
sf_volunteer_cleanups.py — Upcoming community cleanup events in SF.

Sources:
  1. Refuse Refuse SF (refuserefusesf.org/cleanups) — community-organized,
     frequent, hyperlocal. Multiple events per week citywide.
  2. DPW Love Our City NBDs (sfpublicworks.org/LoveOurCity) — official monthly
     neighborhood beautification days, one per month rotating through districts.

Output:
  Upcoming cleanup events in the next N days, filtered by district neighborhoods.
  JSON output (--json) for integration into sf_weekly_digest.py.

Usage:
  python3 sf_volunteer_cleanups.py                  # D5, next 14 days
  python3 sf_volunteer_cleanups.py --district 9     # D9 neighborhoods
  python3 sf_volunteer_cleanups.py --days 7         # next 7 days only
  python3 sf_volunteer_cleanups.py --all            # all SF events, no filter
  python3 sf_volunteer_cleanups.py --json           # JSON output
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, date, timedelta, timezone

# ---------------------------------------------------------------------------
# District config
# ---------------------------------------------------------------------------

try:
    from config_loader import get_district_config as _get_district_config
    _DISTRICT_CFG = _get_district_config()
except ImportError:
    _DISTRICT_CFG = {"district": 5, "neighborhoods": [], "streets": []}

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sf_volunteer_cleanups_archive.json")
ARCHIVE_MAX = 5000

# Neighborhood keyword lists per district (fallback if config_loader missing/sparse)
DISTRICT_NEIGHBORHOODS = {
    1: ["richmond", "inner richmond", "outer richmond", "sea cliff", "lake street"],
    2: ["marina", "cow hollow", "pacific heights", "presidio heights", "anza vista"],
    3: ["north beach", "chinatown", "telegraph hill", "russian hill", "fisherman"],
    4: ["sunset", "inner sunset", "outer sunset", "parkside", "west portal"],
    5: ["nopa", "western addition", "haight", "lower haight", "alamo square",
        "divisadero", "fillmore", "panhandle", "hayes valley", "ashbury"],
    6: ["soma", "south of market", "tenderloin", "civic center", "mid-market",
        "yerba buena", "south beach", "rincon hill"],
    7: ["west portal", "forest hill", "st. francis wood", "inner sunset",
        "miraloma", "glen park", "diamond heights", "twin peaks"],
    8: ["castro", "noe valley", "eureka valley", "corona heights", "dolores"],
    9: ["mission", "bernal heights", "portola", "excelsior", "outer mission"],
    10: ["bayview", "hunters point", "potrero hill", "dogpatch", "visitacion valley"],
    11: ["ingleside", "oceanview", "balboa terrace", "ingleside terrace",
         "lakeshore", "merced heights", "oceanview"],
}

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
        rid = record.get("id", "")
        if not rid or rid in existing_ids:
            continue
        record["scraped_at"] = now
        archive["items"].append(record)
        existing_ids.add(rid)
        added += 1
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new records ({len(archive['items'])} total)", file=sys.stderr)
    return archive


def _get_neighborhoods(district):
    """Return neighborhood keywords for a given district."""
    cfg = _DISTRICT_CFG
    cfg_district = cfg.get("district", 5)
    cfg_neighborhoods = [n.lower() for n in cfg.get("neighborhoods", [])]

    # If config matches requested district, use config neighborhoods
    if cfg_district == district and cfg_neighborhoods:
        return cfg_neighborhoods

    # Fall back to hardcoded list
    return DISTRICT_NEIGHBORHOODS.get(district, [])


# ---------------------------------------------------------------------------
# Refuse Refuse SF scraper
# ---------------------------------------------------------------------------

REFUSEREFUSE_URL = "https://refuserefusesf.org/cleanups"
REFUSEREFUSE_BASE = "https://refuserefusesf.org"

def _fetch_url(url, timeout=15):
    """Fetch URL content as string."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; CivicClaw/1.0)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        print(f"  ⚠️  fetch {url} failed: {e}", file=sys.stderr)
        return ""


def _get_bundle_url(html):
    """
    Extract the GoDaddy/Weebly JS bundle URL from the main page HTML.
    The bundle contains the full event dataset as embedded JSON.
    Returns None if not found.
    """
    # The bundle is the largest script from wsimg.com blobby/go path
    bundle_re = re.compile(
        r'src=["\']?(//img1\.wsimg\.com/blobby/go/[a-z0-9/-]+/gpub/[a-f0-9]+/script\.js)["\']?',
        re.IGNORECASE
    )
    matches = bundle_re.findall(html)
    # Pick the largest bundle (usually the second one — the page-specific bundle)
    if matches:
        return "https:" + matches[-1]
    return None


def _parse_refuse_refuse_bundle(bundle_js, days_ahead=14):
    """
    Parse all Refuse Refuse SF events from the GoDaddy/Weebly JS bundle.

    The site is a SPA that lazy-loads events. The HTML only shows one event
    per date. But the full dataset (136+ events) is baked into the JS bundle
    as triple-escaped JSON. We extract it from there to get all events.

    Each date entry in the bundle has:
      date: "Thursday, March 26"
      title: "18 Cleanups"
      desc: (escaped Draft.js JSON with "text" fields containing pipe-delimited events)

    Each event text: "Name | time | neighborhood | Organizer: X | Meet at Y. Sign up..."
    """
    events = []
    today = date.today()
    cutoff = today + timedelta(days=days_ahead)
    current_year = today.year

    # Extract date entries: \\\"date\\\":\\\"DATESTR\\\" ... \\\"desc\\\":\\\"ESCAPED_JSON\\\"
    entry_re = re.compile(
        r'\\\"date\\\":\\\"([^\\\"]+)\\\"'
        r'.*?\\\"title\\\":\\\"([^\\\"]+)\\\"'
        r'.*?\\\"desc\\\":\\\"(.+?)\\\"(?=,\\\")',
        re.DOTALL
    )

    # Event line parser (pipe-delimited)
    event_line_re = re.compile(
        r'([^|]+?)\s*\|\s*'
        r'(\d{1,2}:\d{2}[ap]m\s*[-–]\s*\d{1,2}:\d{2}[ap]m)\s*\|\s*'
        r'([^|]+?)\s*\|\s*'
        r'Organizer:\s*([^|]+?)\s*\|\s*'
        r'Meet at\s+(.+?)(?:\.\s*Sign up|$)',
        re.IGNORECASE
    )

    for entry_m in entry_re.finditer(bundle_js):
        date_str = entry_m.group(1)
        desc_raw = entry_m.group(3)

        # Parse date
        try:
            event_date = datetime.strptime(f"{date_str} {current_year}", "%A, %B %d %Y").date()
            if event_date < today - timedelta(days=1):
                event_date = event_date.replace(year=current_year + 1)
        except ValueError:
            continue

        if event_date > cutoff:
            continue

        # Extract event text lines from triple-escaped desc
        # text fields look like: \\\\\\\"text\\\\\\\":\\\\\\\"EVENT TEXT\\\\\\\"
        text_matches = re.findall(r'\\\\+\"text\\\\+\":\\\\+\"([^\\\\]+)', desc_raw)

        for text in text_matches:
            if '|' not in text or 'Organizer' not in text:
                continue
            em = event_line_re.search(text)
            if not em:
                continue

            name = em.group(1).strip()
            time_range = em.group(2).strip()
            neighborhood = em.group(3).strip()
            organizer = em.group(4).strip()
            location = em.group(5).strip()[:120]
            # Clean location: stop at ". Stay", ". Sign up", or just "Sign up"
            location = re.sub(r'\s*[\.\(]?\s*(?:Stay afterwards|Sign up|Email info).*$', '', location, flags=re.IGNORECASE).strip()
            location = location.rstrip('.,; ')[:100]

            events.append({
                "name": name,
                "date": event_date.isoformat(),
                "date_display": event_date.strftime("%a %b %-d"),
                "time": time_range,
                "neighborhood": neighborhood,
                "organizer": organizer,
                "location": location,
                "source": "Refuse Refuse SF",
                "signup_url": REFUSEREFUSE_URL,
            })

    return events


# ---------------------------------------------------------------------------
# DPW Love Our City scraper
# ---------------------------------------------------------------------------

DPW_NBD_URL = "https://sfpublicworks.org/LoveOurCity"

# District number → readable district name/location used in the NBD list
DISTRICT_NAMES = {
    1: "District 1", 2: "District 2", 3: "District 3", 4: "District 4",
    5: "District 5", 6: "District 6", 7: "District 7", 8: "District 8",
    9: "District 9", 10: "District 10", 11: "District 11",
}


def _parse_dpw_nbd(html, days_ahead=14):
    """
    Parse DPW Love Our City page for upcoming NBD events.
    Returns list of event dicts.
    """
    events = []
    today = date.today()
    cutoff = today + timedelta(days=days_ahead)
    current_year = today.year

    # Events are in an <ul> as <li> items like:
    # <strong>April 11</strong>: District 11 – Balboa Pool Grass Lawn (<a href="...">sign up here</a>)
    # Strikethrough (<s>) = past events

    # Find the "2026 events:" section
    year_match = re.search(r'20\d\d events:', html, re.IGNORECASE)
    if not year_match:
        return events
    section = html[year_match.start():]

    # Match each <li> — skip strikethrough ones (past events)
    # Non-strikethrough: <li ...><strong>Month Day</strong>: District N – Location (<a href="url">sign up here</a>)
    # Strikethrough: <li ...><s>...</s></li>
    li_re = re.compile(r'<li[^>]*>(.*?)</li>', re.DOTALL | re.IGNORECASE)
    date_re = re.compile(r'<strong[^>]*>([A-Za-z]+ \d{1,2})</strong>', re.IGNORECASE)
    district_re = re.compile(r'District\s+(\d{1,2})', re.IGNORECASE)
    location_re = re.compile(r'District\s+\d{1,2}\s*[–-]\s*(.+?)(?:\s*\(|$)', re.IGNORECASE)
    signup_re = re.compile(r'href="(https://www\.mobilize\.us/[^"]+)"', re.IGNORECASE)

    for li_match in li_re.finditer(section):
        li_content = li_match.group(1)

        # Skip past (strikethrough) events
        if re.search(r'<s>', li_content, re.IGNORECASE):
            continue

        date_m = date_re.search(li_content)
        if not date_m:
            continue

        try:
            event_date = datetime.strptime(f"{date_m.group(1)} {current_year}", "%B %d %Y").date()
            if event_date < today - timedelta(days=1):
                event_date = event_date.replace(year=current_year + 1)
        except ValueError:
            continue

        if event_date > cutoff:
            continue

        # Extract district number
        district_m = district_re.search(li_content)
        district_num = int(district_m.group(1)) if district_m else None

        # Extract location (text after "District N – ")
        location_m = location_re.search(li_content)
        raw_location = location_m.group(1).strip() if location_m else ""
        # Strip HTML tags
        location = re.sub(r'<[^>]+>', '', raw_location).strip()

        # Extract signup URL
        signup_m = signup_re.search(li_content)
        signup_url = signup_m.group(1) if signup_m else DPW_NBD_URL

        # Get neighborhood hint from location text
        neighborhood = f"District {district_num}" if district_num else "SF"

        events.append({
            "name": f"DPW Neighborhood Beautification Day",
            "date": event_date.isoformat(),
            "date_display": event_date.strftime("%a %b %-d"),
            "time": "8:30am–noon",
            "neighborhood": neighborhood,
            "organizer": "SF Public Works",
            "location": location,
            "district": district_num,
            "source": "DPW Love Our City",
            "signup_url": signup_url,
        })

    return events


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def _event_matches_district(event, district, neighborhoods):
    """Return True if event is relevant to the given district."""
    # DPW events have explicit district number
    if "district" in event and event["district"] is not None:
        return event["district"] == district

    # For Refuse Refuse, match on neighborhood keywords
    event_neighborhood = event.get("neighborhood", "").lower()
    event_name = event.get("name", "").lower()
    event_location = event.get("location", "").lower()
    combined = f"{event_neighborhood} {event_name} {event_location}"

    for kw in neighborhoods:
        if kw.lower() in combined:
            return True

    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def get_cleanups(district=5, days=14, all_sf=False):
    """Fetch and return upcoming cleanup events."""
    neighborhoods = _get_neighborhoods(district)

    # Fetch Refuse Refuse SF: get the HTML page to find the JS bundle URL,
    # then fetch the bundle which contains the full event dataset.
    rr_events = []
    rr_html = _fetch_url(REFUSEREFUSE_URL)
    if rr_html:
        bundle_url = _get_bundle_url(rr_html)
        if bundle_url:
            bundle_js = _fetch_url(bundle_url)
            if bundle_js:
                rr_events = _parse_refuse_refuse_bundle(bundle_js, days_ahead=days)
        if not rr_events:
            print("  ⚠️  Could not parse Refuse Refuse bundle, got 0 events", file=sys.stderr)

    # Fetch DPW Love Our City
    dpw_html = _fetch_url(DPW_NBD_URL)
    dpw_events = _parse_dpw_nbd(dpw_html, days_ahead=days) if dpw_html else []

    all_events = rr_events + dpw_events

    # Sort by date then time
    all_events.sort(key=lambda e: (e["date"], e.get("time", "")))

    if all_sf:
        return all_events

    # Filter to district
    relevant = [e for e in all_events if _event_matches_district(e, district, neighborhoods)]

    return relevant


def main():
    parser = argparse.ArgumentParser(description="SF volunteer cleanup event tracker")
    parser.add_argument("--district", type=int, default=_DISTRICT_CFG.get("district", 5))
    parser.add_argument("--days", type=int, default=14, help="Days ahead to look (default: 14)")
    parser.add_argument("--all", dest="all_sf", action="store_true",
                        help="Show all SF events regardless of district")
    parser.add_argument("--json", dest="json_out", action="store_true",
                        help="Output JSON")
    args = parser.parse_args()

    events = get_cleanups(district=args.district, days=args.days, all_sf=args.all_sf)

    # Archive events
    archive_records = []
    for e in events:
        archive_records.append({
            "id": f"{e.get('name','')}|{e.get('date','')}|{e.get('time','')}",
            "source": "sf_volunteer_cleanups",
            "name": e.get("name", ""),
            "date": e.get("date", ""),
            "time": e.get("time", ""),
            "neighborhood": e.get("neighborhood", ""),
            "organizer": e.get("organizer", ""),
            "location": e.get("location", ""),
            "event_source": e.get("source", ""),
            "signup_url": e.get("signup_url", ""),
        })
    update_archive(archive_records)

    if args.json_out:
        print(json.dumps(events, indent=2))
        return

    # Human-readable output
    if not events:
        label = "SF" if args.all_sf else f"D{args.district} / nearby neighborhoods"
        print(f"No upcoming cleanups found in next {args.days} days ({label}).")
        return

    label = "All SF" if args.all_sf else f"District {args.district}"
    print(f"🧹 Upcoming Cleanups — {label} — next {args.days} days\n")

    current_date = None
    for e in events:
        if e["date"] != current_date:
            current_date = e["date"]
            print(f"\n{e['date_display']}")

        print(f"  • {e['name']}")
        print(f"    {e['time']} | {e['neighborhood']}")
        if e.get("location"):
            print(f"    📍 Meet at: {e['location']}")
        if e.get("organizer") and e["organizer"] != "SF Public Works":
            print(f"    Organizer: {e['organizer']}")
        if e.get("signup_url") and e["signup_url"] != REFUSEREFUSE_URL:
            print(f"    🔗 {e['signup_url']}")
        else:
            print(f"    🔗 refuserefusesf.org/cleanups")


if __name__ == "__main__":
    main()
