#!/usr/bin/env python3
"""
SF Planning public notices scraper.
Fetches project notices from sfplanning.org/notices — includes:
  - Planning Commission hearings (CUA, DRP, ENV, etc.)
  - Historic Preservation Commission hearings (COA, DES)
  - Zoning Variance hearings (VAR)
  - Section 311 neighborhood notices (individual project applications)

Usage:
  python3 sf_planning_notices.py                   # all active notices
  python3 sf_planning_notices.py --district 5      # D5 neighborhoods only
  python3 sf_planning_notices.py --upcoming        # only items with future hearing dates
  python3 sf_planning_notices.py --json            # JSON output

Source: https://sfplanning.org/notices
Note: requires Accept: text/html header — page returns empty without it.
All data is in a single concatenated text block in the HTML (no JS needed).
"""

import os
import sys
import re
import json
import urllib.request
import urllib.error
from datetime import date, datetime, timezone
from html import unescape

NOTICES_URL = "https://sfplanning.org/notices"

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sf_planning_notices_archive.json")
ARCHIVE_MAX = 5000

# District 5 neighborhoods per SF Planning's neighborhood names
DISTRICT_NEIGHBORHOODS = {
    1: ["Richmond", "Inner Richmond", "Outer Richmond", "Sea Cliff", "Jordan Park"],
    2: ["Marina", "Cow Hollow", "Pacific Heights", "Presidio Heights"],
    3: ["North Beach", "Chinatown", "Telegraph Hill", "Russian Hill", "Fisherman's Wharf", "Nob Hill"],
    4: ["Sunset", "Inner Sunset", "Outer Sunset", "Parkside"],
    5: ["Western Addition", "Haight Ashbury", "Haight", "Hayes Valley", "Lower Haight",
        "Alamo Square", "Cole Valley", "Duboce", "NOPA", "North of Panhandle"],
    6: ["South of Market", "SoMa", "Tenderloin", "Civic Center", "Downtown", "Mid-Market"],
    7: ["West Portal", "Forest Hill", "Twin Peaks", "Diamond Heights", "Glen Park", "Miraloma Park",
        "West of Twin Peaks"],
    8: ["Castro", "Noe Valley", "Corona Heights", "Eureka Valley", "Duboce Triangle", "Upper Market"],
    9: ["Mission", "Bernal Heights", "Portola", "Bernal"],
    10: ["Bayview", "Hunters Point", "Visitacion Valley", "Excelsior", "Crocker Amazon", "Potrero Hill"],
    11: ["Excelsior", "Ingleside", "Oceanview", "Outer Mission", "Crocker"],
}

# Notice type codes → human readable
NOTICE_TYPES = {
    "CUA": "Conditional Use Authorization",
    "DRP": "Discretionary Review",
    "VAR": "Zoning Variance",
    "COA": "Certificate of Appropriateness",
    "DES": "Landmark Designation",
    "ENV": "Environmental Review",
    "MAP": "Map Amendment",
    "PCA": "Planning Code Amendment",
    "PRJ": "Section 311 Neighbor Notice",
    "SRV": "Survey/Study",
    "DNX": "Downtown Project Authorization",
}


# ---------------------------------------------------------------------------
# Notice archive
# ---------------------------------------------------------------------------

def load_archive():
    if os.path.exists(ARCHIVE_FILE):
        try:
            with open(ARCHIVE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"items": [], "updated_at": datetime.now(timezone.utc).isoformat()}


def save_archive(archive):
    with open(ARCHIVE_FILE, "w") as f:
        json.dump(archive, f, indent=2)


