#!/usr/bin/env python3
"""
SF Civic Digest — configurable SF Board of Supervisors tracker.
Fetches meetings from Legistar, filters by district/neighborhood/topic.

Usage:
  python3 sf_civic_digest.py                     # weekly digest (upcoming + recap)
  python3 sf_civic_digest.py --daily             # delta: new since last check
  python3 sf_civic_digest.py --days 14           # look ahead N days (weekly mode)
  python3 sf_civic_digest.py --config path.json  # use custom config file
  python3 sf_civic_digest.py --json              # JSON output

District data comes from config_loader.py. Pass --district N to filter.
  All flags optional. Omit --district to get all SF meetings unfiltered.
"""

import sys
import re
import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone
from html import unescape

LEGISTAR_CALENDAR = "https://sfgov.legistar.com/Calendar.aspx"
LEGISTAR_BASE = "https://sfgov.legistar.com"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "civic_config.json")  # optional user override, not shipped
DEFAULT_STATE_FILE = os.path.join(SCRIPT_DIR, "sf_civic_state.json")
ARCHIVE_FILE = os.path.join(SCRIPT_DIR, "sf_civic_digest_archive.json")
ARCHIVE_MAX = 5000

# District → supervisor + default neighborhoods
DISTRICT_MAP = {
    1: {"supervisor": "Connie Chan", "neighborhoods": ["Richmond", "Inner Richmond", "Outer Richmond", "Sea Cliff", "Jordan Park"]},
    2: {"supervisor": "Stephen Sherrill", "neighborhoods": ["Marina", "Cow Hollow", "Pacific Heights", "Presidio Heights"]},
    3: {"supervisor": "Danny Sauter", "neighborhoods": ["North Beach", "Chinatown", "Telegraph Hill", "Russian Hill", "Fisherman's Wharf"]},
    4: {"supervisor": "Alan Wong", "neighborhoods": ["Sunset", "Inner Sunset", "Outer Sunset", "Parkside"]},
    5: {"supervisor": "Bilal Mahmood", "neighborhoods": ["NOPA", "North of Panhandle", "Western Addition", "Haight", "Hayes Valley", "Lower Haight", "Alamo Square", "Cole Valley", "Duboce"]},
    6: {"supervisor": "Matt Dorsey", "neighborhoods": ["SoMa", "South of Market", "Tenderloin", "Civic Center", "Mid-Market"]},
    7: {"supervisor": "Myrna Melgar", "neighborhoods": ["West Portal", "Forest Hill", "Twin Peaks", "Diamond Heights", "Glen Park", "Miraloma Park"]},
    8: {"supervisor": "Rafael Mandelman", "neighborhoods": ["Castro", "Noe Valley", "Corona Heights", "Eureka Valley", "Duboce Triangle"]},
    9: {"supervisor": "Jackie Fielder", "neighborhoods": ["Mission", "Bernal Heights", "Portola"]},
    10: {"supervisor": "Shamann Walton", "neighborhoods": ["Bayview", "Hunters Point", "Visitacion Valley", "Excelsior", "Crocker Amazon"]},
    11: {"supervisor": "Chyanne Chen", "neighborhoods": ["Excelsior", "Ingleside", "Oceanview", "Outer Mission"]},
}

# Always-relevant civic topics (city-wide significance)
CITYWIDE_TOPICS = [
    "planning code", "zoning map", "special use district",
    "affordable housing", "accessory dwelling", "density bonus",
    "landmark designation", "historic preservation",
    "shelter", "navigation center", "encampment",
    "rent board", "eviction", "tenant protection",
    "police code", "surveillance technology",
    "building permit", "conditional use", "variance",
    "land use", "sidewalk permit",
]

PRIORITY_BODIES = [
    "land use and transportation",
    "public safety and neighborhood services",
    "board of supervisors",
    "planning commission",
]


