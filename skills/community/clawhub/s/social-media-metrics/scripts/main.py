#!/usr/bin/env python3
"""Social media metrics fetcher - main entry point.

Usage:
    python main.py --url "https://space.bilibili.com/946974"
    python main.py --nickname "影视飓风" --platform bilibili
    python main.py --url "https://www.youtube.com/@MrBeast"
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from platforms import PLATFORM_REGISTRY
from platforms.base import MetricsResult
from utils.resolver import resolve_input
from utils.browser import BrowserManager


async def fetch_metrics(
    url: str | None = None,
    nickname: str | None = None,
    platform: str | None = None,
) -> MetricsResult:
    if not url and not nickname:
        return MetricsResult(
            platform=platform or "unknown",
            success=False,
            error="Either --url or --nickname must be provided.",
        )

    try:
        resolved = resolve_input(url or nickname, platform_hint=platform)  # type: ignore[arg-type]
    except ValueError as e:
        return MetricsResult(
            platform=platform or "unknown",
            success=False,
            error=str(e),
        )

    platform_cls = PLATFORM_REGISTRY.get(resolved.platform)
    if platform_cls is None:
        return MetricsResult(
            platform=resolved.platform,
            success=False,
            error=f"Platform '{resolved.platform}' is not supported.",
        )

    scraper = platform_cls()

    try:
        if resolved.url and resolved.uid:
            result = await scraper.fetch_by_url(resolved.url)
        elif resolved.nickname:
            result = await scraper.fetch_by_nickname(resolved.nickname)
        else:
            result = await scraper.fetch_by_url(resolved.url or "")
    except Exception as e:
        result = MetricsResult(
            platform=resolved.platform,
            success=False,
            error=f"Unexpected error: {e}",
        )
    finally:
        mgr = await BrowserManager.get_instance()
        await mgr.close()

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch social media follower metrics")
    parser.add_argument("--url", help="Profile page URL")
    parser.add_argument("--nickname", help="Account display name / nickname")
    parser.add_argument(
        "--platform",
        help="Platform name (required when using --nickname)",
        choices=list(PLATFORM_REGISTRY.keys()),
    )
    args = parser.parse_args()

    if not args.url and not args.nickname:
        parser.error("At least one of --url or --nickname is required")

    if args.nickname and not args.platform:
        parser.error("--platform is required when using --nickname")

    result = asyncio.run(fetch_metrics(args.url, args.nickname, args.platform))
    print(result.to_json())

    if not result.success:
        sys.exit(1)


if __name__ == "__main__":
    main()
