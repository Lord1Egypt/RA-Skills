#!/usr/bin/env python3
"""
SFMTA Engineering Public Hearing fetcher.
Scrapes sfmta.com/public-notices for upcoming Engineering Public Hearings,
downloads the agenda PDF, and extracts items filtered by supervisor district.

Usage (standalone):
  python3 sfmta_hearings.py                  # upcoming hearings, all districts
  python3 sfmta_hearings.py --district 5     # filter to D5 items only
  python3 sfmta_hearings.py --json           # JSON output

Engineering hearings happen roughly every 2-3 weeks (bi-weekly pattern).
Decisions are posted the Friday after the hearing at sfmta.com/EngineeringResults.
How to participate: join via sfmta.com/EngHearing or submit written comment to staff listed per item.
"""

import sys
import re
import json
import io
import os
import urllib.request
from datetime import datetime, date, timezone
from html import unescape

SFMTA_BASE = "https://www.sfmta.com"
NOTICES_URL = "https://www.sfmta.com/public-notices"

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sfmta_hearings_archive.json")
ARCHIVE_MAX = 5000

# Month name → number for date parsing
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={
        "User-Agent": "sf-civic-digest/1.0",
        "Accept": "text/html,*/*"
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_bytes(url, timeout=30):
    req = urllib.request.Request(url, headers={
        "User-Agent": "sf-civic-digest/1.0",
        "Accept": "*/*",
        "Referer": SFMTA_BASE,
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def parse_date(text):
    """Parse 'April 3, 2026' or 'April 3,2026' → date object."""
    m = re.search(
        r'(January|February|March|April|May|June|July|August|September|October|November|December)'
        r'\s+(\d{1,2}),?\s*(\d{4})',
        text, re.IGNORECASE
    )
    if not m:
        return None
    try:
        return date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2)))
    except (ValueError, KeyError):
        return None


def get_upcoming_hearing_notices():
    """Return list of upcoming engineering hearing notice paths from public-notices page."""
    html = fetch(NOTICES_URL)
    links = re.findall(r'href="(/notices/engineering-public-hearing[^"]+)"', html)
    # Deduplicate, preserve order
    seen = set()
    unique = []
    for l in links:
        if l not in seen:
            seen.add(l)
            unique.append(l)
    return unique


def get_pdf_links_for_notice(notice_path):
    """Fetch a notice page and return PDF media download paths."""
    html = fetch(SFMTA_BASE + notice_path)
    # PDFs are linked as /media/{id}/download
    pdfs = re.findall(r'(/media/\d+/download[^"]*)', html)
    # Also check linked reports page
    reports = re.findall(r'href="(/reports/engineering-public-hearing[^"]+)"', html)
    if not pdfs and reports:
        for rpath in reports[:1]:
            try:
                rhtml = fetch(SFMTA_BASE + rpath)
                pdfs = re.findall(r'(/media/\d+/download[^"]*)', rhtml)
            except Exception:
                pass
    # Also get date and time from the notice page
    date_obj = parse_date(html)
    time_m = re.search(r'(\d{1,2}:\d{2}\s*[AP]M)', html, re.IGNORECASE)
    time_str = time_m.group(1) if time_m else ""
    # Get join link
    join_m = re.search(r'sfmta\.com/EngHearing', html, re.IGNORECASE)
    join_url = "https://www.sfmta.com/EngHearing" if join_m else ""
    # Phone
    phone_m = re.search(r'(\(\d{3}\)\s*\d{3}-\d{4})', html)
    conf_m = re.search(r'conference ID\s*([\d\s#]+)', html, re.IGNORECASE)
    phone_str = phone_m.group(1) if phone_m else ""
    conf_str = conf_m.group(1).strip() if conf_m else ""

    return {
        "pdf_paths": list(dict.fromkeys(pdfs)),  # deduplicated
        "date": date_obj,
        "time": time_str,
        "join_url": join_url,
        "phone": phone_str,
        "conference_id": conf_str,
        "notice_url": SFMTA_BASE + notice_path,
    }