def load_config(config_path=None):
    """Load user config. Returns empty dict if no config file found."""
    path = config_path or DEFAULT_CONFIG_FILE
    if path and os.path.exists(path):
        with open(path) as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def build_keywords(config):
    """Build keyword list from config + defaults."""
    keywords = list(CITYWIDE_TOPICS)

    district = config.get("district")
    if district and district in DISTRICT_MAP:
        for n in DISTRICT_MAP[district]["neighborhoods"]:
            keywords.append(n.lower())

    for n in config.get("neighborhoods", []):
        keywords.append(n.lower())

    for s in config.get("streets", []):
        keywords.append(s.lower())

    for t in config.get("topics", []):
        keywords.append(t.lower())

    return list(set(keywords))


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={
        "User-Agent": "sf-civic-digest/1.0",
        "Accept": "text/html,*/*"
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def clean_html(html):
    text = re.sub(r'<[^>]+>', ' ', html)
    text = unescape(text)
    return re.sub(r'\s+', ' ', text).strip()


def is_relevant(text, keywords):
    t = text.lower()
    return any(kw in t for kw in keywords)


def is_priority_body(name):
    n = name.lower()
    return any(p in n for p in PRIORITY_BODIES)


def load_state(state_file):
    if os.path.exists(state_file):
        try:
            with open(state_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print(f"Warning: corrupt state file {state_file}, resetting.", file=sys.stderr)
    return {"seen_meetings": {}, "last_weekly": None, "last_daily": None}


def save_state(state, state_file):
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# Meeting archive
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


def update_archive(meeting_results):
    """Merge new meetings into the archive. Dedup by meeting ID. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_ids = {m["id"] for m in archive["items"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for m in meeting_results:
        mid = m.get("meeting_id")
        if mid and mid not in existing_ids:
            entry = {
                "id": mid,
                "source": "sf_civic_digest",
                "scraped_at": now,
                "body": m["body"],
                "date": m["date"],
                "time": m["time"],
                "url": m["url"],
                "items": [i["text"] for i in m.get("tagged_items", [])],
                "actions": m.get("actions", {}),
            }
            archive["items"].append(entry)
            existing_ids.add(mid)
            added += 1
    # Cap: keep most recent
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new meetings ({len(archive['items'])} total)", file=sys.stderr)
    return archive


def parse_meeting_ids(html):
    raw_urls = re.findall(r'href="(MeetingDetail\.aspx\?ID=\d+[^"]*)"', html)
    meetings = []
    seen = set()
    for url_path in raw_urls:
        url_path = url_path.replace("&amp;", "&")
        id_match = re.search(r'ID=(\d+)', url_path)
        if not id_match:
            continue
        mid = id_match.group(1)
        if mid in seen:
            continue
        seen.add(mid)
        meetings.append({"id": mid, "url": LEGISTAR_BASE + "/" + url_path})
    return meetings


def fetch_meeting_detail(url):
    html = fetch(url)

    title_match = re.search(
        r'Meeting of (.+?) on (\d{1,2}/\d{1,2}/\d{4}) at (\d{1,2}:\d{2} [AP]M)', html)
    if title_match:
        body = title_match.group(1).strip()
        date_str = title_match.group(2)
        time_str = title_match.group(3)
    else:
        body = ""
        dt = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', html)
        tm = re.search(r'(\d{1,2}:\d{2} [AP]M)', html)
        date_str = dt.group(1) if dt else ""
        time_str = tm.group(1) if tm else ""

    cells = re.findall(r'<td[^>]*>(.*?)</td>', html, re.DOTALL)
    items = []
    seen_texts = set()
    ITEM_STARTERS = (
        'Ordinance', 'Resolution', 'Motion', 'Hearing', 'Planning',
        'Administrative', 'Public', 'Health', 'Police', 'Business',
        'Street', 'Real', 'Project', 'Commemorative', 'Budget',
    )
    for cell in cells:
        text = clean_html(cell)
        if 30 < len(text) < 500:
            first_word = text.split()[0] if text.split() else ""
            if first_word in ITEM_STARTERS and text not in seen_texts:
                seen_texts.add(text)
                items.append(text)

    items_sorted = sorted(items, key=len, reverse=True)
    deduped = []
    for item in items_sorted:
        if not any(item in longer for longer in deduped):
            deduped.append(item)

    actions = {}
    action_rows = re.findall(
        r'(Passed|Failed|Continued|Tabled|Amended|Approved|Adopted|Disapproved)', html)
    if action_rows:
        actions["summary"] = list(set(action_rows))

    parsed_date = None
    if date_str:
        try:
            parsed_date = datetime.strptime(date_str, "%m/%d/%Y").date()
        except ValueError:
            pass

    return {
        "body": body,
        "date": date_str,
        "time": time_str,
        "parsed_date": parsed_date,
        "url": url,
        "items": deduped,
        "actions": actions,
    }


def get_meetings_in_range(start, end, state, keywords, mode="weekly"):
    cal_html = fetch(LEGISTAR_CALENDAR)
    stubs = parse_meeting_ids(cal_html)

    results = []
    new_state = dict(state["seen_meetings"])

    for stub in stubs:
        mid = stub["id"]
        try:
            detail = fetch_meeting_detail(stub["url"])
        except Exception as e:
            print(f"  Error fetching {stub['url']}: {e}", file=sys.stderr)
            continue

        d = detail.get("parsed_date")
        if not d or not (start <= d <= end):
            continue

        if mode == "daily":
            prev = state["seen_meetings"].get(mid, {})
            is_new = mid not in state["seen_meetings"]
            agenda_updated = len(detail["items"]) > prev.get("item_count", 0)
            if not is_new and not agenda_updated:
                continue

        new_state[mid] = {
            "body": detail["body"],
            "date": detail["date"],
            "item_count": len(detail["items"]),
            "last_seen": datetime.now().isoformat()
        }

        body_relevant = is_priority_body(detail["body"])
        tagged_items = [
            {"text": item, "relevant": is_relevant(item, keywords)}
            for item in detail["items"]
        ]
        content_relevant = any(i["relevant"] for i in tagged_items)

        if not body_relevant and not content_relevant:
            continue

        results.append({
            "meeting_id": mid,
            "body": detail["body"],
            "date": detail["date"],
            "time": detail["time"],
            "parsed_date": d,
            "url": detail["url"],
            "tagged_items": tagged_items,
            "priority_body": body_relevant,
            "actions": detail.get("actions", {}),
            "is_past": d < datetime.now().date(),
        })

    state["seen_meetings"] = new_state
    results.sort(key=lambda x: x["parsed_date"])
    return results


def format_weekly(upcoming, recap, today, config):
    district = config.get("district")
    label = f"District {district}" if district else "SF"
    supervisor = DISTRICT_MAP.get(district, {}).get("supervisor", "")

    lines = [f"🏛️  SF CIVIC DIGEST — {label} — Week of {today.strftime('%B %d, %Y')}"]
    if supervisor:
        lines.append(f"   Supervisor: {supervisor}")
    lines.append("")

    if recap:
        lines.append("📰 LAST WEEK'S RECAP")
        lines.append("─" * 50)
        for m in recap:
            rel_items = [i for i in m["tagged_items"] if i["relevant"]]
            actions = m.get("actions", {}).get("summary", [])
            lines.append(f"  {m['body']} ({m['date']})")
            if actions:
                lines.append(f"    Actions taken: {', '.join(actions)}")
            for item in rel_items[:3]:
                text = item["text"][:120] + ("..." if len(item["text"]) > 120 else "")
                lines.append(f"    • {text}")
            if not rel_items:
                lines.append("    (no items matching your filters)")
            lines.append("")

    if upcoming:
        lines.append("📅 THIS WEEK AHEAD")
        lines.append("─" * 50)
        for m in upcoming:
            rel_items = [i for i in m["tagged_items"] if i["relevant"]]
            icon = "⭐" if rel_items else "📋"
            lines.append(f"  {icon} {m['body']}")
            lines.append(f"     {m['date']} at {m['time']}")
            for item in rel_items[:5]:
                text = item["text"][:130] + ("..." if len(item["text"]) > 130 else "")
                lines.append(f"     • {text}")
            if not rel_items:
                lines.append("     (agenda not yet published or no matching items)")
            lines.append(f"     🔗 {m['url']}")
            lines.append("")
    else:
        lines.append("No relevant meetings this week.")

    return "\n".join(lines)


def format_daily(new_meetings):
    if not new_meetings:
        return None

    lines = ["🏛️ SF Civic Update"]
    for m in new_meetings:
        rel_items = [i for i in m["tagged_items"] if i["relevant"]]
        if rel_items:
            lines.append(f"\n⭐ New agenda: {m['body']} ({m['date']} {m['time']})")
            for item in rel_items[:3]:
                text = item["text"][:120] + ("..." if len(item["text"]) > 120 else "")
                lines.append(f"  • {text}")
            lines.append(f"  🔗 {m['url']}")
        elif m["priority_body"]:
            lines.append(f"\n📋 Agenda published: {m['body']} ({m['date']} {m['time']})")
            lines.append(f"  🔗 {m['url']}")

    return "\n".join(lines) if len(lines) > 1 else None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SF Civic Digest — Board of Supervisors tracker")
    parser.add_argument("--daily", action="store_true", help="Delta mode: new since last check")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--days", type=int, default=7, help="Look-ahead window in days")
    parser.add_argument("--district", type=int, help="Supervisorial district (1-11)")
    parser.add_argument("--config", help="Path to config JSON file")
    args = parser.parse_args()

    daily_mode = args.daily
    as_json = args.json
    days = args.days
    config_path = args.config

    config = load_config(config_path)
    # --district flag overrides config file
    if args.district is not None:
        from config_loader import get_district_config as _get_dc
        dc = _get_dc(args.district)
        config["district"] = dc.get("district")
        config["neighborhoods"] = dc.get("neighborhoods", [])
        config["streets"] = dc.get("streets", [])
    keywords = build_keywords(config)
    state_file = config.get("state_file", DEFAULT_STATE_FILE)
    if not os.path.isabs(state_file):
        state_file = os.path.join(SCRIPT_DIR, state_file)
    state = load_state(state_file)

    today = datetime.now().date()

    if daily_mode:
        print("Daily delta check...", file=sys.stderr)
        new_meetings = get_meetings_in_range(
            today, today + timedelta(days=7), state, keywords, mode="daily")
        update_archive(new_meetings)
        state["last_daily"] = today.isoformat()
        save_state(state, state_file)

        output = format_daily(new_meetings)
        if output:
            print(output)
        else:
            print("No new civic updates since last check.")
    else:
        ahead_end = today + timedelta(days=days)
        recap_start = today - timedelta(days=7)

        print(f"Fetching upcoming meetings ({today}→{ahead_end})...", file=sys.stderr)
        upcoming = get_meetings_in_range(today, ahead_end, state, keywords, mode="weekly")

        print(f"Fetching last week recap ({recap_start}→{today})...", file=sys.stderr)
        recap = get_meetings_in_range(recap_start, today - timedelta(days=1), state, keywords, mode="weekly")
        recap = [m for m in recap if m["is_past"]]

        update_archive(upcoming + recap)
        state["last_weekly"] = today.isoformat()
        save_state(state, state_file)

        if as_json:
            print(json.dumps({
                "upcoming": [{
                    "body": m["body"], "date": m["date"], "time": m["time"],
                    "url": m["url"],
                    "relevant_items": [i["text"] for i in m["tagged_items"] if i["relevant"]],
                } for m in upcoming],
                "recap": [{
                    "body": m["body"], "date": m["date"],
                    "relevant_items": [i["text"] for i in m["tagged_items"] if i["relevant"]],
                    "actions": m.get("actions", {}),
                } for m in recap],
            }, indent=2))
        else:
            print(format_weekly(upcoming, recap, today, config))


if __name__ == "__main__":
    main()
