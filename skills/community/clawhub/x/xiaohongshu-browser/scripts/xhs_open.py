# -*- coding: utf-8 -*-
"""Open visible XHS browser for login. Stays alive until .close_browser file appears."""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

HOME = Path.home()
OPENCLAW = HOME / ".openclaw"
USER_DATA = str(OPENCLAW / "xhs_data")
CTRL = OPENCLAW / ".close_browser"
AUTH_FILE = str(OPENCLAW / "xhs_auth.json")

CTRL.unlink(missing_ok=True)

pw = sync_playwright().start()
browser = pw.chromium.launch_persistent_context(
    USER_DATA,
    headless=False,
    viewport={"width": 1280, "height": 900},
    locale="zh-CN",
)

page = browser.pages[0] if browser.pages else browser.new_page()
page.goto("https://www.xiaohongshu.com", wait_until="domcontentloaded", timeout=60000)
print("BROWSER_READY", flush=True)

while not CTRL.exists():
    time.sleep(1)
CTRL.unlink(missing_ok=True)

browser.storage_state(path=AUTH_FILE)
print("AUTH_SAVED", flush=True)
browser.close()
pw.stop()
print("DONE", flush=True)
