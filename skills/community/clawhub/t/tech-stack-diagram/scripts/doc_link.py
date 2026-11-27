#!/usr/bin/env python3
"""Turn a Tekyous diagram spec into a builder link, offline.

    python3 doc_link.py spec.json        # or: ... | python3 doc_link.py -

Prints https://tekyous.dev/builder#doc=v1.… : the spec itself, raw-deflated and base64url-encoded into the link's
fragment. Nothing is sent anywhere: the link opens the diagram in the Tekyous builder, where the user can edit it and
export the image. Python standard library only; no network, no files written.

The bytes match what the Tekyous MCP server puts in its own links (tests/test_doc_link.py checks them against links
the server's encoder made).
"""

from __future__ import annotations

import base64
import json
import sys
import zlib

BUILDER = "https://tekyous.dev/builder?utm_source=skill&utm_medium=offline"
VERSION = "v1"
# The builder refuses documents over 1 MB
MAX_JSON_BYTES = 1_000_000


def encode(spec: dict) -> str:
    """`v1.` + base64url (no padding) of raw deflate (level 9) of compact UTF-8 JSON."""
    raw = json.dumps(spec, separators=(",", ":"), ensure_ascii=False).encode()
    if len(raw) > MAX_JSON_BYTES:
        raise ValueError("the diagram is larger than 1 MB")
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    payload = base64.urlsafe_b64encode(c.compress(raw) + c.flush()).rstrip(b"=").decode()
    return f"{VERSION}.{payload}"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    try:
        text = sys.stdin.read() if argv[1] == "-" else open(argv[1], encoding="utf-8").read()
        spec = json.loads(text)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Could not read the spec: {e}", file=sys.stderr)
        return 1
    if not isinstance(spec, dict) or spec.get("format") != "tekyous-diagram":
        print('The spec must be a JSON object with "format": "tekyous-diagram".', file=sys.stderr)
        return 1
    try:
        print(f"{BUILDER}#doc={encode(spec)}")
    except ValueError as e:
        print(f"Could not encode the spec: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
