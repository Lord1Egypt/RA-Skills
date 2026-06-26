from __future__ import annotations

import asyncio
import glob
import os
import platform
import shutil
import subprocess
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from playwright.async_api import async_playwright, Browser, Page, Playwright

_DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

_SYSTEM = platform.system()

_SYSTEM_CHROME_PATHS: list[str] = []

if _SYSTEM == "Darwin":
    _SYSTEM_CHROME_PATHS.append(
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    )
elif _SYSTEM == "Windows":
    for env_var in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
        base = os.environ.get(env_var, "")
        if base:
            _SYSTEM_CHROME_PATHS.append(
                os.path.join(base, "Google", "Chrome", "Application", "chrome.exe")
            )

for _cmd in ("google-chrome", "google-chrome-stable", "chromium-browser", "chromium"):
    _found = shutil.which(_cmd)
    if _found:
        _SYSTEM_CHROME_PATHS.append(_found)


def _find_playwright_chromium() -> str | None:
    """Find Playwright's installed Chromium executable as fallback.

    Playwright >= 1.39 ships "Google Chrome for Testing" instead of plain
    Chromium.  Both old and new directory layouts are searched.
    """
    if _SYSTEM == "Darwin":
        base = os.path.expanduser("~/Library/Caches/ms-playwright")
        patterns = [
            # New layout (Playwright >= 1.39): "Google Chrome for Testing"
            "chromium-*/chrome-mac-*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
            # Old layout: plain Chromium
            "chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
        ]
    elif _SYSTEM == "Linux":
        base = os.path.expanduser("~/.cache/ms-playwright")
        patterns = [
            "chromium-*/chrome-linux*/chrome",
        ]
    elif _SYSTEM == "Windows":
        base = os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright")
        patterns = [
            "chromium-*/chrome-win*/chrome.exe",
        ]
    else:
        return None
    if not os.path.isdir(base):
        return None
    for pattern in patterns:
        matches = glob.glob(os.path.join(base, pattern))
        if matches:
            return sorted(matches)[-1]
    return None


def _find_chrome() -> str:
    for p in _SYSTEM_CHROME_PATHS:
        if p and os.path.isfile(p):
            return p
    pw_chromium = _find_playwright_chromium()
    if pw_chromium:
        return pw_chromium
    raise RuntimeError(
        "Chrome/Chromium not found. Please install Google Chrome, "
        "or run 'playwright install chromium' to install Playwright's Chromium."
    )


