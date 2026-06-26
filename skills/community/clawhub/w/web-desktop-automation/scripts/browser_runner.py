"""Playwright browser automation template.

Usage:
    python scripts/browser_runner.py https://example.com

Install:
    pip install playwright
    playwright install
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Optional

try:
    from playwright.sync_api import Browser, Page, sync_playwright
except ImportError:  # pragma: no cover - graceful degradation when dependency is missing
    Browser = None  # type: ignore[assignment]
    Page = None  # type: ignore[assignment]
    sync_playwright = None  # type: ignore[assignment]


@dataclass
class BrowserConfig:
    headless: bool = False
    slow_mo_ms: int = 0
    timeout_ms: int = 30000


class BrowserUnavailableError(RuntimeError):
    pass


class BrowserRunner:
    def __init__(self, config: Optional[BrowserConfig] = None) -> None:
        self.config = config or BrowserConfig()
        self._pw = None
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None

    @staticmethod
    def available() -> bool:
        return sync_playwright is not None

    def _ensure_available(self) -> None:
        if not self.available():
            raise BrowserUnavailableError(
                "Playwright is not installed. Run: pip install playwright && playwright install"
            )

    def start(self) -> Page:
        self._ensure_available()
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(
            headless=self.config.headless,
            slow_mo=self.config.slow_mo_ms,
        )
        context = self._browser.new_context()
        self._page = context.new_page()
        self._page.set_default_timeout(self.config.timeout_ms)
        return self._page

    @property
    def page(self) -> Page:
        if not self._page:
            raise RuntimeError("BrowserRunner not started")
        return self._page

    def goto(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def search_text(self, text: str) -> bool:
        locator = self.page.get_by_text(text)
        return locator.count() > 0

    def click_text(self, text: str) -> None:
        self.page.get_by_text(text).first.click()

    def fill(self, selector: str, value: str) -> None:
        self.page.locator(selector).fill(value)

    def html(self) -> str:
        return self.page.content()

    def screenshot(self, path: str) -> None:
        self.page.screenshot(path=path, full_page=True)

    def close(self) -> None:
        if self._browser:
            self._browser.close()
        if self._pw:
            self._pw.stop()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Target URL")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    if not BrowserRunner.available():
        raise SystemExit(
            "Playwright is not installed. Run: pip install playwright && playwright install"
        )

    runner = BrowserRunner(BrowserConfig(headless=args.headless))
    try:
        page = runner.start()
        runner.goto(args.url)
        print(page.title())
        print(runner.html()[:1000])
    finally:
        runner.close()


if __name__ == "__main__":
    main()
