#!/usr/bin/env python3
# final_test_k1.py
print("\n" + "="*55)
print("TEST K.1 — Keyboard Navigation")
print("="*55)

import time, os
from chrome_session_vbox_fixed import get_ctrl
from verify_helpers import screen_hash, current_url

ctrl = get_ctrl()
ctrl._send("Page.navigate", {"url": "https://github.com/login"})
time.sleep(2)

hash_before = screen_hash(ctrl)
print(f" BEFORE hash : {hash_before}")

# Focus and type
ctrl.js('document.getElementById("login_field").focus()')
time.sleep(0.3)
ctrl._send("Input.insertText", {"text": "keyboardtest"})
time.sleep(0.2)

ctrl.key("Tab")
time.sleep(0.4)
ctrl._send("Input.insertText", {"text": "keyboardpass123"})
time.sleep(0.2)

username = ctrl.js('document.getElementById("login_field")?.value')
password = ctrl.js('document.getElementById("password")?.value')
hash_after = screen_hash(ctrl)

ctrl.screenshot("/tmp/final_k1.png")
size = os.path.getsize("/tmp/final_k1.png")

print(f" username DOM : '{username}'")
print(f" password DOM : '{password}'")
print(f" AFTER hash : {hash_after}")
print(f" screenshot : {size:,} bytes")

assert username == "keyboardtest", f"FAIL K.1: username='{username}'"
assert password == "keyboardpass123", f"FAIL K.1: password='{password}'"
assert hash_before != hash_after, "FAIL K.1: hash unchanged"
print("✅ K.1 PASSED")
