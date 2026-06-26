#!/usr/bin/env python3
"""TrendAI Vision One Threat Intelligence CLI.

Workflow-oriented threat intelligence queries for AI agents.
"""

import argparse
import sys
import os
from datetime import datetime, timedelta, timezone

# Add parent dir to path so lib imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.client import VisionOneClient, APIError
from lib.ioc_detect import detect_ioc_type
from lib.pagination import paginate
from lib.cache import SessionCache
from lib.formatters import (
    format_error,
    format_stix_indicator,
    format_indicator_table,
    format_suspicious_object,
    format_suspicious_table,
    format_report,
    format_report_table,
    format_lookup_result,
)

# Vision One uses lowercase 'threatintel' in the path
API_PREFIX = "/v3.0/threatintel"

cache = SessionCache()


def _iso_days_ago(days):
    dt = datetime.now(timezone.utc) - timedelta(days=days)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Command: lookup
# ---------------------------------------------------------------------------
def cmd_lookup(client, args):
    """Look up a single IOC across feed indicators and suspicious objects."""
    ioc_type, value = detect_ioc_type(args.indicator)
    if ioc_type is None:
        print(value, file=sys.stderr)
        sys.exit(1)

    days = args.days or 90

    # 1. Search feed indicators (STIX bundle response)
    params = {
        "startDateTime": _iso_days_ago(days),
        "endDateTime": _now_iso(),
        "top": 200,
    }
    feed_matches = []
    try:
        for item in paginate(client, f"{API_PREFIX}/feedIndicators", params, max_items=200):
            # Client-side filter: check if indicator value appears in the STIX pattern
            pattern = item.get("pattern", "")
            if value.lower() in pattern.lower():
                feed_matches.append(item)
                if len(feed_matches) >= 20:
                    break
    except APIError as e:
        print(format_error(str(e), "Valid API credentials and endpoint access", "v1ti.py feed --days 7"), file=sys.stderr)
        sys.exit(1)

    # 2. Check suspicious objects list
    suspicious_match = None
    try:
        resp = client.get(f"{API_PREFIX}/suspiciousObjects", {"top": 200})
        items = resp.get("items", [])
        # Client-side filter: match by value
        for obj in items:
            # Value field name matches the type (e.g., fileSha256: 'HASH')
            for field in ["value", "ip", "domain", "url", "fileSha1", "fileSha256", "senderMailAddress"]:
                obj_val = obj.get(field, "")
                if obj_val and value.lower() == str(obj_val).lower():
                    suspicious_match = [obj]
                    break
            if suspicious_match:
                break
    except APIError:
        pass  # Non-fatal: suspicious objects check is supplementary

    print(format_lookup_result(feed_matches, suspicious_match))


# ---------------------------------------------------------------------------
# Command: feed
# ---------------------------------------------------------------------------
def cmd_feed(client, args):
    """List latest feed indicators."""
    days = args.days or 7
    limit = args.limit or 50

    params = {
        "startDateTime": _iso_days_ago(days),
        "endDateTime": _now_iso(),
    }

    indicators = []
    try:
        for item in paginate(client, f"{API_PREFIX}/feedIndicators", params, max_items=limit):
            # Client-side filtering by type/risk if specified
            if args.type:
                pattern = item.get("pattern", "").lower()
                type_patterns = {
                    "ip": "ipv4-addr",
                    "domain": "domain-name",
                    "url": "url:",
                    "fileSha1": "file:hashes.'sha-1'",
                    "fileSha256": "file:hashes.'sha-256'",
                    "senderMailAddress": "email-addr",
                }
                search = type_patterns.get(args.type, args.type)
                if search.lower() not in pattern:
                    continue
            indicators.append(item)
    except APIError as e:
        print(format_error(str(e), "Valid API credentials", "v1ti.py feed --days 7 --limit 10"), file=sys.stderr)
        sys.exit(1)

    title = f"Feed Indicators (last {days} days"
    if args.type:
        title += f", type={args.type}"
    title += ")"

    print(format_indicator_table(indicators, title))