class BrowserManager:
    """Manages a shared Playwright browser instance."""

    _instance: BrowserManager | None = None
    _lock: asyncio.Lock = asyncio.Lock()

    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._cdp_browser: Browser | None = None
        self._chrome_proc: subprocess.Popen | None = None

    @classmethod
    async def get_instance(cls) -> BrowserManager:
        async with cls._lock:
            if cls._instance is None:
                cls._instance = BrowserManager()
            return cls._instance

    async def _ensure_playwright(self) -> Playwright:
        if self._playwright is None:
            self._playwright = await async_playwright().start()
        return self._playwright

    async def _ensure_browser(self) -> Browser:
        if self._browser is None or not self._browser.is_connected():
            pw = await self._ensure_playwright()
            for channel in ("chrome", "msedge", None):
                try:
                    self._browser = await pw.chromium.launch(
                        headless=True,
                        channel=channel,
                    )
                    return self._browser
                except Exception:
                    continue
            raise RuntimeError(
                "No usable browser found. Install Google Chrome, "
                "or run 'playwright install chromium' to download one."
            )
        return self._browser

    async def _ensure_cdp_browser(self) -> Browser:
        """Launch a real Chrome process and connect via CDP.

        This bypasses automation detection used by sites like Douyin
        because Chrome runs without --enable-automation and other
        Playwright-injected flags.  We reuse a persistent profile so
        cookies survive across runs.
        """
        if self._cdp_browser is not None and self._cdp_browser.is_connected():
            return self._cdp_browser

        pw = await self._ensure_playwright()
        port = 19222
        user_data = os.path.expanduser("~/.playwright_cdp_profile")

        chrome_bin = _find_chrome()
        self._chrome_proc = subprocess.Popen(
            [
                chrome_bin,
                f"--remote-debugging-port={port}",
                f"--user-data-dir={user_data}",
                "--no-first-run",
                "--no-default-browser-check",
                "--window-size=1280,800",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        await asyncio.sleep(2)

        self._cdp_browser = await pw.chromium.connect_over_cdp(
            f"http://127.0.0.1:{port}"
        )
        # Close the initial about:blank tab so each platform starts clean
        default_ctx = self._cdp_browser.contexts[0]
        for p in default_ctx.pages:
            try:
                await p.close()
            except Exception:
                pass

        return self._cdp_browser

    @asynccontextmanager
    async def new_page(self, **kwargs) -> AsyncGenerator[Page, None]:  # type: ignore[override]
        browser = await self._ensure_browser()
        context = await browser.new_context(
            user_agent=_DEFAULT_UA,
            viewport={"width": 1280, "height": 800},
            **kwargs,
        )
        page = await context.new_page()
        try:
            yield page
        finally:
            await context.close()

    @asynccontextmanager
    async def new_cdp_page(self) -> AsyncGenerator[Page, None]:  # type: ignore[override]
        """Create a page in a real Chrome process connected via CDP.

        Uses the default browser context (not an incognito context) so that
        cookies from prior visits are available — required by sites like
        Douyin that gate content behind cookie checks.
        """
        browser = await self._ensure_cdp_browser()
        default_ctx = browser.contexts[0]
        page = await default_ctx.new_page()
        try:
            yield page
        finally:
            await page.close()

    async def close(self) -> None:
        if self._browser and self._browser.is_connected():
            await self._browser.close()
        if self._cdp_browser and self._cdp_browser.is_connected():
            await self._cdp_browser.close()
        if self._chrome_proc:
            self._chrome_proc.terminate()
            self._chrome_proc.wait()
            self._chrome_proc = None
        if self._playwright:
            await self._playwright.stop()
        self._browser = None
        self._cdp_browser = None
        self._playwright = None
        BrowserManager._instance = None


_DEFAULT_FOLLOWER_KEYWORDS: tuple[str, ...] = (
    "粉丝",
    "关注者",
    "followers",
    "follower",
    "fans",
    "subscribers",
    "subscriber",
)


def extract_follower_count(
    text: str,
    keyword: str | tuple[str, ...] | None = None,
) -> int | None:
    """Extract the follower number adjacent to a keyword.

    *keyword* may be:
      - ``str``  – match that single keyword (backward-compatible)
      - ``tuple[str, ...]`` – try each keyword in order
      - ``None`` (default) – try all common keywords
        (粉丝 / 关注者 / followers / fans / subscribers …)

    Handles both orderings:
      - Number before keyword: '2.1万粉丝', '1.2M followers'
      - Keyword before number: '粉丝 206.1万', 'Followers 1.2M'
    """
    if keyword is None:
        keywords = _DEFAULT_FOLLOWER_KEYWORDS
    elif isinstance(keyword, str):
        keywords = (keyword,)
    else:
        keywords = keyword

    for kw in keywords:
        result = _extract_for_keyword(text, kw)
        if result is not None:
            return result
    return None


def _extract_for_keyword(text: str, keyword: str) -> int | None:
    """Core extraction logic for a single keyword."""
    import re

    if not text or keyword.lower() not in text.lower():
        return None

    escaped = re.escape(keyword)
    flags = re.IGNORECASE

    # A1: number WITH unit suffix before keyword
    #     '2.1万粉丝', '1.2M followers'
    m = re.search(r"([\d,.]+\s*[万亿kKmMbB])\+?\s*" + escaped, text, flags)
    if m:
        return parse_follower_text(m.group(1))
    # A2: bare number directly touching keyword
    #     '12345粉丝', '12345followers'
    m = re.search(r"([\d,.]+)\s*" + escaped, text, flags)
    if m:
        return parse_follower_text(m.group(1))
    # B: keyword BEFORE number
    #     '粉丝 206.1万', 'Followers 1.2M', '粉丝・2.1万'
    m = re.search(
        escaped + r"[\s·•・:：\-]*(\d[\d,.]*\s*[万亿kKmMbB]?)\+?",
        text,
        flags,
    )
    if m:
        return parse_follower_text(m.group(1))
    return None


def parse_follower_text(text: str) -> int | None:
    """Parse human-readable follower counts like '123.4万', '1.2M', '5k'."""
    if not text:
        return None
    text = text.strip().replace(",", "").replace(" ", "")

    multipliers = {
        "亿": 100_000_000,
        "万": 10_000,
        "k": 1_000,
        "K": 1_000,
        "m": 1_000_000,
        "M": 1_000_000,
        "b": 1_000_000_000,
        "B": 1_000_000_000,
    }

    for suffix, mult in multipliers.items():
        if text.endswith(suffix):
            try:
                return int(float(text[: -len(suffix)]) * mult)
            except ValueError:
                return None

    try:
        return int(float(text))
    except ValueError:
        return None
