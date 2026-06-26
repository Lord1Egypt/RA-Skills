#!/usr/bin/env python3
# final_test_e1_fixed.py
# TEST NAME: E.1 - Login Form Filling (Fixed)

import time, os
from chrome_session_vbox_fixed import get_ctrl
from verify_helpers import screen_hash, current_url

print("=" * 55)
print("TEST E.1 — Login Form Filling (Fixed)")
print("=" * 55)

ctrl = get_ctrl()
ctrl._send("Page.navigate", {"url": "https://github.com/login"})
time.sleep(2)

hash_before = screen_hash(ctrl)
url_before = current_url(ctrl)
print(f" BEFORE url : {url_before}")
print(f" BEFORE hash : {hash_before}")

# Verify fields exist
username_exists = ctrl.js('document.getElementById("login_field") !== null')
password_exists = ctrl.js('document.getElementById("password") !== null')
print(f" username field exists : {username_exists}")
print(f" password field exists : {password_exists}")
assert username_exists, "FAIL E.1: username field not found"
assert password_exists, "FAIL E.1: password field not found"

# Step 1: Clear and fill username
ctrl.js('document.getElementById("login_field").value = ""')
ctrl.js('document.getElementById("login_field").focus()')
time.sleep(0.4)

# Verify focus is on username
focused_id = ctrl.js('document.activeElement?.id')
print(f" Focused element : '{focused_id}'")

ctrl._send("Input.insertText", {"text": "testuser_uiagent"})
time.sleep(0.3)

# Read back username immediately
username_check = ctrl.js('document.getElementById("login_field")?.value')
print(f" Username after type : '{username_check}'")
assert username_check == "testuser_uiagent", (
    f"FAIL E.1: username wrong after typing: '{username_check}'"
)

# Step 2: Use Tab key to move to password field
# Clear password field first
ctrl.js('document.getElementById("password").value = ""')

# Send Tab to move focus from username to password
ctrl._send("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Tab", "code": "Tab", "keyCode": 9})
time.sleep(0.1)
ctrl._send("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Tab", "code": "Tab", "keyCode": 9})
time.sleep(0.4)

# Verify focus moved
focused_id2 = ctrl.js('document.activeElement?.id')
print(f" Focused element : '{focused_id2}'")

# If Tab didn't work, try typing password into whatever field has focus
ctrl._send("Input.insertText", {"text": "testpassword123"})
time.sleep(0.3)

# Step 3: Read both fields from DOM
username = ctrl.js('document.getElementById("login_field")?.value')
password = ctrl.js('document.getElementById("password")?.value')
hash_after = screen_hash(ctrl)

ctrl.screenshot("/tmp/final_e1_fixed.png")
size = os.path.getsize("/tmp/final_e1_fixed.png")

print(f"\n username DOM : '{username}'")
print(f" password DOM : '{password}'")
print(f" AFTER hash : {hash_after}")
print(f" screenshot : {size:,} bytes")

# Assert both fields correct and separate
assert username == "testuser_uiagent", (
    f"FAIL E.1: username='{username}'\n"
    f" → Both strings ended up in username — focus didn't move"
)
print(" ✅ username DOM verified: 'testuser_uiagent'")

assert password == "testpassword123", (
    f"FAIL E.1: password='{password}'\n"
    f" → Password field empty — focus issue"
)
print(" ✅ password DOM verified: 'testpassword123'")

assert hash_before != hash_after, "FAIL E.1: hash unchanged"
print(" ✅ hash changed")

assert "github.com/login" in current_url(ctrl), \
    "FAIL E.1: navigated away — form may have submitted"
print(" ✅ still on login page")

print(f"\n{'='*55}")
print("✅ E.1 PASSED — both fields verified separately")
print(f" username DOM = '{username}'")
print(f" password DOM = '{password}'")
print(f"{'='*55}")
