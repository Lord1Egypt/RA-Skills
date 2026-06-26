#!/usr/bin/env python3
"""
SF Planning Commission hearing scraper.
Fetches upcoming Planning Commission agendas via sfplanning.org,
downloads agenda PDFs, and extracts items filtered by supervisor district.

All calendar pages are server-rendered HTML — no browser needed.

Usage:
  python3 sf_planning_commission.py                  # upcoming hearings, all items
  python3 sf_planning_commission.py --district 5     # filter to D5 items
  python3 sf_planning_commission.py --next           # next hearing only
  python3 sf_planning_commission.py --json           # JSON output

Also covers:
  Historic Preservation Commission: --body hpc
  Zoning Administrator hearings:    --body za
"""

import os
import sys
import re
import json
import urllib.request
import urllib.error
import io
from datetime import date, datetime, timezone
from html import unescape

SFPLANNING_BASE = "https://sfplanning.org"

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sf_planning_commission_archive.json")
ARCHIVE_MAX = 5000

GRID_URLS = {
    "cpc": f"{SFPLANNING_BASE}/hearings-cpc-list",
    "hpc": f"{SFPLANNING_BASE}/hearings-hpc-list",
    "za":  f"{SFPLANNING_BASE}/hearings-za-grid",
}

# District number -> neighborhood/street keywords for filtering
DISTRICT_KEYWORDS = {
    1: ["district 1", "richmond", "sea cliff", "jordan park", "inner richmond", "outer richmond"],
    2: ["district 2", "marina", "cow hollow", "pacific heights", "presidio heights"],
    3: ["district 3", "north beach", "chinatown", "telegraph hill", "russian hill", "nob hill", "fisherman"],
    4: ["district 4", "sunset", "parkside", "inner sunset", "outer sunset"],
    5: ["district 5", "western addition", "haight", "hayes valley", "lower haight",
        "alamo square", "cole valley", "duboce", "nopa", "north of panhandle",
        "divisadero", "fillmore", "masonic", "broderick", "baker", "lyon", "stanyan",
        "golden gate ave", "mcallister", "fulton", "grove", "fell", "oak", "page", "waller"],
    6: ["district 6", "south of market", "soma", "tenderloin", "civic center", "mid-market"],
    7: ["district 7", "west portal", "forest hill", "twin peaks", "diamond heights",
        "glen park", "miraloma", "west of twin peaks"],
    8: ["district 8", "castro", "noe valley", "corona heights", "eureka valley", "duboce triangle"],
    9: ["district 9", "mission", "bernal heights", "portola"],
    10: ["district 10", "bayview", "hunters point", "visitacion valley", "excelsior",
         "potrero hill", "dogpatch", "india basin"],
    11: ["district 11", "ingleside", "oceanview", "outer mission", "ocean view", "crocker amazon"],
}

# Case type codes -> human readable
CASE_TYPES = {
    "CUA": "Conditional Use Authorization",
    "DRP": "Discretionary Review",
    "DRM": "Discretionary Review (Minor)",
    "ENV": "Environmental Review",
    "MAP": "Zoning Map Amendment",
    "PCA": "Planning Code Amendment",
    "PUD": "Planned Unit Development",
    "APL": "Appeal",
    "PPS": "SB 423 Informational",
    "COA": "Certificate of Appropriateness",
    "DES": "Landmark Designation",
    "VAR": "Zoning Variance",
    "OFA": "Office Allocation",
    "DNX": "Downtown Project Authorization",
    "SHD": "State Density Bonus",
}


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
    return {"items": []}


