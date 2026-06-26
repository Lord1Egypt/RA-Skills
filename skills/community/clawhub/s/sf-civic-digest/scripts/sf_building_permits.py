#!/usr/bin/env python3
"""
sf_building_permits.py — SF building permit tracker for a supervisor district.

Queries the SF Open Data building permits dataset (Socrata), filters by
district, surfaces new/interesting activity for neighborhood tracking.

Data source: https://data.sfgov.org/resource/i98e-djp9.json
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

ENDPOINT = "https://data.sfgov.org/resource/i98e-djp9.json"
STATE_FILE = os.path.join(os.path.dirname(__file__), "sf_permits_state.json")
ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), "sf_building_permits_archive.json")
ARCHIVE_MAX = 5000

# Permit types that are always interesting regardless of cost
HIGH_INTEREST_TYPES = {
    "new construction wood frame",
    "new construction",
    "demolitions",
}

# Permit types that are interesting when large
MEDIUM_INTEREST_TYPES = {
    "additions alterations or repairs",
    "otc alterations permit",
    "sign-errect",
}

# Permit type keywords that are mostly noise (electrical/plumbing/mechanical)
NOISE_KEYWORDS = [
    "electrical",
    "plumbing",
    "mechanical",
    "boiler",
    "elevator",
    "sprinkler",
]

COST_THRESHOLD_NOISE = 5_000       # skip permits under this if noisy type
COST_THRESHOLD_INTERESTING = 100_000  # flag as "large" above this


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
    return {"seen_permits": {}}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# Permit archive
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


def update_archive(permits):
    """Merge new permits into the archive. Dedup by permit_number. Cap at ARCHIVE_MAX."""
    archive = load_archive()
    existing_ids = {a["id"] for a in archive["items"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for permit in permits:
        pid = permit.get("permit_number", "")
        if not pid or pid in existing_ids:
            continue
        entry = {
            "id": pid,
            "source": "sf_building_permits",
            "scraped_at": now,
            "permit_number": permit.get("permit_number"),
            "permit_type": permit.get("permit_type_definition") or permit.get("permit_type"),
            "description": permit.get("description"),
            "status": permit.get("status"),
            "estimated_cost": permit.get("estimated_cost"),
            "street_number": permit.get("street_number"),
            "street_name": permit.get("street_name"),
            "street_suffix": permit.get("street_suffix"),
            "supervisor_district": permit.get("supervisor_district"),
            "permit_creation_date": permit.get("permit_creation_date"),
            "block": permit.get("block"),
            "lot": permit.get("lot"),
        }
        archive["items"].append(entry)
        existing_ids.add(pid)
        added += 1
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new permits ({len(archive['items'])} total)", file=sys.stderr)
    return archive


# ---------------------------------------------------------------------------
# API fetch
# ---------------------------------------------------------------------------

def fetch_permits(district: int, since_date: str, limit: int = 1000) -> list:
    """Fetch permits from SF Open Data for a given district since a date."""
    params = {
        "supervisor_district": str(district),
        "$where": f"permit_creation_date >= '{since_date}'",
        "$order": "permit_creation_date DESC",
        "$limit": str(limit),
    }
    url = ENDPOINT + "?" + urllib.parse.urlencode(params)

    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP error fetching permits: {e.code} {e.reason}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error fetching permits: {e}", file=sys.stderr)
        return []


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_permit(p: dict) -> tuple[str, bool]:
    """
    Returns (tier, is_new_to_state) where tier is one of:
      'high'    — new construction or demolition
      'medium'  — large alteration / signage
      'low'     — small routine permit
      'noise'   — filter out
    """
    ptype = (p.get("permit_type_definition") or p.get("permit_type") or "").lower()
    desc = (p.get("description") or "").lower()
    cost_raw = p.get("estimated_cost")
    try:
        cost = float(cost_raw) if cost_raw is not None else 0.0
    except (ValueError, TypeError):
        cost = 0.0

    # Pure noise: electrical/plumbing/mechanical with low cost
    for kw in NOISE_KEYWORDS:
        if kw in ptype or kw in desc:
            if cost < COST_THRESHOLD_NOISE:
                return "noise", False
            # Even if big, flag as low interest (infrastructure, not construction)
            return "low", False

    # High interest regardless of cost
    for ht in HIGH_INTEREST_TYPES:
        if ht in ptype:
            return "high", False

    # Medium interest types
    for mt in MEDIUM_INTEREST_TYPES:
        if mt in ptype:
            if cost >= COST_THRESHOLD_INTERESTING:
                return "high", False  # large alteration → bump to high
            if cost >= COST_THRESHOLD_NOISE:
                return "medium", False
            return "noise", False  # tiny OTC permit → skip

    # Fallback: keep if cost >= threshold
    if cost >= COST_THRESHOLD_NOISE:
        return "medium", False

    return "noise", False


def is_new_permit(p: dict, state: dict) -> bool:
    permit_num = p.get("permit_number", "")
    return permit_num not in state.get("seen_permits", {})


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_address(p: dict) -> str:
    parts = [
        p.get("street_number", ""),
        p.get("street_name", ""),
        p.get("street_suffix", ""),
    ]
    return " ".join(x for x in parts if x).strip() or "Unknown address"


def format_cost(p: dict) -> str:
    cost_raw = p.get("estimated_cost")
    try:
        cost = float(cost_raw)
        if cost >= 1_000_000:
            return f"${cost/1_000_000:.1f}M"
        elif cost >= 1_000:
            return f"${cost/1_000:.0f}k"
        else:
            return f"${cost:.0f}"
    except (ValueError, TypeError):
        return "cost unknown"


def format_date(p: dict) -> str:
    raw = p.get("permit_creation_date", "")
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return raw[:10] if raw else "?"


def format_permit_text(p: dict, tier: str, new: bool) -> str:
    addr = format_address(p)
    cost = format_cost(p)
    date = format_date(p)
    ptype = p.get("permit_type_definition") or p.get("permit_type") or "unknown type"
    desc = p.get("description") or ""
    permit_num = p.get("permit_number", "")
    status = p.get("status", "")

    # Tier emoji
    emoji = {"high": "🔴", "medium": "🟡", "low": "⚪"}.get(tier, "")
    new_tag = " 🆕" if new else ""

    lines = [
        f"{emoji} **{addr}**{new_tag}",
        f"   Type: {ptype}",
    ]
    if desc:
        lines.append(f"   Desc: {desc[:120]}")
    lines.append(f"   Cost: {cost} | Filed: {date} | Status: {status}")
    if permit_num:
        lines.append(f"   Permit: {permit_num}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="SF building permit tracker")
    parser.add_argument("--district", type=int, default=_DEFAULT_DISTRICT,
                        help=f"Supervisor district number (default: {_DEFAULT_DISTRICT})")
    parser.add_argument("--days", type=int, default=7,
                        help="Look back N days (default: 7)")
    parser.add_argument("--all", action="store_true",
                        help="Include small/noise permits too")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--no-state", action="store_true",
                        help="Don't load/save state file (for testing)")
    parser.add_argument("--mark-seen", action="store_true",
                        help="Mark all fetched permits as seen in state")
    args = parser.parse_args()

    # Date range
    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    since_str = since.strftime("%Y-%m-%dT00:00:00")

    # State
    state = load_state() if not args.no_state else {"seen_permits": {}}

    # Fetch
    print(f"Fetching D{args.district} permits since {since_str[:10]}...", file=sys.stderr)
    raw_permits = fetch_permits(args.district, since_str)
    print(f"Got {len(raw_permits)} permits from API", file=sys.stderr)

    # Archive
    update_archive(raw_permits)

    # Classify
    results = []
    for p in raw_permits:
        tier, _ = classify_permit(p)
        new = is_new_permit(p, state)
        results.append({
            "permit": p,
            "tier": tier,
            "new": new,
        })

    # Filter
    if not args.all:
        results = [r for r in results if r["tier"] != "noise"]

    # Sort: high first, then medium, then low; new first within tier
    tier_order = {"high": 0, "medium": 1, "low": 2, "noise": 3}
    results.sort(key=lambda r: (tier_order[r["tier"]], 0 if r["new"] else 1))

    # Output
    if args.json:
        output = []
        for r in results:
            p = r["permit"]
            output.append({
                "permit_number": p.get("permit_number"),
                "address": format_address(p),
                "type": p.get("permit_type_definition") or p.get("permit_type"),
                "description": p.get("description"),
                "cost": p.get("estimated_cost"),
                "date": format_date(p),
                "status": p.get("status"),
                "tier": r["tier"],
                "new": r["new"],
                "block": p.get("block"),
                "lot": p.get("lot"),
            })
        print(json.dumps(output, indent=2))
    else:
        if not results:
            print(f"No permits found for D{args.district} in the last {args.days} days.")
        else:
            high = [r for r in results if r["tier"] == "high"]
            medium = [r for r in results if r["tier"] == "medium"]
            low = [r for r in results if r["tier"] == "low"]
            noise_count = sum(1 for _, _ in [(p, c) for p in raw_permits
                                              for c in [classify_permit(p)[0]]
                                              if c == "noise"])

            print(f"\n🏗️  SF Building Permits — District {args.district} — Last {args.days} days")
            print(f"   {len(raw_permits)} total permits | {len(results)} shown | ~{noise_count} filtered")
            print()

            if high:
                print(f"━━ 🔴 HIGH INTEREST ({len(high)}) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                for r in high:
                    print(format_permit_text(r["permit"], r["tier"], r["new"]))
                    print()

            if medium:
                print(f"━━ 🟡 NOTABLE ({len(medium)}) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                for r in medium:
                    print(format_permit_text(r["permit"], r["tier"], r["new"]))
                    print()

            if low and args.all:
                print(f"━━ ⚪ LOW INTEREST ({len(low)}) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                for r in low:
                    print(format_permit_text(r["permit"], r["tier"], r["new"]))
                    print()

    # Update state
    if not args.no_state and args.mark_seen:
        for r in results:
            p = r["permit"]
            permit_num = p.get("permit_number", "")
            if permit_num:
                state.setdefault("seen_permits", {})[permit_num] = {
                    "address": format_address(p),
                    "date": format_date(p),
                    "type": p.get("permit_type_definition"),
                    "seen_at": datetime.now(timezone.utc).isoformat(),
                }
        save_state(state)
        print(f"State updated: {len(state['seen_permits'])} permits tracked.", file=sys.stderr)

    return results


if __name__ == "__main__":
    main()