def parse_hearing_pdf(pdf_path):
    """
    Download and parse an SFMTA Engineering Hearing agenda PDF.
    Returns list of items: {number, title, description, districts, contact_email, location}
    """
    try:
        import pdfplumber
    except ImportError:
        print("pdfplumber not available — install with: pip install pdfplumber", file=sys.stderr)
        return []

    try:
        pdf_bytes = fetch_bytes(SFMTA_BASE + pdf_path)
    except Exception as e:
        print(f"  Could not download PDF {pdf_path}: {e}", file=sys.stderr)
        return []

    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        print(f"  Could not parse PDF: {e}", file=sys.stderr)
        return []

    return extract_items_from_pdf_text(full_text)


def extract_items_from_pdf_text(text):
    """
    Parse agenda items from SFMTA hearing PDF text.
    Items follow a pattern: number. ESTABLISH/RESCIND/ACTION — location — description
    """
    items = []

    # Split on item number patterns: "1.", "2.", "9(a).", etc.
    # Items start with a number (possibly with letter suffix) at start of line
    item_pattern = re.compile(
        r'^(\d+(?:\([a-z]\))?)\.\s+(.*?)(?=^\d+(?:\([a-z]\))?\.|\Z)',
        re.MULTILINE | re.DOTALL
    )

    for m in item_pattern.finditer(text):
        num = m.group(1)
        body = m.group(2).strip()

        # Skip boilerplate sections
        if any(skip in body[:50] for skip in [
            "CALL TO ORDER", "INTRODUCTION", "PUBLIC COMMENT", "ADJOURNMENT",
            "California Environmental", "CEQA"
        ]):
            continue

        # Extract district(s)
        districts = re.findall(r'Supervisor District\s+(\d+)', body, re.IGNORECASE)
        districts = [int(d) for d in districts]

        # Extract contact email
        email_m = re.search(r'[\w.+-]+@sfmta\.com', body)
        email = email_m.group(0) if email_m else ""

        # Extract location (first line, before action verbs)
        lines = body.split('\n')
        location = lines[0].strip() if lines else ""

        # Action type (ESTABLISH, RESCIND, etc.)
        action_m = re.search(
            r'\b(ESTABLISH|RESCIND|EXTEND|MODIFY|CONVERT|REMOVE|ADD)\b',
            body[:200], re.IGNORECASE
        )
        action = action_m.group(1).upper() if action_m else ""

        # Clean description (remove email, district refs)
        desc = re.sub(r'[\w.+-]+@sfmta\.com', '', body)
        desc = re.sub(r'\(Supervisor District \d+\)', '', desc)
        desc = re.sub(r'\(Approvable by the City Traffic Engineer\)', '', desc)
        desc = re.sub(r'\(Requires approval by the SFMTA Board\)', '(requires SFMTA Board approval)', desc)
        desc = re.sub(r'\s+', ' ', desc).strip()

        items.append({
            "number": num,
            "action": action,
            "location": location,
            "description": desc[:600],
            "districts": districts,
            "contact_email": email,
        })

    return items


# ---------------------------------------------------------------------------
# Hearing archive
# ---------------------------------------------------------------------------

def load_archive():
    if os.path.exists(ARCHIVE_FILE):
        try:
            with open(ARCHIVE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"items": [], "updated_at": None}


