#!/usr/bin/env python3
"""List Zoho Social scheduled posts for a brand."""
from __future__ import annotations
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from social_client import ENDPOINT, build_base_parser, field, finish, headers_from, paginate, positive_int

COLUMNS = [
    ("ID", ["id", "post_id"]),
    ("When", ["scheduled_time", "schedule_time", "publish_time"]),
    ("Networks", ["networks", "network"]),
    ("Status", ["status", "post_status"]),
]


def build_parser():
    parser = build_base_parser("List Zoho Social scheduled posts for a brand.")
    parser.add_argument("--limit", type=positive_int, help="return at most this many schedules")
    parser.add_argument("--page-size", type=positive_int, default=20, help="page size (default: 20)")
    parser.add_argument("--networks", help="comma-separated network filter")
    parser.add_argument("--failed", action="store_true", help="only failed schedules")
    parser.add_argument("--approval", action="store_true", help="only posts awaiting approval")
    parser.add_argument("--full", action="store_true", help="with --json, print complete records")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    try:
        headers = headers_from(args, portal=True, brand=True)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    params = {}
    if args.networks:
        params["networks"] = args.networks
    if args.failed:
        params["is_failed"] = True
    if args.approval:
        params["is_approval"] = True
    result = paginate(
        "listSocialSchedules",
        headers=headers,
        params=params,
        page_size=args.page_size,
        max_records=args.limit,
        timeout=args.timeout,
    )
    records = result.get("data", []) if "error" not in result else []
    if args.json and not args.full:
        records = [
            {
                "id": field(row, ["id", "post_id"], ""),
                "scheduled_time": field(row, ["scheduled_time", "schedule_time"], ""),
                "networks": field(row, ["networks", "network"], ""),
                "status": field(row, ["status", "post_status"], ""),
            }
            for row in records
        ]
    return finish(result, records, args, COLUMNS, empty="No scheduled posts found.")


if __name__ == "__main__":
    sys.exit(main())
