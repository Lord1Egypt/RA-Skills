#!/usr/bin/env python3
"""Check fetching and optional Next.js JSON extraction with Scrapling 0.5.x.

Usage:
  python scrapling_smoke_test.py URL [URL ...] --fetcher fetcher|stealthy
  python scrapling_smoke_test.py URL --extract next_data
  python scrapling_smoke_test.py URL --fetcher stealthy --no-headless

Install: python -m pip install "scrapling[fetchers]>=0.5,<0.6"
Browser mode also needs: scrapling install
Exit 1 means a fetch/HTTP error, failed requested extraction, or a heuristic
indicator when --fail-on-indicator is set. Indicators otherwise warn only;
ordinary pages can legitimately mention CAPTCHA or include Turnstile scripts.
Exit 2 means invalid arguments or unavailable dependencies.
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import sys
from typing import Any


BLOCK_INDICATORS = (
    "something went wrong", "enable javascript", "turnstile", "captcha",
    "access denied", "verify you are human", "cf-chl-",
)


def _pick_fetcher(kind: str):
    if kind == "fetcher":
        from scrapling.fetchers import Fetcher

        return "Fetcher", Fetcher.get
    if kind == "stealthy":
        from scrapling.fetchers import StealthyFetcher

        return "StealthyFetcher", StealthyFetcher.fetch
    raise ValueError(f"Unknown fetcher: {kind}")


class _NextDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.active = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "script" and dict(attrs).get("id") == "__NEXT_DATA__":
            self.active = True

    def handle_data(self, data: str) -> None:
        if self.active:
            self.parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self.active = False


def _extract_next_data(html: str) -> Any:
    parser = _NextDataParser()
    parser.feed(html)
    parser.close()
    if not parser.parts:
        raise ValueError("__NEXT_DATA__ script not found or empty")
    return json.loads("".join(parser.parts))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="+", help="One or more URLs")
    parser.add_argument("--fetcher", choices=["fetcher", "stealthy"], default="fetcher")
    parser.add_argument("--extract", choices=["none", "next_data"], default="none")
    parser.add_argument("--timeout", type=float, default=60, help="Timeout in seconds")
    parser.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--solve-cloudflare", action="store_true", help="Browser mode only")
    parser.add_argument(
        "--fail-on-indicator", action="store_true",
        help="Fail on heuristic block keywords (default: warn only)",
    )
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.fetcher == "fetcher" and args.solve_cloudflare:
        parser.error("--solve-cloudflare requires --fetcher stealthy")

    try:
        fetcher_name, fetch = _pick_fetcher(args.fetcher)
    except ImportError as exc:
        print(
            f"Dependency import failed: {exc}. Install with this Python: "
            'python -m pip install "scrapling[fetchers]>=0.5,<0.6"',
            file=sys.stderr,
        )
        return 2

    failed = False
    for url in args.urls:
        print(f"\n=== {url}\nfetcher: {fetcher_name}")
        options: dict[str, Any] = {"timeout": args.timeout}
        if args.fetcher == "stealthy":
            options.update(
                timeout=args.timeout * 1000, headless=args.headless,
                network_idle=True, solve_cloudflare=args.solve_cloudflare,
                google_search=False,
            )
        try:
            response = fetch(url, **options)
            html = response.html_content or ""
            print("status:", response.status)
            print("html_len:", len(html))
            if not 200 <= response.status < 400:
                failed = True
            for indicator in BLOCK_INDICATORS:
                if indicator in html.lower():
                    print("possible_block_indicator:", indicator)
                    if args.fail_on_indicator:
                        failed = True
            title = response.css("title::text").get()
            if title:
                print("title:", title[:240])
            if args.extract == "next_data":
                data = _extract_next_data(html)
                print("next_data:", json.dumps(data, ensure_ascii=False))
        except Exception as exc:
            print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
