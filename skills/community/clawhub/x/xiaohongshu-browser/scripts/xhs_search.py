# -*- coding: utf-8 -*-
"""XHS Search - Click posts and screenshot the modal preview."""
import sys, json, time, urllib.parse, re, random
from pathlib import Path
from playwright.sync_api import sync_playwright

SKILL_DIR = Path(__file__).resolve().parent.parent
HOME = Path.home()
OPENCLAW = HOME / ".openclaw"

OUT = SKILL_DIR / "output"
OUT.mkdir(exist_ok=True)
USER_DATA = str(OPENCLAW / "xhs_data")
XHS = "https://www.xiaohongshu.com"

def ts(): return str(int(time.time()))

def human_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

keyword = sys.argv[1] if len(sys.argv) > 1 else "御姐"
count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
max_retry = 3

# Check if IP is blocked by looking for error indicators
def is_ip_blocked(page):
    url = page.url
    body_text = page.content()
    if "IP存在风险" in body_text or "IP" in url:
        return True
    return False

with sync_playwright() as pw:
    browser = pw.chromium.launch_persistent_context(
        USER_DATA, headless=True,
        viewport={"width": 1280, "height": 900}, locale="zh-CN",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    )
    page = browser.pages[0] if browser.pages else browser.new_page()

    kw = urllib.parse.quote(keyword)
    search_url = f"{XHS}/search_result?keyword={kw}&source=web_search_result_notes&type=51"

    # Retry loop for IP block
    for attempt in range(max_retry):
        print(f"[*] Searching: {keyword} (attempt {attempt+1}/{max_retry})", flush=True)
        page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
        human_delay(3, 6)

        if is_ip_blocked(page):
            wait_time = (attempt + 1) * 300  # 5, 10, 15 minutes
            print(f"[!] IP blocked. Waiting {wait_time}s before retry...", flush=True)
            time.sleep(wait_time)
            continue
        break

    # Dismiss login/overlay popups
    page.keyboard.press("Escape")
    human_delay(1, 2)

    print(f"[*] URL: {page.url}", flush=True)

    # Check if blocked on final load
    if is_ip_blocked(page):
        print("[!] IP is blocked. Please try again later or switch network.", flush=True)
        browser.close()
        sys.exit(1)

    covers = page.query_selector_all("section.note-item a.cover")
    if not covers:
        covers = page.query_selector_all("a.cover")
    print(f"[*] Found {len(covers)} posts", flush=True)

    results = []
    clicked = 0
    for i, cover in enumerate(covers):
        if clicked >= count:
            break
        try:
            cover.scroll_into_view_if_needed()
            human_delay(0.5, 1.5)

            href = cover.get_attribute("href") or ""
            note_id = ""
            m = re.search(r'/search_result/([a-f0-9]+)', href)
            if m:
                note_id = m.group(1)

            cover.click()
            human_delay(3, 5)

            # Dismiss overlay popups
            for popup_sel in [".close-button", ".login-close", "[class*='close']"]:
                try:
                    btn = page.query_selector(popup_sel)
                    if btn and btn.is_visible():
                        btn.click()
                        human_delay(0.3, 0.8)
                except:
                    pass

            clicked += 1
            p = OUT / f"post_{clicked}_{ts()}.png"
            page.screenshot(path=str(p))
            post_url = f"{XHS}/explore/{note_id}" if note_id else ""
            print(f"[+] Post {clicked}: {p}", flush=True)
            print(f"    URL: {post_url}", flush=True)
            results.append({"index": clicked, "url": post_url, "screenshot": str(p)})

            page.keyboard.press("Escape")
            human_delay(1, 3)

        except Exception as e:
            print(f"[!] Error: {e}", flush=True)
            page.keyboard.press("Escape")
            human_delay(1, 2)

    browser.close()

print("\n=== RESULTS ===")
print(json.dumps(results, ensure_ascii=False, indent=2))
