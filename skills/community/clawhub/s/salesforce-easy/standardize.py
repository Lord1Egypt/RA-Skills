#!/usr/bin/env python3
"""
Salesforce GTM Data Standardizer — Backfill Engine
Cleans and maps existing Salesforce data into GTM taxonomy:
  industry, vertical, role category, seniority

Author: Sawera Khadium
"""

import os
import sys
import json
import re
import argparse
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher
from simple_salesforce import Salesforce
from dotenv import load_dotenv

load_dotenv()

# ── Paths ─────────────────────────────────────────────────────────────────────
_SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
_TAXONOMY    = os.path.join(_SCRIPT_DIR, "..", "config", "taxonomy.json")

# ── GTM Custom Field API Names ────────────────────────────────────────────────
GTM_FIELDS = {
    "industry":      "GTM_Industry__c",
    "vertical":      "GTM_Vertical__c",
    "role_category": "GTM_Role_Category__c",
    "seniority":     "GTM_Seniority__c",
    "standardized":  "GTM_Standardized__c",
}

SUPPORTED_OBJECTS = ["Lead", "Contact", "Account"]
BATCH_SIZE        = 200   # Salesforce bulk API limit


# ── Connection ────────────────────────────────────────────────────────────────

def _get_sf() -> Optional[Salesforce]:
    """
    Build Salesforce session from environment.
    SECURITY: credential values are read into short-lived locals
    and never returned or logged.
    """
    instance_url = (os.getenv("SALESFORCE_INSTANCE_URL") or "").strip()
    _sid         = (os.getenv("SALESFORCE_ACCESS_TOKEN") or "").strip()
    username     = (os.getenv("SALESFORCE_USERNAME") or "").strip()
    _pw          = (os.getenv("SALESFORCE_PASSWORD") or "").strip()
    _sec         = (os.getenv("SALESFORCE_SECURITY_TOKEN") or "").strip()

    try:
        if instance_url and _sid:
            return Salesforce(instance_url=instance_url, session_id=_sid)
        if username and _pw:
            return Salesforce(
                username=username,
                password=_pw + _sec,
                domain="test" if "sandbox" in username.lower() else "login",
            )
        return None
    except Exception:
        return None


# ── Taxonomy Loader ───────────────────────────────────────────────────────────

def _load_taxonomy() -> Dict:
    """Load GTM taxonomy from config/taxonomy.json."""
    path = os.path.normpath(_TAXONOMY)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ── Mapping Logic ─────────────────────────────────────────────────────────────

def _map_industry(raw_industry: str, taxonomy: Dict) -> str:
    """Map a raw Industry field value to a GTM industry bucket."""
    if not raw_industry:
        return ""
    raw = raw_industry.strip()
    raw_lower = raw.lower()

    for bucket, keywords in taxonomy.get("industry", {}).items():
        if bucket == "Other":
            continue
        for kw in keywords:
            if kw.lower() in raw_lower or raw_lower in kw.lower():
                return bucket

    # Fuzzy fallback — 80% similarity threshold
    best_score = 0.0
    best_bucket = "Other"
    for bucket, keywords in taxonomy.get("industry", {}).items():
        if bucket == "Other":
            continue
        for kw in keywords:
            score = SequenceMatcher(None, raw_lower, kw.lower()).ratio()
            if score > best_score:
                best_score = score
                best_bucket = bucket

    return best_bucket if best_score >= 0.80 else "Other"


def _map_seniority(title: str, taxonomy: Dict) -> str:
    """Map a job title to a seniority level."""
    if not title:
        return "Unknown"
    title_upper = title.upper()

    for level, keywords in taxonomy.get("seniority", {}).items():
        if level == "Unknown":
            continue
        for kw in keywords:
            if kw.upper() in title_upper:
                return level

    return "Unknown"


def _map_role_category(title: str, taxonomy: Dict) -> str:
    """Map a job title to a buyer persona role category."""
    if not title:
        return "Unknown"
    title_upper = title.upper()

    for category, keywords in taxonomy.get("role_category", {}).items():
        if category == "Unknown":
            continue
        for kw in keywords:
            if kw.upper() in title_upper:
                return category

    return "Unknown"


