#!/usr/bin/env python3
"""List Zoho Social brands in a portal."""
from __future__ import annotations
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from social_client import ENDPOINT, build_base_parser, call, field, finish, headers_from, rows

COLUMNS = [
    ("ID", ["id", "brand_id"]),
    ("Name", ["name", "brand_name", "display_name"]),
    ("Timezone", ["timezone", "time_zone"]),
    ("Location", ["location", "city"]),
]


def build_parser():
    parser = build_base_parser("List Zoho Social brands in a portal.")
    parser.add_argument("--full", action="store_true", help="with --json, print complete records")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    try:
        headers = headers_from(args, portal=True)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    result = call("getSocialBrands", {"headers": headers}, timeout=args.timeout)
    records = rows(result) if "error" not in result else []
    if args.json and not args.full:
        records = [
            {
                "id": field(row, ["id", "brand_id"], ""),
                "name": field(row, ["name", "brand_name", "display_name"], ""),
                "timezone": field(row, ["timezone", "time_zone"], ""),
            }
            for row in records
        ]
    return finish(result, records, args, COLUMNS, empty="No brands found.")


if __name__ == "__main__":
    sys.exit(main())
