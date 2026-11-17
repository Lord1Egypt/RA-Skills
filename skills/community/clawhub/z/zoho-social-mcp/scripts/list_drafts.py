#!/usr/bin/env python3
"""List Zoho Social draft posts for a brand."""
from __future__ import annotations
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from social_client import ENDPOINT, build_base_parser, field, finish, headers_from, paginate, positive_int

COLUMNS = [
    ("ID", ["id", "post_id"]),
    ("Status", ["status", "post_status"]),
    ("Networks", ["networks", "network"]),
    ("Updated", ["updated_time", "modified_time", "created_time"]),
]


def build_parser():
    parser = build_base_parser("List Zoho Social draft posts for a brand.")
    parser.add_argument("--limit", type=positive_int, help="return at most this many drafts")
    parser.add_argument("--page-size", type=positive_int, default=20, help="page size (default: 20)")
    parser.add_argument("--networks", help="comma-separated network filter")
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
    result = paginate(
        "listSocialDrafts",
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
                "status": field(row, ["status", "post_status"], ""),
                "networks": field(row, ["networks", "network"], ""),
            }
            for row in records
        ]
    return finish(result, records, args, COLUMNS, empty="No drafts found.")


if __name__ == "__main__":
    sys.exit(main())
