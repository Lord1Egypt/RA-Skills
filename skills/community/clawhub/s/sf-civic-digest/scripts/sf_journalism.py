#!/usr/bin/env python3
"""
SF Journalism Aggregator — unified multi-outlet RSS monitor.
Fetches RSS from 6 SF news outlets, deduplicates across outlets,
and outputs all articles as structured data for agent consumption.

Relevance ranking is NOT done here — the calling agent applies editorial
judgment to the raw article list.

Usage:
  python3 sf_journalism.py                   # all recent stories (JSON)
  python3 sf_journalism.py --json            # explicit JSON output
  python3 sf_journalism.py --daily           # only new since last check
  python3 sf_journalism.py --days 7          # limit to last N days
  python3 sf_journalism.py --district 9      # tag articles district/citywide
  python3 sf_journalism.py --outlet yimby    # single outlet only
  python3 sf_journalism.py --archive         # include archived articles
"""

import sys
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from email.utils import parsedate_to_datetime
from html import unescape

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCRIPTS_DIR, "sf_journalism_state.json")
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sf_journalism_archive.json")
ARCHIVE_MAX = 2000  # ~6 months at current volume

# ---------------------------------------------------------------------------
# Outlet definitions
# ---------------------------------------------------------------------------

OUTLETS = {
    "mission_local": {
        "name": "Mission Local",
        "url": "https://missionlocal.org/feed/",
    },
    "sf_standard": {
        "name": "SF Standard",
        "url": "https://sfstandard.com/feed/",
    },
    "sf_examiner": {
        "name": "SF Examiner",
        "url": "https://sfexaminer.com/feed/",
    },
    "48_hills": {
        "name": "48 Hills",
        "url": "https://48hills.org/feed/",
    },
    "streetsblog": {
        "name": "Streetsblog SF",
        "url": "https://sf.streetsblog.org/feed/",
    },
    "sfyimby": {
        "name": "SF YIMBY",
        "url": "https://sfyimby.com/feed/",
    },
}

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
    return {"outlets": {}, "last_check": None}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# Article archive
# ---------------------------------------------------------------------------

def load_archive():
    if os.path.exists(ARCHIVE_FILE):
        try:
            with open(ARCHIVE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"articles": []}


def save_archive(archive):
    with open(ARCHIVE_FILE, "w") as f:
        json.dump(archive, f, indent=2)


def update_archive(new_articles):
    """Merge new articles into the archive. Dedup by GUID. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_guids = {a["guid"] for a in archive["articles"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for article in new_articles:
        if article["guid"] not in existing_guids:
            entry = {
                "title": article["title"],
                "link": article["link"],
                "guid": article["guid"],
                "pub_date": article["pub_date"],
                "description": article.get("description", ""),
                "categories": article.get("categories", []),
                "author": article.get("author", ""),
                "outlet_key": article.get("outlet_key", ""),
                "outlet_name": article.get("outlet_name", ""),
                "first_seen": now,
            }
            archive["articles"].append(entry)
            existing_guids.add(article["guid"])
            added += 1
    # Cap: keep most recent by first_seen
    if len(archive["articles"]) > ARCHIVE_MAX:
        archive["articles"] = archive["articles"][-ARCHIVE_MAX:]
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new articles ({len(archive['articles'])} total)", file=sys.stderr)
    return archive


# ---------------------------------------------------------------------------
# Fetching & parsing
# ---------------------------------------------------------------------------

def fetch_rss(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")


def parse_feed(xml_text, outlet_key):
    outlet = OUTLETS[outlet_key]
    root = ET.fromstring(xml_text)
    items = []
    for item in root.findall(".//item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        guid = item.findtext("guid", link).strip()
        pub_date = item.findtext("pubDate", "").strip()
        desc_raw = item.findtext("description", "")
        description = unescape(re.sub(r"<[^>]+>", " ", desc_raw)).strip()
        categories = [c.text.strip().lower() for c in item.findall("category") if c.text]
        author_el = item.find("{http://purl.org/dc/elements/1.1/}creator")
        author = author_el.text.strip() if author_el is not None and author_el.text else ""

        items.append({
            "title": title,
            "link": link,
            "guid": guid,
            "pub_date": pub_date,
            "description": description[:300],
            "categories": categories,
            "author": author,
            "outlet_key": outlet_key,
            "outlet_name": outlet["name"],
        })
    return items


def fetch_outlet(outlet_key):
    """Fetch and parse one outlet. Returns (outlet_key, items, error)."""
    url = OUTLETS[outlet_key]["url"]
    try:
        xml_text = fetch_rss(url)
        items = parse_feed(xml_text, outlet_key)
        return outlet_key, items, None
    except Exception as e:
        return outlet_key, [], str(e)


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def normalize_url(url):
    """Strip query params and trailing slashes for URL comparison."""
    url = re.sub(r"\?.*$", "", url)
    return url.rstrip("/").lower()


def titles_similar(a, b, threshold=0.7):
    """Return True if two titles are similar enough to be the same story."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold


