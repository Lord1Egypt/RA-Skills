#!/usr/bin/env python3
"""Set up an X/Twitter session by logging in via a visible browser.

Opens x.com/login in a real browser window. The user logs in manually
(username, password, 2FA if needed). Once the home timeline is visible,
press Enter in the terminal to save cookies for future headless use.

Usage:
    python3 scripts/setup_session.py
    python3 scripts/setup_session.py --verify-only
"""
from __future__ import annotations

import argparse
import sys

from session_lib import (
    launch_browser,
    launch_browser_fresh,
    has_saved_session,
    looks_logged_out,
    require_playwright,
    save_session,
    verify_session,
)


LOGIN_URL = "https://x.com/i/flow/login"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Log in to X and save session cookies")
    p.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify the existing saved session (no login flow)",
    )
    p.add_argument("--timeout-ms", type=int, default=60000, help="Timeout in ms (default: 60000)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    sync_playwright = require_playwright()

    with sync_playwright() as pw:
        # --verify-only: just check existing cookies
        if args.verify_only:
            browser, context, page = launch_browser(
                pw, headless=False, timeout_ms=args.timeout_ms,
            )
            try:
                verify_session(page, args.timeout_ms)
            finally:
                context.close()
                browser.close()
            return

        # Login flow: start fresh (no cookies)
        browser, context, page = launch_browser_fresh(
            pw, headless=False, timeout_ms=args.timeout_ms,
        )
        try:
            page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=args.timeout_ms)

            print(
                "\n"
                "╔══════════════════════════════════════════════════════════════╗\n"
                "║  X/Twitter Login                                            ║\n"
                "║                                                             ║\n"
                "║  A browser window has opened with the X login page.         ║\n"
                "║  Please log in with your account:                           ║\n"
                "║                                                             ║\n"
                "║  1. Enter your username/email                               ║\n"
                "║  2. Enter your password                                     ║\n"
                "║  3. Complete 2FA if prompted                                ║\n"
                "║  4. Wait until you see the home timeline                    ║\n"
                "║  5. Come back here and press ENTER to save session          ║\n"
                "╚══════════════════════════════════════════════════════════════╝",
                file=sys.stderr,
            )
            input()

            if looks_logged_out(page):
                print(
                    "WARNING: The page still looks like a login page. "
                    "Make sure you are logged in before pressing Enter.",
                    file=sys.stderr,
                )
                print("Press ENTER to save anyway, or Ctrl+C to abort.", file=sys.stderr)
                input()

            path = save_session(context)
            print(f"Session saved -> {path}", file=sys.stderr)
            print("You can now use all X actions (post, reply, like, etc.) in headless mode.", file=sys.stderr)

        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
