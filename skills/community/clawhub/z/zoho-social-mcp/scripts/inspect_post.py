#!/usr/bin/env python3
"""Inspect one Zoho Social draft, schedule, or published post."""
from __future__ import annotations
import json
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from social_client import ENDPOINT, build_base_parser, call, field, headers_from

KINDS = {
    "draft": "getSocialDraft",
    "schedule": "getSocialSchedule",
    "published": "getSocialPublishedPostDetail",
}


def build_parser():
    parser = build_base_parser("Inspect one Zoho Social draft, schedule, or published post.")
    parser.add_argument("post_id", help="Social post ID")
    parser.add_argument("--kind", choices=sorted(KINDS), default="draft", help="post kind (default: draft)")
    parser.add_argument("--network", help="required for --kind published")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    try:
        headers = headers_from(args, portal=True, brand=True)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    payload = {"headers": headers, "path_variables": {"post_id": args.post_id}}
    if args.kind == "published":
        if not args.network:
            print("Error: --network is required for --kind published", file=sys.stderr)
            return 2
        payload["query_params"] = {"network": args.network}
    result = call(KINDS[args.kind], payload, timeout=args.timeout)
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    data = result.get("data", result)
    if isinstance(data, dict) and isinstance(data.get("data"), dict):
        data = data["data"]
    if not isinstance(data, dict):
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    print(f"ID:       {field(data, ['id', 'post_id'])}")
    print(f"Status:   {field(data, ['status', 'post_status'])}")
    print(f"Type:     {field(data, ['type', 'post_type'])}")
    print(f"Networks: {field(data, ['networks', 'network'])}")
    print(f"Created:  {field(data, ['created_time', 'created_at'])}")
    print(f"Updated:  {field(data, ['updated_time', 'modified_time'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