def _map_vertical(industry: str, title: str, company: str,
                  employee_count: Optional[int], taxonomy: Dict) -> str:
    """
    Map to a GTM vertical using industry, title, company name,
    and employee count signals.
    """
    combined = f"{industry} {title} {company}".lower()

    for vertical, config in taxonomy.get("vertical", {}).items():
        if vertical in ("Other", "Enterprise Non-Tech"):
            continue
        if not isinstance(config, dict):
            continue
        signals = [s.lower() for s in config.get("signals", [])]
        if not signals:
            continue
        if any(sig in combined for sig in signals):
            # Check employee count constraints if present
            emp_min = config.get("employee_min")
            emp_max = config.get("employee_max")
            if emp_min and employee_count and employee_count < emp_min:
                continue
            if emp_max and employee_count and employee_count > emp_max:
                continue
            return vertical

    # Enterprise Non-Tech fallback for large companies
    if employee_count and employee_count >= 1000:
        return "Enterprise Non-Tech"

    return "Other"


def _standardize_record(record: Dict, taxonomy: Dict) -> Dict:
    """
    Compute GTM field values for a single record.
    Returns a dict of {field_api_name: value} to write back.
    """
    industry      = record.get("Industry", "") or ""
    title         = record.get("Title", "") or ""
    company       = record.get("Company", "") or record.get("Name", "") or ""
    employee_count = record.get("NumberOfEmployees")

    gtm_industry      = _map_industry(industry, taxonomy)
    gtm_seniority     = _map_seniority(title, taxonomy)
    gtm_role_category = _map_role_category(title, taxonomy)
    gtm_vertical      = _map_vertical(
        gtm_industry, title, company, employee_count, taxonomy
    )

    return {
        GTM_FIELDS["industry"]:      gtm_industry      or None,
        GTM_FIELDS["vertical"]:      gtm_vertical      or None,
        GTM_FIELDS["role_category"]: gtm_role_category or None,
        GTM_FIELDS["seniority"]:     gtm_seniority     or None,
        GTM_FIELDS["standardized"]:  True,
    }


# ── Audit ─────────────────────────────────────────────────────────────────────

def audit(sf: Salesforce, obj: str = "Lead") -> Dict:
    """
    Scan all records and report data quality score.
    No writes — read-only operation.
    """
    objects = SUPPORTED_OBJECTS if obj.lower() == "all" else [obj]
    results = {}

    for sf_obj in objects:
        query = (
            f"SELECT Id, {GTM_FIELDS['industry']}, {GTM_FIELDS['vertical']}, "
            f"{GTM_FIELDS['role_category']}, {GTM_FIELDS['seniority']}, "
            f"Industry, Title "
            f"FROM {sf_obj} LIMIT 50000"
        )
        try:
            data = sf.query_all(query)
        except Exception as exc:
            results[sf_obj] = {"error": str(exc)}
            continue

        records = data.get("records", [])
        total   = len(records)
        if total == 0:
            results[sf_obj] = {"total": 0, "score": 100}
            continue

        field_counts = {k: 0 for k in GTM_FIELDS if k != "standardized"}
        unmapped_industry: Dict[str, int] = {}
        unmapped_title: Dict[str, int]    = {}

        for r in records:
            for key, api_name in GTM_FIELDS.items():
                if key == "standardized":
                    continue
                if r.get(api_name):
                    field_counts[key] += 1

            # Track unmapped source values
            raw_ind = (r.get("Industry") or "").strip()
            if raw_ind and not r.get(GTM_FIELDS["industry"]):
                unmapped_industry[raw_ind] = unmapped_industry.get(raw_ind, 0) + 1

            raw_title = (r.get("Title") or "").strip()
            if raw_title and not r.get(GTM_FIELDS["seniority"]):
                unmapped_title[raw_title] = unmapped_title.get(raw_title, 0) + 1

        # Score = average coverage across the 4 GTM fields
        score = round(
            sum(field_counts.values()) / (total * len(field_counts)) * 100, 1
        )

        results[sf_obj] = {
            "total":    total,
            "score":    score,
            "coverage": {k: {"count": v, "pct": round(v / total * 100, 1)}
                         for k, v in field_counts.items()},
            "unmapped_industry": dict(
                sorted(unmapped_industry.items(), key=lambda x: -x[1])[:10]
            ),
            "unmapped_titles": dict(
                sorted(unmapped_title.items(), key=lambda x: -x[1])[:10]
            ),
        }

    return {"success": True, "audit": results}


# ── Preview ───────────────────────────────────────────────────────────────────

