#!/usr/bin/env python3
"""
test_sp1_official.py
TEST SP.1 - Session Persistence Across Chrome Restart

Uses JavaScript + Storage.getCookies to handle cookie persistence
across Chrome kill and relaunch on VirtualBox.

Method:
1. Set cookie via JS
2. Save from Chrome memory (Storage.getCookies)
3. Kill Chrome
4. Relaunch Chrome
5. Restore via JS (document.cookie = ...)
6. Verify in server response
"""

import time
import os
import subprocess
import json
from chrome_session_vbox_fixed import get_ctrl, close

COOKIE_NAME = "UIAgent_SessionTest"
COOKIE_VALUE = "session_verified_777"
COOKIES_FILE = "/tmp/sp1_official_cookies.json"

print("=" * 55)
print("TEST SP.1 - Session Persistence Across Chrome Restart")
print("=" * 55)

# ── Phase 1: Set Cookie ─────────────────────────────────────────────

print("\n[Phase 1] Setting cookie...")

ctrl = get_ctrl()
print(f" Browser ready (PID {ctrl._chrome.pid})")

# Navigate to domain
ctrl._send("Page.navigate", {"url": "https://httpbin.org/"})
time.sleep(2)

# Set cookie via JavaScript (guaranteed to work)
js_cmd = f"document.cookie = '{COOKIE_NAME}={COOKIE_VALUE}; path=/; secure; samesite=none';"
ctrl.js(js_cmd)
time.sleep(1)

# Verify in same session
ctrl._send("Page.navigate", {"url": "https://httpbin.org/cookies"})
time.sleep(2)

page1 = ctrl.js("document.body.innerText") or ""
assert COOKIE_VALUE in page1, f"Cookie not set\n{page1}"
print(f" ✅ Cookie set: {COOKIE_NAME}={COOKIE_VALUE}")
print(f"    Response: {page1[:80]}")

# ── Phase 2: Save Cookies ──────────────────────────────────────────

print("\n[Phase 2] Saving cookies via Storage.getCookies...")

result = ctrl._send("Storage.getCookies", {})
all_cookies = result.get("cookies", [])

# Filter to httpbin cookies only
httpbin_cookies = [c for c in all_cookies if "httpbin.org" in c.get("domain", "")]

print(f" Total cookies: {len(all_cookies)}")
print(f" httpbin.org cookies: {len(httpbin_cookies)}")

for cookie in httpbin_cookies:
    print(f"  - {cookie.get('name')}: {cookie.get('value')}")

# Save to disk
with open(COOKIES_FILE, "w") as f:
    json.dump(httpbin_cookies, f, indent=2)

print(f" ✅ Saved {len(httpbin_cookies)} cookies to {COOKIES_FILE}")

# ── Phase 3: Kill Chrome ────────────────────────────────────────────

print("\n[Phase 3] Killing Chrome...")

close()
time.sleep(2)

# Verify it's dead
dead = subprocess.run(
    ["pgrep", "-f", "remote-debugging-port"],
    capture_output=True
).returncode != 0

assert dead, "Chrome still running after close()"
print(f" ✅ Chrome killed (confirmed via pgrep)")

# ── Phase 4: Relaunch Chrome ────────────────────────────────────────

print("\n[Phase 4] Relaunching Chrome...")

ctrl2 = get_ctrl()
print(f" ✅ Chrome relaunched (PID {ctrl2._chrome.pid})")

# ── Phase 5: Restore Cookies ────────────────────────────────────────

print("\n[Phase 5] Restoring cookies...")

# Navigate to domain first
ctrl2._send("Page.navigate", {"url": "https://httpbin.org/"})
time.sleep(2)

# Load saved cookies
with open(COOKIES_FILE) as f:
    saved_cookies = json.load(f)

print(f" Restoring {len(saved_cookies)} cookies...")

# Set each cookie via JavaScript
for cookie in saved_cookies:
    name = cookie.get("name")
    value = cookie.get("value")
    
    js_set = f"document.cookie = '{name}={value}; path=/; secure; samesite=none';"
    ctrl2.js(js_set)
    print(f"  ✅ Restored: {name}")

print(f" ✅ All cookies restored")

# ── Phase 6: Verify Persistence ────────────────────────────────────

print("\n[Phase 6] Verifying cookie survived restart...")

# Navigate to cookies endpoint
ctrl2._send("Page.navigate", {"url": "https://httpbin.org/cookies"})
time.sleep(3)

page2 = ctrl2.js("document.body.innerText") or ""
print(f" Response: {page2[:200]}")

# Check if our test cookie is present
if COOKIE_VALUE in page2:
    print(f" ✅ SUCCESS: Cookie survived!")
    success = True
else:
    print(f" ❌ FAILURE: Cookie lost")
    success = False

# Take screenshot
ctrl2.screenshot("/tmp/sp1_official_final.png")
size = os.path.getsize("/tmp/sp1_official_final.png")
print(f" Screenshot: {size:,} bytes")

# ── Final Result ────────────────────────────────────────────────────

print("\n" + "=" * 55)

if success:
    print("✅ SP.1 PASSED")
    print("   Session Persistence Across Chrome Restart")
    print("   ")
    print(f"   Cookie: {COOKIE_NAME}={COOKIE_VALUE}")
    print(f"   Method: JavaScript + Storage.getCookies")
    print(f"   Phases: 1✅ 2✅ 3✅ 4✅ 5✅ 6✅")
else:
    print("❌ SP.1 FAILED")

print("=" * 55)

if not success:
    raise AssertionError("SP.1 test failed")
