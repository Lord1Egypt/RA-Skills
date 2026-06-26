#!/usr/bin/env python3
"""
SF Civic Weekly Digest — orchestrates all civic data scripts into one report.

Usage:
  python3 sf_weekly_digest.py                    # D5, last 7 days
  python3 sf_weekly_digest.py --district 5       # explicit district
  python3 sf_weekly_digest.py --days 14          # longer window
  python3 sf_weekly_digest.py --brief            # short version for Telegram
  python3 sf_weekly_digest.py --json             # raw JSON from all sources
"""

import sys
import os
import json
import subprocess
from datetime import date, datetime

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Load district config for default district
try:
    from config_loader import get_district_config as _get_district_config
    _DISTRICT_CFG = _get_district_config()
    _DEFAULT_DISTRICT = _DISTRICT_CFG.get("district", 5)
except ImportError:
    _DEFAULT_DISTRICT = 5


def run_script(script_name, args=None, timeout=60):
    """Run a civic script with --json flag, return parsed output or None on failure."""
    cmd = [sys.executable, os.path.join(SCRIPTS_DIR, script_name), "--json"]
    if args:
        cmd.extend(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  {script_name} timed out", file=sys.stderr)
    except Exception as e:
        print(f"  ⚠️  {script_name} failed: {e}", file=sys.stderr)
    return None


def run_script_text(script_name, args=None, timeout=60):
    """Run a civic script, return raw text output."""
    cmd = [sys.executable, os.path.join(SCRIPTS_DIR, script_name)]
    if args:
        cmd.extend(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  {script_name} timed out", file=sys.stderr)
    except Exception as e:
        print(f"  ⚠️  {script_name} failed: {e}", file=sys.stderr)
    return None


def fmt_date(d=None):
    d = d or date.today()
    return d.strftime("%B %d, %Y")


def clean_allcaps(text):
    """Convert ALL CAPS or mostly-caps text to readable title case."""
    if not text:
        return text
    # Check if most alpha chars are uppercase
    alpha = [c for c in text if c.isalpha()]
    if not alpha:
        return text
    upper_ratio = sum(1 for c in alpha if c.isupper()) / len(alpha)
    if upper_ratio < 0.6:
        return text
    # Strip action prefixes commonly baked into SFMTA location fields
    import re
    text = re.sub(r'^(ESTABLISH|RESCIND|EXTEND|MODIFY|CONVERT|REMOVE|ADD)\s*[-–—]\s*', '', text, flags=re.IGNORECASE)
    # Title-case then fix common abbreviations
    result = text.title()
    for abbr in ["St", "Ave", "Blvd", "Dr", "Ct", "Pl", "Ln", "Rd", "Hwy"]:
        result = result.replace(f" {abbr} ", f" {abbr}. ")
    return result


def _shorten_item(text, max_len=80):
    """Shorten a Legistar item title to something readable."""
    import re
    # Strip boilerplate prefixes
    text = re.sub(r'^(Resolution|Ordinance)\s+(initiating|approving|amending)\s+', '', text, flags=re.IGNORECASE)
    # Strip assessor parcel references
    text = re.sub(r",?\s*Assessor's Parcel Block.*$", '', text)
    # Strip "making findings..." clauses
    text = re.sub(r';\s*making findings.*$', '', text)
    text = text.strip().rstrip('.')
    if len(text) > max_len:
        text = text[:max_len-1] + "…"
    return text


def _condense_items(items, limit=4):
    """Group similar items and return condensed list."""
    import re
    # Detect repeated patterns (e.g. many landmark designations)
    landmarks = [i for i in items if "landmark designation" in i.lower()]
    others = [i for i in items if "landmark designation" not in i.lower()]

    result = []
    if landmarks:
        # Extract addresses from landmark items
        addrs = []
        for lm in landmarks:
            m = re.search(r'located at ([^,]+)', lm)
            if m:
                addrs.append(m.group(1).strip())
        if len(landmarks) > 2:
            sample = ", ".join(addrs[:3])
            result.append(f"Landmark designations ({len(landmarks)} buildings): {sample}, …")
        else:
            for lm in landmarks:
                result.append(_shorten_item(lm))

    for item in others:
        if len(result) >= limit:
            remaining = len(others) - (limit - (1 if landmarks else 0))
            if remaining > 0:
                result.append(f"+ {remaining} more items")
            break
        result.append(_shorten_item(item))

    return result[:limit + 1]


def section_recap(district, days, brief):
    """LAST WEEK'S RECAP — what passed, what was amended at Board/committee meetings."""
    lines = []
    d_arg = ["--district", str(district)] if district else []
    data = run_script("sf_civic_digest.py", d_arg + ["--days", str(days)], timeout=90)
    if not data:
        return lines

    recap = data.get("recap", [])
    if not recap:
        return lines

    for meeting in recap:
        body = meeting.get("body", "?")
        mdate = meeting.get("date", "")
        items = meeting.get("relevant_items", [])
        actions = meeting.get("actions", {})
        action_summary = actions.get("summary", []) if isinstance(actions, dict) else []

        if not items:
            continue

        action_str = ", ".join(action_summary) if action_summary else ""
        lines.append(f"  📅 {body} — {mdate}" + (f" [{action_str}]" if action_str else ""))

        # Condense items: group similar ones (e.g. many landmark designations)
        condensed = _condense_items(items, limit=4 if not brief else 2)
        for item in condensed:
            lines.append(f"    • {item}")

    return lines


def section_hearings(district, days, brief):
    """THIS WEEK'S HEARINGS — Planning Commission, Board of Appeals, ZA"""
    lines = []
    d_arg = ["--district", str(district)] if district else []

    # Planning Commission (browser — use text mode, shorter timeout)
    pc = run_script_text("sf_planning_commission.py", d_arg + ["--next"], timeout=45)
    pc_has_items = False
    if pc:
        # Extract just the items, not the boilerplate
        item_lines = [l for l in pc.split('\n') if l.strip().startswith('Item') or '📍' in l or '→' in l]
        if item_lines:
            pc_has_items = True
            lines.append("🏛️ Planning Commission (Thu 12pm, City Hall Rm 400)")
            for l in item_lines[:6 if not brief else 3]:
                lines.append(f"  {l.strip()}")

    # If no upcoming PC items, check the Board recap for recent Planning Commission actions
    if not pc_has_items:
        legistar = run_script("sf_civic_digest.py", d_arg + ["--days", str(days)], timeout=90)
        if legistar:
            recap = legistar.get("recap", [])
            pc_recap = [m for m in recap if "planning" in m.get("body", "").lower()]
            if pc_recap:
                lines.append("🏛️ Planning Commission (recent)")
                for m in pc_recap[:2]:
                    for item in m.get("relevant_items", [])[:3]:
                        lines.append(f"  • {item[:70]}")
            else:
                lines.append("🏛️ Planning Commission — no D{} items this week".format(district or "?"))
        else:
            lines.append("🏛️ Planning Commission — no D{} items this week".format(district or "?"))

    # ZA hearings (no browser needed)
    za = run_script_text("sf_planning_commission.py", ["--body", "za"] + d_arg + ["--next"], timeout=30)
    if za and "no agenda" not in za.lower() and "no items" not in za.lower():
        za_items = [l for l in za.split('\n') if l.strip().startswith('Item') or '📍' in l]
        if za_items:
            lines.append("⚖️ Zoning Administrator (4th Wed 9:30am, City Hall Rm 408)")
            for l in za_items[:4 if not brief else 2]:
                lines.append(f"  {l.strip()}")

    # Board of Appeals
    boa = run_script_text("sf_board_of_appeals.py", ["--next"], timeout=45)
    if boa:
        boa_lines = [l for l in boa.split('\n') if any(k in l for k in ['Appeal', 'Jurisdiction', '📍', 'Wednesday'])]
        if boa_lines:
            lines.append("📋 Board of Appeals (next hearing)")
            for l in boa_lines[:3 if not brief else 2]:
                lines.append(f"  {l.strip()}")

    return lines


def section_housing_pipeline(district, days, brief):
    """HOUSING PIPELINE — streamlined approvals, major projects."""
    lines = []
    d_str = str(district) if district else "5"
    d_arg = ["--district", d_str]
    pipeline_days = str(max(days, 90))

    data = run_script("sf_housing_pipeline.py", d_arg + ["--days", pipeline_days], timeout=45)
    if not data:
        return lines

    streamlined = [p for p in data if p.get("tier") == "STREAMLINED"]
    major = [p for p in data if p.get("tier") == "MAJOR"]
    changes = [p for p in data if p.get("status_changed") and p.get("previous_status")]

    for p in (streamlined + major)[:5 if not brief else 3]:
        addr = p.get("address", "?")
        units = p.get("units_net", 0)
        pathway = p.get("pathway") or ""
        status = p.get("status", "")
        tags = []
        if p.get("new"):
            tags.append("🆕")
        if "approval" in status.lower() or "approved" in status.lower():
            tags.append("✅")
        if p.get("watchlist_match"):
            tags.append("📌")
        tag = " ".join(tags)
        detail = f"{pathway} — " if pathway else ""
        lines.append(f"  • {addr} ({units} units) {tag}")
        lines.append(f"    {detail}{status}")

    if changes:
        lines.append(f"  ⚡ {len(changes)} status change(s) since last run")

    return lines


def _load_hpc_watchlist():
    """Load the HPC landmark watchlist. Merges sf_hpc_watchlist.json with config."""
    watchlist_path = os.path.join(SCRIPTS_DIR, "sf_hpc_watchlist.json")
    result = {"watched_addresses": [], "watched_case_numbers": []}
    try:
        with open(watchlist_path) as f:
            result = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    # Merge watchlist addresses from config if present
    cfg_addrs = _DISTRICT_CFG.get("watchlist_addresses", [])
    cfg_cases = _DISTRICT_CFG.get("watchlist_case_numbers", [])
    existing_addrs = {a.upper() for a in result.get("watched_addresses", [])}
    for a in cfg_addrs:
        if a.upper() not in existing_addrs:
            result.setdefault("watched_addresses", []).append(a)
    existing_cases = set(result.get("watched_case_numbers", []))
    for c in cfg_cases:
        if c not in existing_cases:
            result.setdefault("watched_case_numbers", []).append(c)
    return result


def _matches_watchlist(item, watchlist):
    """Check if an HPC agenda item matches any watchlist address or case number."""
    addr = (item.get("address") or "").upper()
    record = (item.get("record") or "").upper()
    snippet = (item.get("body_snippet") or "").upper()

    for watched_addr in watchlist.get("watched_addresses", []):
        wa = watched_addr.upper()
        if wa in addr or wa in snippet:
            return True

    for watched_case in watchlist.get("watched_case_numbers", []):
        wc = watched_case.upper()
        if wc in record or wc in snippet:
            return True

    return False


def section_historic_preservation(district, days, brief):
    """HISTORIC PRESERVATION — HPC hearings, landmark designations, watchlist matches."""
    lines = []
    d_arg = ["--district", str(district)] if district else []

    # Fetch HPC hearings via the planning commission script with --body hpc
    hpc_data = run_script("sf_planning_commission.py", ["--body", "hpc"] + d_arg, timeout=60)
    if not hpc_data:
        return lines

    watchlist = _load_hpc_watchlist()
    has_watchlist = bool(watchlist.get("watched_addresses") or watchlist.get("watched_case_numbers"))

    for hearing in hpc_data:
        hdate = hearing.get("date", "")
        items = hearing.get("items", [])
        cancelled = hearing.get("cancelled", False)

        if cancelled:
            lines.append(f"  HPC hearing {hdate} — CANCELLED")
            continue

        if not items:
            lines.append(f"  Next HPC hearing: {hdate} (agenda not yet posted)")
            continue

        lines.append(f"  HPC hearing — {hdate}")

        watchlist_hits = []
        other_items = []

        for item in items:
            if has_watchlist and _matches_watchlist(item, watchlist):
                watchlist_hits.append(item)
            else:
                other_items.append(item)

        # Show watchlist matches first, flagged
        for item in watchlist_hits:
            codes_str = "/".join(item.get("codes", []))
            addr = item.get("address", "?")[:80]
            rec = item.get("recommendation", "")
            rec_str = f" -> {rec}" if rec else ""
            lines.append(f"  \U0001F4CC Item {item.get('number','')} [{codes_str}] {addr}{rec_str}")

        # Then other items (condensed)
        show_limit = 4 if not brief else 2
        for item in other_items[:show_limit]:
            codes_str = "/".join(item.get("codes", []))
            addr = item.get("address", "?")[:80]
            lines.append(f"  \u2022 Item {item.get('number','')} [{codes_str}] {addr}")

        remaining = len(other_items) - show_limit
        if remaining > 0:
            lines.append(f"  + {remaining} more items")

        if watchlist_hits:
            lines.append(f"  \u26a0\ufe0f {len(watchlist_hits)} watchlist match(es) — attend/comment!")

    return lines


def section_development(district, days, brief):
    """PLANNING & DEVELOPMENT — permits, planning notices"""
    lines = []
    d_str = str(district) if district else "5"
    d_arg = ["--district", d_str]

    # Building permits
    permits = run_script("sf_building_permits.py", d_arg + ["--days", str(days)], timeout=30)
    if permits:
        high = [p for p in permits if p.get("tier") == "HIGH"]
        notable = [p for p in permits if p.get("tier") == "NOTABLE"]
        if high:
            lines.append(f"🔴 High-interest permits ({len(high)}):")
            for p in high[:3 if not brief else 2]:
                raw_cost = p.get('estimated_cost')
                try:
                    cost_val = float(raw_cost) if raw_cost is not None else 0
                    cost = f"${cost_val/1e6:.1f}M" if cost_val > 1e6 else f"${cost_val:,.0f}" if cost_val > 0 else ""
                except (ValueError, TypeError):
                    cost = ""
                lines.append(f"  • {p.get('address','?')} — {p.get('description','')[:60]} {cost}")
        if notable and not brief:
            lines.append(f"🟡 Notable permits: {len(notable)} filed (alterations, signage, etc.)")

    # Planning notices
    notices = run_script("sf_planning_notices.py", d_arg, timeout=20)
    if notices:
        upcoming = [n for n in notices if n.get("hearing_date") and n.get("hearing_date") >= date.today().isoformat()]
        if upcoming:
            lines.append(f"📋 Planning notices with upcoming hearings ({len(upcoming)}):")
            for n in upcoming[:3 if not brief else 2]:
                lines.append(f"  • {n.get('address','?')} [{'/'.join(n.get('codes',[]))}] — {n.get('hearing_date','')}")

    return lines


def section_streets(district, days, brief):
    """STREET CHANGES — SFMTA Engineering Hearings"""
    lines = []
    d_arg = ["--district", str(district)] if district else []
    data = run_script("sfmta_hearings.py", d_arg, timeout=30)
    if not data:
        return lines

    for hearing in data[:1]:  # just next hearing
        items = hearing.get("items", [])
        if not items:
            continue
        hdate = hearing.get("date", "")
        lines.append(f"🚦 SFMTA Engineering Hearing — {hdate}")
        lines.append(f"   Join: sfmta.com/EngHearing | Comment deadline: day of hearing")
        for item in items[:4 if not brief else 2]:
            loc = item.get("location", "")
            desc = item.get("description", "")
            action = item.get("action", "").upper()

            # Convert ALL CAPS location/description to readable text
            loc = clean_allcaps(loc)

            # Build a plain-English summary: "Broderick St: parking changing to 4-hour meters Apr 3"
            action_verbs = {
                "ESTABLISH": "adding", "RESCIND": "removing", "EXTEND": "extending",
                "MODIFY": "modifying", "CONVERT": "converting to", "REMOVE": "removing",
                "ADD": "adding",
            }
            verb = action_verbs.get(action, action.lower())
            # Use description only if it adds info beyond the location
            short_desc = clean_allcaps(desc[:80]).rstrip('.') if desc else ""
            # Avoid duplicating when desc starts with same text as loc
            if short_desc and loc and short_desc.lower()[:20] != loc.lower()[:20]:
                lines.append(f"  • {loc}: {verb} — {short_desc}")
            elif loc:
                lines.append(f"  • {loc} ({verb})")
            else:
                lines.append(f"  • {verb}: {short_desc}")

    return lines



def section_transit(district, days, brief):
    """TRANSIT — SFMTA Board of Directors meetings and agenda items."""
    lines = []
    data = run_script("sf_sfmta_board.py", ["--past", "1"], timeout=45)
    if not data:
        return lines

    for meeting in data:
        mdate = meeting.get("date", "?")
        items = meeting.get("items", [])
        high_count = meeting.get("high_count", 0)

        if not items:
            # Future meeting, no agenda yet
            lines.append(f"  Next SFMTA Board: {mdate} 1pm, City Hall Rm 400 (agenda TBD)")
            break  # Only show one future meeting

        tag = f" -- {high_count} rider-impact items" if high_count else ""
        lines.append(f"  SFMTA Board {mdate}{tag}")
        high_items = [i for i in items if i.get("tier") == "high"]
        medium_items = [i for i in items if i.get("tier") == "medium"]
        for i in high_items[:3 if not brief else 2]:
            num = f"Item {i['item_number']}: " if i.get("item_number") else ""
            lines.append(f"    !!! {num}{i.get('title', '?')}")
        for i in medium_items[:3 if not brief else 1]:
            num = f"Item {i['item_number']}: " if i.get("item_number") else ""
            lines.append(f"    ** {num}{i.get('title', '?')}")

    return lines


def section_pulse(district, days, brief):
    """NEIGHBORHOOD PULSE — 311 spikes"""
    lines = []
    d_arg = ["--district", str(district)] if district else []
    data = run_script("sf_311.py", d_arg + ["--days", str(days)], timeout=60)
    if not data:
        return lines

    categories = data.get("categories", []) if isinstance(data, dict) else data
    spikes = [d for d in categories if d.get("spike")]
    if not spikes:
        return lines

    total = sum(s.get("count", 0) for s in spikes)
    lines.append(f"📞 311 spikes — {len(spikes)} categories, {total} reports in {days} days")
    # Top 4 by count
    top = sorted(spikes, key=lambda x: x.get("count", 0), reverse=True)[:4 if not brief else 3]
    for s in top:
        name = s.get("service_name") or s.get("category") or "?"
        lines.append(f"  • {name}: {s.get('count',0)} reports")
    return lines


def section_ethics(district, days, brief):
    """MONEY & POWER — lobbying, ethics notices"""
    lines = []
    sup_arg = ["--supervisor", str(district)] if district else []
    data = run_script("sf_ethics.py", sup_arg + ["--days", str(days)], timeout=30)
    if not data:
        return lines

    notices = data.get("notices", [])
    contacts = data.get("lobbyist_contacts", [])
    contributions = data.get("contributions", [])

    if contacts:
        lines.append(f"🔍 Lobbyist activity — {len(contacts)} contacts with D{district or '?'}/President:")
        for c in contacts[:3 if not brief else 2]:
            client = c.get("clientname", c.get("filer_name", c.get("firmname", "?")))[:30]
            official = c.get("officialname", c.get("official_name", "?"))[:20]
            topic = c.get("issue", c.get("subjectarea", c.get("subject", "?")))[:40]
            lines.append(f"  • {client} → {official}: {topic}")

    if notices and not brief:
        enforcement = [n for n in notices if "enforcement" in n.get("category", "").lower() or "fine" in n.get("title", "").lower()]
        if enforcement:
            lines.append(f"⚠️ Ethics enforcement: {enforcement[0].get('title','')[:60]}")

    if not lines and not brief:
        lines.append("⚖️ Ethics: no lobbying activity flagged this period")

    return lines


def section_journalism(district, days, brief):
    """JOURNALISM — recent stories from local outlets, with scope tags."""
    lines = []
    args = ["--days", str(days)]
    if district:
        args.extend(["--district", str(district)])
    data = run_script("sf_journalism.py", args, timeout=45)
    if not data:
        return lines

    articles = data if isinstance(data, list) else data.get("articles", [])
    if not articles:
        return lines

    from collections import Counter
    outlet_counts = Counter(a.get("outlet_name", "?") for a in articles)
    lines.append(f"📰 {len(articles)} stories from {len(outlet_counts)} outlets")
    outlet_summary = ", ".join(f"{name} ({n})" for name, n in outlet_counts.most_common())
    lines.append(f"   {outlet_summary}")

    # Show all article titles grouped by scope
    district_articles = [a for a in articles if a.get("scope") == "district"]
    citywide_articles = [a for a in articles if a.get("scope") != "district"]

    if district_articles:
        lines.append(f"  📍 Local ({len(district_articles)}):")
        show = 5 if not brief else 3
        for a in district_articles[:show]:
            lines.append(f"    • [{a.get('outlet_name','?')}] {a.get('title','?')[:75]}")
        if len(district_articles) > show:
            lines.append(f"    + {len(district_articles) - show} more")

    if citywide_articles and not brief:
        lines.append(f"  🌐 Citywide ({len(citywide_articles)}):")
        show = 3
        for a in citywide_articles[:show]:
            lines.append(f"    • [{a.get('outlet_name','?')}] {a.get('title','?')[:75]}")
        if len(citywide_articles) > show:
            lines.append(f"    + {len(citywide_articles) - show} more")

    return lines


def section_tenant(brief):
    """TENANT INFO — rent board"""
    lines = []
    data = run_script("sf_rent_board.py", ["--next"], timeout=45)
    if not data:
        # Fallback: link to Rent Board instead of hardcoding a rate that goes stale
        lines.append("🏠 Allowable rent increase: see https://sf.gov/departments/rent-board")
        lines.append("   (sf_rent_board.py unavailable — check site for current rate and next meeting)")
        return lines

    increase = data.get("allowable_rent_increase")
    if isinstance(increase, dict):
        increase = increase.get("percent")
    if increase:
        lines.append(f"🏠 Allowable rent increase: {increase} (through Feb 2027)")
    else:
        lines.append("🏠 Allowable rent increase: see https://sf.gov/departments/rent-board")
    meetings = data.get("meetings", [])
    if meetings:
        m = meetings[0]
        lines.append(f"   Next commission: {m.get('date','?')} {m.get('time','6pm')} — {m.get('location','25 Van Ness Rm 610')}")
    return lines


def section_parks(district, days, brief):
    """PARKS & OPEN SPACE — Rec & Park Commission meetings and agenda items."""
    lines = []
    data = run_script("sf_rec_park.py", ["--past", "1"], timeout=60)
    if not data:
        return lines

    for meeting in data:
        mdate = meeting.get("date", "?")
        items = meeting.get("items", [])
        high_count = meeting.get("high_count", 0)

        if not items:
            lines.append(f"  Next Rec & Park Commission: {mdate} (agenda TBD)")
            break

        tag = f" -- {high_count} district-relevant items" if high_count else ""
        lines.append(f"  Rec & Park Commission {mdate}{tag}")
        high_items = [i for i in items if i.get("tier") == "high"]
        medium_items = [i for i in items if i.get("tier") == "medium"]
        for i in high_items[:4 if not brief else 2]:
            lines.append(f"    !!! {i.get('title', '?')[:90]}")
        for i in medium_items[:3 if not brief else 1]:
            lines.append(f"    ** {i.get('title', '?')[:90]}")

    return lines


def section_volunteer_cleanups(district, brief):
    """VOLUNTEER CLEANUPS — upcoming community cleanups in the district."""
    lines = []
    d_arg = ["--district", str(district)] if district else []
    data = run_script("sf_volunteer_cleanups.py", d_arg + ["--days", "14"], timeout=20)
    if not data:
        return lines

    limit = 2 if brief else 4
    for event in data[:limit]:
        name = event.get("name", "Community Cleanup")
        date_display = event.get("date_display", "?")
        time_str = event.get("time", "")
        location = event.get("location", "")
        neighborhood = event.get("neighborhood", "")
        organizer = event.get("organizer", "")
        source = event.get("source", "")
        signup_url = event.get("signup_url", "")

        loc_str = f" @ {location}" if location else ""
        org_str = f" (org: {organizer})" if organizer and organizer != "SF Public Works" else ""
        lines.append(f"  🧹 {date_display}: {name} — {time_str}{loc_str}{org_str}")
        if signup_url and "mobilize.us" in signup_url:
            lines.append(f"     Sign up: {signup_url}")
        else:
            lines.append(f"     More info: refuserefusesf.org/cleanups")

    if len(data) > limit:
        lines.append(f"  + {len(data) - limit} more at refuserefusesf.org/cleanups")

    return lines


def section_evictions(district, brief):
    """EVICTIONS — displacement notices by type and neighborhood."""
    lines = []
    d_arg = ["--district", str(district)] if district else []
    data = run_script("sf_evictions.py", d_arg + ["--days", "30"], timeout=30)
    if not data or not isinstance(data, dict):
        return lines

    total = data.get("total_notices", 0)
    prior = data.get("prior_total", 0)
    trend = data.get("trend", "")
    if not total:
        return lines

    trend_str = f" ({trend})" if trend else ""
    lines.append(f"  {total} eviction notices in last 30 days{trend_str}" +
                 (f" vs {prior} prior period" if prior else ""))

    # Breakdown by type — highlight displacement signals
    by_type = data.get("by_type", [])
    displacement = [t for t in by_type if t.get("displacement_signal") and t.get("count", 0) > 0]
    for t in displacement[:3 if not brief else 2]:
        reason = t.get("reason", "?")
        count = t.get("count", 0)
        prior_count = t.get("prior_count", 0)
        t_trend = t.get("trend", "")
        t_str = f" {t_trend}" if t_trend else ""
        lines.append(f"  ⚠️  {reason}: {count}" + (f" (was {prior_count})" if prior_count else "") + t_str)

    # Top displacement notices (specific addresses)
    notices = data.get("displacement_notices", [])
    if notices and not brief:
        lines.append(f"  Recent displacement notices ({len(notices)}):")
        for n in notices[:3]:
            addr = n.get("address", "?")
            reasons = ", ".join(n.get("reasons", []))
            nhood = n.get("neighborhood", "")
            nhood_str = f" ({nhood})" if nhood else ""
            lines.append(f"    • {addr}{nhood_str} — {reasons}")

    return lines


def section_bart(brief):
    """BART — upcoming board meetings and agenda status."""
    lines = []
    data = run_script("sf_bart_board.py", ["--days", "14"], timeout=30)
    if not data or not isinstance(data, list):
        return lines

    upcoming = [m for m in data if m.get("tier") in ("upcoming", "soon", "HIGH", "MEDIUM") or
                m.get("agenda_status", "").lower() in ("posted", "draft")]
    show = upcoming[:2] if upcoming else data[:2]
    for m in show[:2 if not brief else 1]:
        body = m.get("body_name", "BART Board")
        mdate = m.get("date", "?")
        mtime = m.get("time", "")
        status = m.get("agenda_status", "")
        status_str = f" [{status}]" if status else ""
        lines.append(f"  🚇 {body} — {mdate} {mtime}{status_str}")
        agenda_url = m.get("agenda_url") or m.get("meeting_url")
        if agenda_url and not brief:
            lines.append(f"     {agenda_url}")

    return lines


def section_sfcta(brief):
    """SFCTA — SF County Transportation Authority meetings."""
    lines = []
    data = run_script("sf_sfcta.py", ["--days", "30"], timeout=45)
    if not data or not isinstance(data, list):
        return lines

    high = [m for m in data if m.get("relevance") == "HIGH" or m.get("high_count", 0) > 0]
    show = high[:2] if high else data[:1]
    for m in show[:2 if not brief else 1]:
        title = m.get("title", "SFCTA Meeting")
        mdate = m.get("date_display") or m.get("date", "?")
        high_count = m.get("high_count", 0)
        items = m.get("items", [])
        tag = f" — {high_count} notable items" if high_count else ""
        lines.append(f"  🚊 {title} — {mdate}{tag}")
        if items and not brief:
            for item in items[:2]:
                item_title = item.get("title", "") if isinstance(item, dict) else str(item)
                lines.append(f"    • {item_title[:80]}")
        elif not items:
            url = m.get("url", "")
            if url:
                lines.append(f"     {url}")

    return lines


def section_sfusd(brief):
    """SFUSD — School board meetings."""
    lines = []
    data = run_script("sf_sfusd_board.py", ["--days", "60"], timeout=30)
    if not data or not isinstance(data, list):
        return lines

    upcoming = [m for m in data if m.get("tier") in ("upcoming", "soon") or
                not m.get("tier")]  # default to showing if tier not set
    show = upcoming[:1] if upcoming else data[:1]
    for m in show:
        mtype = m.get("meeting_type", "Board Meeting")
        mdate = m.get("date", "?")
        mtime = m.get("time", "")
        notes = m.get("notes", "")
        notes_str = f" — {notes}" if notes and len(notes) < 60 else ""
        lines.append(f"  🏫 SFUSD {mtype} — {mdate} {mtime}{notes_str}")
        url = m.get("boarddocs_url") or m.get("granicus_url")
        if url and not brief:
            lines.append(f"     {url}")

    return lines


def section_coming_up(district, brief):
    """COMING UP — next key meetings"""
    lines = []
    d_arg = ["--district", str(district)] if district else []

    # Board of Supervisors from Legistar
    legistar = run_script("sf_civic_digest.py", d_arg + ["--days", "7"], timeout=90)
    if legistar:
        upcoming = legistar.get("upcoming", [])
        for m in upcoming[:3 if not brief else 2]:
            body = m.get("body", "?")
            dt = m.get("date", "")
            time = m.get("time", "")
            lines.append(f"  📅 {body} — {dt} {time}")

    return lines



def collect_all_data(district=None, days=7):
    district = district or _DEFAULT_DISTRICT
    """Collect raw JSON from all civic sources for AI-powered narration."""
    d_str = str(district)
    d_arg = ["--district", d_str]
    sup_arg = ["--supervisor", d_str]
    raw = {"district": district, "supervisor": get_supervisor(district),
           "date": date.today().isoformat(), "days": days}

    print("  Fetching Legistar (Board/committees)...", file=sys.stderr)
    raw["legistar"] = run_script("sf_civic_digest.py", d_arg + ["--days", str(days)], timeout=90)

    print("  Fetching building permits...", file=sys.stderr)
    raw["permits"] = run_script("sf_building_permits.py", d_arg + ["--days", str(days)], timeout=30)

    print("  Fetching planning notices...", file=sys.stderr)
    raw["planning_notices"] = run_script("sf_planning_notices.py", d_arg, timeout=20)

    print("  Fetching SFMTA hearings...", file=sys.stderr)
    raw["sfmta"] = run_script("sfmta_hearings.py", d_arg, timeout=30)

    print("  Fetching SFMTA Board...", file=sys.stderr)
    raw["sfmta_board"] = run_script("sf_sfmta_board.py", ["--past", "1"], timeout=45)

    print("  Fetching 311...", file=sys.stderr)
    raw["311"] = run_script("sf_311.py", d_arg + ["--days", str(days)], timeout=60)

    print("  Fetching ethics/lobbying...", file=sys.stderr)
    raw["ethics"] = run_script("sf_ethics.py", sup_arg + ["--days", str(days)], timeout=30)

    print("  Fetching rent board...", file=sys.stderr)
    raw["rent_board"] = run_script("sf_rent_board.py", ["--next"], timeout=45)

    print("  Fetching housing pipeline...", file=sys.stderr)
    raw["housing_pipeline"] = run_script("sf_housing_pipeline.py",
                                          d_arg + ["--days", str(max(days, 90))], timeout=45)

    print("  Fetching historic preservation (HPC)...", file=sys.stderr)
    raw["hpc"] = run_script("sf_planning_commission.py", ["--body", "hpc"] + d_arg, timeout=60)

    print("  Fetching parks (Rec & Park)...", file=sys.stderr)
    raw["rec_park"] = run_script("sf_rec_park.py", ["--past", "1"], timeout=60)

    print("  Fetching journalism...", file=sys.stderr)
    raw["journalism"] = run_script("sf_journalism.py", d_arg + ["--days", str(days)], timeout=45)

    print("  Fetching upcoming meetings...", file=sys.stderr)
    # Already in legistar, but fetch events separately
    raw["events"] = run_script("sfgov_events.py", d_arg, timeout=20)

    print("  Fetching volunteer cleanups...", file=sys.stderr)
    raw["volunteer_cleanups"] = run_script("sf_volunteer_cleanups.py", d_arg + ["--days", "14"], timeout=20)

    print("  Fetching civic actions (protests/rallies)...", file=sys.stderr)
    raw["civic_actions"] = run_script("sf_civic_actions.py", ["--days", "14"], timeout=30)

    print("  Fetching evictions...", file=sys.stderr)
    raw["evictions"] = run_script("sf_evictions.py", d_arg + ["--days", "14"], timeout=30)

    print("  Fetching BART Board...", file=sys.stderr)
    raw["bart"] = run_script("sf_bart_board.py", ["--days", "14"], timeout=30)

    print("  Fetching SFCTA...", file=sys.stderr)
    raw["sfcta"] = run_script("sf_sfcta.py", ["--days", "30"], timeout=45)

    print("  Fetching SFUSD Board...", file=sys.stderr)
    raw["sfusd"] = run_script("sf_sfusd_board.py", ["--days", "14"], timeout=30)

    return raw


def build_digest(district=None, days=7, brief=False):
    district = district or _DEFAULT_DISTRICT
    today = fmt_date()
    lines = []
    lines.append(f"🏛️ SF CIVIC DIGEST — Week of {today}")
    if district:
        lines.append(f"   District {district} | Supervisor: {get_supervisor(district)}")
    lines.append("")

    # ── DISTRICT-SPECIFIC SECTIONS ──────────────────────────────────────

    print("  Fetching housing pipeline...", file=sys.stderr)
    hp = section_housing_pipeline(district, days, brief)
    if hp:
        lines.append("🏠 HOUSING PIPELINE")
        lines.extend(hp)
        lines.append("")

    print("  Fetching development...", file=sys.stderr)
    dev = section_development(district, days, brief)
    if dev:
        lines.append("🏗️ PLANNING & DEVELOPMENT")
        lines.extend(dev)
        lines.append("")

    print("  Fetching historic preservation...", file=sys.stderr)
    hpc = section_historic_preservation(district, days, brief)
    if hpc:
        lines.append("🏛️ HISTORIC PRESERVATION")
        lines.extend(hpc)
        lines.append("")

    print("  Fetching street changes...", file=sys.stderr)
    st = section_streets(district, days, brief)
    if st:
        lines.append("🚦 STREET CHANGES")
        lines.extend(st)
        lines.append("")

    print("  Fetching 311...", file=sys.stderr)
    pulse = section_pulse(district, days, brief)
    if pulse:
        lines.append("📞 NEIGHBORHOOD PULSE")
        lines.extend(pulse)
        lines.append("")

    print("  Fetching ethics...", file=sys.stderr)
    eth = section_ethics(district, days, brief)
    if eth:
        lines.append("⚖️ MONEY & POWER")
        lines.extend(eth)
        lines.append("")

    # ── CITYWIDE SECTIONS ───────────────────────────────────────────────

    lines.append("━" * 50)
    lines.append("🌐 CITYWIDE")
    lines.append("")

    print("  Fetching last week's recap...", file=sys.stderr)
    recap = section_recap(district, days, brief)
    if recap:
        lines.append("📜 BOARD RECAP")
        lines.extend(recap)
        lines.append("")

    print("  Fetching hearings...", file=sys.stderr)
    h = section_hearings(district, days, brief)
    if h:
        lines.append("📋 HEARINGS")
        lines.extend(h)
        lines.append("")

    print("  Fetching SFMTA Board...", file=sys.stderr)
    transit = section_transit(district, days, brief)
    if transit:
        lines.append("🚌 SFMTA BOARD")
        lines.extend(transit)
        lines.append("")

    print("  Fetching rent board...", file=sys.stderr)
    tenant = section_tenant(brief)
    if tenant:
        lines.append("🏠 TENANT INFO")
        lines.extend(tenant)
        lines.append("")

    print("  Fetching parks...", file=sys.stderr)
    parks = section_parks(district, days, brief)
    if parks:
        lines.append("🌳 PARKS & OPEN SPACE")
        lines.extend(parks)
        lines.append("")

    print("  Fetching evictions...", file=sys.stderr)
    evictions = section_evictions(district, brief)
    if evictions:
        lines.append("🏚️ EVICTIONS")
        lines.extend(evictions)
        lines.append("")

    print("  Fetching BART Board...", file=sys.stderr)
    bart = section_bart(brief)
    if bart:
        lines.append("🚇 BART")
        lines.extend(bart)
        lines.append("")

    print("  Fetching SFCTA...", file=sys.stderr)
    sfcta = section_sfcta(brief)
    if sfcta:
        lines.append("🚊 TRANSPORTATION AUTHORITY")
        lines.extend(sfcta)
        lines.append("")

    print("  Fetching SFUSD...", file=sys.stderr)
    sfusd = section_sfusd(brief)
    if sfusd:
        lines.append("🏫 SCHOOL BOARD")
        lines.extend(sfusd)
        lines.append("")

    print("  Fetching volunteer cleanups...", file=sys.stderr)
    cleanups = section_volunteer_cleanups(district, brief)
    if cleanups:
        lines.append("🧹 VOLUNTEER CLEANUPS")
        lines.extend(cleanups)
        lines.append("")

    # ── JOURNALISM (district + citywide combined) ───────────────────────

    print("  Fetching journalism...", file=sys.stderr)
    news = section_journalism(district, days, brief)
    if news:
        lines.append("📰 JOURNALISM")
        lines.extend(news)
        lines.append("")

    if not brief:
        print("  Fetching upcoming...", file=sys.stderr)
        coming = section_coming_up(district, brief)
        if coming:
            lines.append("📅 COMING UP")
            lines.extend(coming)
            lines.append("")

    return "\n".join(lines)


SUPERVISOR_MAP = {
    1: "Connie Chan", 2: "Stephen Sherrill", 3: "Danny Sauter",
    4: "Alan Wong", 5: "Bilal Mahmood", 6: "Matt Dorsey",
    7: "Myrna Melgar", 8: "Rafael Mandelman", 9: "Jackie Fielder",
    10: "Shamann Walton", 11: "Chyanne Chen",
}

def get_supervisor(district):
    return SUPERVISOR_MAP.get(district, "")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SF Civic Weekly Digest — orchestrates all civic data scripts")
    parser.add_argument("--district", type=int, help="Supervisorial district (1-11)")
    parser.add_argument("--days", type=int, default=7, help="Look-back/look-ahead window in days")
    parser.add_argument("--brief", action="store_true", help="Short version for Telegram")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Raw JSON from all sources (for AI narration)")
    args = parser.parse_args()

    district = args.district or _DEFAULT_DISTRICT
    days = args.days
    brief = args.brief
    as_json = args.as_json

    print(f"Building SF Civic Digest (D{district}, {days} days)...", file=sys.stderr)

    if as_json:
        raw = collect_all_data(district=district, days=days)
        print(json.dumps(raw, indent=2, default=str))
    else:
        digest = build_digest(district=district, days=days, brief=brief)
        print(digest)


if __name__ == "__main__":
    main()