# ---------------------------------------------------------------------------
# Command: report
# ---------------------------------------------------------------------------
def cmd_report(client, args):
    """List or retrieve intelligence reports (via feeds endpoint)."""
    if args.id:
        # Search for a specific report by ID among feeds
        try:
            reports = []
            for item in paginate(client, f"{API_PREFIX}/feeds", {}, max_items=500, use_top=False):
                if item.get("type") == "report" and item.get("id") == args.id:
                    reports.append(item)
                    break
            if reports:
                print(f"=== Intelligence Report ===\n")
                print(format_report(reports[0]))
                print("\n===")
            else:
                print(format_error(
                    f"Report '{args.id}' not found",
                    "A valid STIX report ID (e.g., report--abc123)",
                    "v1ti.py report  (to list available reports)",
                ))
        except APIError as e:
            print(format_error(str(e), "Valid API credentials", "v1ti.py report"), file=sys.stderr)
            sys.exit(1)
    else:
        # List reports from feeds endpoint
        limit = args.limit or 10
        reports = []
        try:
            for item in paginate(client, f"{API_PREFIX}/feeds", {}, max_items=200, use_top=False):
                if item.get("type") != "report":
                    continue
                # Client-side keyword filter
                if args.search:
                    name = item.get("name", "").lower()
                    if args.search.lower() not in name:
                        continue
                reports.append(item)
                if len(reports) >= limit:
                    break
        except APIError as e:
            print(format_error(str(e), "Valid API credentials", "v1ti.py report --limit 5"), file=sys.stderr)
            sys.exit(1)

        title = "Intelligence Reports"
        if args.search:
            title += f" (search: '{args.search}')"
        print(format_report_table(reports, title))


# ---------------------------------------------------------------------------
# Command: suspicious
# ---------------------------------------------------------------------------
def cmd_suspicious_list(client, args):
    """List suspicious objects."""
    limit = args.limit or 50
    params = {}

    objects = []
    try:
        for item in paginate(client, f"{API_PREFIX}/suspiciousObjects", params, max_items=limit):
            # Client-side type filter
            if args.type and item.get("type") != args.type:
                continue
            objects.append(item)
    except APIError as e:
        print(format_error(str(e), "Valid API credentials", "v1ti.py suspicious list --limit 10"), file=sys.stderr)
        sys.exit(1)

    title = "Suspicious Objects"
    if args.type:
        title += f" (type={args.type})"
    print(format_suspicious_table(objects, title))


