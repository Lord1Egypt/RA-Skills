#!/usr/bin/env python3
# final_test_sd1.py
print("\n" + "="*55)
print("TEST SD.1 — Shadow DOM")
print("="*55)

import time, os
from chrome_session_vbox_fixed import get_ctrl
from verify_helpers import screen_hash

ctrl = get_ctrl()
ctrl._send("Page.navigate", {"url": "https://example.com"})
time.sleep(2)

ctrl.js("""
 const host = document.createElement('div');
 host.id = 'shadow-host';
 host.style.cssText = 'padding:20px;border:3px solid purple;margin:20px;';
 document.body.insertBefore(host, document.body.firstChild);
 const shadow = host.attachShadow({mode: 'open'});
 shadow.innerHTML = '<input id="shadow-input" type="text" placeholder="Shadow input" style="font-size:18px;padding:10px;width:300px;">';
""")
time.sleep(0.5)

value_before = ctrl.js("""
 document.getElementById('shadow-host')?.shadowRoot?.getElementById('shadow-input')?.value
""")
hash_before = screen_hash(ctrl)
print(f" BEFORE value : '{value_before}'")
print(f" BEFORE hash : {hash_before}")

pos = ctrl.js("""
 (function() {
 const el = document.getElementById('shadow-host').shadowRoot.getElementById('shadow-input');
 const r = el.getBoundingClientRect();
 return {x: Math.round(r.left + r.width/2), y: Math.round(r.top + r.height/2)};
 })()
""")
ctrl.click(pos["x"], pos["y"])
time.sleep(0.3)
ctrl._send("Input.insertText", {"text": "UIAgent shadow DOM test"})
time.sleep(0.3)

value_after = ctrl.js("""
 document.getElementById('shadow-host')?.shadowRoot?.getElementById('shadow-input')?.value
""")
hash_after = screen_hash(ctrl)

ctrl.screenshot("/tmp/final_sd1.png")
size = os.path.getsize("/tmp/final_sd1.png")

print(f" AFTER value : '{value_after}'")
print(f" AFTER hash : {hash_after}")
print(f" screenshot : {size:,} bytes")

assert "UIAgent shadow DOM test" in str(value_after), f"FAIL SD.1: value='{value_after}'"
assert hash_before != hash_after, "FAIL SD.1: hash unchanged"
print("✅ SD.1 PASSED")
