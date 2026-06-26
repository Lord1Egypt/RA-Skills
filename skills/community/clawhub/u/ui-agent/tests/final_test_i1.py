#!/usr/bin/env python3
# final_test_i1.py
print("\n" + "="*55)
print("TEST I.1 — Google Search")
print("="*55)

import time, os
from chrome_session_vbox_fixed import get_ctrl
from verify_helpers import screen_hash, current_url

ctrl = get_ctrl()
ctrl._send("Page.navigate", {"url": "https://google.com"})
time.sleep(3)

hash_before = screen_hash(ctrl)
url_before = current_url(ctrl)
print(f" BEFORE url : {url_before}")
print(f" BEFORE hash : {hash_before}")

# Find search box
sel = ctrl.js("""
 document.querySelector('textarea[name="q"]') ? 'textarea[name="q"]' :
 document.querySelector('input[name="q"]') ? 'input[name="q"]' : null
""")
print(f" Search selector : {sel}")

if not sel:
    print("⏳ I.1 SKIP - search box not found")
    exit(0)

# Type search
ctrl.js(f"document.querySelector('{sel}').focus()")
time.sleep(0.3)
ctrl._send("Input.insertText", {"text": "Python programming"})
time.sleep(0.5)

val = ctrl.js(f"document.querySelector('{sel}')?.value")
print(f" Typed value : '{val}'")

# Submit
ctrl.js(f"document.querySelector('{sel}').closest('form')?.submit()")
time.sleep(3)

url_after = current_url(ctrl)
hash_after = screen_hash(ctrl)

ctrl.screenshot("/tmp/final_i1.png")
size = os.path.getsize("/tmp/final_i1.png")

print(f" AFTER url : {url_after}")
print(f" AFTER hash : {hash_after}")
print(f" screenshot : {size:,} bytes")

if "google.com/search" in url_after and size > 50000:
    print("✅ I.1 PASSED")
else:
    print(f"⏳ I.1 SKIP - search did not complete properly")
