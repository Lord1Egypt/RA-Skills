#!/usr/bin/env python3
"""
SF Board of Appeals hearing scraper (API-based).

Fetches upcoming Board of Appeals hearings from the sf.gov Wagtail CMS API,
extracts agenda items directly from meeting records (individual item PDFs),
and filters by supervisor district.

Board of Appeals meets on the 1st and 3rd Wednesdays, 5pm, Room 416 City Hall.

Usage:
  python3 sf_board_of_appeals.py                  # all upcoming hearings
  python3 sf_board_of_appeals.py --district 5     # filter to D5 items
  python3 sf_board_of_appeals.py --next           # next hearing only
  python3 sf_board_of_appeals.py --json           # JSON output
"""

import sys
import re
import json
import os
import urllib.request
import urllib.error
from datetime import date, datetime, timezone

BOA_MEETINGS_API = "https://api.sf.gov/api/v2/pages/?type=sf.Meeting&search=board+of+appeals&limit=10&order=-id&locale=en&fields=*"
BOA_DETAIL_API = "https://api.sf.gov/api/v2/pages/{id}/"

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sf_board_of_appeals_archive.json")
ARCHIVE_MAX = 5000

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

# Appeal types we recognize
APPEAL_TYPES = {
    "appeal": "Appeal",
    "jurisdiction": "Jurisdiction Request",
    "rehearing": "Rehearing Request",
    "revocation": "Revocation Hearing",
    "variance": "Variance Appeal",
    "permit": "Permit Appeal",
    "minutes": "Adoption of Minutes",
    "public comment": "Public Comment",
    "commissioner": "Commissioner Comments",
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


def update_archive(hearings):
    """Merge new hearings into the archive. Dedup by URL. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_ids = {a["id"] for a in archive["items"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for hearing in hearings:
        hid = hearing["url"]
        if hid not in existing_ids:
            entry = {
                "id": hid,
                "source": "sf_board_of_appeals",
                "scraped_at": now,
                "body": hearing.get("body"),
                "date": hearing.get("date"),
                "hearing_date": hearing.get("hearing_date"),
                "time": hearing.get("time"),
                "location": hearing.get("location"),
                "url": hearing["url"],
                "agenda_pdf": hearing.get("agenda_pdf"),
                "items": hearing.get("items", []),
            }
            archive["items"].append(entry)
            existing_ids.add(hid)
            added += 1
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new hearings ({len(archive['items'])} total)", file=sys.stderr)
    return archive


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def api_get(url):
    """Fetch JSON from a URL using urllib. Returns parsed dict or None."""
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError) as e:
        print(f"  API error for {url}: {e}", file=sys.stderr)
        return None


def fetch_meetings():
    """
    Fetch upcoming Board of Appeals meetings from the Wagtail API.
    Returns list of meeting dicts from the API.
    """
    data = api_get(BOA_MEETINGS_API)
    if not data or "items" not in data:
        return []
    return data["items"]


def extract_location(meeting):
    """Extract location string from meeting_location array."""
    locations = meeting.get("meeting_location", [])
    parts = []
    for loc in locations:
        if loc.get("type") == "address":
            val = loc.get("value", {})
            addr_parts = [val.get("line1", ""), val.get("line2", "")]
            city = val.get("city", "")
            state = val.get("state", "")
            zip_code = val.get("zip", "")
            addr = ", ".join(p for p in addr_parts if p)
            if city:
                addr += f", {city}"
            if state:
                addr += f", {state}"
            if zip_code:
                addr += f" {zip_code}"
            if addr:
                parts.append(addr)
    return parts[0] if parts else "City Hall, Room 416"


def extract_zoom_info(meeting):
    """Extract Zoom link, phone, and meeting ID from meeting_location."""
    zoom_link = ""
    zoom_phone = ""
    zoom_id = ""
    locations = meeting.get("meeting_location", [])
    for loc in locations:
        if loc.get("type") == "online":
            val = loc.get("value", {})
            link_info = val.get("link", {})
            if isinstance(link_info, dict):
                zoom_link = link_info.get("url", "")
            phones = val.get("phone", [])
            if phones:
                phone_val = phones[0].get("value", {})
                zoom_phone = phone_val.get("phone_number", "")
                details = phone_val.get("details", "")
                # Try to extract meeting ID from details
                id_m = re.search(r'Meeting\s+ID:\s*([\d\s]+)', details, re.IGNORECASE)
                if id_m:
                    zoom_id = id_m.group(1).strip()
    # Also try extracting meeting ID from the zoom link itself
    if zoom_link and not zoom_id:
        id_m = re.search(r'/j/(\d+)', zoom_link)
        if id_m:
            zoom_id = id_m.group(1)
    return zoom_link, zoom_phone, zoom_id


def extract_date_time(meeting):
    """Extract date and time strings from date_time array. Returns (date_str, time_str, date_obj)."""
    date_times = meeting.get("date_time", [])
    if not date_times:
        return "", "5:00 pm", None

    val = date_times[0].get("value", {})
    start_date = val.get("start_date", "")
    start_time = val.get("start_time", "")
    end_time = val.get("end_time", "")

    date_obj = None
    date_str = ""
    if start_date:
        try:
            date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            date_str = date_obj.strftime("%A, %B %-d, %Y")
        except ValueError:
            date_str = start_date

    time_str = ""
    if start_time:
        try:
            t = datetime.strptime(start_time, "%H:%M:%S")
            time_str = t.strftime("%-I:%M %p").lower()
        except ValueError:
            time_str = start_time
    if not time_str:
        time_str = "5:00 pm"

    return date_str, time_str, date_obj


def extract_agenda_pdf(meeting):
    """Extract main agenda PDF URL from agenda or related_documents."""
    # Try agenda items first — look for one whose title includes "agenda"
    agenda = meeting.get("agenda", [])
    if agenda:
        # The first agenda item's documents often contain the main agenda PDF
        first_docs = agenda[0].get("value", {}).get("documents", [])
        for doc in first_docs:
            doc_val = doc.get("value", {})
            title = doc_val.get("title", "").lower()
            file_url = doc_val.get("file", "")
            if file_url and ("agenda" in title or not title.startswith("item")):
                return file_url

    # Try related_documents
    for rd in meeting.get("related_documents", []):
        docs = rd.get("value", {}).get("documents", [])
        for doc in docs:
            doc_val = doc.get("value", {})
            title = doc_val.get("title", "").lower()
            file_url = doc_val.get("file", "")
            if file_url and "agenda" in title:
                return file_url

    return ""


def extract_items_from_agenda(meeting):
    """
    Extract agenda items from the meeting's agenda array.
    Each agenda entry has value.title_and_text.title (the item text) and
    value.documents (list of PDFs for that item).
    Returns list of dicts: {text, href}
    """
    items = []
    agenda = meeting.get("agenda", [])
    for entry in agenda:
        val = entry.get("value", {})
        title_text_block = val.get("title_and_text", {})
        title = title_text_block.get("title", "")
        body_text = title_text_block.get("text", "")

        if not title:
            continue

        # Get the first document PDF for this item if available
        docs = val.get("documents", [])
        href = ""
        if docs:
            first_doc = docs[0].get("value", {})
            href = first_doc.get("file", "")

        # Only include items that look like agenda items (start with "Item" or contain appeal-related text)
        title_lower = title.lower()
        if (title_lower.startswith("item") or
            "appeal" in title_lower or
            "jurisdiction" in title_lower or
            "rehearing" in title_lower or
            "revocation" in title_lower):
            items.append({"text": title, "href": href})

    return items


def parse_item_from_text(item_text, item_href):
    """
    Parse an agenda item from its title text and any document link.

    Title text examples:
      "Item 4A and 4B Appeal Nos. 25-056 at 850 Corbett Avenue"
      "Item 5, Jurisdiction Request No. 26-1 at 158 15th Avenue"
      "Item 6, Appeal No. 26-008 at 460-462 Vallejo"
      "Item 7. Appeal No. 25-059 at 3446 Balboa Street"
      "Item 4A and 4B Appeal Nos. 25-056 at 850 Corbett Avenue (This matter has been rescheduled to April 15, 2026)"

    Returns dict: number, type, appeal_no, address, description, pdf_url, notes
    """
    item = {
        "number": "",
        "type": "",
        "appeal_no": "",
        "address": "",
        "description": item_text,
        "pdf_url": item_href,
        "notes": "",
    }

    # Extract item number: "Item 4A", "Item 5", "Item 4A and 4B"
    num_m = re.match(r'Item\s+([0-9]+[A-Za-z]*(?:\s+and\s+[0-9]+[A-Za-z]*)?)', item_text, re.IGNORECASE)
    if num_m:
        item["number"] = num_m.group(1).strip()

    # Determine type
    text_lower = item_text.lower()
    if "appeal" in text_lower and "jurisdiction" not in text_lower:
        item["type"] = "Appeal"
    elif "jurisdiction" in text_lower:
        item["type"] = "Jurisdiction Request"
    elif "rehearing" in text_lower:
        item["type"] = "Rehearing Request"
    elif "revocation" in text_lower:
        item["type"] = "Revocation Hearing"
    elif "minutes" in text_lower:
        item["type"] = "Minutes"
        return item  # Skip further parsing for minutes
    else:
        item["type"] = "Other"

    # Extract appeal/case number: "Appeal No. 25-059", "Appeal Nos. 25-056", "No. 26-1"
    appeal_m = re.search(r'(?:Appeal\s+Nos?\.|Jurisdiction\s+Request\s+No\.|No\.)\s*([\d]{2,4}-\d+)', item_text, re.IGNORECASE)
    if appeal_m:
        item["appeal_no"] = appeal_m.group(1)

    # Extract address -- typically after "at " keyword
    addr_m = re.search(r'\bat\s+(.+?)(?:\s*\(|$)', item_text, re.IGNORECASE)
    if addr_m:
        addr = addr_m.group(1).strip()
        # Clean up trailing punctuation
        addr = re.sub(r'[,\.\s]+$', '', addr)
        item["address"] = addr

    # Extract parenthetical notes directly from the title text
    # e.g., "(This matter has been rescheduled to April 15, 2026)"
    note_m = re.search(r'\(([^)]{10,})\)', item_text)
    if note_m:
        note = note_m.group(1).strip()
        if not note.lower().startswith('subject to'):
            item["notes"] = note

    return item


def is_relevant(item, district):
    """Check if an item is relevant to a given district."""
    if district is None:
        return True
    kws = DISTRICT_KEYWORDS.get(district, [])
    text = (
        item.get("address", "") + " " +
        item.get("description", "") + " " +
        item.get("notes", "")
    ).lower()
    return any(kw in text for kw in kws)


def format_hearing(hearing, district=None):
    """Format a single hearing for human-readable output."""
    lines = []
    lines.append(f"\n{'─'*55}")
    lines.append(f"⚖️  SF BOARD OF APPEALS")
    lines.append(f"   {hearing.get('date', 'date unknown')}  {hearing.get('time', '5:00 pm')}")
    lines.append(f"   {hearing.get('location', 'City Hall, Room 416')}")

    zoom = hearing.get("zoom_link", "")
    zoom_phone = hearing.get("zoom_phone", "")
    zoom_id = hearing.get("zoom_id", "")
    if zoom:
        lines.append(f"   🔗 Zoom: {zoom}")
    if zoom_phone and zoom_id:
        lines.append(f"      Phone: {zoom_phone}  ID: {zoom_id}")

    agenda_pdf = hearing.get("agenda_pdf", "")
    if agenda_pdf:
        lines.append(f"   📄 Agenda: {agenda_pdf}")

    lines.append(f"   🌐 {hearing.get('url', '')}")

    items = hearing.get("items", [])
    if not items:
        lines.append("\n   (no agenda items posted yet)")
        return "\n".join(lines)

    # Filter items for display
    show_items = [i for i in items if is_relevant(i, district)] if district else items

    # Skip administrative items when filtering by district
    if district:
        show_items = [i for i in show_items if i.get("type") not in ("Minutes", "Other")]

    if not show_items:
        lines.append(f"\n   (no District {district} items)")
    else:
        lines.append("")
        for item in show_items:
            num = item.get("number", "?")
            itype = item.get("type", "")
            appeal_no = item.get("appeal_no", "")
            address = item.get("address", "")
            notes = item.get("notes", "")
            pdf = item.get("pdf_url", "")

            type_str = f" [{itype}]" if itype else ""
            appeal_str = f" No. {appeal_no}" if appeal_no else ""
            notes_str = f"\n     ⚠️  {notes}" if notes else ""

            lines.append(f"  Item {num}{type_str}{appeal_str}")
            if address:
                lines.append(f"  📍 {address}")
            if notes_str:
                lines.append(f"     ⚠️  {notes}")
            if pdf:
                lines.append(f"     📎 {pdf}")
            lines.append("")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SF Board of Appeals scraper")
    parser.add_argument("--district", type=int, help="Supervisorial district (1-11)")
    parser.add_argument("--next", action="store_true", dest="next_only", help="Next meeting only")
    parser.add_argument("--json", action="store_true", dest="as_json", help="JSON output")
    args = parser.parse_args()

    district = args.district
    next_only = args.next_only
    as_json = args.as_json

    today = date.today()

    print("Fetching Board of Appeals meetings from sf.gov API...", file=sys.stderr)
    meetings = fetch_meetings()
    print(f"Found {len(meetings)} meetings from API", file=sys.stderr)

    if not meetings:
        print("No meetings found from API.", file=sys.stderr)
        sys.exit(1)

    hearings = []
    for meeting in meetings:
        # Check if cancelled
        if meeting.get("cancelled", False):
            continue

        # Extract date/time
        date_str, time_str, date_obj = extract_date_time(meeting)

        # Skip past meetings
        if date_obj and date_obj < today:
            continue

        # Get the sf.gov page URL (API returns http://api.sf.gov/..., fix to https://www.sf.gov/...)
        meta = meeting.get("meta", {})
        url = meta.get("html_url", "")
        url = re.sub(r'^https?://api\.sf\.gov/', 'https://www.sf.gov/', url)

        print(f"  Processing: {meeting.get('title', 'unknown')}", file=sys.stderr)

        # Extract location and zoom info
        location = extract_location(meeting)
        zoom_link, zoom_phone, zoom_id = extract_zoom_info(meeting)

        # Extract agenda PDF
        agenda_pdf = extract_agenda_pdf(meeting)

        # Extract and parse agenda items
        raw_items = extract_items_from_agenda(meeting)
        parsed_items = []
        for raw in raw_items:
            item = parse_item_from_text(raw.get("text", ""), raw.get("href", ""))
            parsed_items.append(item)

        hearing = {
            "body": "Board of Appeals",
            "date": date_str,
            "hearing_date": date_obj.isoformat() if date_obj else "",
            "time": time_str,
            "location": location,
            "zoom_link": zoom_link,
            "zoom_phone": zoom_phone,
            "zoom_id": zoom_id,
            "agenda_pdf": agenda_pdf,
            "url": url,
            "items": parsed_items,
        }
        hearings.append(hearing)

        if next_only:
            break

    # Sort by date
    hearings.sort(key=lambda h: h.get("hearing_date", ""))

    # Archive
    update_archive(hearings)

    if as_json:
        print(json.dumps(hearings, indent=2))
        return

    if not hearings:
        label = f"District {district}" if district else "SF"
        print(f"No upcoming Board of Appeals hearings found for {label}.")
        return

    label = f"District {district}" if district else "all districts"
    print(f"\n⚖️  SF BOARD OF APPEALS — UPCOMING HEARINGS ({label})")
    for h in hearings:
        print(format_hearing(h, district=district))


if __name__ == "__main__":
    main()
