#!/usr/bin/env python3
"""Upload an image into a Zoho Social brand media library.

Local files are read here and sent as a complete data-URI base64 payload.
Do not paste base64 into chat, tickets, or shell history. Remote URLs use
uploadSocialMediaFromUrl instead.

An agent that truncates the base64 stream produces a corrupt library asset
while the MCP call can still report success. This helper never truncates.
"""
from __future__ import annotations
import base64
import json
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from social_client import ENDPOINT, build_base_parser, call, field, headers_from

ALLOWED_SUFFIXES = {".png": "image/png", ".gif": "image/gif", ".jpeg": "image/jpeg", ".jpg": "image/jpeg"}
MAX_BYTES = 8 * 1024 * 1024


def build_parser():
    parser = build_base_parser(
        "Upload an image to a Zoho Social brand media library from a local file or URL."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", help="local PNG/GIF/JPEG path; encoded here, never truncated")
    source.add_argument("--image-url", help="https URL for uploadSocialMediaFromUrl")
    parser.add_argument("--filename", help="override stored filename")
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=MAX_BYTES,
        help=f"reject local files larger than this (default: {MAX_BYTES})",
    )
    return parser


def encode_local(path: Path, max_bytes: int):
    suffix = path.suffix.lower()
    mime = ALLOWED_SUFFIXES.get(suffix)
    if mime is None:
        print("Error: only PNG, GIF, JPEG, and JPG are supported", file=sys.stderr)
        sys.exit(2)
    if not path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    size = path.stat().st_size
    if size > max_bytes:
        print(f"Error: file exceeds --max-bytes ({size} > {max_bytes})", file=sys.stderr)
        sys.exit(2)
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}", path.name


def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    try:
        headers = headers_from(args, portal=True, brand=True)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    if args.file:
        path = Path(args.file).expanduser()
        data_uri, default_name = encode_local(path, args.max_bytes)
        filename = args.filename or default_name
        result = call(
            "uploadSocialMedia",
            {"headers": headers, "body": {"file": data_uri, "file_name": filename}},
            timeout=args.timeout,
        )
    else:
        body = {"image_url": args.image_url}
        if args.filename:
            body["file_name"] = args.filename
        result = call(
            "uploadSocialMediaFromUrl",
            {"headers": headers, "body": body},
            timeout=args.timeout,
        )
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1
    data = result.get("data", result)
    if isinstance(data, dict) and isinstance(data.get("data"), dict):
        data = data["data"]
    payload = data if isinstance(data, dict) else {}
    # Live evidence 2026-09-21: the usable ID arrives in file_path, not id, and a
    # success status with every field empty means Zoho silently dropped the image.
    file_id = field(payload, ["file_path", "id", "file_id", "media_id"], "")
    if not file_id:
        print("Error: upload reported success but returned no file ID", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    print(f"file_id: {file_id}")
    name = field(payload, ["file_name", "name", "filename"], "")
    if name and name != "-":
        print(f"name:    {name}")
    print("Re-list the library with list_media.py before attaching this ID to a post.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
