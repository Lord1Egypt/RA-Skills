#!/usr/bin/env python3
"""Late Reddit helper CLI.

Reads Late API key from:
- env LATE_API_KEY
- or ~/.config/late/api_key

Base URL: https://getlate.dev/api

This is focused on Reddit workflows: list accounts, validate subreddit, list subreddits/flairs, search/feed, and create posts.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "https://getlate.dev/api"


def load_api_key() -> str:
    key = os.environ.get("LATE_API_KEY")
    if key:
        return key.strip()

    p = Path.home() / ".config" / "late" / "api_key"
    if p.exists():
        return p.read_text(encoding="utf-8").strip()

    raise SystemExit(
        "Missing Late API key. Set LATE_API_KEY or create ~/.config/late/api_key"
    )


def http_request(method: str, path: str, params: dict[str, object | None] | None = None, body: object | None = None) -> object:
    url = f"{BASE_URL}{path}"

    if params:
        query: dict[str, str] = {}
        for k, v in params.items():
            if v is None:
                continue
            if isinstance(v, bool):
                query[k] = "true" if v else "false"
            else:
                query[k] = str(v)
        if query:
            url = url + "?" + urllib.parse.urlencode(query)

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {load_api_key()}")
    req.add_header("accept", "application/json")
    if body is not None:
        req.add_header("content-type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        raise SystemExit(f"HTTP {e.code} {e.reason}\n{body_txt}")


def print_json(obj: object, pretty: bool) -> None:
    if pretty:
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(obj, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="late_reddit", description="Late API Reddit helper")
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("accounts", help="List connected accounts")
    s.add_argument("--platform", help="Filter by platform (e.g. reddit)")

    s = sub.add_parser("validate-subreddit", help="Check subreddit existence and basic info")
    s.add_argument("--subreddit", required=True, help="Subreddit name, with or without r/")

    s = sub.add_parser("reddit-subreddits", help="List subreddits the account can post to")
    s.add_argument("--account-id", required=True)

    s = sub.add_parser("reddit-flairs", help="List flairs for a subreddit")
    s.add_argument("--account-id", required=True)
    s.add_argument("--subreddit", required=True)

    s = sub.add_parser("feed", help="Get subreddit feed")
    s.add_argument("--account-id", required=True)
    s.add_argument("--subreddit", required=True)
    s.add_argument("--sort", choices=["hot", "new", "top", "rising"], default="hot")
    s.add_argument("--time", choices=["hour", "day", "week", "month", "year", "all"], default="week")
    s.add_argument("--limit", type=int, default=25)
    s.add_argument("--after", help="Pagination cursor")

    s = sub.add_parser("search", help="Search Reddit posts")
    s.add_argument("--account-id", required=True)
    s.add_argument("--query", required=True)
    s.add_argument("--subreddit", help="Optional subreddit scope")
    s.add_argument("--sort", choices=["relevance", "hot", "top", "new", "comments"], default="new")
    s.add_argument("--limit", type=int, default=25)
    s.add_argument("--after", help="Pagination cursor")
    s.add_argument("--restrict-sr", choices=["0", "1"], default="1")

    s = sub.add_parser("create-post", help="Create a Reddit post (publish now or schedule)")
    s.add_argument("--account-id", required=True)
    s.add_argument("--subreddit", required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--body", default="")
    s.add_argument("--url", help="If set, creates a link post (unless --force-self)")
    s.add_argument("--force-self", action="store_true")
    s.add_argument("--flair-id")
    s.add_argument("--publish-now", action="store_true")
    s.add_argument("--scheduled-for", help="ISO datetime (e.g. 2026-03-20T10:00:00Z)")
    s.add_argument(
        "--media",
        action="append",
        default=[],
        help="Remote media URL (repeatable). Uses type=image by default.",
    )

    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    pretty = bool(args.pretty)

    if args.cmd == "accounts":
        obj = http_request("GET", "/v1/accounts", {"platform": args.platform})
        print_json(obj, pretty)
        return 0

    if args.cmd == "validate-subreddit":
        # Late expects query param `name` (subreddit name, with or without r/)
        obj = http_request("GET", "/v1/tools/validate/subreddit", {"name": args.subreddit})
        print_json(obj, pretty)
        return 0

    if args.cmd == "reddit-subreddits":
        obj = http_request("GET", f"/v1/accounts/{args.account_id}/reddit-subreddits")
        print_json(obj, pretty)
        return 0

    if args.cmd == "reddit-flairs":
        obj = http_request(
            "GET",
            f"/v1/accounts/{args.account_id}/reddit-flairs",
            {"subreddit": args.subreddit},
        )
        print_json(obj, pretty)
        return 0

    if args.cmd == "feed":
        obj = http_request(
            "GET",
            "/v1/reddit/feed",
            {
                "accountId": args.account_id,
                "subreddit": args.subreddit,
                "sort": args.sort,
                "t": args.time,
                "limit": args.limit,
                "after": args.after,
            },
        )
        print_json(obj, pretty)
        return 0

    if args.cmd == "search":
        obj = http_request(
            "GET",
            "/v1/reddit/search",
            {
                "accountId": args.account_id,
                "subreddit": args.subreddit,
                "q": args.query,
                "restrict_sr": args.restrict_sr,
                "sort": args.sort,
                "limit": args.limit,
                "after": args.after,
            },
        )
        print_json(obj, pretty)
        return 0

    if args.cmd == "create-post":
        content = args.title.strip()
        if args.body.strip():
            content = content + "\n\n" + args.body.strip()

        platform_specific: dict[str, object] = {
            "subreddit": args.subreddit,
            "title": args.title.strip(),
        }
        if args.url:
            platform_specific["url"] = args.url
        if args.force_self:
            platform_specific["forceSelf"] = True
        if args.flair_id:
            platform_specific["flairId"] = args.flair_id

        media_items = []
        for u in args.media:
            media_items.append({"type": "image", "url": u})

        payload: dict[str, object] = {
            "content": content,
            "mediaItems": media_items if media_items else None,
            "platforms": [
                {
                    "platform": "reddit",
                    "accountId": args.account_id,
                    "platformSpecificData": platform_specific,
                    "scheduledFor": args.scheduled_for,
                }
            ],
            "publishNow": bool(args.publish_now),
            "scheduledFor": args.scheduled_for,
            "timezone": "UTC",
        }
        # Remove Nones (Late tolerates them but keep request clean)
        payload = {k: v for k, v in payload.items() if v is not None}
        if payload.get("mediaItems") is None:
            payload.pop("mediaItems", None)

        obj = http_request("POST", "/v1/posts", body=payload)
        print_json(obj, pretty)
        return 0

    raise SystemExit(f"Unknown command: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
