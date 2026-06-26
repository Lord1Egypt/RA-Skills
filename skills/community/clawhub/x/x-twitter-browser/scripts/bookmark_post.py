#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys

from session_lib import launch_browser, require_playwright, verify_session


def extract_tweet_id(url_or_id: str) -> str:
    s = url_or_id.strip()
    match = re.search(r"/status/(\d+)", s)
    if match:
        return match.group(1)
    if s.isdigit():
        return s
    raise ValueError(f"Cannot extract tweet ID from: {url_or_id}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bookmark or remove bookmark from an X tweet")
    parser.add_argument("--tweet", required=True, help="Tweet URL or ID")
    parser.add_argument("--undo", action="store_true", help="Remove bookmark instead of adding")
    parser.add_argument("--verify-only", action="store_true", help="Only verify the session")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    parser.add_argument("--headless", action=argparse.BooleanOptionalAction, default=False)
    return parser.parse_args()


def open_tweet_and_bookmark(page, tweet_url: str, tweet_id: str, undo: bool, timeout_ms: int) -> None:
    target = tweet_url if "/status/" in tweet_url else f"https://x.com/i/status/{tweet_id}"
    page.goto(target, wait_until="domcontentloaded", timeout=timeout_ms)
    page.wait_for_timeout(3000)

    if undo:
        btn = page.locator(
            '[data-testid="removeBookmark"], [aria-label="Remove bookmark"]'
        ).or_(page.get_by_text("Remove post from Bookmarks")).first
    else:
        btn = page.locator(
            '[data-testid="bookmark"], [aria-label="Add bookmark"], [aria-label="Bookmark"]'
        ).or_(page.get_by_text("Add post to Bookmarks")).first
    btn.wait_for(state="visible", timeout=timeout_ms)
    btn.scroll_into_view_if_needed()
    btn.click()


def main() -> None:
    args = parse_args()
    tweet_input = args.tweet.strip()
    tweet_id = extract_tweet_id(tweet_input)
    sync_playwright = require_playwright()

    with sync_playwright() as pw:
        browser, context, page = launch_browser(
            pw, headless=args.headless, timeout_ms=args.timeout_ms,
        )
        try:
            verify_session(page, args.timeout_ms)
            if args.verify_only:
                return
            tweet_url = tweet_input if "/status/" in tweet_input else f"https://x.com/i/status/{tweet_id}"
            open_tweet_and_bookmark(page, tweet_url, tweet_id, args.undo, args.timeout_ms)
            page.wait_for_timeout(2000)
            action = "Remove bookmark" if args.undo else "Bookmark"
            print(f"{action} flow executed. Check the tweet or Bookmarks to confirm.")
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
