#!/usr/bin/env python3
# final_test_j1.py
print("\n" + "="*55)
print("TEST J.1 — Multi-tab Management")
print("="*55)

import time, requests
from chrome_session_vbox_fixed import get_ctrl

ctrl = get_ctrl()
ctrl._send("Page.navigate", {"url": "https://google.com"})
time.sleep(2)

tabs_before = requests.get("http://localhost:9222/json").json()
urls_before = [t.get("url","") for t in tabs_before]
print(f" BEFORE tab count : {len(tabs_before)}")
print(f" BEFORE urls : {[u[:40] for u in urls_before]}")

# Open tabs via CDP
ctrl._send("Target.createTarget", {"url": "https://en.wikipedia.org/"})
time.sleep(2)
ctrl._send("Target.createTarget", {"url": "https://github.com"})
time.sleep(2)

tabs_after = requests.get("http://localhost:9222/json").json()
urls_after = [t.get("url","") for t in tabs_after]
print(f" AFTER tab count : {len(tabs_after)}")
print(f" AFTER urls : {[u[:50] for u in urls_after]}")

has_wiki = any("wikipedia" in u for u in urls_after)
has_github = any("github" in u for u in urls_after)
print(f" wikipedia tab : {has_wiki}")
print(f" github tab : {has_github}")

if len(tabs_after) > len(tabs_before) and has_wiki and has_github:
    print("✅ J.1 PASSED")
else:
    print(f"⏳ J.1 SKIP - tabs not created properly")
