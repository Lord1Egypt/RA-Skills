#!/usr/bin/env python3
"""
SF Ethics Commission scraper.

Surfaces:
  - Recent public notices (enforcement, press releases, agendas, audits)
  - Lobbyist contacts with the district supervisor or Board President (Peskin)
  - Lobbyist campaign contributions (recent)
  - Cross-reference flags for any ethics notice mentioning tracked projects

Data sources:
  - sfethics.org WordPress RSS feeds (public notices, press releases, audits)
  - data.sfgov.org Socrata API:
      5f5n-tdbf  Contact Lobbyist Activity — Contact of Public Official
      e6py-fg8b  Lobbyist Activity — Campaign Contributions Made
      vckx-s5ks  Lobbyist Filings Directory
      s4ub-8j3t  Lobbyist Activity Directory (payments received)

Usage:
  python3 sf_ethics.py                    # recent notices + D5 relevant (30-day window)
  python3 sf_ethics.py --supervisor 5     # filter lobbyist contacts to D5 only
  python3 sf_ethics.py --days 30          # look back N days (default 30)
  python3 sf_ethics.py --json             # JSON output
  python3 sf_ethics.py --all-supervisors  # show contacts across all supervisors
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
import urllib.request
import urllib.error
from xml.etree import ElementTree as ET
from urllib.parse import urlencode, quote

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# ── Socrata dataset IDs (all on data.sfgov.org) ──────────────────────────────
SOCRATA_BASE = "https://data.sfgov.org/resource"
DS_LOBBYIST_CONTACTS   = "5f5n-tdbf"   # Contact Lobbyist Activity — Contact of Public Official
DS_LOBBYIST_CONTRIB    = "e6py-fg8b"   # Lobbyist Activity — Campaign Contributions
DS_LOBBYIST_FILINGS    = "vckx-s5ks"   # Lobbyist Filings Directory
DS_LOBBYIST_ACTIVITY   = "s4ub-8j3t"   # Lobbyist Activity Directory (payments)

# ── RSS feeds ─────────────────────────────────────────────────────────────────
RSS_FEEDS = {
    "public-notices":  "https://sfethics.org/ethics/category/public-notices/feed",
    "press-releases":  "https://sfethics.org/ethics/category/press-releases/feed",
    "audits":          "https://sfethics.org/ethics/category/audits/feed",
    "news":            "https://sfethics.org/feed",  # main feed = broadest coverage
}

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sf_ethics_archive.json")
ARCHIVE_MAX = 5000

# ── Load district config ─────────────────────────────────────────────────────
try:
    from config_loader import get_district_config as _get_district_config
    _DISTRICT_CFG = _get_district_config()
except ImportError:
    _DISTRICT_CFG = {"district": None, "supervisor_name": "", "neighborhoods": [], "streets": [], "key_people": []}

# ── Supervisor names for filtering ────────────────────────────────────────────
SUPERVISOR_NAMES = {
    1: ["CHAN", "Connie"],
    2: ["SHERRILL", "Stephen"],
    3: ["SAUTER", "Danny"],
    4: ["WONG", "Alan"],
    5: ["MAHMOOD", "Bilal"],
    6: ["DORSEY", "Matt"],
    7: ["MELGAR", "Myrna"],
    8: ["MANDELMAN", "Rafael"],
    9: ["FIELDER", "Jackie"],
    10: ["WALTON", "Shamann"],
    11: ["CHEN", "Chyanne"],
}
# Board President as of Jan 2026: Aaron Peskin
BOARD_PRESIDENT = "Peskin"
BOARD_PRESIDENT_NAMES = ["PESKIN", "Peskin", "Aaron"]

def _build_default_focus():
    """Build default focus names from config district."""
    district = _DISTRICT_CFG.get("district", 5)
    sup_names = SUPERVISOR_NAMES.get(district, [])
    # Include both case variants for Socrata matching
    names = []
    for n in sup_names:
        names.extend([n.upper(), n, n.lower()])
    names.extend(BOARD_PRESIDENT_NAMES)
    return list(dict.fromkeys(names))  # dedup preserving order

DEFAULT_FOCUS_NAMES = _build_default_focus()

# ── Keywords for cross-referencing with tracked Planning/Legistar items ───────
def _build_tracked_keywords():
    """Build cross-reference keywords from config neighborhoods/streets."""
    cfg = _DISTRICT_CFG
    kw = [n.lower() for n in cfg.get("neighborhoods", [])]
    kw.extend(s.lower() for s in cfg.get("streets", []))
    # Always include these citywide civic terms
    kw.extend([
        "planning commission", "board of supervisors", "zoning",
        "affordable housing", "homeless shelter", "navigation center",
    ])
    return kw

TRACKED_KEYWORDS = _build_tracked_keywords()


# ─────────────────────────────────────────────────────────────────────────────
# Archive helpers
# ─────────────────────────────────────────────────────────────────────────────

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
    archive = load_archive()
    existing_ids = {r["id"] for r in archive["items"]}
    now = datetime.now(tz=timezone.utc).isoformat()
    added = 0
    for record in new_records:
        rid = record["id"]
        if rid not in existing_ids:
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


# ─────────────────────────────────────────────────────────────────────────────
# HTTP helpers
# ─────────────────────────────────────────────────────────────────────────────

def http_get(url, timeout=20):
    """Fetch URL via urllib, return text or None."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"  HTTP error fetching {url}: {e}", file=sys.stderr)
        return None


