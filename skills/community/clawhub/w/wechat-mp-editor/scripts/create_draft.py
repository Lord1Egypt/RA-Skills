#!/usr/bin/env python3
"""
Create or update a WeChat Official Account draft article.

Usage:
  # Create draft
  python3 create_draft.py --token TOKEN --json /path/to/article.json

  # Update draft (requires "media_id" in JSON)
  python3 create_draft.py --token TOKEN --json /path/to/article.json --update
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def call_api(token: str, endpoint: str, payload: dict) -> dict:
    """Call WeChat API with JSON payload."""
    url = f"https://api.weixin.qq.com/cgi-bin/{endpoint}?access_token={token}"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url, data=data)
    req.add_header("Content-Type", "application/json; charset=utf-8")

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Manage WeChat MP drafts")
    parser.add_argument("--token", required=True, help="WeChat access token")
    parser.add_argument("--json", required=True, help="Path to JSON file with article data")
    parser.add_argument("--update", action="store_true", help="Update existing draft instead of create")
    args = parser.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        payload = json.load(f)

    if args.update:
        if "media_id" not in payload:
            print("Error: --update requires 'media_id' in the JSON payload", file=sys.stderr)
            sys.exit(1)
        endpoint = "draft/update"
    else:
        endpoint = "draft/add"

    result = call_api(args.token, endpoint, payload)

    if "errcode" in result and result["errcode"] != 0:
        print(f"API Error [{result['errcode']}]: {result.get('errmsg', 'Unknown')}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
