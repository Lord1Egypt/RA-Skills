#!/usr/bin/env python3
"""List Zoho Social portals accessible to the authenticated user."""
from __future__ import annotations
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from social_client import ENDPOINT, build_base_parser, call, field, finish, rows

COLUMNS = [
    ("ID", ["id", "portal_id"]),
    ("Name", ["name", "portal_name", "display_name"]),
    ("Plan", ["plan", "plan_name"]),
    ("Role", ["role", "user_role"]),
]


def build_parser():
    parser = build_base_parser("List Zoho Social portals.")
    parser.add_argument("--full", action="store_true", help="with --json, print complete records")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    payload = {"headers": {}}
    if args.portal_id:
        payload["headers"]["portal_id"] = str(args.portal_id)
    result = call("getSocialPortals", payload, timeout=args.timeout)
    records = rows(result) if "error" not in result else []
    if args.json and not args.full:
        records = [
            {
                "id": field(row, ["id", "portal_id"], ""),
                "name": field(row, ["name", "portal_name", "display_name"], ""),
                "plan": field(row, ["plan", "plan_name"], ""),
            }
            for row in records
        ]
    return finish(result, records, args, COLUMNS, empty="No portals found.")


if __name__ == "__main__":
    sys.exit(main())
