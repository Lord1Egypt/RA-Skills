#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys

from session_lib import launch_browser, require_playwright, verify_session


EDITOR_SELECTOR = '[data-testid="tweetTextarea_0"]'
POST_BUTTON_SELECTOR = '[data-testid="tweetButton"]'


def extract_tweet_id(url_or_id: str) -> str:
    s = url_or_id.strip()
    match = re.search(r"/status/(\d+)", s)
    if match:
        return match.group(1)
    if s.isdigit():
        return s
    raise ValueError(f"Cannot extract tweet ID from: {url_or_id}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repost (retweet) or Quote tweet")
    parser.add_argument("--tweet", required=True, help="Tweet URL or ID")
    parser.add_argument("--text", help="Add your comment (Quote tweet). Omit for plain repost.")
    parser.add_argument("--verify-only", action="store_true", help="Only verify the session")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    parser.add_argument("--headless", action=argparse.BooleanOptionalAction, default=False)
    return parser.parse_args()


def open_tweet_and_repost(page, tweet_url: str, tweet_id: str, timeout_ms: int) -> None:
    target = tweet_url if "/status/" in tweet_url else f"https://x.com/i/status/{tweet_id}"
    page.goto(target, wait_until="domcontentloaded", timeout=timeout_ms)
    page.wait_for_timeout(3000)

    retweet_btn = page.locator('[data-testid="retweet"], [aria-label="Repost"]').first
    retweet_btn.wait_for(state="visible", timeout=timeout_ms)
    retweet_btn.scroll_into_view_if_needed()
    retweet_btn.click()
    page.wait_for_timeout(2000)

    confirm_btn = page.locator('[data-testid="retweetConfirm"]').or_(page.get_by_text("Repost", exact=True)).first
    confirm_btn.wait_for(state="visible", timeout=timeout_ms)
    confirm_btn.click()


def open_tweet_and_quote(page, tweet_url: str, tweet_id: str, text: str, timeout_ms: int) -> None:
    target = tweet_url if "/status/" in tweet_url else f"https://x.com/i/status/{tweet_id}"
    page.goto(target, wait_until="domcontentloaded", timeout=timeout_ms)
    page.wait_for_timeout(3000)

    retweet_btn = page.locator('[data-testid="retweet"], [aria-label="Repost"]').first
    retweet_btn.wait_for(state="visible", timeout=timeout_ms)
    retweet_btn.scroll_into_view_if_needed()
    retweet_btn.click()
    page.wait_for_timeout(2000)

    quote_btn = (
        page.locator('[data-testid="quote"]')
        .or_(page.get_by_text("Quote", exact=True))
        .or_(page.get_by_text("Quote Post", exact=True))
        .first
    )
    quote_btn.wait_for(state="visible", timeout=timeout_ms)
    quote_btn.click()
    page.wait_for_timeout(3000)

    editor = page.locator(EDITOR_SELECTOR).nth(0)
    editor.wait_for(state="visible", timeout=timeout_ms)
    editor.click()
    editor.press_sequentially(text, delay=60)
    page.wait_for_timeout(300)
    if "#" in text or "@" in text:
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    button = page.locator(POST_BUTTON_SELECTOR).first
    page.wait_for_function(
        """
        selector => {
          const element = document.querySelector(selector);
          return !!element && element.getAttribute('aria-disabled') !== 'true' && !element.disabled;
        }
        """,
        arg=POST_BUTTON_SELECTOR,
        timeout=timeout_ms,
    )
    button.click()


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
            text = (args.text or "").strip()
            if text:
                open_tweet_and_quote(page, tweet_url, tweet_id, text, args.timeout_ms)
                page.wait_for_timeout(5000)
                print("Quote tweet flow executed. Check your profile to confirm.")
            else:
                open_tweet_and_repost(page, tweet_url, tweet_id, args.timeout_ms)
                page.wait_for_timeout(3000)
                print("Repost flow executed. Check your profile to confirm.")
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
