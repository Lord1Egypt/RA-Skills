#!/usr/bin/env python3
"""
sf_311.py — SF 311 service request tracker for a supervisor district.

Queries the SF 311 Cases dataset (Socrata), groups by service category,
and flags unusual volume as neighborhood quality-of-life signals.

Data source: https://data.sfgov.org/resource/vw6y-z8j6.json

Notes on the dataset schema:
  - Date field is `requested_datetime` (not `opened`)
  - `supervisor_district` is stored as a float string, e.g. "5.0"
  - `service_name` is the category label

Usage:
  python3 sf_311.py                          # D5, last 7 days
  python3 sf_311.py --district 5             # explicit district
  python3 sf_311.py --days 30               # longer window
  python3 sf_311.py --category Encampment   # single category filter
  python3 sf_311.py --json                  # JSON output
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

try:
    from config_loader import get_district_config as _get_district_config
    _DEFAULT_DISTRICT = _get_district_config().get("district") or 5
except ImportError:
    _DEFAULT_DISTRICT = 5

ENDPOINT = "https://data.sfgov.org/resource/vw6y-z8j6.json"

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sf_311_archive.json")
ARCHIVE_MAX = 5000

PAGE_SIZE = 1000    # Socrata max per request
FETCH_LIMIT_BASE = 10000   # base cap for 7-day queries
FETCH_LIMIT_PER_DAY = 1500  # scale limit with query window

# Categories worth calling out explicitly — shown first, marked with ●
HIGHLIGHT_CATEGORIES = [
    "Encampment",
    "Homeless Concerns",
    "Illegal Dumping",
    "Graffiti",
    "Graffiti Public",
    "Graffiti Private",
    "Streetlights",
    "Street Defect",
    "Sidewalk and Curb",
    "Noise",
    "Tree Maintenance",
]

# High-volume but largely routine/administrative — excluded from spike alerts,
# shown in a separate section so they don't drown out QoL signals
ROUTINE_CATEGORIES = {
    "street and sidewalk cleaning",
    "parking enforcement",
    "litter receptacle maintenance",
    "mta parking traffic signs normal priority",
    "mta parking traffic signs high priority",
    "muni employee feedback",
    "muni service feedback",
    "rpd general",
    "general request",
}

# Spike threshold for a 7-day window; scaled proportionally for longer windows
SPIKE_BASE_THRESHOLD = 5
SPIKE_BASE_DAYS = 7


# ---------------------------------------------------------------------------
# Case archive
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
    with open(ARCHIVE_FILE, "w") as f:
        json.dump(archive, f, indent=2)


def update_archive(new_cases):
    """Merge new cases into the archive. Dedup by service_request_id. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_ids = {a["id"] for a in archive["items"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for case in new_cases:
        cid = case.get("service_request_id", "")
        if not cid or cid in existing_ids:
            continue
        entry = {
            "id": cid,
            "source": "sf_311",
            "scraped_at": now,
            "service_request_id": case.get("service_request_id"),
            "service_name": case.get("service_name"),
            "address": case.get("address"),
            "requested_datetime": case.get("requested_datetime"),
            "status_description": case.get("status_description"),
            "supervisor_district": case.get("supervisor_district"),
            "neighborhood": case.get("neighborhoods_sffind_boundaries") or case.get("analysis_neighborhood"),
            "lat": case.get("lat"),
            "long": case.get("long"),
        }
        archive["items"].append(entry)
        existing_ids.add(cid)
        added += 1
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    archive["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new cases ({len(archive['items'])} total)", file=sys.stderr)
    return archive


# ---------------------------------------------------------------------------
# API fetch
# ---------------------------------------------------------------------------

def fetch_requests(district: int, since_iso: str, category: str | None = None,
                   days: int = 7, until_iso: str | None = None) -> list[dict]:
    """
    Fetch 311 cases from SF Open Data, paginating as needed.
    Returns a flat list of case dicts.
    """
    where_clauses = [
        f"supervisor_district = '{float(district)}'",
        f"requested_datetime >= '{since_iso}'",
    ]
    if until_iso:
        where_clauses.append(f"requested_datetime < '{until_iso}'")
    if category:
        # Restrict to alphanumeric and spaces only to prevent SoQL injection.
        # Strip any character that isn't a letter, digit, or space, then
        # escape remaining single-quotes (belt-and-suspenders).
        import re as _re
        safe_cat = _re.sub(r"[^\w\s]", "", category.upper()).replace("'", "''")
        where_clauses.append(f"upper(service_name) like '%{safe_cat}%'")

    base_params = {
        "$where": " AND ".join(where_clauses),
        "$order": "requested_datetime DESC",
        "$limit": str(PAGE_SIZE),
    }

    # Scale fetch limit with query window to avoid truncation on long queries
    fetch_limit = max(FETCH_LIMIT_BASE, days * FETCH_LIMIT_PER_DAY)

    results = []
    offset = 0
    while True:
        params = dict(base_params)
        params["$offset"] = str(offset)
        url = ENDPOINT + "?" + urllib.parse.urlencode(params)

        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                page = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"HTTP error fetching 311 data: {e.code} {e.reason}", file=sys.stderr)
            break
        except Exception as e:
            print(f"Error fetching 311 data: {e}", file=sys.stderr)
            break

        results.extend(page)
        if len(page) < PAGE_SIZE:
            break   # last page
        offset += PAGE_SIZE
        if offset >= fetch_limit:
            print(f"Warning: hit fetch limit ({fetch_limit}), data may be incomplete.",
                  file=sys.stderr)
            break

    return results


# ---------------------------------------------------------------------------
# Data processing
# ---------------------------------------------------------------------------

def parse_dt(case: dict) -> datetime | None:
    raw = case.get("requested_datetime", "")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def normalize_category(case: dict) -> str:
    return (case.get("service_name") or "Unknown").strip()


def group_by_category(cases: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for c in cases:
        groups[normalize_category(c)].append(c)
    return dict(groups)


def spike_threshold(days: int) -> int:
    """Scale threshold proportionally with time window (capped at 3×)."""
    ratio = min(days / SPIKE_BASE_DAYS, 3.0)
    return max(SPIKE_BASE_THRESHOLD, int(SPIKE_BASE_THRESHOLD * ratio))


def recent_address(cases: list[dict]) -> str:
    for c in cases:
        addr = c.get("address", "").strip()
        if addr and addr.lower() not in ("", "none"):
            return addr
    return "—"


def most_recent_date(cases: list[dict]) -> str:
    for c in cases:
        dt = parse_dt(c)
        if dt:
            return dt.strftime("%Y-%m-%d")
    return "?"


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

SEPARATOR = "━" * 60


def format_summary(groups: dict[str, list[dict]], district: int, days: int,
                   total: int, threshold: int) -> str:
    lines = []
    lines.append(f"\n📞  SF 311 Service Requests — District {district} — Last {days} days")
    lines.append(f"    {total} total cases | spike threshold: >{threshold} reports\n")

    highlight_set = {h.lower() for h in HIGHLIGHT_CATEGORIES}

    def sort_key(name: str) -> tuple:
        nl = name.lower()
        is_routine = nl in ROUTINE_CATEGORIES
        in_highlight = nl in highlight_set
        tier = 0 if in_highlight else (2 if is_routine else 1)
        hl_idx = next(
            (i for i, h in enumerate(HIGHLIGHT_CATEGORIES) if h.lower() == nl),
            len(HIGHLIGHT_CATEGORIES),
        )
        return (tier, hl_idx, -len(groups[name]), name)

    sorted_cats = sorted(groups.keys(), key=sort_key)

    # Split into QoL spikes vs. routine spikes
    qol_spikes = [
        cat for cat in sorted_cats
        if len(groups[cat]) > threshold and cat.lower() not in ROUTINE_CATEGORIES
    ]
    routine_spikes = [
        cat for cat in sorted_cats
        if len(groups[cat]) > threshold and cat.lower() in ROUTINE_CATEGORIES
    ]

    # --- QoL spikes ---
    if qol_spikes:
        lines.append(SEPARATOR)
        lines.append(f"🚨  SPIKES — Quality-of-life signals (>{threshold} reports in {days} days)")
        lines.append(SEPARATOR)
        for cat in qol_spikes:
            cases = groups[cat]
            lines.append(f"  🔴 {cat}: {len(cases)} reports")
            lines.append(f"     Most recent: {recent_address(cases)} ({most_recent_date(cases)})")
        lines.append("")

    # --- Routine high-volume (informational, de-emphasized) ---
    if routine_spikes:
        lines.append(SEPARATOR)
        lines.append(f"📊  HIGH VOLUME — Routine/administrative (>{threshold} in {days} days)")
        lines.append(SEPARATOR)
        for cat in routine_spikes:
            lines.append(f"  · {cat}: {len(groups[cat])} reports")
        lines.append("")

    # --- Full category breakdown ---
    lines.append(SEPARATOR)
    lines.append("📋  ALL CATEGORIES")
    lines.append(SEPARATOR)

    for cat in sorted_cats:
        cases = groups[cat]
        count = len(cases)
        is_routine = cat.lower() in ROUTINE_CATEGORIES
        in_hl = cat.lower() in highlight_set
        is_spike = count > threshold

        flag = "" if is_routine else (" 🚨" if is_spike else "")
        bullet = "  ●" if in_hl else ("  ~" if is_routine else "  ·")
        lines.append(f"{bullet} {cat}: {count}{flag}")
        lines.append(f"       Latest: {recent_address(cases)} ({most_recent_date(cases)})")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

def build_json_output(groups: dict[str, list[dict]], district: int, days: int,
                      threshold: int, prior_groups: dict | None = None) -> dict:
    categories = []
    for cat, cases in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        count = len(cases)
        prior_count = len(prior_groups.get(cat, [])) if prior_groups is not None else None
        if prior_count is not None and prior_count > 0:
            pct = int(round((count - prior_count) / prior_count * 100))
            if pct > 5:
                trend = f"+{pct}%"
            elif pct < -5:
                trend = f"{pct}%"
            else:
                trend = "flat"
        elif prior_count == 0 and count > 0:
            trend = "new"
        else:
            trend = None
        categories.append({
            "service_name": cat,
            "category": cat,
            "count": count,
            "prior_count": prior_count,
            "trend": trend,
            "spike": count > threshold and cat.lower() not in ROUTINE_CATEGORIES,
            "routine": cat.lower() in ROUTINE_CATEGORIES,
            "most_recent_address": recent_address(cases),
            "most_recent_date": most_recent_date(cases),
            "cases": [
                {
                    "case_id": c.get("service_request_id"),
                    "address": c.get("address"),
                    "opened": c.get("requested_datetime"),
                    "status": c.get("status_description"),
                    "neighborhood": (
                        c.get("neighborhoods_sffind_boundaries")
                        or c.get("analysis_neighborhood")
                    ),
                    "lat": c.get("lat"),
                    "long": c.get("long"),
                }
                for c in cases[:5]
            ],
        })
    return {
        "district": district,
        "days": days,
        "spike_threshold": threshold,
        "total_cases": sum(len(v) for v in groups.values()),
        "prior_total_cases": sum(len(v) for v in prior_groups.values()) if prior_groups is not None else None,
        "categories": categories,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="SF 311 service request tracker — neighborhood quality-of-life signals"
    )
    parser.add_argument("--district", type=int, default=_DEFAULT_DISTRICT,
                        help=f"Supervisor district (default: {_DEFAULT_DISTRICT})")
    parser.add_argument("--days", type=int, default=7,
                        help="Look back N days (default: 7)")
    parser.add_argument("--category", type=str, default=None,
                        help="Filter to a single service category (partial match)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    args = parser.parse_args()

    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    since_iso = since.strftime("%Y-%m-%dT%H:%M:%S")
    threshold = spike_threshold(args.days)

    print(f"Fetching D{args.district} 311 cases since {since_iso[:10]}...", file=sys.stderr)
    cases = fetch_requests(args.district, since_iso, category=args.category, days=args.days)
    print(f"Got {len(cases)} cases from API", file=sys.stderr)
    update_archive(cases)

    if not cases:
        if args.json:
            print(json.dumps({"district": args.district, "days": args.days,
                               "total_cases": 0, "categories": []}))
        else:
            print(f"No 311 cases found for D{args.district} in the last {args.days} days.")
        return

    groups = group_by_category(cases)

    # Fetch prior period for trend comparison
    prior_groups = None
    if args.json:
        prior_since = datetime.now(timezone.utc) - timedelta(days=args.days * 2)
        prior_until = since
        prior_since_iso = prior_since.strftime("%Y-%m-%dT%H:%M:%S")
        prior_until_iso = prior_until.strftime("%Y-%m-%dT%H:%M:%S")
        print(f"Fetching prior period ({prior_since_iso[:10]} → {prior_until_iso[:10]})...", file=sys.stderr)
        try:
            prior_cases = fetch_requests(args.district, prior_since_iso, category=args.category,
                                         days=args.days, until_iso=prior_until_iso)
            prior_groups = group_by_category(prior_cases)
            print(f"Got {len(prior_cases)} prior-period cases", file=sys.stderr)
        except Exception as e:
            print(f"Warning: prior period fetch failed: {e}", file=sys.stderr)

    if args.json:
        out = build_json_output(groups, args.district, args.days, threshold, prior_groups)
        print(json.dumps(out, indent=2))
    else:
        print(format_summary(groups, args.district, args.days, len(cases), threshold))


if __name__ == "__main__":
    main()
