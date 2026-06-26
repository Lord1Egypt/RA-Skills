"""Mixed-flow orchestrator template.

This file shows how to chain browser and desktop phases.
"""

from __future__ import annotations

from dataclasses import dataclass

from browser_runner import BrowserConfig, BrowserRunner
from desktop_runner import DesktopRunner


@dataclass
class MixedFlowResult:
    downloaded_path: str | None = None
    notes: str = ""


def run_mixed_flow(url: str) -> MixedFlowResult:
    browser = BrowserRunner(BrowserConfig(headless=False))
    desktop = DesktopRunner()
    result = MixedFlowResult()

    try:
        if browser.available():
            page = browser.start()
            browser.goto(url)

            # Browser phase
            title = page.title()
            result.notes += f"Opened: {title}\n"
        else:
            result.notes += "Browser phase skipped: Playwright unavailable\n"

        # Desktop phase placeholder
        # Example: switch to a native app, paste content, or process downloaded file
        # desktop.hotkey("alt", "tab")
        # desktop.write("hello")

        return result
    finally:
        if browser.available():
            browser.close()


if __name__ == "__main__":
    print(run_mixed_flow("https://example.com"))
