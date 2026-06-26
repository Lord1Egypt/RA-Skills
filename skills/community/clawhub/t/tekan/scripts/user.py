#!/usr/bin/env python3
"""Query Tekan account credit balance and benefit consumption history.

Usage:
    python user.py credit [--json]
    python user.py logs [--type TYPE] [--benefit-ids ID,...] [--benefit-group-ids ID,...]
                        [--start TIME] [--end TIME] [--page N] [--size N] [--json]
"""

import argparse
import json as json_mod
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from shared.client import TopviewClient, TEKAN_API_URL

QUOTA_PATH = "/user/benefit/tekan-video/quota"
BENEFIT_LIST_PATH = "/user/benefit/list"


def cmd_credit(client: TopviewClient, args):
    import requests as _req
    url = f"{TEKAN_API_URL}{QUOTA_PATH}"
    resp = _req.get(url, headers=client.token_headers)
    resp.raise_for_status()
    result = client._check(resp.json())

    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
    else:
        quota = result if isinstance(result, (int, float)) else result.get("quota", result)
        print(f"Credit balance: {quota}")


def cmd_logs(client: TopviewClient, args):
    body = {
        "pageNo": args.page,
        "pageSize": args.size,
    }
    if args.type:
        body["type"] = args.type
    if args.benefit_ids:
        body["benefitIds"] = [int(x) for x in args.benefit_ids.split(",")]
    if args.benefit_group_ids:
        body["benefitGroupIds"] = [int(x) for x in args.benefit_group_ids.split(",")]
    if args.start:
        body["gmtCreateStart"] = args.start
    if args.end:
        body["gmtCreateEnd"] = args.end

    result = client.post(BENEFIT_LIST_PATH, json=body)

    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
        return

    records = result.get("records", result.get("data", []))
    total = result.get("total", len(records))
    page_no = result.get("pageNo", args.page)

    if not args.quiet:
        print(
            f"Page {page_no} | {len(records)} items | {total} total",
            file=sys.stderr,
        )

    if not records:
        print("No records found.")
        return

    header = f"{'Date':<22} {'Type':<35} {'Cost':>8}  {'TaskId'}"
    print(header)
    print("-" * len(header))
    for entry in records:
        date = str(entry.get("gmtCreate", entry.get("date", "")))[:19]
        benefit_type = entry.get("type", entry.get("taskType", ""))
        cost = entry.get("costCredit", entry.get("amount", 0))
        task_id = entry.get("taskId", entry.get("id", ""))
        print(f"{date:<22} {benefit_type:<35} {cost:>8}  {task_id}")


def main():
    parser = argparse.ArgumentParser(
        description="Tekan account credit management."
    )
    parser.add_argument("--json", action="store_true",
                        help="Output full JSON response")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress status messages on stderr")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("credit", help="Query credit balance (tekan-video quota)")

    logs_p = sub.add_parser("logs", help="Query benefit consumption history")
    logs_p.add_argument("--type", default=None,
                        help="Filter by benefit type")
    logs_p.add_argument("--benefit-ids", default=None,
                        help="Comma-separated benefit IDs to filter")
    logs_p.add_argument("--benefit-group-ids", default=None,
                        help="Comma-separated benefit group IDs to filter")
    logs_p.add_argument("--start", default=None,
                        help="Start time (yyyy-MM-dd HH:mm:ss)")
    logs_p.add_argument("--end", default=None,
                        help="End time (yyyy-MM-dd HH:mm:ss)")
    logs_p.add_argument("--page", type=int, default=1,
                        help="Page number (default: 1)")
    logs_p.add_argument("--size", type=int, default=20,
                        help="Items per page (default: 20)")

    args = parser.parse_args()
    client = TopviewClient()

    if args.command == "credit":
        cmd_credit(client, args)
    elif args.command == "logs":
        cmd_logs(client, args)


if __name__ == "__main__":
    main()
