#!/usr/bin/env python3
"""ScrapeCreators Reddit API CLI.

Reads API key from:
- env SCRAPECREATORS_API_KEY
- or ~/.config/scrapecreators/api_key

Outputs JSON to stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "https://api.scrapecreators.com/v1"


def load_api_key() -> str:
    key = os.environ.get("SCRAPECREATORS_API_KEY")
    if key:
        return key.strip()

    p = Path.home() / ".config" / "scrapecreators" / "api_key"
    if p.exists():
        return p.read_text(encoding="utf-8").strip()

    raise SystemExit(
        "Missing ScrapeCreators API key. Set SCRAPECREATORS_API_KEY or create ~/.config/scrapecreators/api_key"
    )


def http_get(path: str, params: dict[str, object | None]) -> object:
    query: dict[str, str] = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, bool):
            query[k] = "true" if v else "false"
        elif isinstance(v, (int, float)):
            query[k] = str(v)
        else:
            query[k] = str(v)

    url = f"{BASE_URL}{path}"
    if query:
        url = url + "?" + urllib.parse.urlencode(query)

    req = urllib.request.Request(url)
    req.add_header("x-api-key", load_api_key())
    req.add_header("accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        raise SystemExit(f"HTTP {e.code} {e.reason}\n{body}")


def print_json(obj: object, pretty: bool) -> None:
    if pretty:
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(obj, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sc_reddit",
        description="ScrapeCreators Reddit API helper",
    )
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    sub = p.add_subparsers(dest="cmd", required=True)

    # /reddit/subreddit/details
    s = sub.add_parser("subreddit-details", help="Get subreddit details")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--subreddit", help="Case-sensitive subreddit name (e.g. AskReddit)")
    g.add_argument("--url", help="Full subreddit URL")

    # /reddit/subreddit
    s = sub.add_parser("subreddit-posts", help="Get subreddit posts")
    s.add_argument("--subreddit", required=True, help="Subreddit name")
    s.add_argument("--timeframe", choices=["all", "day", "week", "month", "year"])
    s.add_argument("--sort", choices=["best", "hot", "new", "top", "rising"])
    s.add_argument("--after", help="Pagination cursor from previous response")
    s.add_argument("--trim", action="store_true", help="Trim response")

    # /reddit/subreddit/search
    s = sub.add_parser("subreddit-search", help="Search within a subreddit")
    s.add_argument("--subreddit", required=True, help="Subreddit name")
    s.add_argument("--query", help="Search query")
    s.add_argument(
        "--sort",
        choices=["relevance", "hot", "top", "new", "comments"],
        help="Sort order",
    )
    s.add_argument("--timeframe", choices=["all", "year", "month", "week", "day", "hour"])
    s.add_argument("--cursor", help="Pagination cursor from previous response")

    # /reddit/search
    s = sub.add_parser("search", help="Search Reddit posts")
    s.add_argument("--query", required=True, help="Search query")
    s.add_argument("--sort", choices=["relevance", "new", "top", "comment_count"])
    s.add_argument("--timeframe", choices=["all", "day", "week", "month", "year"])
    s.add_argument("--after", help="Pagination 'after' from previous response")
    s.add_argument("--trim", action="store_true", help="Trim response")

    # /reddit/post/comments
    s = sub.add_parser("post-comments", help="Get post + comments")
    s.add_argument("--url", required=True, help="Full Reddit post URL")
    s.add_argument("--cursor", help="Cursor for more comments/replies")
    s.add_argument("--trim", action="store_true", help="Trim response")

    # /reddit/ads/search
    s = sub.add_parser("ads-search", help="Search Reddit Ad Library")
    s.add_argument("--query", required=True, help="Search query")
    s.add_argument(
        "--industries",
        choices=[
            "RETAIL_AND_ECOMMERCE",
            "TECH_B2B",
            "TECH_B2C",
            "EDUCATION",
            "ENTERTAINMENT",
            "GAMING",
            "FINANCIAL_SERVICES",
            "HEALTH_AND_BEAUTY",
            "CONSUMER_PACKAGED_GOODS",
            "EMPLOYMENT",
            "AUTO",
            "TRAVEL",
            "REAL_ESTATE",
            "GAMBLING_AND_FANTASY_SPORTS",
            "POLITICS_AND_GOVERNMENT",
            "OTHER",
        ],
    )
    s.add_argument("--budgets", choices=["LOW", "MEDIUM", "HIGH"])
    s.add_argument("--formats", choices=["IMAGE", "VIDEO", "CAROUSEL", "FREE_FORM"])
    s.add_argument("--placements", choices=["FEED", "COMMENTS_PAGE"])
    s.add_argument(
        "--objectives",
        choices=[
            "IMPRESSIONS",
            "CLICKS",
            "CONVERSIONS",
            "VIDEO_VIEWABLE_IMPRESSIONS",
            "APP_INSTALLS",
        ],
    )

    # /reddit/ad
    s = sub.add_parser("ad", help="Get a Reddit ad by id")
    s.add_argument("--id", required=True, help="Ad id")

    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)

    cmd = args.cmd
    pretty = bool(args.pretty)

    if cmd == "subreddit-details":
        params = {"subreddit": getattr(args, "subreddit", None), "url": getattr(args, "url", None)}
        obj = http_get("/reddit/subreddit/details", params)
        print_json(obj, pretty)
        return 0

    if cmd == "subreddit-posts":
        obj = http_get(
            "/reddit/subreddit",
            {
                "subreddit": args.subreddit,
                "timeframe": args.timeframe,
                "sort": args.sort,
                "after": args.after,
                "trim": args.trim or None,
            },
        )
        print_json(obj, pretty)
        return 0

    if cmd == "subreddit-search":
        obj = http_get(
            "/reddit/subreddit/search",
            {
                "subreddit": args.subreddit,
                "query": args.query,
                "sort": args.sort,
                "timeframe": args.timeframe,
                "cursor": args.cursor,
            },
        )
        print_json(obj, pretty)
        return 0

    if cmd == "search":
        obj = http_get(
            "/reddit/search",
            {
                "query": args.query,
                "sort": args.sort,
                "timeframe": args.timeframe,
                "after": args.after,
                "trim": args.trim or None,
            },
        )
        print_json(obj, pretty)
        return 0

    if cmd == "post-comments":
        obj = http_get(
            "/reddit/post/comments",
            {
                "url": args.url,
                "cursor": args.cursor,
                "trim": args.trim or None,
            },
        )
        print_json(obj, pretty)
        return 0

    if cmd == "ads-search":
        obj = http_get(
            "/reddit/ads/search",
            {
                "query": args.query,
                "industries": args.industries,
                "budgets": args.budgets,
                "formats": args.formats,
                "placements": args.placements,
                "objectives": args.objectives,
            },
        )
        print_json(obj, pretty)
        return 0

    if cmd == "ad":
        obj = http_get("/reddit/ad", {"id": args.id})
        print_json(obj, pretty)
        return 0

    raise SystemExit(f"Unknown command: {cmd}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
