#!/usr/bin/env python3
"""List connected Zoho Social channels for a brand."""
from __future__ import annotations
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from social_client import ENDPOINT, build_base_parser, call, field, finish, headers_from, rows

COLUMNS = [
    ("ID", ["id", "channel_id"]),
    ("Network", ["network", "network_name", "channel_type"]),
    ("Name", ["name", "display_name", "page_name"]),
    ("Status", ["status", "connection_status"]),
]


def build_parser():
    parser = build_base_parser("List connected Zoho Social channels for a brand.")
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
    result = call("getSocialChannels", {"headers": headers}, timeout=args.timeout)
    records = rows(result) if "error" not in result else []
    if args.json and not args.full:
        records = [
            {
                "id": field(row, ["id", "channel_id"], ""),
                "network": field(row, ["network", "network_name", "channel_type"], ""),
                "name": field(row, ["name", "display_name", "page_name"], ""),
                "status": field(row, ["status", "connection_status"], ""),
            }
            for row in records
        ]
    return finish(result, records, args, COLUMNS, empty="No channels found.")


if __name__ == "__main__":
    sys.exit(main())