def cmd_suspicious_add(client, args):
    """Add an indicator to the suspicious objects list."""
    ioc_type, value = detect_ioc_type(args.indicator)
    if ioc_type is None:
        print(value, file=sys.stderr)
        sys.exit(1)

    if ioc_type == "md5":
        print(format_error(
            "MD5 hashes are not supported for suspicious objects",
            "SHA-1 or SHA-256 hash",
            "v1ti.py suspicious add <sha256-hash> --action block --risk high",
        ), file=sys.stderr)
        sys.exit(1)

    body = [
        {
            "type": ioc_type,
            "value": value,
            "scanAction": args.action,
            "riskLevel": args.risk,
        }
    ]

    if args.description:
        body[0]["description"] = args.description

    if args.expiry_days:
        expiry = datetime.now(timezone.utc) + timedelta(days=args.expiry_days)
        body[0]["expiredDateTime"] = expiry.strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        resp = client.post(f"{API_PREFIX}/suspiciousObjects", body=body)
        print(f"=== Suspicious Object Added ===\n")
        print(f"Type: {ioc_type}")
        print(f"Value: {value}")
        print(f"Action: {args.action}")
        print(f"Risk: {args.risk.upper()}")
        if args.description:
            print(f"Description: {args.description}")
        if args.expiry_days:
            print(f"Expires: {body[0]['expiredDateTime']}")

        # Show multi-response status if available
        items = resp.get("items", [])
        if items:
            status = items[0].get("status", "")
            if status:
                print(f"Status: {status}")
            task_id = items[0].get("taskId", "")
            if task_id:
                print(f"Task ID: {task_id}")

        print("\n===")
    except APIError as e:
        print(format_error(str(e), "Valid credentials and write permissions", "v1ti.py suspicious add evil.com --action block --risk high"), file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Command: hunt
# ---------------------------------------------------------------------------
def cmd_hunt(client, args):
    """Hunt for threats by keyword in STIX patterns and report names."""
    days = args.days or 90
    limit = args.limit or 50

    # Collect all search terms
    search_terms = []
    hunt_desc_parts = []

    for attr, label in [(args.campaign, "campaign"), (args.actor, "actor"),
                         (args.industry, "industry"), (args.country, "country"),
                         (args.cve, "cve")]:
        if attr:
            search_terms.append(attr.lower())
            hunt_desc_parts.append(f"{label}='{attr}'")

    if not search_terms:
        print(format_error(
            "No hunt criteria specified",
            "At least one of: --campaign, --actor, --industry, --country, --cve",
            "v1ti.py hunt --industry Finance --days 30",
        ), file=sys.stderr)
        sys.exit(1)

    params = {
        "startDateTime": _iso_days_ago(days),
        "endDateTime": _now_iso(),
    }

    indicators = []
    try:
        for item in paginate(client, f"{API_PREFIX}/feedIndicators", params, max_items=500):
            item_str = str(item).lower()
            if all(term in item_str for term in search_terms):
                indicators.append(item)
                if len(indicators) >= limit:
                    break
    except APIError as e:
        print(format_error(str(e), "Valid API credentials", "v1ti.py hunt --industry Finance"), file=sys.stderr)
        sys.exit(1)

    title = f"Threat Hunt ({', '.join(hunt_desc_parts)}, last {days} days)"
    print(format_indicator_table(indicators, title))


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(
        prog="v1ti",
        description="TrendAI Vision One Threat Intelligence CLI",
    )
    parser.add_argument("--region", help="Vision One region (us, eu, jp, sg, au, in, mea)")
    sub = parser.add_subparsers(dest="command", required=True)

    # lookup
    p_lookup = sub.add_parser("lookup", help="Look up an IOC across feed and suspicious objects")
    p_lookup.add_argument("indicator", help="IOC value (IP, domain, URL, hash, email)")
    p_lookup.add_argument("--days", type=int, default=90, help="Look back N days (default: 90)")

    # feed
    p_feed = sub.add_parser("feed", help="List latest feed indicators")
    p_feed.add_argument("--days", type=int, default=7, help="Look back N days (default: 7)")
    p_feed.add_argument("--type", choices=["ip", "domain", "url", "fileSha1", "fileSha256", "senderMailAddress"], help="Filter by indicator type")
    p_feed.add_argument("--limit", type=int, default=50, help="Max results (default: 50)")

    # report
    p_report = sub.add_parser("report", help="List or view intelligence reports")
    p_report.add_argument("--id", help="Get a specific report by STIX ID")
    p_report.add_argument("--search", help="Search reports by keyword in name")
    p_report.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")

    # suspicious
    p_suspicious = sub.add_parser("suspicious", help="Manage suspicious objects list")
    sus_sub = p_suspicious.add_subparsers(dest="suspicious_command", required=True)

    # suspicious list
    p_sus_list = sus_sub.add_parser("list", help="List suspicious objects")
    p_sus_list.add_argument("--type", choices=["ip", "domain", "url", "fileSha1", "fileSha256", "senderMailAddress"], help="Filter by type")
    p_sus_list.add_argument("--limit", type=int, default=50, help="Max results (default: 50)")

    # suspicious add
    p_sus_add = sus_sub.add_parser("add", help="Add indicator to suspicious objects list")
    p_sus_add.add_argument("indicator", help="IOC value (IP, domain, URL, hash, email)")
    p_sus_add.add_argument("--action", required=True, choices=["block", "log"], help="Scan action (required)")
    p_sus_add.add_argument("--risk", required=True, choices=["high", "medium", "low"], help="Risk level (required)")
    p_sus_add.add_argument("--description", help="Description/reason for adding")
    p_sus_add.add_argument("--expiry-days", type=int, help="Auto-expire after N days")

    # hunt
    p_hunt = sub.add_parser("hunt", help="Hunt for threats by criteria")
    p_hunt.add_argument("--campaign", help="Filter by campaign name")
    p_hunt.add_argument("--actor", help="Filter by threat actor")
    p_hunt.add_argument("--industry", help="Filter by targeted industry")
    p_hunt.add_argument("--country", help="Filter by targeted country")
    p_hunt.add_argument("--cve", help="Filter by CVE ID")
    p_hunt.add_argument("--days", type=int, default=90, help="Look back N days (default: 90)")
    p_hunt.add_argument("--limit", type=int, default=50, help="Max results (default: 50)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    client = VisionOneClient(region=args.region)

    try:
        if args.command == "lookup":
            cmd_lookup(client, args)
        elif args.command == "feed":
            cmd_feed(client, args)
        elif args.command == "report":
            cmd_report(client, args)
        elif args.command == "suspicious":
            if args.suspicious_command == "list":
                cmd_suspicious_list(client, args)
            elif args.suspicious_command == "add":
                cmd_suspicious_add(client, args)
        elif args.command == "hunt":
            cmd_hunt(client, args)
    except APIError as e:
        print(format_error(str(e), "Check credentials and region", "export VISION_ONE_REGION=us"), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