def deduplicate(items):
    """Merge items that are the same story from different outlets.
    Returns list of merged items; each has 'outlets' list and 'outlet_links'."""
    merged = []
    for item in items:
        norm_link = normalize_url(item["link"])
        found = False
        for existing in merged:
            if normalize_url(existing["link"]) == norm_link or \
               titles_similar(existing["title"], item["title"]):
                existing["outlets"].append(item["outlet_name"])
                existing["outlet_links"].append(item["link"])
                # Keep the version with the longer description
                if len(item.get("description", "")) > len(existing.get("description", "")):
                    existing["title"] = item["title"]
                    existing["link"] = item["link"]
                    existing["description"] = item["description"]
                    existing["pub_date"] = item["pub_date"]
                found = True
                break
        if not found:
            item["outlets"] = [item["outlet_name"]]
            item["outlet_links"] = [item["link"]]
            merged.append(item)
    return merged


# ---------------------------------------------------------------------------
# District scope tagging
# ---------------------------------------------------------------------------

def _build_district_keywords(district):
    """Build keyword list for a district from config_loader."""
    try:
        from config_loader import get_district_config
        cfg = get_district_config(district=district)
    except ImportError:
        cfg = {"district": district, "neighborhoods": [], "streets": [],
               "key_addresses": [], "key_people": []}
    kw = [f"district {district}", f"d{district}"]
    kw.extend(n.lower() for n in cfg.get("neighborhoods", []))
    kw.extend(s.lower() for s in cfg.get("streets", []))
    kw.extend(a.lower() for a in cfg.get("key_addresses", []))
    kw.extend(p.lower() for p in cfg.get("key_people", []))
    return kw


def tag_scope(articles, district):
    """Tag each article as 'district' or 'citywide' based on district keywords."""
    district_kw = _build_district_keywords(district)
    for article in articles:
        haystack = " ".join([
            article["title"].lower(),
            article.get("description", "").lower(),
            " ".join(article.get("categories", [])),
        ])
        article["scope"] = "district" if any(kw in haystack for kw in district_kw) else "citywide"
    return articles


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def parse_pub_date(date_str):
    """Parse RSS pubDate to datetime. Returns None on failure."""
    try:
        return parsedate_to_datetime(date_str)
    except Exception:
        return None


