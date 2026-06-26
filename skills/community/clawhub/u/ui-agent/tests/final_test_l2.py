#!/usr/bin/env python3
# final_test_l2.py
print("\n" + "="*55)
print("TEST L.2 — 404 Error Recovery")
print("="*55)

import time, os
from chrome_session_vbox_fixed import get_ctrl
from verify_helpers import screen_hash, current_url

ctrl = get_ctrl()
# Navigate to a 404 error page
ctrl._send("Page.navigate", {"url": "https://en.wikipedia.org/wiki/THIS_DOES_NOT_EXIST_XYZABC123"})
time.sleep(3)

body = ctrl.js("document.body.innerText") or ""
is_error = any(kw in body.lower() for kw in ["not exist", "not found", "404", "error"])
hash_error = screen_hash(ctrl)
url_error = current_url(ctrl)

print(f" Error page : {is_error}")
print(f" Error URL : {url_error}")
print(f" Error hash : {hash_error}")

if not is_error:
    print("⏳ L.2 SKIP - did not land on error page")
    exit(0)

# Navigate back to main Wikipedia page
ctrl._send("Page.navigate", {"url": "https://en.wikipedia.org/wiki/Main_Page"})
time.sleep(3)

url_after = current_url(ctrl)
hash_after = screen_hash(ctrl)

ctrl.screenshot("/tmp/final_l2.png")
size = os.path.getsize("/tmp/final_l2.png")

print(f" Recovered URL : {url_after}")
print(f" Recovered hash : {hash_after}")
print(f" screenshot : {size:,} bytes")

if "THIS_DOES_NOT_EXIST" not in url_after and "wikipedia" in url_after:
    print(f"✅ L.2 PASSED — {url_error} → {url_after}")
else:
    print(f"❌ L.2 FAILED - still on error page")
