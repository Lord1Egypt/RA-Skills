#!/usr/bin/env python3
"""
sf_evictions.py — SF eviction notice tracker for a supervisor district.

Queries the SF Eviction Notices dataset (Socrata) for recent filings,
groups by eviction type, computes trend vs. prior period, and flags
displacement signals (Ellis Act, Owner Move-In).

Data source: https://data.sfgov.org/resource/5cei-gny5.json
Dataset: Eviction Notices — San Francisco Rent Board

Schema notes:
  - `file_date` is the eviction filing date
  - `supervisor_district` is stored as a string ("5"), but may appear as "5.0"
  - Eviction reasons are boolean columns: `ellis_act_withdrawal`, `owner_move_in`,
    `breach`, `nuisance`, `non_payment`, `illegal_use`, `demolition`, etc.
  - `neighborhood` and `address` are text fields
  - `eviction_id` is the unique identifier (e.g. "M260550")
  - `constraints_date` indicates elderly/disabled tenant protections

Usage:
  python3 sf_evictions.py                        # D5, last 30 days
  python3 sf_evictions.py --district 5           # explicit district
  python3 sf_evictions.py --days 60              # longer window
  python3 sf_evictions.py --json                 # JSON output
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

ENDPOINT = "https://data.sfgov.org/resource/5cei-gny5.json"

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_FILE = os.path.join(SCRIPTS_DIR, "sf_evictions_archive.json")
ARCHIVE_MAX = 5000

PAGE_SIZE = 1000    # Socrata max per request
FETCH_LIMIT = 10000

# Eviction reason columns — order matters for display priority
EVICTION_REASONS = [
    ("ellis_act_withdrawal", "Ellis Act"),
    ("owner_move_in", "Owner Move-In"),
    ("non_payment", "Non-Payment"),
    ("breach", "Breach"),
    ("nuisance", "Nuisance"),
    ("illegal_use", "Illegal Use"),
    ("failure_to_sign_renewal", "Failure to Sign Renewal"),
    ("access_denial", "Access Denial"),
    ("unapproved_subtenant", "Unapproved Subtenant"),
    ("demolition", "Demolition"),
    ("capital_improvement", "Capital Improvement"),
    ("substantial_rehab", "Substantial Rehab"),
    ("condo_conversion", "Condo Conversion"),
    ("roommate_same_unit", "Roommate Same Unit"),
    ("late_payments", "Late Payments"),
    ("lead_remediation", "Lead Remediation"),
    ("development", "Development"),
    ("good_samaritan_ends", "Good Samaritan Ends"),
    ("other_cause", "Other"),
]

# These are the displacement signals — called out prominently
DISPLACEMENT_REASONS = {"ellis_act_withdrawal", "owner_move_in"}

# ---------------------------------------------------------------------------
# Archive
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


def update_archive(new_records):
    """Merge new eviction notices into the archive. Dedup by eviction_id."""
    archive = load_archive()
    existing_ids = {a["id"] for a in archive["items"]}
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for rec in new_records:
        eid = rec.get("eviction_id", "")
        if not eid or eid in existing_ids:
            continue
        entry = {
            "id": eid,
            "source": "sf_evictions",
            "scraped_at": now,
            "eviction_id": eid,
            "address": rec.get("address"),
            "neighborhood": rec.get("neighborhood"),
            "file_date": rec.get("file_date"),
            "supervisor_district": rec.get("supervisor_district"),
            "constraints_date": rec.get("constraints_date"),
            "reasons": classify_reasons(rec),
        }
        archive["items"].append(entry)
        existing_ids.add(eid)
        added += 1
    if len(archive["items"]) > ARCHIVE_MAX:
        archive["items"] = archive["items"][-ARCHIVE_MAX:]
    archive["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_archive(archive)
    if added:
        print(f"  Archive: +{added} new notices ({len(archive['items'])} total)",
              file=sys.stderr)
    return archive


# ---------------------------------------------------------------------------
# API fetch
# ---------------------------------------------------------------------------

def normalize_district(val):
    """Handle supervisor_district stored as '5', '5.0', or 5."""
    if val is None:
        return None
    s = str(val).strip()
    try:
        return str(int(float(s)))
    except (ValueError, TypeError):
        return s


def fetch_evictions(district, since_iso, until_iso=None):
    """
    Fetch eviction notices from SF Open Data, paginating as needed.
    If district is None, fetch citywide.
    """
    where_clauses = [
        f"file_date >= '{since_iso}'",
    ]
    if until_iso:
        where_clauses.append(f"file_date < '{until_iso}'")
    if district is not None:
        # Handle both '5' and '5.0' storage formats
        d = int(district)
        where_clauses.append(
            f"(supervisor_district = '{d}' OR supervisor_district = '{float(d)}')"
        )

    base_params = {
        "$where": " AND ".join(where_clauses),
        "$order": "file_date DESC",
        "$limit": str(PAGE_SIZE),
    }

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
            print(f"HTTP error fetching eviction data: {e.code} {e.reason}",
                  file=sys.stderr)
            break
        except Exception as e:
            print(f"Error fetching eviction data: {e}", file=sys.stderr)
            break

        results.extend(page)
        if len(page) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        if offset >= FETCH_LIMIT:
            print(f"Warning: hit fetch limit ({FETCH_LIMIT}), data may be incomplete.",
                  file=sys.stderr)
            break

    return results


# ---------------------------------------------------------------------------
# Data processing
# ---------------------------------------------------------------------------

def parse_date(rec):
    raw = rec.get("file_date", "")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def is_true(val):
    """Check if a Socrata boolean field is truthy (handles bool and string)."""
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ("true", "1", "yes")
    return False


def classify_reasons(rec):
    """Return list of eviction reason labels for a record."""
    reasons = []
    for col, label in EVICTION_REASONS:
        if is_true(rec.get(col)):
            reasons.append(label)
    return reasons if reasons else ["Unknown"]


def has_constraints(rec):
    """Check if the eviction involves elderly/disabled tenant protections."""
    return bool(rec.get("constraints_date"))


def group_by_reason(records):
    """Group records by eviction reason. A record can appear in multiple groups."""
    groups = defaultdict(list)
    for rec in records:
        reasons = classify_reasons(rec)
        for reason in reasons:
            groups[reason].append(rec)
    return dict(groups)


def compute_trend(current_count, prior_count):
    """Compute trend string comparing current vs prior period."""
    if prior_count == 0:
        if current_count == 0:
            return "flat (0 both periods)"
        return f"UP from 0 prior"
    pct = ((current_count - prior_count) / prior_count) * 100
    if abs(pct) < 5:
        return "flat"
    direction = "UP" if pct > 0 else "DOWN"
    return f"{direction} {abs(pct):.0f}% (was {prior_count})"


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

SEPARATOR = "━" * 60


def format_summary(records, prior_records, district, days):
    lines = []
    total = len(records)
    prior_total = len(prior_records)
    trend = compute_trend(total, prior_total)

    district_label = f"District {district}" if district else "Citywide"
    lines.append(f"\n🏠  SF Eviction Notices — {district_label} — Last {days} days")
    lines.append(f"    {total} notices filed | trend vs. prior {days} days: {trend}\n")

    groups = group_by_reason(records)
    prior_groups = group_by_reason(prior_records)

    # --- Displacement signals (Ellis Act, OMI) ---
    displacement_types = [
        (label, col) for col, label in EVICTION_REASONS
        if col in DISPLACEMENT_REASONS
    ]
    displacement_found = False
    for label, col in displacement_types:
        if label in groups:
            displacement_found = True

    if displacement_found:
        lines.append(SEPARATOR)
        lines.append("🚨  DISPLACEMENT SIGNALS — Ellis Act & Owner Move-In")
        lines.append(SEPARATOR)
        for label, col in displacement_types:
            cur = groups.get(label, [])
            pri = prior_groups.get(label, [])
            if not cur:
                continue
            t = compute_trend(len(cur), len(pri))
            lines.append(f"  🔴 {label}: {len(cur)} notices ({t})")
            # Show addresses
            for rec in cur[:5]:
                addr = rec.get("address", "—")
                nbhd = rec.get("neighborhood", "")
                constraint = " ⚠ ELDERLY/DISABLED" if has_constraints(rec) else ""
                dt = parse_date(rec)
                date_str = dt.strftime("%Y-%m-%d") if dt else "?"
                nbhd_str = f" ({nbhd})" if nbhd else ""
                lines.append(f"     · {addr}{nbhd_str} — filed {date_str}{constraint}")
        lines.append("")

    # --- Constrained evictions (elderly/disabled) ---
    constrained = [r for r in records if has_constraints(r)]
    if constrained:
        lines.append(SEPARATOR)
        lines.append(f"⚠️   ELDERLY/DISABLED PROTECTIONS — {len(constrained)} notices")
        lines.append(SEPARATOR)
        for rec in constrained[:8]:
            addr = rec.get("address", "—")
            nbhd = rec.get("neighborhood", "")
            reasons = ", ".join(classify_reasons(rec))
            nbhd_str = f" ({nbhd})" if nbhd else ""
            lines.append(f"  · {addr}{nbhd_str} — {reasons}")
        if len(constrained) > 8:
            lines.append(f"  ... and {len(constrained) - 8} more")
        lines.append("")

    # --- Breakdown by type ---
    lines.append(SEPARATOR)
    lines.append("📋  EVICTIONS BY TYPE")
    lines.append(SEPARATOR)

    # Sort: displacement first, then by count descending
    reason_order = []
    for col, label in EVICTION_REASONS:
        if label in groups:
            is_displacement = col in DISPLACEMENT_REASONS
            reason_order.append((0 if is_displacement else 1, -len(groups[label]), label))
    reason_order.sort()

    for _, _, label in reason_order:
        cur = groups[label]
        pri = prior_groups.get(label, [])
        t = compute_trend(len(cur), len(pri))
        flag = " 🔴" if any(
            col for col, l in EVICTION_REASONS
            if l == label and col in DISPLACEMENT_REASONS
        ) else ""
        lines.append(f"  · {label}: {len(cur)}{flag}  ({t})")

    lines.append("")

    # --- Neighborhood breakdown ---
    nbhd_counts = defaultdict(int)
    for rec in records:
        nbhd = rec.get("neighborhood", "Unknown") or "Unknown"
        nbhd_counts[nbhd] += 1

    if nbhd_counts:
        lines.append(SEPARATOR)
        lines.append("📍  BY NEIGHBORHOOD")
        lines.append(SEPARATOR)
        for nbhd, count in sorted(nbhd_counts.items(), key=lambda x: -x[1])[:10]:
            lines.append(f"  · {nbhd}: {count}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

def build_json_output(records, prior_records, district, days):
    groups = group_by_reason(records)
    prior_groups = group_by_reason(prior_records)

    by_type = []
    for col, label in EVICTION_REASONS:
        cur = groups.get(label, [])
        pri = prior_groups.get(label, [])
        if not cur:
            continue
        by_type.append({
            "reason": label,
            "column": col,
            "count": len(cur),
            "prior_count": len(pri),
            "trend": compute_trend(len(cur), len(pri)),
            "displacement_signal": col in DISPLACEMENT_REASONS,
            "notices": [
                {
                    "eviction_id": r.get("eviction_id"),
                    "address": r.get("address"),
                    "neighborhood": r.get("neighborhood"),
                    "file_date": r.get("file_date"),
                    "has_constraints": has_constraints(r),
                }
                for r in cur[:10]
            ],
        })

    nbhd_counts = defaultdict(int)
    for rec in records:
        nbhd = rec.get("neighborhood", "Unknown") or "Unknown"
        nbhd_counts[nbhd] += 1

    constrained = [r for r in records if has_constraints(r)]

    return {
        "district": district,
        "days": days,
        "total_notices": len(records),
        "prior_total": len(prior_records),
        "trend": compute_trend(len(records), len(prior_records)),
        "by_type": by_type,
        "by_neighborhood": dict(sorted(nbhd_counts.items(), key=lambda x: -x[1])),
        "constrained_count": len(constrained),
        "displacement_notices": [
            {
                "eviction_id": r.get("eviction_id"),
                "address": r.get("address"),
                "neighborhood": r.get("neighborhood"),
                "file_date": r.get("file_date"),
                "reasons": classify_reasons(r),
                "has_constraints": has_constraints(r),
            }
            for r in records
            if any(
                is_true(r.get(col))
                for col in DISPLACEMENT_REASONS
            )
        ],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="SF eviction notice tracker — displacement and tenant signals"
    )
    parser.add_argument("--district", type=int, default=_DEFAULT_DISTRICT,
                        help=f"Supervisor district (default: {_DEFAULT_DISTRICT})")
    parser.add_argument("--days", type=int, default=30,
                        help="Look back N days (default: 30)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    current_start = now - timedelta(days=args.days)
    prior_start = current_start - timedelta(days=args.days)

    current_since = current_start.strftime("%Y-%m-%dT%H:%M:%S")
    prior_since = prior_start.strftime("%Y-%m-%dT%H:%M:%S")
    current_until = now.strftime("%Y-%m-%dT%H:%M:%S")

    print(f"Fetching D{args.district} eviction notices since {current_since[:10]}...",
          file=sys.stderr)

    # Current period
    records = fetch_evictions(args.district, current_since)
    print(f"Got {len(records)} notices (current period)", file=sys.stderr)

    # Prior period for trend comparison
    prior_records = fetch_evictions(args.district, prior_since, until_iso=current_since)
    print(f"Got {len(prior_records)} notices (prior period)", file=sys.stderr)

    # Archive current period records
    update_archive(records)

    if not records and not prior_records:
        if args.json:
            print(json.dumps({
                "district": args.district,
                "days": args.days,
                "total_notices": 0,
                "by_type": [],
            }))
        else:
            print(f"No eviction notices found for D{args.district} "
                  f"in the last {args.days} days.")
        return

    if args.json:
        out = build_json_output(records, prior_records, args.district, args.days)
        print(json.dumps(out, indent=2))
    else:
        print(format_summary(records, prior_records, args.district, args.days))


if __name__ == "__main__":
    main()
