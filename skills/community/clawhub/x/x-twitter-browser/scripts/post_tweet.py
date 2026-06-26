#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from session_lib import launch_browser, require_playwright, verify_session


COMPOSE_URL = "https://x.com/compose/post"
EDITOR_SELECTOR = '[data-testid="tweetTextarea_0"]'
POST_BUTTON_SELECTOR = '[data-testid="tweetButton"]'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post to X with Playwright browser auth")
    parser.add_argument("--text", help="Tweet text")
    parser.add_argument("--text-file", help="Read tweet text from file")
    parser.add_argument("--verify-only", action="store_true", help="Only verify the session")
    parser.add_argument("--timeout-ms", type=int, default=30000, help="Timeout per operation in ms (default: 30000)")
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Run Chromium headless (default: False).",
    )
    return parser.parse_args()


def load_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.text_file:
        return Path(args.text_file).read_text(encoding="utf-8").strip()
    return ""


def post_text(page, text: str, timeout_ms: int) -> None:
    page.goto(COMPOSE_URL, wait_until="domcontentloaded", timeout=timeout_ms)

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
    text = load_text(args)
    if not args.verify_only and not text:
        raise SystemExit("Provide --text or --text-file unless using --verify-only")

    sync_playwright = require_playwright()

    with sync_playwright() as pw:
        browser, context, page = launch_browser(
            pw, headless=args.headless, timeout_ms=args.timeout_ms,
        )
        try:
            verify_session(page, args.timeout_ms)
            if args.verify_only:
                return
            post_text(page, text, args.timeout_ms)
            page.wait_for_timeout(5000)
            print("Post flow executed. Check the timeline to confirm delivery.")
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