def filter_by_days(items, days):
    """Keep only articles published within the last N days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    filtered = []
    for i in items:
        pub = parse_pub_date(i["pub_date"])
        if pub is None or pub >= cutoff:
            filtered.append(i)
    return filtered


# ---------------------------------------------------------------------------
# Output formatting (text mode)
# ---------------------------------------------------------------------------

def format_item(item):
    outlets_str = " + ".join(item.get("outlets", [item["outlet_name"]]))
    scope_tag = f" [{item['scope']}]" if "scope" in item else ""

    lines = [f"📰 [{outlets_str}]{scope_tag} {item['title']}"]
    if item["description"]:
        lines.append(f"  {item['description'][:200]}")
    meta = []
    for link in item.get("outlet_links", [item["link"]]):
        m = re.match(r"https?://([^/]+)", link)
        if m:
            meta.append(m.group(1))
    if item["pub_date"]:
        meta.append(item["pub_date"][:16])
    if meta:
        lines.append(f"  [{' | '.join(dict.fromkeys(meta))}]")
    lines.append(f"  {item['link']}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    daily_mode = "--daily" in sys.argv
    json_mode = "--json" in sys.argv
    archive_mode = "--archive" in sys.argv

    # --outlet filter
    outlet_filter = None
    if "--outlet" in sys.argv:
        idx = sys.argv.index("--outlet")
        if idx + 1 < len(sys.argv):
            outlet_filter = sys.argv[idx + 1].lower()

    # --days filter
    days_filter = None
    if "--days" in sys.argv:
        idx = sys.argv.index("--days")
        if idx + 1 < len(sys.argv):
            try:
                days_filter = int(sys.argv[idx + 1])
            except ValueError:
                pass

    # --district (for scope tagging)
    district = None
    if "--district" in sys.argv:
        idx = sys.argv.index("--district")
        if idx + 1 < len(sys.argv):
            try:
                district = int(sys.argv[idx + 1])
            except ValueError:
                pass

    state = load_state()
    errors = []

    # Determine which outlets to fetch
    if outlet_filter:
        keys = [k for k in OUTLETS if outlet_filter in k or
                outlet_filter in OUTLETS[k]["name"].lower()]
        if not keys:
            print(f"Unknown outlet: {outlet_filter}", file=sys.stderr)
            print(f"Available: {', '.join(OUTLETS.keys())}", file=sys.stderr)
            sys.exit(1)
    else:
        keys = list(OUTLETS.keys())

    # Fetch all feeds concurrently
    all_items = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fetch_outlet, k): k for k in keys}
        for future in as_completed(futures):
            outlet_key, items, error = future.result()
            if error:
                errors.append(f"{OUTLETS[outlet_key]['name']}: {error}")
            else:
                all_items.extend(items)

    # Archive new articles (always, before any filtering)
    update_archive(all_items)

    # In archive mode, load from archive instead of just RSS
    if archive_mode:
        archive = load_archive()
        # Merge archive articles (dedup with RSS by GUID)
        rss_guids = {i["guid"] for i in all_items}
        for archived in archive["articles"]:
            if archived["guid"] not in rss_guids:
                all_items.append(archived)

    # Filter by days
    if days_filter:
        all_items = filter_by_days(all_items, days_filter)

    # Daily mode: filter to unseen GUIDs
    if daily_mode:
        seen = set()
        for outlet_state in state.get("outlets", {}).values():
            seen.update(outlet_state.get("seen_guids", []))
        all_items = [i for i in all_items if i["guid"] not in seen]

    # Sort by pub_date descending
    def _sort_key(item):
        pub = parse_pub_date(item.get("pub_date", ""))
        return pub or datetime.min.replace(tzinfo=timezone.utc)
    all_items.sort(key=_sort_key, reverse=True)

    # Deduplicate
    results = deduplicate(all_items)

    # Tag scope if district specified
    if district is not None:
        tag_scope(results, district)

    # Update state — track all GUIDs per outlet
    for item in all_items:
        okey = item.get("outlet_key", "")
        if not okey:
            continue
        if okey not in state.get("outlets", {}):
            state.setdefault("outlets", {})[okey] = {"seen_guids": []}
        outlet_state = state["outlets"][okey]
        guids = set(outlet_state.get("seen_guids", []))
        guids.add(item["guid"])
        outlet_state["seen_guids"] = list(guids)[-300:]
    state["last_check"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    # Print errors
    for err in errors:
        print(f"[WARN] Feed error — {err}", file=sys.stderr)

    # Output
    if json_mode:
        print(json.dumps(results, indent=2))
        return

    if not results:
        label = "new " if daily_mode else ""
        print(f"SF Journalism: no {label}stories found.")
        return

    label = "new " if daily_mode else ""
    print(f"=== SF Journalism — {len(results)} {label}stories ===\n")
    for item in results:
        print(format_item(item))
        print()


if __name__ == "__main__":
    main()