def socrata_query(dataset_id, params, limit=100):
    """Query a Socrata dataset and return list of dicts."""
    params["$limit"] = limit
    qs = urlencode(params)
    url = f"{SOCRATA_BASE}/{dataset_id}.json?{qs}"
    raw = http_get(url)
    if not raw:
        return []
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
        # Error response
        return []
    except json.JSONDecodeError:
        return []


# ─────────────────────────────────────────────────────────────────────────────
# RSS parsing
# ─────────────────────────────────────────────────────────────────────────────

def parse_rss_date(date_str):
    """Parse RSS pubDate → datetime (UTC-aware)."""
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
    ]
    date_str = date_str.strip()
    # Handle "GMT" suffix which %z doesn't parse
    if date_str.endswith(" GMT"):
        date_str = date_str[:-4] + " +0000"
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    return None


def fetch_rss_items(feed_url, since: datetime):
    """Fetch RSS feed, return items newer than `since`."""
    raw = http_get(feed_url)
    if not raw:
        return []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return []

    channel = root.find("channel")
    if channel is None:
        return []

    items = []
    for item in channel.findall("item"):
        title = item.findtext("title", "").strip()
        link  = item.findtext("link", "").strip()
        date_str = item.findtext("pubDate", "")
        cats  = [c.text for c in item.findall("category") if c.text]
        desc  = item.findtext("description", "").strip()
        desc  = re.sub(r"<[^>]+>", " ", desc)  # strip HTML tags
        desc  = re.sub(r"\s+", " ", desc).strip()

        pub_dt = parse_rss_date(date_str)
        if pub_dt is None:
            continue
        if pub_dt < since:
            continue

        items.append({
            "title": title,
            "link":  link,
            "date":  pub_dt.strftime("%Y-%m-%d"),
            "categories": cats,
            "description": desc[:300],
        })

    return items


# ─────────────────────────────────────────────────────────────────────────────
# Lobbyist contact activity (Socrata)
# ─────────────────────────────────────────────────────────────────────────────

def fetch_lobbyist_contacts(since: datetime, official_names=None):
    """
    Fetch recent lobbyist contacts with public officials.
    official_names: list of name fragments to filter by (e.g. ["MAHMOOD", "PESKIN"])
    Returns list of contact records.
    """
    since_str = since.strftime("%Y-%m-%dT00:00:00")
    
    if official_names:
        # Build OR filter for multiple names
        name_clauses = " OR ".join(
            f"upper(officialname) like '%{n.upper()}%'" for n in official_names
        )
        where = f"date >= '{since_str}' AND ({name_clauses})"
    else:
        where = f"date >= '{since_str}'"

    records = socrata_query(DS_LOBBYIST_CONTACTS, {
        "$where": where,
        "$order": "date DESC",
    }, limit=200)

    return records


