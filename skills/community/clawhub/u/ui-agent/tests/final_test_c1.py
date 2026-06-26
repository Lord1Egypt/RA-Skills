#!/usr/bin/env python3
# final_test_c1.py
print("\n" + "="*55)
print("TEST C.1 — Contenteditable Typing")
print("="*55)

import time, os
from chrome_session_vbox_fixed import get_ctrl
from verify_helpers import screen_hash

ctrl = get_ctrl()
ctrl._send("Page.navigate", {"url": "https://example.com"})
time.sleep(2)

# Inject contenteditable
ctrl.js("""
 const div = document.createElement('div');
 div.id = 'test-editor';
 div.contentEditable = 'true';
 div.style.cssText = 'border:3px solid blue;padding:20px;font-size:18px;min-height:80px;';
 div.innerText = 'Click here to edit...';
 document.body.insertBefore(div, document.body.firstChild);
""")
time.sleep(0.5)

content_before = ctrl.js("document.getElementById('test-editor')?.innerText")
hash_before = screen_hash(ctrl)
print(f" BEFORE content : '{content_before}'")
print(f" BEFORE hash : {hash_before}")

# Click and type
pos = ctrl.js("""
 (function() {
 const el = document.getElementById('test-editor');
 const r = el.getBoundingClientRect();
 return {x: Math.round(r.left + r.width/2), y: Math.round(r.top + r.height/2)};
 })()
""")
ctrl.click(pos["x"], pos["y"])
time.sleep(0.3)
ctrl._send("Input.insertText", {"text": "UIAgent successfully typed this text"})
time.sleep(0.5)

content_after = ctrl.js("document.getElementById('test-editor')?.innerText")
hash_after = screen_hash(ctrl)

ctrl.screenshot("/tmp/final_c1.png")
size = os.path.getsize("/tmp/final_c1.png")

print(f" AFTER content : '{content_after}'")
print(f" AFTER hash : {hash_after}")
print(f" screenshot : {size:,} bytes")

assert "UIAgent" in str(content_after), f"FAIL C.1: content='{content_after}'"
assert hash_before != hash_after, "FAIL C.1: hash unchanged"
print("✅ C.1 PASSED")