def preview(sf: Salesforce, obj: str = "Lead", limit: int = 10) -> Dict:
    """
    Show what the backfill would change — no writes.
    """
    taxonomy = _load_taxonomy()
    query = (
        f"SELECT Id, Name, Title, Industry, Company, NumberOfEmployees "
        f"FROM {obj} "
        f"WHERE {GTM_FIELDS['standardized']} = false OR {GTM_FIELDS['standardized']} = null "
        f"LIMIT {limit}"
    )
    try:
        data = sf.query_all(query)
    except Exception as exc:
        return {"success": False, "error": str(exc)}

    records  = data.get("records", [])
    previews = []

    for r in records:
        gtm = _standardize_record(r, taxonomy)
        previews.append({
            "id":      r.get("Id"),
            "name":    r.get("Name", ""),
            "title":   r.get("Title", ""),
            "company": r.get("Company", "") or r.get("Name", ""),
            "changes": {
                "GTM Industry":       gtm.get(GTM_FIELDS["industry"]),
                "GTM Vertical":       gtm.get(GTM_FIELDS["vertical"]),
                "GTM Role Category":  gtm.get(GTM_FIELDS["role_category"]),
                "GTM Seniority":      gtm.get(GTM_FIELDS["seniority"]),
            },
        })

    # Count total records that need standardization
    count_query = (
        f"SELECT COUNT() FROM {obj} "
        f"WHERE {GTM_FIELDS['standardized']} = false OR {GTM_FIELDS['standardized']} = null"
    )
    try:
        count_data = sf.query(count_query)
        total_pending = count_data.get("totalSize", 0)
    except Exception:
        total_pending = "unknown"

    return {
        "success":       True,
        "preview":       previews,
        "total_pending": total_pending,
        "message":       f"Showing {len(previews)} of {total_pending} records that need standardization.",
    }


# ── Execute (Backfill) ────────────────────────────────────────────────────────

def execute(sf: Salesforce, obj: str = "Lead", field: str = "all",
            dry_run: bool = False) -> Dict:
    """
    Write GTM fields to all unstandardized records.
    Processes in batches of 200 (Salesforce bulk API limit).
    """
    taxonomy = _load_taxonomy()
    objects  = SUPPORTED_OBJECTS if obj.lower() == "all" else [obj]
    summary  = {}

    for sf_obj in objects:
        query = (
            f"SELECT Id, Name, Title, Industry, Company, NumberOfEmployees "
            f"FROM {sf_obj} "
            f"WHERE {GTM_FIELDS['standardized']} = false OR {GTM_FIELDS['standardized']} = null "
            f"LIMIT 50000"
        )
        try:
            data = sf.query_all(query)
        except Exception as exc:
            summary[sf_obj] = {"error": str(exc)}
            continue

        records = data.get("records", [])
        if not records:
            summary[sf_obj] = {"updated": 0, "skipped": 0, "errors": 0,
                               "message": "No records need standardization."}
            continue

        updated = skipped = errors = 0
        batches = [records[i:i + BATCH_SIZE]
                   for i in range(0, len(records), BATCH_SIZE)]

        for batch_num, batch in enumerate(batches, 1):
            updates = []
            for r in batch:
                gtm = _standardize_record(r, taxonomy)
                # Skip if nothing to write
                if not any(v for k, v in gtm.items() if k != GTM_FIELDS["standardized"]):
                    skipped += 1
                    continue
                updates.append({"Id": r["Id"], **gtm})

            if not updates or dry_run:
                skipped += len(batch)
                continue

            try:
                sf_obj_api = getattr(sf.bulk, sf_obj)
                results    = sf_obj_api.update(updates, batch_size=BATCH_SIZE)
                for res in results:
                    if res.get("success"):
                        updated += 1
                    else:
                        errors += 1
            except Exception as exc:
                errors += len(updates)

        summary[sf_obj] = {
            "total":   len(records),
            "updated": updated,
            "skipped": skipped,
            "errors":  errors,
        }

    return {"success": True, "dry_run": dry_run, "results": summary}


# ── Rollback ──────────────────────────────────────────────────────────────────

def rollback(sf: Salesforce, obj: str = "Lead") -> Dict:
    """
    Clear all GTM fields on a given object.
    Use before re-running backfill with an updated taxonomy.
    Requires explicit confirmation.
    """
    objects = SUPPORTED_OBJECTS if obj.lower() == "all" else [obj]
    summary = {}

    for sf_obj in objects:
        query = (
            f"SELECT Id FROM {sf_obj} "
            f"WHERE {GTM_FIELDS['standardized']} = true LIMIT 50000"
        )
        try:
            data = sf.query_all(query)
        except Exception as exc:
            summary[sf_obj] = {"error": str(exc)}
            continue

        records = data.get("records", [])
        if not records:
            summary[sf_obj] = {"cleared": 0}
            continue

        cleared = errors = 0
        clear_payload = [
            {
                "Id": r["Id"],
                GTM_FIELDS["industry"]:      None,
                GTM_FIELDS["vertical"]:      None,
                GTM_FIELDS["role_category"]: None,
                GTM_FIELDS["seniority"]:     None,
                GTM_FIELDS["standardized"]:  False,
            }
            for r in records
        ]

        batches = [clear_payload[i:i + BATCH_SIZE]
                   for i in range(0, len(clear_payload), BATCH_SIZE)]
        for batch in batches:
            try:
                sf_obj_api = getattr(sf.bulk, sf_obj)
                results    = sf_obj_api.update(batch, batch_size=BATCH_SIZE)
                for res in results:
                    if res.get("success"):
                        cleared += 1
                    else:
                        errors += 1
            except Exception:
                errors += len(batch)

        summary[sf_obj] = {"cleared": cleared, "errors": errors}

    return {"success": True, "rollback": summary}