def save_archive(archive):
    archive["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(ARCHIVE_FILE, "w") as f:
        json.dump(archive, f, indent=2)


def update_archive(new_hearings):
    """Merge new hearings into the archive. Dedup by event URL. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_ids = {h["id"] for h in archive["items"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for hearing in new_hearings:
        url = hearing["url"]
        if url not in existing_ids:
            entry = {
                "id": url,
                "source": "sf_planning_commission",
                "scraped_at": now,
                "body": hearing["body"],
                "date": hearing.get("date"),
                "hearing_date": hearing.get("hearing_date"),
                "url": hearing["url"],
                "pdf_url": hearing.get("pdf_url"),
                "items": hearing.get("items", []),
            }
            archive["items"].append(entry)
            existing_ids.add(url)
            added += 1
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new hearings ({len(archive['items'])} total)", file=sys.stderr)
    return archive


# ---------------------------------------------------------------------------
# Curl-based fetchers for CPC / HPC list pages
# ---------------------------------------------------------------------------

def fetch_event_links_curl(list_url):
    """Fetch hearing event links from a -list calendar page.

    Parses <article about="/event/..."> tags and detects cancelled events
    from title text or URL slug.
    """
    req = urllib.request.Request(list_url, headers={
        "Accept": "text/html,application/xhtml+xml",
        "User-Agent": "sf-civic-digest/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"  HTTP error for {list_url}: {e}", file=sys.stderr)
        return []

    # Extract event URLs from <article about="/event/..."> tags
    articles = re.findall(r'<article\s[^>]*about="(/event/[^"]+)"', html)

    # Also look for heading text before each article to detect cancellations.
    # We'll scan for <h3>...</h3> or title text near each article.
    # Build a map: for each article URL, check surrounding context for "cancel".
    seen = set()
    events = []
    for url_path in articles:
        if url_path in seen:
            continue
        seen.add(url_path)

        # Check if the URL slug contains "cancelled"
        cancelled = "cancel" in url_path.lower()

        # Also check for "Cancelled" in nearby HTML context
        if not cancelled:
            # Find the article tag and look at ~500 chars before it for cancel text
            idx = html.find(f'about="{url_path}"')
            if idx >= 0:
                context = html[max(0, idx - 500):idx].lower()
                cancelled = "cancel" in context

        events.append({
            "url": SFPLANNING_BASE + url_path,
            "text": "",
            "cancelled": cancelled,
        })

    return events


def fetch_event_pdf_url_curl(event_url):
    """Fetch a hearing event page and extract the agenda PDF URL and date.

    Returns (pdf_url, date_str).
    """
    req = urllib.request.Request(event_url, headers={
        "Accept": "text/html,application/xhtml+xml",
        "User-Agent": "sf-civic-digest/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"  HTTP error for {event_url}: {e}", file=sys.stderr)
        return None, ""

    # Extract date from <h3 class="date">Thursday, April 2, 2026</h3>
    # or from <time> elements
    date_str = ""
    date_m = re.search(r'<h3[^>]*class="date"[^>]*>([^<]+)</h3>', html)
    if date_m:
        date_str = unescape(date_m.group(1)).strip()
    else:
        # Fallback: <time> element
        time_m = re.search(r'<time[^>]*>([^<]+)</time>', html)
        if time_m:
            date_str = unescape(time_m.group(1)).strip()
        else:
            # Fallback: any full date string in the page
            fallback_m = re.search(
                r'((?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+'
                r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
                r'\s+\d+,?\s*\d{4})', html)
            if fallback_m:
                date_str = unescape(fallback_m.group(1)).strip()

    # Extract PDF URL — look for <a> tags with .pdf href containing sfplanning
    pdf_url = None
    # Pattern 1: href containing both .pdf and sfplanning (absolute URL)
    pdf_m = re.search(r'href="(https?://[^"]*sfplanning[^"]*\.pdf)"', html, re.IGNORECASE)
    if pdf_m:
        pdf_url = pdf_m.group(1)
    else:
        # Pattern 2: relative path to agenda PDF
        pdf_m = re.search(r'href="(/sites/default/files/[^"]*\.pdf)"', html, re.IGNORECASE)
        if pdf_m:
            pdf_url = SFPLANNING_BASE + pdf_m.group(1)
        else:
            # Pattern 3: any .pdf link with "agenda" in text or href
            for m in re.finditer(r'<a[^>]*href="([^"]*\.pdf)"[^>]*>([^<]*)</a>', html, re.IGNORECASE):
                href, text = m.group(1), m.group(2).lower()
                if "agenda" in text or "agenda" in href.lower():
                    pdf_url = href if href.startswith("http") else SFPLANNING_BASE + href
                    break

    return pdf_url, date_str


# ---------------------------------------------------------------------------
# ZA-specific fetchers (unchanged — already curl-based)
# ---------------------------------------------------------------------------

def fetch_za_event_links():
    """ZA hearings use static HTML — no browser needed."""
    req = urllib.request.Request(GRID_URLS["za"], headers={
        "Accept": "text/html,application/xhtml+xml",
        "User-Agent": "sf-civic-digest/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"  HTTP error for ZA grid: {e}", file=sys.stderr)
        return []
    links = re.findall(r'href="(/event/zoning-variance-hearing[^"]+)"', html)
    seen = set()
    events = []
    for l in links:
        if l not in seen:
            seen.add(l)
            events.append({"url": SFPLANNING_BASE + l, "text": "", "cancelled": False})
    return events


def fetch_za_pdf_url(event_url):
    """Get ZA hearing agenda PDF via static HTML."""
    req = urllib.request.Request(event_url, headers={
        "Accept": "text/html,application/xhtml+xml",
        "User-Agent": "sf-civic-digest/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"  HTTP error for {event_url}: {e}", file=sys.stderr)
        return None, ""
    pdf_m = re.search(r'(/sites/default/files/agendas/[^\s"\']+_za[^\s"\']*\.pdf)', html)
    date_m = re.search(
        r'(January|February|March|April|May|June|July|August|September|October|November|December)'
        r'\s+\d+,?\s*\d{4}', html)
    pdf = SFPLANNING_BASE + pdf_m.group(1) if pdf_m else None
    date_str = date_m.group(0) if date_m else ""
    return pdf, date_str


# ---------------------------------------------------------------------------
# PDF parsing
# ---------------------------------------------------------------------------

def download_and_parse_pdf(pdf_url):
    """Download agenda PDF and extract case items."""
    try:
        import pdfplumber
    except ImportError:
        print("  pdfplumber not available", file=sys.stderr)
        return []

    req = urllib.request.Request(pdf_url, headers={
        "User-Agent": "sf-civic-digest/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            with open("/tmp/sf_hearing_agenda.pdf", "wb") as f:
                f.write(resp.read())
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"  HTTP error downloading PDF {pdf_url}: {e}", file=sys.stderr)
        return []

    try:
        with pdfplumber.open("/tmp/sf_hearing_agenda.pdf") as pdf:
            full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        print(f"  PDF parse error: {e}", file=sys.stderr)
        return []

    return parse_agenda_items(full_text)


def parse_agenda_items(text):
    """
    Extract case items from Planning Commission or ZA agenda PDF text.
    Items follow: {num}. {RECORD} ({PLANNER}: {phone})\n{ADDRESS}...
    """
    items = []

    # Split on item number boundaries — lines starting with a digit followed by a period
    # and a 4-digit year (record number pattern)
    item_blocks = re.split(r'\n(?=\d+\.\s+\d{4}-\d{6})', text)

    SKIP_SECTIONS = [
        'LAND ACKNOWLEDGEMENT', 'ROLL CALL', 'PUBLIC COMMENT', 'DIRECTOR',
        'COMMISSION MATTERS', 'DEPARTMENT MATTERS', 'CONSIDERATION OF ADOPTION',
        'HEARING PROCEDURES', 'COMMISSION COMMENTS', 'REVIEW OF PAST',
        'GENERAL PUBLIC COMMENT', 'REGULAR CALENDAR', 'DISCRETIONARY REVIEW CALENDAR',
        'CONSENT CALENDAR',
    ]

    for block in item_blocks:
        block = block.strip()
        if not block:
            continue

        # Must start with a number
        num_m = re.match(r'^(\d+)\.\s+', block)
        if not num_m:
            continue
        num = num_m.group(1)

        # Extract record number
        record_m = re.search(r'(\d{4}-\d{6,7}[A-Z/]+)', block)
        if not record_m:
            continue
        record = record_m.group(1)

        # Skip boilerplate sections
        first_200 = block[:200].upper()
        if any(s in first_200 for s in SKIP_SECTIONS):
            continue

        # Extract case type codes from record
        codes = re.findall(r'[A-Z]{2,}', record.split('-')[-1])
        type_labels = [CASE_TYPES.get(c, c) for c in codes]

        # Extract district(s)
        districts = [int(d) for d in re.findall(r'District\s+(\d+)', block, re.IGNORECASE)]

        # Extract address — usually the line after the record/planner line
        lines = block.split('\n')
        address = ""
        for line in lines[1:4]:
            line = line.strip()
            # Address lines look like "1053-1055 TEXAS STREET" or "2089 INGALLS STREET"
            if re.match(r'^\d+[\d\-\s]+[A-Z]', line) or re.match(r'^[A-Z\d].*STREET|AVE|BLVD|WAY|PLACE|DRIVE', line):
                address = line[:100]
                break
        if not address:
            # fallback: first non-empty line after line 0
            for line in lines[1:3]:
                if line.strip() and len(line.strip()) > 10:
                    address = line.strip()[:100]
                    break

        # Recommendation
        rec_m = re.search(r'Preliminary Recommendation:\s*(.+?)(?:\n|$)', block)
        recommendation = rec_m.group(1).strip() if rec_m else ""

        # Status flags
        action = ""
        bl = block.upper()
        if 'WITHDRAWN' in bl:
            action = "WITHDRAWN"
        elif 'INDEFINITE CONTINUANCE' in bl or 'PROPOSED FOR CONTINUANCE' in bl:
            action = "CONTINUANCE"
        elif 'CONTINUED FROM' in bl:
            action = "CONTINUED"

        # Planner
        planner_m = re.search(r'\(([A-Z]\.\s+\w+):', block)
        planner = planner_m.group(1) if planner_m else ""

        items.append({
            "number": num,
            "record": record,
            "codes": codes,
            "type_labels": type_labels,
            "address": address,
            "districts": districts,
            "recommendation": recommendation,
            "action": action,
            "planner": planner,
            "body_snippet": block[:400],
        })

    return items


def is_relevant(item, district):
    """Check if an item is relevant to a given district."""
    if district is None:
        return True
    if district in item.get("districts", []):
        return True
    kws = DISTRICT_KEYWORDS.get(district, [])
    text = (item.get("address", "") + " " + item.get("body_snippet", "")).lower()
    return any(kw in text for kw in kws)


def format_hearing(hearing, district=None):
    """Format a single hearing for output."""
    lines = []
    body_label = hearing.get("body", "Planning Commission").upper()
    date_str = hearing.get("date", "date unknown")
    cancelled = hearing.get("cancelled", False)

    lines.append(f"\n{'─'*55}")
    status = " ⚠️ CANCELLED" if cancelled else ""
    lines.append(f"🏛️  {body_label}{status}")
    lines.append(f"   {date_str}")
    if hearing.get("pdf_url"):
        lines.append(f"   Agenda: {hearing['pdf_url']}")
    lines.append("")

    items = hearing.get("items", [])
    if not items:
        lines.append("   (no agenda items parsed)")
        return "\n".join(lines)

    filtered = [i for i in items if is_relevant(i, district)]
    if district and not filtered:
        lines.append(f"   (no District {district} items)")
        return "\n".join(lines)

    show_items = filtered if district else items
    for item in show_items:
        codes_str = "/".join(item.get("codes", []))
        dist_str = f" [D{', D'.join(str(d) for d in item['districts'])}]" if item['districts'] else ""
        rec = item.get("recommendation", "")
        rec_str = f" → {rec}" if rec else ""
        withdrawn = " [WITHDRAWN]" if "WITHDRAWN" in item.get("action","").upper() else ""
        continued = " [CONTINUANCE]" if "CONTINUANCE" in item.get("action","").upper() else ""

        lines.append(f"  Item {item['number']}{dist_str} [{codes_str}]{withdrawn}{continued}")
        lines.append(f"  📍 {item['address'][:90]}")
        if rec_str:
            lines.append(f"  {rec_str.strip()}")
        lines.append("")

    return "\n".join(lines)


def main():
    district = None
    next_only = "--next" in sys.argv
    as_json = "--json" in sys.argv
    body = "cpc"

    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--district" and i + 1 < len(args):
            try:
                district = int(args[i + 1])
            except ValueError:
                pass
        elif arg == "--body" and i + 1 < len(args):
            body = args[i + 1].lower()

    today = date.today()

    # All bodies now use curl — no browser needed
    if body == "za":
        print("Fetching ZA hearing schedule...", file=sys.stderr)
        event_links = fetch_za_event_links()
        get_pdf = fetch_za_pdf_url
    else:
        list_url = GRID_URLS.get(body, GRID_URLS["cpc"])
        print(f"Fetching {body.upper()} hearing schedule from {list_url}...", file=sys.stderr)
        event_links = fetch_event_links_curl(list_url)
        get_pdf = fetch_event_pdf_url_curl

    print(f"Found {len(event_links)} event links", file=sys.stderr)

    hearings = []
    for ev in event_links:
        if ev.get("cancelled"):
            continue
        print(f"  Fetching: {ev['url']}", file=sys.stderr)
        pdf_url, date_str = get_pdf(ev["url"])

        # Parse date
        hearing_date = None
        if date_str:
            for fmt in ["%A, %B %d, %Y", "%B %d, %Y", "%B %d,%Y"]:
                try:
                    hearing_date = datetime.strptime(
                        re.sub(r'\s+', ' ', date_str.strip().split('\n')[0]), fmt
                    ).date()
                    break
                except ValueError:
                    continue

        if hearing_date and hearing_date < today:
            continue

        items = []
        if pdf_url:
            print(f"    Parsing PDF: {pdf_url[-60:]}", file=sys.stderr)
            items = download_and_parse_pdf(pdf_url)
            print(f"    Found {len(items)} items", file=sys.stderr)

        hearing = {
            "body": body.upper(),
            "date": date_str,
            "hearing_date": hearing_date.isoformat() if hearing_date else "",
            "url": ev["url"],
            "pdf_url": pdf_url,
            "cancelled": ev.get("cancelled", False),
            "items": items,
        }
        hearings.append(hearing)

        if next_only:
            break

    update_archive(hearings)

    if as_json:
        print(json.dumps(hearings, indent=2))
        return

    if not hearings:
        label = f"District {district}" if district else "SF"
        print(f"No upcoming {body.upper()} hearings found for {label}.")
        return

    label = f"District {district}" if district else "all districts"
    print(f"\n🏛️  SF PLANNING — {body.upper()} HEARINGS ({label})")
    for h in hearings:
        print(format_hearing(h, district=district))


if __name__ == "__main__":
    main()