def update_archive(new_notices):
    """Merge new notices into the archive. Dedup by record number. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_ids = {n["id"] for n in archive["items"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for notice in new_notices:
        record = notice["record"]
        if record not in existing_ids:
            entry = {
                "id": record,
                "source": "sf_planning_notices",
                "scraped_at": now,
                "address": notice["address"],
                "record": notice["record"],
                "codes": notice["codes"],
                "type_labels": notice["type_labels"],
                "neighborhood": notice["neighborhood"],
                "hearing_body": notice["hearing_body"],
                "date_posted": notice["date_posted"],
                "expiration": notice["expiration"],
                "hearing_date": notice["hearing_date"],
                "contact_email": notice["contact_email"],
            }
            archive["items"].append(entry)
            existing_ids.add(record)
            added += 1
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    archive["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new notices ({len(archive['items'])} total)", file=sys.stderr)
    return archive


def fetch_notices_html():
    """Fetch the planning notices page. Requires Accept header to get full content."""
    req = urllib.request.Request(NOTICES_URL, headers={
        "Accept": "text/html,application/xhtml+xml",
        "User-Agent": "sf-civic-digest/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"  HTTP error fetching {NOTICES_URL}: {e}", file=sys.stderr)
        return ""


def parse_notices(html):
    """
    Parse the notices table from SF Planning HTML.
    The table renders as a single concatenated text blob.
    Structure per entry: {address} {record_num} {type_text} {neighborhood} {date_posted} {expiration} {hearing_date} {staff}
    """
    text = re.sub(r'<[^>]+>', ' ', html)
    text = unescape(text)
    text = re.sub(r'\xa0', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Find the table region
    start = text.find("Address")
    # Match any year in the copyright footer
    copyright_match = re.search(r'©\s*\d{4}\s*San Francisco Planning', text)
    end = copyright_match.start() if copyright_match else -1
    if start < 0:
        return []
    table = text[start:end if end > 0 else len(text)]

    # Split on record number pattern — each record number starts an entry
    # Record numbers: YYYY-NNNNNN followed by type codes (PRJ, CUA, VAR, etc.)
    record_re = re.compile(r'(\d{4}-\d{6,7}[A-Z/\-]+)')
    parts = record_re.split(table)
    # parts = [pre_text, record1, post1, record2, post2, ...]

    notices = []
    i = 1  # start at first record
    while i < len(parts) - 1:
        record_num = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        address_raw = parts[i - 1].strip() if i > 0 else ""

        # Extract address — it's the last meaningful chunk before the record number
        # Remove header words and previous entry's tail
        address_words = address_raw.split()
        # Take last run of words that look like a street address (up to 8 words)
        address_str = " ".join(address_words[-8:]).strip()
        # Strip any email/phone leftovers from previous entry
        address_str = re.sub(r'[\w.+-]+@\w+\.\w+', '', address_str).strip()
        address_str = re.sub(r'\(\d{3}\)\s*\d{3}-\d{4}', '', address_str).strip()

        # Extract codes from record number
        codes_m = re.search(r'\d{4}-\d{6,7}([A-Z/\-]+)', record_num)
        raw_codes = codes_m.group(1) if codes_m else ""
        codes = [c for c in re.split(r'[/\-]', raw_codes) if c]
        type_labels = [NOTICE_TYPES.get(c, c) for c in codes]

        # Extract neighborhood — look for known neighborhood names in body
        neighborhood = ""
        for dist_hoods in DISTRICT_NEIGHBORHOODS.values():
            for hood in dist_hoods:
                if hood in body:
                    neighborhood = hood
                    break
            if neighborhood:
                break
        # Also try common Planning neighborhood names not in our district map
        if not neighborhood:
            extra_hoods = ["Pacific Heights", "Marina", "North Beach", "Mission", 
                          "Bayview", "Potrero Hill", "Noe Valley", "Bernal Heights",
                          "Lakeshore", "Parkside", "Excelsior", "Ocean View",
                          "Presidio Heights", "Financial District", "Crocker Amazon",
                          "Visitacion Valley", "Outer Mission", "Inner Sunset",
                          "Inner Richmond", "Outer Richmond"]
            for hood in extra_hoods:
                if hood in body:
                    neighborhood = hood
                    break

        # Extract dates (MM/DD/YYYY)
        dates = re.findall(r'\d{2}/\d{2}/\d{4}', body)
        date_posted = dates[0] if len(dates) > 0 else ""
        expiration = dates[1] if len(dates) > 1 else ""
        hearing_date_raw = dates[2] if len(dates) > 2 else ""

        # Check for N/A hearing date
        na_match = re.search(r'N/A', body)
        if not hearing_date_raw and na_match:
            hearing_date_raw = "N/A"

        hearing_date = None
        if hearing_date_raw and hearing_date_raw != "N/A":
            try:
                hearing_date = datetime.strptime(hearing_date_raw, "%m/%d/%Y").date()
            except ValueError:
                pass

        # Extract staff email
        email_m = re.search(r'[\w.+-]+@sfgov\.org', body)
        email = email_m.group(0) if email_m else ""

        # Determine hearing body
        hearing_body = ""
        if any(c in codes for c in ["COA", "DES"]):
            hearing_body = "Historic Preservation Commission"
        elif "VAR" in codes and not any(c in codes for c in ["CUA", "DRP", "ENV"]):
            hearing_body = "Zoning Administrator (Variance)"
        elif any(c in codes for c in ["CUA", "DRP", "ENV", "DNX", "MAP", "PCA", "SHD"]):
            hearing_body = "Planning Commission"
        elif "PRJ" in codes:
            hearing_body = "Section 311 Notice (no hearing)"

        notices.append({
            "address": address_str,
            "record": record_num,
            "codes": codes,
            "type_labels": type_labels,
            "neighborhood": neighborhood,
            "hearing_body": hearing_body,
            "date_posted": date_posted,
            "expiration": expiration,
            "hearing_date": hearing_date.isoformat() if hearing_date else hearing_date_raw,
            "contact_email": email,
        })
        i += 2

    return notices


def _parse_date_flexible(date_str):
    """Parse MM/DD/YYYY or YYYY-MM-DD to a date object, or None."""
    if not date_str or date_str == "N/A":
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None


def filter_notices(notices, district=None, upcoming_only=False):
    today = date.today()
    results = []
    for n in notices:
        if district:
            hoods = DISTRICT_NEIGHBORHOODS.get(district, [])
            if not any(h.lower() in n["neighborhood"].lower() for h in hoods):
                continue
        if upcoming_only:
            hd = _parse_date_flexible(n.get("hearing_date", ""))
            exp = _parse_date_flexible(n.get("expiration", ""))
            # Keep if hearing date is future, or expiration is future (for PRJ notices)
            hd_ok = hd is not None and hd >= today
            exp_ok = exp is not None and exp >= today
            if not hd_ok and not exp_ok:
                continue
        results.append(n)
    return results


def format_notices(notices, district=None):
    if not notices:
        label = f"District {district}" if district else "SF"
        return f"No planning notices found for {label}."

    lines = []
    label = f"District {district}" if district else "all SF"
    lines.append(f"🏗️  SF PLANNING NOTICES — {label}")
    lines.append(f"   Source: sfplanning.org/notices")
    lines.append("")

    # Group by hearing body
    by_body = {}
    for n in notices:
        body = n["hearing_body"] or "Other"
        by_body.setdefault(body, []).append(n)

    order = [
        "Planning Commission",
        "Historic Preservation Commission",
        "Zoning Administrator (Variance)",
        "Section 311 Notice (no hearing)",
        "Other",
    ]

    for body in order:
        items = by_body.get(body, [])
        if not items:
            continue
        lines.append(f"  {'─'*50}")
        lines.append(f"  {body.upper()}")
        lines.append("")
        items.sort(key=lambda x: x.get("hearing_date") or x.get("expiration") or "")
        for n in items:
            hd = n.get("hearing_date", "")
            date_label = f"Hearing: {hd}" if hd and hd != "N/A" else f"Expires: {n.get('expiration','')}"
            lines.append(f"  📍 {n['address']}")
            lines.append(f"     Record: {n['record']}  |  {date_label}")
            if n["neighborhood"]:
                lines.append(f"     Neighborhood: {n['neighborhood']}")
            if n["contact_email"]:
                lines.append(f"     Contact: {n['contact_email']}")
            lines.append("")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SF Planning notices scraper")
    parser.add_argument("--district", type=int, help="Supervisorial district (1-11)")
    parser.add_argument("--upcoming", action="store_true", help="Upcoming hearings only")
    parser.add_argument("--json", action="store_true", dest="as_json", help="JSON output")
    args = parser.parse_args()

    district = args.district
    upcoming_only = args.upcoming
    as_json = args.as_json

    print("Fetching SF Planning notices...", file=sys.stderr)
    html = fetch_notices_html()
    if not html:
        print("Error: empty response from sfplanning.org/notices", file=sys.stderr)
        sys.exit(1)

    print("Parsing notices...", file=sys.stderr)
    notices = parse_notices(html)
    print(f"Found {len(notices)} total notices", file=sys.stderr)

    update_archive(notices)

    filtered = filter_notices(notices, district=district, upcoming_only=upcoming_only)
    print(f"After filtering: {len(filtered)} notices", file=sys.stderr)

    if as_json:
        print(json.dumps(filtered, indent=2))
    else:
        print(format_notices(filtered, district=district))


if __name__ == "__main__":
    main()