# ── Attribution Report ────────────────────────────────────────────────────────

def report(sf: Salesforce, report_type: str = "attribution",
           obj: str = "Lead") -> Dict:
    """
    Generate attribution and data quality reports.
    report_type: 'attribution' | 'quality' | 'gaps'
    """
    if report_type == "attribution":
        # Breakdown by vertical, seniority, role category
        breakdowns = {}
        for field_key, api_name in GTM_FIELDS.items():
            if field_key == "standardized":
                continue
            query = (
                f"SELECT {api_name}, COUNT(Id) total "
                f"FROM {obj} "
                f"WHERE {api_name} != null "
                f"GROUP BY {api_name} "
                f"ORDER BY COUNT(Id) DESC"
            )
            try:
                data = sf.query(query)
                breakdowns[field_key] = [
                    {"value": r[api_name], "count": r["total"]}
                    for r in data.get("records", [])
                ]
            except Exception as exc:
                breakdowns[field_key] = {"error": str(exc)}

        return {"success": True, "report_type": "attribution",
                "object": obj, "data": breakdowns}

    elif report_type == "quality":
        return audit(sf, obj)

    elif report_type == "gaps":
        # Records missing GTM fields
        gaps = {}
        for field_key, api_name in GTM_FIELDS.items():
            if field_key == "standardized":
                continue
            query = f"SELECT COUNT() FROM {obj} WHERE {api_name} = null"
            try:
                data = sf.query(query)
                gaps[field_key] = data.get("totalSize", 0)
            except Exception as exc:
                gaps[field_key] = {"error": str(exc)}

        return {"success": True, "report_type": "gaps",
                "object": obj, "missing_counts": gaps}

    return {"success": False, "error": f"Unknown report type: {report_type}"}


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    """
    CLI interface for the backfill engine.

    Commands:
      audit   [--object lead|contact|account|all]
      preview [--object lead] [--limit 10]
      execute [--object lead|all] [--field industry|seniority|all] [--dry-run]
      rollback [--object lead|all]  (requires --confirm)
      report  [--type attribution|quality|gaps] [--object lead]
    """
    parser = argparse.ArgumentParser(
        description="Salesforce GTM Data Standardizer — Backfill Engine"
    )
    parser.add_argument("command",
                        choices=["audit", "preview", "execute", "rollback", "report"])
    parser.add_argument("--object",  default="Lead",
                        help="Salesforce object: Lead, Contact, Account, or all")
    parser.add_argument("--field",   default="all",
                        help="Field to standardize: industry, seniority, role_category, vertical, or all")
    parser.add_argument("--limit",   type=int, default=10,
                        help="Number of records to preview")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without writing to Salesforce")
    parser.add_argument("--confirm", action="store_true",
                        help="Required for rollback operations")
    parser.add_argument("--type",    default="attribution",
                        help="Report type: attribution, quality, or gaps")

    args = parser.parse_args()

    sf = _get_sf()
    if sf is None:
        print(json.dumps({
            "success": False,
            "error": (
                "Not connected to Salesforce. "
                "Set SALESFORCE_INSTANCE_URL + SALESFORCE_ACCESS_TOKEN, "
                "or SALESFORCE_USERNAME + SALESFORCE_PASSWORD."
            )
        }))
        sys.exit(1)

    if args.command == "audit":
        result = audit(sf, args.object)

    elif args.command == "preview":
        result = preview(sf, args.object, args.limit)

    elif args.command == "execute":
        result = execute(sf, args.object, args.field, dry_run=args.dry_run)

    elif args.command == "rollback":
        if not args.confirm:
            print(json.dumps({
                "success": False,
                "error": (
                    "Rollback requires --confirm flag. "
                    "This will clear all GTM fields. "
                    "Re-run with --confirm to proceed."
                )
            }))
            sys.exit(1)
        result = rollback(sf, args.object)

    elif args.command == "report":
        result = report(sf, args.type, args.object)

    else:
        result = {"success": False, "error": f"Unknown command: {args.command}"}

    print(json.dumps(result, default=str, indent=2))


if __name__ == "__main__":
    main()
