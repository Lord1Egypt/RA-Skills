#!/usr/bin/env python3
"""Yep Search API CLI — zero external dependencies."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def main():
    parser = argparse.ArgumentParser(description="Search the web via Yep API")
    parser.add_argument("query", help="Search query (1-1000 chars)")
    parser.add_argument("-n", type=int, default=10, help="Number of results (default: 10, max: 100)")
    parser.add_argument("--highlights", action="store_true", help="Return content highlights (~$0.009/call vs $0.004 basic)")
    parser.add_argument("--mode", choices=["fast", "balanced"], default="balanced", help="Search mode (default: balanced)")
    parser.add_argument("--lang", help="ISO 639-1 language code (e.g., en, de, ja)")
    parser.add_argument("--include-domains", help="Comma-separated domains to restrict search to")
    parser.add_argument("--exclude-domains", help="Comma-separated domains to exclude")
    parser.add_argument("--safe", action="store_true", help="Enable safe search")
    parser.add_argument("--after", help="Only results published after this date (ISO 8601)")
    parser.add_argument("--before", help="Only results published before this date (ISO 8601)")
    parser.add_argument("--crawl-after", help="Only results crawled after this date (ISO 8601)")
    parser.add_argument("--crawl-before", help="Only results crawled before this date (ISO 8601)")

    args = parser.parse_args()

    api_key = os.environ.get("YEP_API_KEY", "").strip()
    if not api_key:
        print("Missing YEP_API_KEY. Get one at https://platform.yep.com/app (free $10 credit on signup)", file=sys.stderr)
        sys.exit(1)

    body = {
        "query": args.query,
        "type": "highlights" if args.highlights else "basic",
        "limit": max(1, min(args.n, 100)),
        "search_mode": args.mode,
        "safe_search": args.safe,
    }

    if args.lang:
        body["language"] = [args.lang]
    if args.include_domains:
        body["include_domains"] = args.include_domains
    if args.exclude_domains:
        body["exclude_domains"] = args.exclude_domains
    if args.after:
        body["start_published_date"] = args.after
    if args.before:
        body["end_published_date"] = args.before
    if args.crawl_after:
        body["start_crawl_date"] = args.crawl_after
    if args.crawl_before:
        body["end_crawl_date"] = args.crawl_before

    req = urllib.request.Request(
        "https://platform.yep.com/api/search",
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "yep-search-skill/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        text = e.read().decode() if e.fp else ""
        print(f"Yep Search failed ({e.code}): {text}", file=sys.stderr)
        sys.exit(1)

    results = (data.get("results") or [])[:args.n]

    if not results:
        print("No results found.")
        sys.exit(0)

    print(f"## Results ({len(results)})\n")

    for r in results:
        title = (r.get("title") or r.get("meta_title") or "").strip()
        url = (r.get("url") or "").strip()
        desc = (r.get("description") or r.get("meta_description") or "").strip()

        if not url:
            continue
        print(f"- **{title or 'Untitled'}**")
        print(f"  {url}")
        if desc:
            print(f"  {desc[:300]}{'...' if len(desc) > 300 else ''}")
        print()

    api_cost = data.get("api_cost")
    if api_cost:
        balance = data.get("balance", {}).get("after", "?")
        print(f"---\nCost: ${api_cost['cost']} | Balance: ${balance}")


if __name__ == "__main__":
    main()