def fetch_lobbyist_contributions(since: datetime, candidate_names=None):
    """
    Fetch lobbyist campaign contributions.
    candidate_names: list of fragments for candidate/committee name filtering.
    """
    since_str = since.strftime("%Y-%m-%dT00:00:00")

    if candidate_names:
        name_clauses = " OR ".join(
            f"upper(candidatename) like '%{n.upper()}%' OR upper(committeename) like '%{n.upper()}%'"
            for n in candidate_names
        )
        where = f"date >= '{since_str}' AND ({name_clauses})"
    else:
        where = f"date >= '{since_str}'"

    records = socrata_query(DS_LOBBYIST_CONTRIB, {
        "$where": where,
        "$order": "date DESC",
    }, limit=100)

    return records


# ─────────────────────────────────────────────────────────────────────────────
# Cross-reference: flag notices mentioning tracked items
# ─────────────────────────────────────────────────────────────────────────────

def flag_tracked(text, keywords=TRACKED_KEYWORDS):
    """Return list of matched tracked keywords in text (case-insensitive)."""
    text_lower = text.lower()
    return [kw for kw in keywords if kw in text_lower]


# ─────────────────────────────────────────────────────────────────────────────
# Deduplicate RSS (main feed has overlap with specific feeds)
# ─────────────────────────────────────────────────────────────────────────────

def dedupe_items(items):
    seen_links = set()
    out = []
    for item in items:
        key = item.get("link", item.get("title", ""))
        if key not in seen_links:
            seen_links.add(key)
            out.append(item)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Classify notice type for display
# ─────────────────────────────────────────────────────────────────────────────

def classify_notice(item):
    cats = [c.lower() for c in item.get("categories", [])]
    title_lower = item.get("title", "").lower()

    if "press releases" in cats or "fine" in title_lower or "fines" in title_lower:
        return "🚨 Enforcement"
    if "audits" in cats or "audit" in title_lower:
        return "🔍 Audit"
    if "commission meeting agendas" in cats or "agenda" in title_lower:
        return "📋 Agenda"
    if "regulation notices" in cats or "proposed regulation" in title_lower:
        return "📝 Regulation"
    if "public finance" in cats or "expenditure ceiling" in title_lower:
        return "💰 Public Finance"
    if "interested persons meetings" in cats:
        return "👥 Interested Persons"
    if "meeting summaries" in cats or "summary" in title_lower:
        return "📊 Meeting Summary"
    return "📣 Notice"


# ─────────────────────────────────────────────────────────────────────────────
# Formatting helpers
# ─────────────────────────────────────────────────────────────────────────────

def fmt_contact(r):
    """Format a lobbyist contact record for display."""
    date  = r.get("date", "")[:10]
    lname = r.get("lobbyistname", "Unknown")
    client= r.get("clientname", "")
    firm  = r.get("firmname", "")
    firm_str = f" ({firm})" if firm and firm.lower() not in lname.lower() else ""
    official = r.get("officialname", "")
    issue = r.get("issue", "")
    subject = r.get("subjectarea", "")
    outcome = r.get("outcomesought", "")
    filenum = r.get("filenumber", "")
    filenum_str = f" [#{filenum}]" if filenum and filenum.strip() not in ("", "N/A") else ""

    lines = [f"  [{date}] {lname}{firm_str} → {official}"]
    lines.append(f"    Client: {client}")
    if issue:
        lines.append(f"    Issue: {issue}{filenum_str}")
    if subject:
        lines.append(f"    Subject: {subject} | Outcome sought: {outcome}")
    return "\n".join(lines)


