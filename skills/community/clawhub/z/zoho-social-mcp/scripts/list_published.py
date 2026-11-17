#!/usr/bin/env python3
"""List published Zoho Social posts for one network on a brand."""
from __future__ import annotations
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from social_client import ENDPOINT, build_base_parser, call, field, finish, headers_from, positive_int, rows

COLUMNS = [
    ("ID", ["id", "post_id"]),
    ("Network", ["network"]),
    ("Published", ["published_time", "created_time"]),
    ("Status", ["status", "publish_status"]),
]


def build_parser():
    parser = build_base_parser("List published Zoho Social posts for a brand and network.")
    parser.add_argument("--network", required=True, help="social network key, e.g. facebook, linkedin")
    parser.add_argument("--limit", type=positive_int, default=20, help="page size (default: 20)")
    parser.add_argument("--cursor", help="pagination cursor from a previous response")
    parser.add_argument("--board-id", help="Pinterest board ID filter")
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
    query = {"network": args.network, "limit": args.limit}
    if args.cursor:
        query["cursor"] = args.cursor
    if args.board_id:
        query["board_id"] = args.board_id
    result = call(
        "getSocialPublishedPosts",
        {"headers": headers, "query_params": query},
        timeout=args.timeout,
    )
    records = rows(result) if "error" not in result else []
    if args.json and not args.full:
        records = [
            {
                "id": field(row, ["id", "post_id"], ""),
                "network": field(row, ["network"], args.network),
                "published_time": field(row, ["published_time", "created_time"], ""),
                "status": field(row, ["status", "publish_status"], ""),
            }
            for row in records
        ]
    return finish(result, records, args, COLUMNS, empty="No published posts found.")


if __name__ == "__main__":
    sys.exit(main())
