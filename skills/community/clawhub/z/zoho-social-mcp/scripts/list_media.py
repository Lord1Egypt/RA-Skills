#!/usr/bin/env python3
"""List assets in a Zoho Social brand media library."""
from __future__ import annotations
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from social_client import ENDPOINT, build_base_parser, field, finish, headers_from, paginate, positive_int

COLUMNS = [
    ("ID", ["id", "file_id", "media_id"]),
    ("Name", ["file_name", "name", "filename"]),
    ("Format", ["format", "type", "mime_type"]),
    ("Created", ["created_time", "uploaded_time"]),
]


def build_parser():
    parser = build_base_parser("List assets in a Zoho Social brand media library.")
    parser.add_argument(
        "--library-type",
        default="sociallibrary",
        choices=["sociallibrary", "pixabay", "pexels", "giphy"],
        help="media library source (default: sociallibrary)",
    )
    parser.add_argument("--search", help="search term (not used for sociallibrary)")
    parser.add_argument("--format", dest="file_format", help="comma-separated formats, e.g. png,jpeg")
    parser.add_argument("--limit", type=positive_int, help="return at most this many assets")
    parser.add_argument("--page-size", type=positive_int, default=10, help="page size (default: 10)")
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
    params = {"library_type": args.library_type}
    if args.search:
        params["search"] = args.search
    if args.file_format:
        params["format"] = args.file_format
    result = paginate(
        "getSocialMediaLibrary",
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
                "id": field(row, ["id", "file_id", "media_id"], ""),
                "name": field(row, ["file_name", "name", "filename"], ""),
                "format": field(row, ["format", "type"], ""),
            }
            for row in records
        ]
    return finish(result, records, args, COLUMNS, empty="No media assets found.")


if __name__ == "__main__":
    sys.exit(main())