def fmt_contribution(r):
    """Format a lobbyist campaign contribution record."""
    date     = r.get("date", "")[:10]
    lname    = r.get("lobbyistname", "")
    amount   = r.get("amount", "0")
    try:
        amount_str = f"${float(amount):,.0f}"
    except (ValueError, TypeError):
        amount_str = f"${amount}"
    candidate = r.get("candidatename", r.get("officialname", ""))
    committee = r.get("committeename", "")
    source    = r.get("sourceoffunds", "")
    source_str = f" (source: {source})" if source else ""

    lines = [f"  [{date}] {lname} → {candidate}{source_str} — {amount_str}"]
    if committee and committee != candidate:
        lines.append(f"    Committee: {committee}")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SF Ethics Commission scraper")
    parser.add_argument("--days", type=int, default=30,
                        help="Look back N days (default: 30)")
    parser.add_argument("--supervisor", "--district", type=int, default=None,
                        help="Filter to a specific supervisor district (e.g. 5)")
    parser.add_argument("--all-supervisors", action="store_true",
                        help="Show lobbyist contacts across all supervisors")
    parser.add_argument("--json", dest="json_out", action="store_true",
                        help="Output JSON instead of text")
    args = parser.parse_args()

    since_dt = datetime.now(tz=timezone.utc) - timedelta(days=args.days)

    # ── Determine which supervisor names to focus on ──────────────────────────
    if args.all_supervisors:
        focus_names = None  # all contacts
        contact_header = "All supervisor contacts"
    elif args.supervisor is not None:
        sup_names = SUPERVISOR_NAMES.get(args.supervisor, [])
        focus_names = sup_names if sup_names else DEFAULT_FOCUS_NAMES
        contact_header = f"D{args.supervisor} supervisor contacts"
    else:
        focus_names = DEFAULT_FOCUS_NAMES
        district = _DISTRICT_CFG.get("district", 5)
        sup_last = SUPERVISOR_NAMES.get(district, ["?"])[0].title()
        contact_header = f"D{district} ({sup_last}) + Board President ({BOARD_PRESIDENT}) contacts"

    # ── Fetch RSS notices ─────────────────────────────────────────────────────
    all_notices = []
    for feed_name, feed_url in RSS_FEEDS.items():
        items = fetch_rss_items(feed_url, since_dt)
        all_notices.extend(items)

    all_notices = dedupe_items(all_notices)
    # Sort by date desc
    all_notices.sort(key=lambda x: x["date"], reverse=True)

    # ── Cross-reference notices with tracked keywords ─────────────────────────
    for item in all_notices:
        text = item["title"] + " " + item.get("description", "")
        flags = flag_tracked(text)
        item["tracked_flags"] = flags

    # ── Fetch lobbyist contacts ───────────────────────────────────────────────
    contacts = fetch_lobbyist_contacts(since_dt, official_names=focus_names)

    # ── Fetch campaign contributions (recent, no supervisor filter — it's broad)
    contributions = fetch_lobbyist_contributions(since_dt)

    # ── Archive all data ─────────────────────────────────────────────────────
    archive_records = []
    for item in all_notices:
        archive_records.append({
            "id": item.get("link", item.get("title", "")),
            "source": "sf_ethics",
            "record_type": "notice",
            "title": item["title"],
            "link": item.get("link", ""),
            "date": item["date"],
            "categories": item.get("categories", []),
            "description": item.get("description", ""),
        })
    for r in contacts:
        archive_records.append({
            "id": f"{r.get('date','')}|{r.get('lobbyistname','')}|{r.get('officialname','')}|{r.get('clientname','')}",
            "source": "sf_ethics",
            "record_type": "lobbyist_contact",
            "date": r.get("date", "")[:10],
            "lobbyistname": r.get("lobbyistname", ""),
            "officialname": r.get("officialname", ""),
            "clientname": r.get("clientname", ""),
            "firmname": r.get("firmname", ""),
            "issue": r.get("issue", ""),
            "subjectarea": r.get("subjectarea", ""),
            "outcomesought": r.get("outcomesought", ""),
            "filenumber": r.get("filenumber", ""),
        })
    for r in contributions:
        archive_records.append({
            "id": f"{r.get('date','')}|{r.get('lobbyistname','')}|{r.get('candidatename','')}|{r.get('amount','')}",
            "source": "sf_ethics",
            "record_type": "campaign_contribution",
            "date": r.get("date", "")[:10],
            "lobbyistname": r.get("lobbyistname", ""),
            "candidatename": r.get("candidatename", ""),
            "amount": r.get("amount", ""),
            "committeename": r.get("committeename", ""),
            "sourceoffunds": r.get("sourceoffunds", ""),
        })
    update_archive(archive_records)

    # ── JSON output ───────────────────────────────────────────────────────────
    if args.json_out:
        output = {
            "as_of": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "since": since_dt.strftime("%Y-%m-%d"),
            "notices": all_notices,
            "lobbyist_contacts": contacts,
            "lobbyist_contributions": contributions,
        }
        print(json.dumps(output, indent=2))
        return

    # ── Text output ───────────────────────────────────────────────────────────
    now_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"╔══════════════════════════════════════════════════════╗")
    print(f"  SF Ethics Commission — last {args.days} days  ({now_str})")
    print(f"╚══════════════════════════════════════════════════════╝")
    print()

    # ── Section 1: Public notices ─────────────────────────────────────────────
    print(f"━━ PUBLIC NOTICES ({len(all_notices)}) ━━")
    if not all_notices:
        print("  (none in window)")
    else:
        for item in all_notices:
            kind  = classify_notice(item)
            title = item["title"]
            date  = item["date"]
            link  = item["link"]
            flags = item.get("tracked_flags", [])
            flag_str = f" ⚑ TRACKED({', '.join(flags)})" if flags else ""
            print(f"\n{kind}  {date}")
            print(f"  {title}{flag_str}")
            print(f"  {link}")
            if item.get("description"):
                desc = item["description"][:200]
                print(f"  └ {desc}…" if len(item["description"]) > 200 else f"  └ {desc}")
    print()

    # ── Section 2: Lobbyist contacts ─────────────────────────────────────────
    print(f"━━ LOBBYIST CONTACTS: {contact_header} ({len(contacts)}) ━━")
    if not contacts:
        print("  (none in window)")
    else:
        # Group by official
        by_official = {}
        for r in contacts:
            off = r.get("officialname", "Unknown")
            by_official.setdefault(off, []).append(r)

        for official, recs in sorted(by_official.items()):
            print(f"\n  🏛  {official} ({len(recs)} contacts)")
            for r in recs:
                print(fmt_contact(r))

    print()

    # ── Section 3: Campaign contributions ────────────────────────────────────
    print(f"━━ LOBBYIST CAMPAIGN CONTRIBUTIONS — last {args.days} days ({len(contributions)}) ━━")
    if not contributions:
        print("  (none in window)")
    else:
        for r in contributions[:30]:
            print(fmt_contribution(r))
        if len(contributions) > 30:
            print(f"  … and {len(contributions) - 30} more (use --json for full list)")
    print()

    # ── Summary line ─────────────────────────────────────────────────────────
    tracked_notices = [n for n in all_notices if n.get("tracked_flags")]
    enforcements = [n for n in all_notices if "Enforcement" in classify_notice(n)]
    audits_found = [n for n in all_notices if "Audit" in classify_notice(n)]

    sup_name = _DISTRICT_CFG.get("supervisor_name") or f"D{_DISTRICT_CFG.get('district', '?')}"
    print(f"━━ SUMMARY ━━")
    print(f"  Notices: {len(all_notices)} total | {len(enforcements)} enforcement | {len(audits_found)} audits | {len(tracked_notices)} match tracked projects")
    print(f"  Lobbyist contacts ({sup_name}): {len(contacts)}")
    print(f"  Lobbyist contributions: {len(contributions)}")
    if tracked_notices:
        print(f"\n  ⚑ TRACKED PROJECT MENTIONS:")
        for n in tracked_notices:
            print(f"    [{n['date']}] {n['title']}")
            print(f"      flags: {', '.join(n['tracked_flags'])}")


if __name__ == "__main__":
    main()
