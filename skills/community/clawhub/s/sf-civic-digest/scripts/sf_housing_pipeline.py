#!/usr/bin/env python3
"""
sf_housing_pipeline.py — SF housing development pipeline tracker.

Monitors AB 2011, SB 35, SB 423, State Density Bonus, and other streamlined
housing approvals that bypass discretionary review (Planning Commission, Board
of Supervisors). Also tracks large projects (50+ units) via any pathway.

Data source: SF Planning Dept Records - Projects (Socrata qvu5-m3a2)
District lookup: SF Parcels - Active (Socrata acdm-wktn)

Usage:
  python3 sf_housing_pipeline.py                     # D5, 90 days
  python3 sf_housing_pipeline.py --district 5 --days 90
  python3 sf_housing_pipeline.py --json              # JSON output
  python3 sf_housing_pipeline.py --streamlined-only  # only AB 2011 / SB 35 etc.
  python3 sf_housing_pipeline.py --all-districts     # citywide
  python3 sf_housing_pipeline.py --watch "469 STEVENSON"  # add to watchlist
  python3 sf_housing_pipeline.py --no-state          # skip state (testing)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

try:
    import urllib.request
    import urllib.parse
    import urllib.error
except ImportError:
    pass

try:
    from config_loader import get_district_config as _get_district_config
    _DEFAULT_DISTRICT = _get_district_config().get("district") or 5
except ImportError:
    _DEFAULT_DISTRICT = 5

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PROJECTS_ENDPOINT = "https://data.sfgov.org/resource/qvu5-m3a2.json"
PARCELS_ENDPOINT = "https://data.sfgov.org/resource/acdm-wktn.json"
STATE_FILE = os.path.join(os.path.dirname(__file__), "sf_housing_pipeline_state.json")
ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), "sf_housing_pipeline_archive.json")
ARCHIVE_MAX = 5000

# Keywords in description that indicate streamlined/ministerial approval pathway
STREAMLINED_KEYWORDS = [
    "AB 2011",
    "AB2011",
    "SB 35",
    "SB35",
    "SB 423",
    "SB423",
    "Housing Sustainability District",
    "HSD",
    "Builder's Remedy",
    "Builders Remedy",
]

# Statuses grouped for transition detection
APPROVED_STATUSES = {
    "closed - approval ltr issued",
    "closed - approved",
    "approved",
}
TERMINAL_STATUSES = {
    "closed",
    "closed - complete",
    "withdrawn",
    "closed - withdrawn",
    "closed - cancelled",
    "cancelled",
}
ACTIVE_STATUSES = {
    "under review",
    "pending review",
    "open",
    "on hold",
}

UNIT_THRESHOLD_MAJOR = 50
UNIT_THRESHOLD_NOTABLE = 10


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
    return {"projects": {}, "block_lot_districts": {}, "watchlist": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# Archive management
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


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def socrata_query(endpoint, params, timeout=30):
    """Query a Socrata endpoint. Returns list of dicts or []."""
    url = endpoint + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}", file=sys.stderr)
        return []


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def fetch_streamlined_projects():
    """Query A: All projects with streamlined pathway keywords or density bonus.

    Uses two queries to avoid Socrata URL length limits with many OR clauses.
    """
    # Query A1: AB 2011, SB 35, SB 423, density bonus
    results_1 = socrata_query(PROJECTS_ENDPOINT, {
        "$where": (
            "upper(description) like '%AB 2011%' OR "
            "upper(description) like '%SB 35%' OR "
            "upper(description) like '%SB 423%' OR "
            "state_density_bonus_individual='CHECKED'"
        ),
        "$order": "open_date DESC",
        "$limit": "200",
    })

    # Query A2: HSD, Builder's Remedy (less common, separate query)
    results_2 = socrata_query(PROJECTS_ENDPOINT, {
        "$where": (
            "upper(description) like '%HOUSING SUSTAINABILITY DISTRICT%' OR "
            "upper(description) like '%BUILDER%REMEDY%'"
        ),
        "$order": "open_date DESC",
        "$limit": "100",
    })

    # Merge and dedup
    seen = {r.get("record_id") for r in results_1}
    for r in results_2:
        if r.get("record_id") not in seen:
            results_1.append(r)
            seen.add(r.get("record_id"))

    return results_1


def fetch_large_projects(since_date):
    """Query B: Projects with 10+ net units filed since a date."""
    return socrata_query(PROJECTS_ENDPOINT, {
        "$where": f"number_of_units_net > {UNIT_THRESHOLD_NOTABLE} AND open_date >= '{since_date}'",
        "$order": "number_of_units_net DESC",
        "$limit": "200",
    })


def lookup_districts(block_lot_pairs, state):
    """Look up supervisor districts for block/lot pairs, using cache."""
    cache = state.get("block_lot_districts", {})
    result = {}
    to_fetch = []

    for block, lot in block_lot_pairs:
        key = f"{block}-{lot}"
        if key in cache:
            result[key] = cache[key]
        else:
            to_fetch.append((block, lot))

    if to_fetch:
        # Batch query — build OR clauses, limit to 40 per call
        for i in range(0, len(to_fetch), 40):
            batch = to_fetch[i:i + 40]
            clauses = [f"(block_num='{b}' AND lot_num='{l}')" for b, l in batch]
            where = " OR ".join(clauses)
            rows = socrata_query(PARCELS_ENDPOINT, {
                "$where": where,
                "$select": "block_num,lot_num,supervisor_district",
                "$limit": "200",
            })
            for row in rows:
                key = f"{row.get('block_num', '')}-{row.get('lot_num', '')}"
                dist = row.get("supervisor_district")
                if dist:
                    try:
                        result[key] = int(dist)
                        cache[key] = int(dist)
                    except (ValueError, TypeError):
                        pass

    state["block_lot_districts"] = cache
    return result


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def detect_pathway(project):
    """Detect streamlined approval pathway from description."""
    desc = (project.get("description") or "").upper()
    pathways = []
    if "AB 2011" in desc or "AB2011" in desc:
        pathways.append("AB 2011")
    if "SB 35" in desc or "SB35" in desc:
        pathways.append("SB 35")
    if "SB 423" in desc or "SB423" in desc:
        pathways.append("SB 423")
    if "HOUSING SUSTAINABILITY DISTRICT" in desc or "HSD" in desc:
        pathways.append("HSD")
    if "BUILDER" in desc and "REMEDY" in desc:
        pathways.append("Builder's Remedy")

    # State density bonus (field-level, not description)
    if project.get("state_density_bonus_individual") == "CHECKED":
        pathways.append("State Density Bonus")

    return pathways


def classify_project(project, pathways, watchlist_match):
    """Classify project into tier: STREAMLINED, MAJOR, NOTABLE, or SKIP."""
    units = _safe_float(project.get("number_of_units_net"))

    if pathways:
        return "STREAMLINED"
    if units >= UNIT_THRESHOLD_MAJOR:
        return "MAJOR"
    if units >= UNIT_THRESHOLD_NOTABLE or watchlist_match:
        return "NOTABLE"
    return "SKIP"


def detect_status_change(project, state):
    """Compare current status against stored state. Returns (changed, prev_status)."""
    rid = project.get("record_id", "")
    current = (project.get("record_status") or "").lower()
    prev_data = state.get("projects", {}).get(rid)
    if prev_data is None:
        return True, None  # new project
    prev = (prev_data.get("status") or "").lower()
    if prev != current:
        return True, prev_data.get("status")
    return False, prev_data.get("status")


def matches_watchlist(project, watchlist):
    """Check if project address matches any watchlist entry."""
    addr = (project.get("project_address") or "").upper()
    name = (project.get("project_name") or "").upper()
    for entry in watchlist:
        e = entry.upper()
        if e in addr or e in name:
            return True
    return False


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def _safe_float(val):
    try:
        return float(val) if val is not None else 0.0
    except (ValueError, TypeError):
        return 0.0


def _safe_int(val):
    return int(_safe_float(val))


def format_date(raw):
    if not raw:
        return "?"
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return raw[:10]


def format_units(project):
    net = _safe_int(project.get("number_of_units_net"))
    market = _safe_int(project.get("number_of_market_rate_units") or project.get("number_market_rate_units_1"))
    affordable = _safe_int(project.get("number_of_affordable_units") or project.get("number_affordable_units_prop"))
    parts = [f"{net} units"]
    if market and affordable:
        parts.append(f"{market} market + {affordable} affordable")
    elif affordable:
        parts.append(f"{affordable} affordable")
    return " (".join(parts) + ")" if len(parts) > 1 else parts[0]


def format_project_text(project, tier, pathways, changed, prev_status, district, watchlist_match):
    emoji = {"STREAMLINED": "🔴", "MAJOR": "🟡", "NOTABLE": "⚪"}.get(tier, "")
    addr = project.get("project_address") or project.get("project_name") or "Unknown"
    status = project.get("record_status") or "?"
    rid = project.get("record_id") or ""
    units = format_units(project)
    open_date = format_date(project.get("open_date"))
    close_date = format_date(project.get("close_date"))
    planner = project.get("assigned_to_planner") or ""
    pim_raw = project.get("pim_link") or ""
    pim = pim_raw.get("url", "") if isinstance(pim_raw, dict) else str(pim_raw)

    # Status tags
    tags = []
    if changed and prev_status is None:
        tags.append("🆕")
    is_approved = status.lower() in APPROVED_STATUSES
    if is_approved:
        tags.append("APPROVED")
    if watchlist_match:
        tags.append("📌 WATCHED")
    tag_str = " ".join(tags)
    if tag_str:
        tag_str = " " + tag_str

    lines = [f"{emoji} **{addr}**{tag_str}"]
    if pathways:
        lines.append(f"   Pathway: {' + '.join(pathways)}")
    lines.append(f"   Units: {units}")
    lines.append(f"   Status: {status}")
    if changed and prev_status:
        lines.append(f"   ⚡ Changed from: {prev_status}")
    if close_date != "?":
        lines.append(f"   Filed: {open_date} | Closed: {close_date}")
    else:
        lines.append(f"   Filed: {open_date}")
    if district:
        lines.append(f"   District: {district}")
    if planner:
        lines.append(f"   Planner: {planner}")
    lines.append(f"   Case: {rid}")
    if pim:
        lines.append(f"   PIM: {pim}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="SF housing pipeline tracker")
    parser.add_argument("--district", type=int, default=_DEFAULT_DISTRICT,
                        help=f"Supervisor district (default: {_DEFAULT_DISTRICT})")
    parser.add_argument("--days", type=int, default=90,
                        help="Look back N days for large projects (default: 90)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--streamlined-only", action="store_true",
                        help="Only show AB 2011 / SB 35 / HSD pathway projects")
    parser.add_argument("--all-districts", action="store_true",
                        help="Show all districts (skip district filter)")
    parser.add_argument("--no-state", action="store_true",
                        help="Don't load/save state (for testing)")
    parser.add_argument("--mark-seen", action="store_true",
                        help="Update state file after run")
    parser.add_argument("--watch", type=str,
                        help="Add an address to the watchlist")
    args = parser.parse_args()

    # State
    state = load_state() if not args.no_state else {"projects": {}, "block_lot_districts": {}, "watchlist": []}
    watchlist = state.get("watchlist", [])

    # Handle --watch
    if args.watch:
        entry = args.watch.strip().upper()
        if entry not in [w.upper() for w in watchlist]:
            watchlist.append(args.watch.strip())
            state["watchlist"] = watchlist
            save_state(state)
            print(f"Added '{args.watch}' to watchlist.", file=sys.stderr)
        else:
            print(f"'{args.watch}' already on watchlist.", file=sys.stderr)

    # Fetch
    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    since_str = since.strftime("%Y-%m-%dT00:00:00")

    print("Fetching streamlined projects...", file=sys.stderr)
    streamlined = fetch_streamlined_projects()
    print(f"  Got {len(streamlined)} streamlined/density bonus projects", file=sys.stderr)

    if not args.streamlined_only:
        print(f"Fetching large projects (last {args.days} days)...", file=sys.stderr)
        large = fetch_large_projects(since_str)
        print(f"  Got {len(large)} large projects", file=sys.stderr)
    else:
        large = []

    # Merge and deduplicate by record_id
    seen_ids = set()
    all_projects = []
    for p in streamlined + large:
        rid = p.get("record_id", "")
        if rid not in seen_ids:
            seen_ids.add(rid)
            all_projects.append(p)

    print(f"  {len(all_projects)} unique projects after dedup", file=sys.stderr)

    # Archive raw projects
    now = datetime.now(timezone.utc).isoformat()
    archive_records = []
    for project in all_projects:
        archive_records.append({
            "id": project.get("record_id", ""),
            "source": "sf_housing_pipeline",
            "scraped_at": now,
            "record_id": project.get("record_id"),
            "project_name": project.get("project_name"),
            "project_address": project.get("project_address"),
            "description": project.get("description"),
            "record_status": project.get("record_status"),
            "number_of_units_net": project.get("number_of_units_net"),
            "number_of_affordable_units": project.get("number_of_affordable_units"),
            "state_density_bonus_individual": project.get("state_density_bonus_individual"),
            "open_date": project.get("open_date"),
            "close_date": project.get("close_date"),
            "block": project.get("block"),
            "lot": project.get("lot"),
        })
    update_archive(archive_records)

    # District lookup
    if not args.all_districts:
        block_lot_pairs = []
        for p in all_projects:
            b, l = p.get("block", ""), p.get("lot", "")
            if b and l:
                block_lot_pairs.append((b, l))

        print(f"Looking up districts for {len(block_lot_pairs)} parcels...", file=sys.stderr)
        district_map = lookup_districts(block_lot_pairs, state)
    else:
        district_map = {}

    # Filter out bad/placeholder addresses
    all_projects = [
        p for p in all_projects
        if not (p.get("project_address") or "").startswith("0 UNKNOWN")
    ]

    # Classify and filter
    results = []
    for p in all_projects:
        pathways = detect_pathway(p)
        wl_match = matches_watchlist(p, watchlist)
        tier = classify_project(p, pathways, wl_match)
        if tier == "SKIP" and not wl_match:
            continue

        # District filter
        bl_key = f"{p.get('block', '')}-{p.get('lot', '')}"
        district = district_map.get(bl_key)
        if not args.all_districts:
            # Watchlist items always pass
            if not wl_match and district != args.district:
                continue

        changed, prev_status = detect_status_change(p, state)

        results.append({
            "project": p,
            "tier": tier,
            "pathways": pathways,
            "district": district,
            "changed": changed,
            "prev_status": prev_status,
            "watchlist_match": wl_match,
        })

    # Flag duplicate address filings (e.g. redesigned projects with old+new records)
    addr_counts = {}
    for r in results:
        addr = (r["project"].get("project_address") or "").upper().strip()
        if addr:
            addr_counts[addr] = addr_counts.get(addr, 0) + 1
    for r in results:
        addr = (r["project"].get("project_address") or "").upper().strip()
        r["duplicate_address"] = addr_counts.get(addr, 1) > 1

    # Sort: STREAMLINED first, then MAJOR, then NOTABLE; changed first within tier
    tier_order = {"STREAMLINED": 0, "MAJOR": 1, "NOTABLE": 2}
    results.sort(key=lambda r: (tier_order.get(r["tier"], 9), 0 if r["changed"] else 1))

    # Output
    if args.json:
        output = []
        for r in results:
            p = r["project"]
            output.append({
                "record_id": p.get("record_id"),
                "project_name": p.get("project_name"),
                "address": p.get("project_address"),
                "description": p.get("description"),
                "pathway": " + ".join(r["pathways"]) if r["pathways"] else None,
                "streamlined": bool(r["pathways"]),
                "tier": r["tier"],
                "status": p.get("record_status"),
                "status_changed": r["changed"],
                "previous_status": r["prev_status"],
                "units_net": _safe_int(p.get("number_of_units_net")),
                "units_affordable": _safe_int(p.get("number_of_affordable_units") or p.get("number_affordable_units_prop")),
                "district": r["district"],
                "open_date": format_date(p.get("open_date")),
                "close_date": format_date(p.get("close_date")),
                "planner": p.get("assigned_to_planner"),
                "pim_url": p.get("pim_link", {}).get("url", "") if isinstance(p.get("pim_link"), dict) else p.get("pim_link"),
                "new": r["changed"] and r["prev_status"] is None,
                "watchlist_match": r["watchlist_match"],
                "duplicate_address": r.get("duplicate_address", False),
                "block": p.get("block"),
                "lot": p.get("lot"),
            })
        print(json.dumps(output, indent=2))
    else:
        dist_label = f"District {args.district}" if not args.all_districts else "all districts"
        if not results:
            print(f"No housing pipeline projects found for {dist_label}.")
        else:
            streamlined_r = [r for r in results if r["tier"] == "STREAMLINED"]
            major_r = [r for r in results if r["tier"] == "MAJOR"]
            notable_r = [r for r in results if r["tier"] == "NOTABLE"]

            print(f"\n🏠  SF Housing Pipeline — {dist_label}")
            print(f"   {len(results)} projects tracked | {len(streamlined_r)} streamlined | {len(major_r)} major | {len(notable_r)} notable")
            print()

            if streamlined_r:
                print(f"━━ 🔴 STREAMLINED APPROVALS ({len(streamlined_r)}) ━━━━━━━━━━━━━━━━━━━━")
                for r in streamlined_r:
                    print(format_project_text(
                        r["project"], r["tier"], r["pathways"],
                        r["changed"], r["prev_status"], r["district"], r["watchlist_match"]
                    ))
                    print()

            if major_r:
                print(f"━━ 🟡 MAJOR PROJECTS — 50+ units ({len(major_r)}) ━━━━━━━━━━━━━━━━━━")
                for r in major_r:
                    print(format_project_text(
                        r["project"], r["tier"], r["pathways"],
                        r["changed"], r["prev_status"], r["district"], r["watchlist_match"]
                    ))
                    print()

            if notable_r:
                print(f"━━ ⚪ NOTABLE ({len(notable_r)}) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                for r in notable_r:
                    print(format_project_text(
                        r["project"], r["tier"], r["pathways"],
                        r["changed"], r["prev_status"], r["district"], r["watchlist_match"]
                    ))
                    print()

            # Status changes summary
            changes = [r for r in results if r["changed"] and r["prev_status"] is not None]
            if changes:
                print("━━ ⚡ STATUS CHANGES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                for r in changes:
                    p = r["project"]
                    addr = p.get("project_address") or "?"
                    units = _safe_int(p.get("number_of_units_net"))
                    pathway = " + ".join(r["pathways"]) if r["pathways"] else ""
                    print(f"  ⚡ {addr}: {r['prev_status']} → {p.get('record_status')} ({units} units{', ' + pathway if pathway else ''})")
                print()

    # Update state
    if not args.no_state and args.mark_seen:
        for r in results:
            p = r["project"]
            rid = p.get("record_id", "")
            if rid:
                state.setdefault("projects", {})[rid] = {
                    "name": p.get("project_address") or p.get("project_name"),
                    "status": p.get("record_status"),
                    "units_net": _safe_int(p.get("number_of_units_net")),
                    "pathway": " + ".join(r["pathways"]) if r["pathways"] else None,
                    "district": r["district"],
                    "first_seen": state.get("projects", {}).get(rid, {}).get(
                        "first_seen", datetime.now(timezone.utc).isoformat()
                    ),
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                }
        save_state(state)
        print(f"State updated: {len(state['projects'])} projects tracked.", file=sys.stderr)

    return results


if __name__ == "__main__":
    main()
