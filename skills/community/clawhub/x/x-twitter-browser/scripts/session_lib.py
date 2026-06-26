#!/usr/bin/env python3
"""Session management for x-twitter-browser.

Provides browser launch with saved cookie session, login verification,
and session save/load — all backed by ~/.openclaw/auth/x-twitter/cookies.json.
"""
from __future__ import annotations

import os
import random
import sys
from pathlib import Path
from typing import Any


PLATFORM = "x-twitter"
AUTH_DIR = Path.home() / ".openclaw" / "auth" / PLATFORM
COOKIE_PATH = AUTH_DIR / "cookies.json"

HOME_URL = "https://x.com/home"
LOGIN_HINTS = (
    "/i/flow/login",
    "/login",
    "/account/access",
    "/account/login_challenge",
)

CHROMIUM_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-software-rasterizer",
    "--disable-setuid-sandbox",
    "--disable-background-networking",
    "--disable-default-apps",
    "--disable-sync",
    "--no-first-run",
    "--no-zygote",
    "--disable-features=TranslateUI",
    "--disable-blink-features=AutomationControlled",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]


# ---------------------------------------------------------------------------
# Playwright bootstrap
# ---------------------------------------------------------------------------

def require_playwright() -> Any:
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependency: playwright. Run ./scripts/setup.sh first."
        ) from exc
    return sync_playwright


def _default_browsers_path() -> Path:
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Library" / "Caches" / "ms-playwright"
    if sys.platform == "win32":
        return home / "AppData" / "Local" / "ms-playwright"
    return home / ".cache" / "ms-playwright"


def ensure_playwright_browser_hint() -> None:
    env_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    bp = Path(env_path) if env_path else _default_browsers_path()
    if not bp.exists():
        raise SystemExit(
            "Playwright browsers not installed. Run: python3 -m playwright install chromium"
        )


# ---------------------------------------------------------------------------
# Session persistence
# ---------------------------------------------------------------------------

def has_saved_session() -> bool:
    return COOKIE_PATH.exists()


def save_session(context: Any) -> Path:
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(COOKIE_PATH))
    return COOKIE_PATH


# ---------------------------------------------------------------------------
# Browser launch
# ---------------------------------------------------------------------------

def launch_browser(
    playwright: Any,
    *,
    headless: bool = False,
    timeout_ms: int = 30_000,
) -> tuple[Any, Any, Any]:
    """Launch Chromium with saved X cookies and return (browser, context, page).

    Raises SystemExit if no saved session exists.
    """
    if not has_saved_session():
        raise SystemExit(
            "No saved session. Run setup_session.py first to log in to X."
        )

    launch_opts: dict[str, Any] = {
        "headless": headless,
        "args": CHROMIUM_ARGS,
    }
    if sys.platform == "darwin":
        launch_opts["channel"] = "chrome"

    try:
        browser = playwright.chromium.launch(**launch_opts)
    except Exception:
        if "channel" in launch_opts:
            del launch_opts["channel"]
            ensure_playwright_browser_hint()
            browser = playwright.chromium.launch(**launch_opts)
        else:
            raise

    context = browser.new_context(
        storage_state=str(COOKIE_PATH),
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        timezone_id="UTC",
        user_agent=random.choice(USER_AGENTS),
    )
    context.set_default_timeout(timeout_ms)

    page = context.new_page()
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        window.chrome = {runtime: {}};
    """)

    return browser, context, page


def launch_browser_fresh(
    playwright: Any,
    *,
    headless: bool = False,
    timeout_ms: int = 30_000,
) -> tuple[Any, Any, Any]:
    """Launch Chromium WITHOUT cookies — for setup_session.py login flow."""
    launch_opts: dict[str, Any] = {
        "headless": headless,
        "args": CHROMIUM_ARGS,
    }
    if sys.platform == "darwin":
        launch_opts["channel"] = "chrome"

    try:
        browser = playwright.chromium.launch(**launch_opts)
    except Exception:
        if "channel" in launch_opts:
            del launch_opts["channel"]
            ensure_playwright_browser_hint()
            browser = playwright.chromium.launch(**launch_opts)
        else:
            raise

    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        timezone_id="UTC",
        user_agent=random.choice(USER_AGENTS),
    )
    context.set_default_timeout(timeout_ms)
    page = context.new_page()
    return browser, context, page


# ---------------------------------------------------------------------------
# Login verification
# ---------------------------------------------------------------------------

def looks_logged_out(page: Any) -> bool:
    url = page.url.lower()
    if any(hint in url for hint in LOGIN_HINTS):
        return True
    title = page.title().lower()
    if "login" in title:
        return True
    content = page.content().lower()
    return "sign in to x" in content or "log in to x" in content


def verify_session(page: Any, timeout_ms: int) -> None:
    page.goto(HOME_URL, wait_until="domcontentloaded", timeout=timeout_ms)
    page.wait_for_timeout(3000)
    if looks_logged_out(page):
        raise RuntimeError(
            "Session is not authenticated. Run setup_session.py to log in again."
        )
    print(f"Session looks valid: {page.url}")
