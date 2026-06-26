#!/usr/bin/env python3
"""
update_tags.py — Update tags on a Readwise Reader article.

The Readwise Save API is idempotent on URL — calling it again with the same
URL but different tags will update the tags on the existing entry.

Usage:
    python3 update_tags.py "https://example.com/article" "AI agent" "China" "Guide"

Environment:
    READWISE_TOKEN — Required.

Output (JSON to stdout):
    {"status": "ok", "tags": ["AI agent", "China", "Guide"]}
    {"status": "error", "error": "description"}
"""

import json
import os
import sys
import urllib.error
import urllib.request

READWISE_API_URL = "https://readwise.io/api/v3/save/"


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"status": "error", "error": "Usage: update_tags.py URL tag1 [tag2 ...]"}))
        sys.exit(1)

    url = sys.argv[1].strip()
    tags = [t.strip() for t in sys.argv[2:] if t.strip()]

    token = os.environ.get("READWISE_TOKEN", "")
    if not token:
        print(json.dumps({"status": "error", "error": "READWISE_TOKEN not set"}))
        sys.exit(1)

    if not tags:
        print(json.dumps({"status": "error", "error": "No tags provided"}))
        sys.exit(1)

    payload = {"url": url, "tags": tags}
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(READWISE_API_URL, data=data, method="POST")
    req.add_header("Authorization", f"Token {token}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status in (200, 201):
                print(json.dumps({"status": "ok", "tags": tags}, ensure_ascii=False))
                sys.exit(0)
            else:
                print(json.dumps({"status": "error", "error": f"API returned {resp.status}"}))
                sys.exit(1)
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8", errors="replace"))
            err = body.get("detail", str(body))
        except Exception:
            err = str(e)
        print(json.dumps({"status": "error", "error": f"API {e.code}: {err}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
