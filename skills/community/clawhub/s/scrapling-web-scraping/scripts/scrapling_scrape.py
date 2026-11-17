#!/usr/bin/env python3
"""One-off CSS/XPath extraction with Scrapling 0.5.x.

Examples:
  python scrapling_scrape.py --url https://example.com --css 'h1::text'
  python scrapling_scrape.py --url https://example.com --xpath '//h1/text()' --mode stealthy --no-headless

Install: python -m pip install "scrapling[fetchers]>=0.5,<0.6"
Browser mode also needs: scrapling install
For larger crawls use Scrapling Spiders. Run offline checks with:
  python -m unittest discover -s openclaw-skill-scrapling-mcp/scripts -p 'test_*.py'
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


def _select(page: Any, *, css: str | None, xpath: str | None, adaptive: bool, auto_save: bool) -> Any:
    options = {"adaptive": adaptive, "auto_save": auto_save}
    return page.css(css, **options) if css else page.xpath(xpath, **options)


def _fetch(args: argparse.Namespace) -> Any:
    # Enable storage before parsing, including fingerprint-only --auto-save runs.
    selector_config = {"adaptive": args.adaptive or args.auto_save}
    if args.mode == "fetcher":
        from scrapling.fetchers import FetcherSession

        with FetcherSession(impersonate="chrome", selector_config=selector_config) as session:
            return session.get(args.url, timeout=args.timeout)

    from scrapling.fetchers import StealthySession

    with StealthySession(headless=args.headless, selector_config=selector_config) as session:
        return session.fetch(
            args.url,
            timeout=args.timeout * 1000,
            network_idle=args.network_idle,
            solve_cloudflare=args.solve_cloudflare,
            google_search=False,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--mode", choices=["fetcher", "stealthy"], default="fetcher")
    selectors = parser.add_mutually_exclusive_group(required=True)
    selectors.add_argument("--css", help="CSS selector (supports ::text and ::attr())")
    selectors.add_argument("--xpath", help="XPath selector")
    parser.add_argument("--first", action="store_true", help="Return only the first match")
    parser.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--solve-cloudflare", action="store_true", help="Browser mode only")
    parser.add_argument("--network-idle", action="store_true", help="Browser mode only")
    parser.add_argument("--timeout", type=float, default=60, help="Timeout in seconds")
    parser.add_argument("--adaptive", action="store_true", help="Relocate saved selector fingerprints")
    parser.add_argument("--auto-save", action="store_true", help="Save selector fingerprints")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.mode == "fetcher" and (args.solve_cloudflare or args.network_idle):
        parser.error("--solve-cloudflare and --network-idle require --mode stealthy")

    try:
        page = _fetch(args)
        if not 200 <= page.status < 400:
            raise RuntimeError(f"HTTP status {page.status}")
        selected = _select(
            page, css=args.css, xpath=args.xpath,
            adaptive=args.adaptive, auto_save=args.auto_save,
        )
        payload = {
            "url": page.url,
            "mode": args.mode,
            "options": {
                "headless": args.headless,
                "solve_cloudflare": args.solve_cloudflare,
                "network_idle": args.network_idle,
                "adaptive": args.adaptive,
                "auto_save": args.auto_save,
            },
            "selector": {"css": args.css, "xpath": args.xpath},
            "result": selected.get() if args.first else selected.getall(),
        }
    except ImportError as exc:
        print(
            f"Dependency import failed: {exc}. Install with this Python: "
            'python -m pip install "scrapling[fetchers]>=0.5,<0.6"',
            file=sys.stderr,
        )
        return 2
    except Exception as exc:
        print(f"Extraction failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
