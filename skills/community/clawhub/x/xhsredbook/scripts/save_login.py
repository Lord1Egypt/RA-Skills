#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
save_login.py - Login to Xiaohongshu and persist session via browser profile.
Run once. After login, publish.py reuses the same profile — no re-login needed.
"""

import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

from config import resolve_profile_dir


def save_login(profile_dir: str | None = None):
    user_data_dir, persistent = resolve_profile_dir(profile_dir)
    if not persistent:
        # For save_login, persistence is the whole point — default to .local/xhs_browser_profile
        user_data_dir = Path(__file__).resolve().parent.parent / ".local" / "xhs_browser_profile"
        user_data_dir.mkdir(parents=True, exist_ok=True)
        persistent = True

    print("\n=== Xiaohongshu Login (Persistent Profile) ===\n")
    print(f"Profile directory: {user_data_dir}")
    print("1. Browser will open Xiaohongshu creator center")
    print("2. Scan QR code to login")
    print("3. After login succeeds, press ENTER here to close browser")
    print("   (All login state is auto-saved to browser profile)\n")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            viewport={"width": 1920, "height": 1080},
            args=["--start-maximized"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        )

        page = context.new_page()

        try:
            print("[INFO] Opening Xiaohongshu creator center...")
            page.goto("https://creator.xiaohongshu.com/", timeout=30000)
            page.wait_for_timeout(3000)

            print("\n" + "=" * 50)
            print("Please scan QR code to login now.")
            print("=" * 50 + "\n")

            # Wait for user confirmation
            import threading
            done = threading.Event()

            def wait_enter():
                input(">>> Press ENTER after login is complete: ")
                done.set()

            t = threading.Thread(target=wait_enter, daemon=True)
            t.start()

            # Also auto-detect login (max 3 min)
            start = time.time()
            while time.time() - start < 180:
                if done.is_set():
                    print("\n[OK] Confirmed by user.")
                    break
                url = page.url
                if "creator.xiaohongshu.com" in url and "login" not in url.lower():
                    print(f"\n[OK] Login detected! URL: {url}")
                    break
                time.sleep(2)
            else:
                print("\n[WARN] Timeout — closing anyway. If you logged in, state is still saved.")

            # Let cookies/storage settle
            page.wait_for_timeout(2000)

            print(f"\n[OK] Browser profile saved to: {user_data_dir}")
            print("You can now run publish.py — no login needed.\n")

        except Exception as e:
            print(f"\n[ERROR] {e}")

        finally:
            context.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Login to Xiaohongshu and persist session")
    parser.add_argument("--profile-dir", default=None, help="Browser profile directory (default: .local/xhs_browser_profile)")
    args = parser.parse_args()
    save_login(profile_dir=args.profile_dir)
