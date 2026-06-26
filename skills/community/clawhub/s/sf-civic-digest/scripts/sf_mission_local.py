#!/usr/bin/env python3
"""
Mission Local news monitor.  **DEPRECATED — use sf_journalism.py instead.**

sf_journalism.py is the unified journalism aggregator covering Mission Local
and 4 other outlets, with --outlet and --topic filtering and cross-outlet dedup.
This script is kept for backwards compatibility but receives no further updates.

Usage (prefer sf_journalism.py --outlet missionlocal):
  python3 sf_mission_local.py           # all recent stories (last 30 items)
  python3 sf_mission_local.py --daily   # only new since last check
  python3 sf_mission_local.py --json    # JSON output
"""

import sys
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape

RSS_URL = "https://missionlocal.org/feed/"
STATE_FILE = os.path.join(os.path.dirname(__file__), "sf_mission_local_state.json")

# Keywords that make a story relevant — D5 geography, civic topics, key players
RELEVANCE_KEYWORDS = [
    # D5 neighborhoods/streets
    "district 5", "d5", "nopa", "north of panhandle", "western addition",
    "haight", "divisadero", "hayes valley", "lower haight", "alamo square",
    "duboce", "cole valley", "panhandle", "fillmore", "masonic",
    # Key addresses / projects
    "400 divisadero", "divisadero corridor",
    # Key people
    "mahmood", "supervisor mahmood", "dean preston",
    # Civic bodies
    "board of supervisors", "planning commission", "sfmta", "mta board",
    "board of appeals", "rent board", "historic preservation",
    "zoning administrator", "rec and park", "rec & park",
    # Housing/development
    "housing", "affordable housing", "density bonus", "ab 2011", "sb 35",
    "accessory dwelling", "adu", "upzoning", "zoning", "development",
    "landmark", "historic", "demolition", "building permit",
    "yimby", "nimby", "tenants union", "eviction", "ellis act",
    "rent control", "displacement",
    # Transit (sgillen is car-free)
    "muni", "bus line", "bike lane", "protected lane", "transit",
    "bart", "caltrain", "bike", "pedestrian", "crosswalk", "vision zero",
    # Citywide civic/political
    "city hall", "mayor lurie", "lurie", "board of education", "sfusd",
    "police commission", "dpw", "public works",
    "proposition", "ballot measure", "legislation", "ordinance",
    "budget", "city budget", "department of",
    # Crime/public safety (neighborhood signal)
    "shooting", "homicide", "robbery", "vandalism",
]

# Categories from Mission Local that are broadly civic-relevant
CIVIC_CATEGORIES = {
    "housing", "planning", "politics", "sfmta", "transportation",
    "board of supervisors", "development", "crime", "education",
    "public safety", "environment", "budget", "elections",
    "election coverage", "real estate",
}

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"seen_guids": [], "last_check": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def fetch_rss():
    req = urllib.request.Request(RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8")

def parse_feed(xml_text):
    root = ET.fromstring(xml_text)
    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    items = []
    for item in root.findall(".//item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        guid = item.findtext("guid", link).strip()
        pub_date = item.findtext("pubDate", "").strip()
        description = unescape(re.sub(r"<[^>]+>", " ", item.findtext("description", ""))).strip()
        categories = [c.text.strip().lower() for c in item.findall("category") if c.text]
        author_el = item.find("{http://purl.org/dc/elements/1.1/}creator")
        author = author_el.text.strip() if author_el is not None else ""

        items.append({
            "title": title,
            "link": link,
            "guid": guid,
            "pub_date": pub_date,
            "description": description[:300],
            "categories": categories,
            "author": author,
        })
    return items

def is_relevant(item):
    """Return True if a story is civic/D5-relevant."""
    haystack = " ".join([
        item["title"].lower(),
        item["description"].lower(),
        " ".join(item["categories"]),
    ])
    # Check keyword match
    for kw in RELEVANCE_KEYWORDS:
        if kw in haystack:
            return True
    # Check civic category
    for cat in item["categories"]:
        if cat in CIVIC_CATEGORIES:
            return True
    return False

def score_item(item):
    """Higher score = more relevant. Used to sort output."""
    haystack = " ".join([
        item["title"].lower(),
        item["description"].lower(),
        " ".join(item["categories"]),
    ])
    score = 0
    # D5/local geography = highest weight
    for geo in ["divisadero", "nopa", "haight", "western addition", "hayes valley", "alamo square", "fillmore", "mahmood"]:
        if geo in haystack:
            score += 3
    # Housing/planning = high weight
    for topic in ["housing", "planning", "zoning", "development", "affordable", "eviction", "landmark"]:
        if topic in haystack:
            score += 2
    # Transit = medium
    for topic in ["muni", "bike", "transit", "sfmta", "pedestrian"]:
        if topic in haystack:
            score += 1
    # General civic
    for topic in ["board of supervisors", "city hall", "budget", "lurie"]:
        if topic in haystack:
            score += 1
    return score

def format_item(item):
    cats = ", ".join(item["categories"][:3]) if item["categories"] else ""
    lines = [f"• {item['title']}"]
    if item["description"]:
        lines.append(f"  {item['description'][:200]}")
    meta = []
    if item["author"]:
        meta.append(item["author"])
    if cats:
        meta.append(cats)
    if item["pub_date"]:
        meta.append(item["pub_date"][:16])
    if meta:
        lines.append(f"  [{' | '.join(meta)}]")
    lines.append(f"  {item['link']}")
    return "\n".join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Mission Local news scraper")
    parser.add_argument("--daily", action="store_true", help="Only show new items since last run")
    parser.add_argument("--json", action="store_true", dest="json_mode", help="JSON output")
    parser.add_argument("--district", type=int, help="Supervisorial district (1-11, informational only)")
    args = parser.parse_args()

    daily_mode = args.daily
    json_mode = args.json_mode

    state = load_state()
    seen_guids = set(state.get("seen_guids", []))

    try:
        xml_text = fetch_rss()
    except Exception as e:
        print(f"Error fetching Mission Local RSS: {e}", file=sys.stderr)
        sys.exit(1)

    items = parse_feed(xml_text)

    # Filter relevant
    relevant = [i for i in items if is_relevant(i)]

    # In daily mode, only show unseen items
    if daily_mode:
        new_items = [i for i in relevant if i["guid"] not in seen_guids]
    else:
        new_items = relevant

    # Sort by relevance score descending
    new_items.sort(key=score_item, reverse=True)

    # Update state
    all_guids = [i["guid"] for i in items]
    state["seen_guids"] = list(seen_guids | set(all_guids))[-200:]  # cap at 200
    state["last_check"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    if json_mode:
        print(json.dumps(new_items, indent=2))
        return

    if not new_items:
        if daily_mode:
            print("Mission Local: no new relevant stories since last check.")
        else:
            print("Mission Local: no relevant stories found.")
        return

    label = "new " if daily_mode else ""
    print(f"=== Mission Local — {len(new_items)} {label}relevant stories ===\n")
    for item in new_items:
        print(format_item(item))
        print()

if __name__ == "__main__":
    main()