def save_archive(archive):
    archive["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(ARCHIVE_FILE, "w") as f:
        json.dump(archive, f, indent=2)


def update_archive(hearing_results):
    """Merge new hearings into the archive. Dedup by notice_path. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_ids = {h["id"] for h in archive["items"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for h in hearing_results:
        notice_path = h.get("notice_path")
        if notice_path and notice_path not in existing_ids:
            entry = {
                "id": notice_path,
                "source": "sfmta_hearings",
                "scraped_at": now,
                "date": h["date"].isoformat() if h.get("date") else None,
                "time": h.get("time"),
                "notice_url": h.get("notice_url"),
                "join_url": h.get("join_url"),
                "items": h.get("items", []),
            }
            archive["items"].append(entry)
            existing_ids.add(notice_path)
            added += 1
    # Cap: keep most recent
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new hearings ({len(archive['items'])} total)", file=sys.stderr)
    return archive


def fetch_hearing(notice_path, district_filter=None):
    """
    Full pipeline: notice page → PDF → parsed items, optionally filtered by district.
    Returns hearing dict with metadata + items.
    """
    meta = get_pdf_links_for_notice(notice_path)
    if not meta["pdf_paths"]:
        return {**meta, "items": [], "error": "no agenda PDF found"}

    # Try the first PDF (usually the agenda, not results)
    items = []
    for pdf_path in meta["pdf_paths"][:2]:
        items = parse_hearing_pdf(pdf_path)
        if items:
            break

    if district_filter is not None:
        # Only include items that are explicitly tagged for this district
        # (items with no district tag are citywide/unclear — include them too)
        # But items tagged for OTHER districts only → exclude
        items = [
            i for i in items
            if not i["districts"] or district_filter in i["districts"]
        ]
        # Secondary pass: if location text mentions another SF neighborhood clearly not in this district, skip
        # (keeps untagged items but removes obviously mismatched ones)
        # For now keep all untagged items — better to over-include than miss something

    return {**meta, "items": items}


def format_hearing(hearing, district_filter=None):
    """Format a hearing for human-readable output."""
    lines = []
    d = hearing.get("date")
    date_str = d.strftime("%A, %B %-d, %Y") if d else "date unknown"
    label = f"District {district_filter}" if district_filter else "all districts"

    lines.append(f"🚦 SFMTA Engineering Public Hearing — {date_str}")
    if hearing.get("time"):
        lines.append(f"   {hearing['time']} · Online")
    if hearing.get("join_url"):
        lines.append(f"   Join: {hearing['join_url']}")
    if hearing.get("phone") and hearing.get("conference_id"):
        lines.append(f"   Phone: {hearing['phone']} · ID: {hearing['conference_id']}")
    lines.append(f"   Source: {hearing.get('notice_url', '')}")
    lines.append(f"   Showing: {label}")
    lines.append("")

    items = hearing.get("items", [])
    if not items:
        err = hearing.get("error", "no items found")
        lines.append(f"   (no items — {err})")
        return "\n".join(lines)

    for item in items:
        district_tag = ""
        if item["districts"]:
            district_tag = f" [D{', D'.join(str(d) for d in item['districts'])}]"
        action_tag = f" {item['action']}" if item["action"] else ""
        lines.append(f"  Item {item['number']}{district_tag}:{action_tag}")
        lines.append(f"   📍 {item['location'][:100]}")
        # Show first 2 lines of description
        desc_lines = [l.strip() for l in item["description"].split('\n') if l.strip()]
        for dl in desc_lines[:3]:
            lines.append(f"   {dl[:130]}")
        if item["contact_email"]:
            lines.append(f"   ✉ {item['contact_email']}")
        lines.append("")

    return "\n".join(lines)


def main():
    district_filter = None
    as_json = "--json" in sys.argv
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--district" and i + 1 < len(args):
            try:
                district_filter = int(args[i + 1])
            except ValueError:
                pass

    print("Fetching SFMTA Engineering Public Hearing notices...", file=sys.stderr)
    notices = get_upcoming_hearing_notices()

    if not notices:
        print("No upcoming engineering hearing notices found.")
        return

    today = date.today()
    results = []

    for notice_path in notices:
        print(f"  Processing {notice_path}...", file=sys.stderr)
        hearing = fetch_hearing(notice_path, district_filter=district_filter)
        hearing["notice_path"] = notice_path
        d = hearing.get("date")
        if d and d < today:
            continue  # skip past hearings
        results.append(hearing)

    update_archive(results)

    if not results:
        print("No upcoming SFMTA Engineering Public Hearings found.")
        return

    if as_json:
        out = []
        for h in results:
            out.append({
                "date": h["date"].isoformat() if h.get("date") else None,
                "time": h.get("time"),
                "join_url": h.get("join_url"),
                "notice_url": h.get("notice_url"),
                "items": h.get("items", []),
            })
        print(json.dumps(out, indent=2))
    else:
        for h in results:
            print(format_hearing(h, district_filter=district_filter))


if __name__ == "__main__":
    main()
