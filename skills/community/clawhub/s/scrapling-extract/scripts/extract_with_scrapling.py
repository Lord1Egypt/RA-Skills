#!/usr/bin/env python3
"""Simple CLI extractor using Scrapling.

Examples:
  python scripts/extract_with_scrapling.py --url https://example.com --css "h1::text"
  python scripts/extract_with_scrapling.py --url https://example.com --css "h1::text" --fetcher dynamic
  python scripts/extract_with_scrapling.py --url https://example.com --css ".price::text" --fetcher stealthy
  python scripts/extract_with_scrapling.py --html-file page.html --xpath "//title/text()"
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)


def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract data from HTML using Scrapling.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url", help="HTTP(S) URL to fetch with Scrapling Fetcher.")
    source.add_argument("--html-file", help="Local HTML file path to parse.")
    parser.add_argument("--css", help="CSS selector (example: h1::text).")
    parser.add_argument("--xpath", help="XPath selector (example: //h1/text()).")
    parser.add_argument(
        "--fetcher",
        choices=["static", "dynamic", "stealthy"],
        default="static",
        help="Fetcher type: static (default), dynamic (JS rendering), stealthy (anti-bot).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30).",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Return all matches. Default returns first match only.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )
    return parser


def _first_or_all(result: Any, want_all: bool) -> Any:
    if want_all:
        return result
    if isinstance(result, list):
        return result[0] if result else None
    return result


def _fetch_url(url: str, fetcher_type: str, timeout: int) -> Any:
    try:
        if fetcher_type == "dynamic":
            from scrapling.fetchers import DynamicFetcher  # type: ignore

            log.info("Fetching with DynamicFetcher: %s", url)
            page = DynamicFetcher().fetch(url, timeout=timeout * 1000)
        elif fetcher_type == "stealthy":
            from scrapling.fetchers import StealthyFetcher  # type: ignore

            log.info("Fetching with StealthyFetcher: %s", url)
            page = StealthyFetcher().fetch(url, timeout=timeout * 1000)
        else:
            from scrapling.fetchers import Fetcher  # type: ignore

            log.info("Fetching with Fetcher (auto_match): %s", url)
            page = Fetcher.auto_match(url, auto_save=True, disable_adaptive=False)
    except ImportError:
        print(
            "Scrapling fetchers not installed. Run: pip install 'scrapling[fetchers]' && scrapling install",
            file=sys.stderr,
        )
        sys.exit(2)
    log.info("Fetch complete: %s", url)
    return page


def main() -> int:
    parser = _make_parser()
    args = parser.parse_args()

    if not args.css and not args.xpath:
        parser.error("Provide at least one selector with --css or --xpath.")

    try:
        if args.url:
            page = _fetch_url(args.url, args.fetcher, args.timeout)
        else:
            from scrapling import Adaptor  # type: ignore

            html_path = Path(args.html_file)
            if not html_path.exists():
                parser.error(f"HTML file not found: {html_path}")
            log.info("Parsing local file: %s", html_path)
            page = Adaptor(html_path.read_text(encoding="utf-8"))
    except ImportError:
        print("Scrapling is not installed. Run: pip install scrapling", file=sys.stderr)
        return 2
    except Exception as exc:
        log.error("Failed to fetch/parse: %s", exc)
        return 1

    output: dict[str, Any] = {}

    if args.css:
        css_data = page.css(args.css).getall() if args.all else page.css_first(args.css)
        result = _first_or_all(css_data, args.all)
        match_count = len(result) if isinstance(result, list) else (0 if result is None else 1)
        log.info("CSS '%s' → %d match(es)", args.css, match_count)
        if result is None:
            log.warning("CSS selector '%s' returned no matches", args.css)
        output["css"] = result

    if args.xpath:
        xpath_data = page.xpath(args.xpath).getall() if args.all else page.xpath_first(args.xpath)
        result = _first_or_all(xpath_data, args.all)
        match_count = len(result) if isinstance(result, list) else (0 if result is None else 1)
        log.info("XPath '%s' → %d match(es)", args.xpath, match_count)
        if result is None:
            log.warning("XPath selector '%s' returned no matches", args.xpath)
        output["xpath"] = result

    if args.pretty:
        print(json.dumps(output, indent=2, ensure_ascii=True))
    else:
        print(json.dumps(output, separators=(",", ":"), ensure_ascii=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
