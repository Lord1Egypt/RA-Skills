#!/usr/bin/env python3
# final_test_cf1.py
print("\n" + "="*55)
print("TEST CF.1 — Complex Form Fill")
print("="*55)

import time, os
from chrome_session_vbox_fixed import get_ctrl
from verify_helpers import screen_hash

ctrl = get_ctrl()
ctrl._send("Page.navigate", {"url": "https://demoqa.com/automation-practice-form"})
time.sleep(4)

form_loaded = ctrl.js("document.getElementById('firstName') !== null")
print(f" Form loaded : {form_loaded}")
assert form_loaded, "FAIL CF.1: form not loaded"

hash_before = screen_hash(ctrl)
print(f" BEFORE hash : {hash_before}")

def fill(field_id, value):
    ctrl.js(f"document.getElementById('{field_id}').focus()")
    time.sleep(0.3)
    ctrl.js(f"document.getElementById('{field_id}').value = ''")
    ctrl._send("Input.insertText", {"text": value})
    ctrl.js(f"""
    const el = document.getElementById('{field_id}');
    el.dispatchEvent(new Event('input', {{bubbles:true}}));
    el.dispatchEvent(new Event('change', {{bubbles:true}}));
    """)
    time.sleep(0.2)
    actual = ctrl.js(f"document.getElementById('{field_id}')?.value")
    print(f" {field_id:<15}: typed='{value}' DOM='{actual}'")
    return actual

r1 = fill("firstName", "John")
r2 = fill("lastName", "UIAgent")
r3 = fill("userEmail", "test@uiagent.com")
r4 = fill("userNumber","1234567890")

hash_after = screen_hash(ctrl)
ctrl.screenshot("/tmp/final_cf1.png")
size = os.path.getsize("/tmp/final_cf1.png")

print(f" AFTER hash : {hash_after}")
print(f" screenshot : {size:,} bytes")

assert r1 == "John", f"FAIL CF.1: firstName='{r1}'"
assert r2 == "UIAgent", f"FAIL CF.1: lastName='{r2}'"
assert r3 == "test@uiagent.com", f"FAIL CF.1: email='{r3}'"
assert r4 == "1234567890", f"FAIL CF.1: phone='{r4}'"
assert hash_before != hash_after, "FAIL CF.1: hash unchanged"
print("✅ CF.1 PASSED")
