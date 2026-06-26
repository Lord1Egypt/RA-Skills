#!/usr/bin/env python3
# final_test_ca1.py
print("\n" + "="*55)
print("TEST CA.1 — Canvas Drawing")
print("="*55)

import time, os, hashlib, base64
from chrome_session_vbox_fixed import get_ctrl
from verify_helpers import screen_hash

ctrl = get_ctrl()
ctrl._send("Page.navigate", {"url": "https://example.com"})
time.sleep(2)

ctrl.js("""
 document.body.innerHTML = '';
 const canvas = document.createElement('canvas');
 canvas.id = 'test-canvas';
 canvas.width = 800; canvas.height = 400;
 canvas.style.cssText = 'display:block;background:white;';
 document.body.appendChild(canvas);
 const ctx = canvas.getContext('2d');
 ctx.fillStyle = 'white';
 ctx.fillRect(0, 0, 800, 400);
 let drawing = false;
 canvas.addEventListener('mousedown', e => { drawing=true; ctx.beginPath(); ctx.moveTo(e.clientX, e.clientY); });
 canvas.addEventListener('mousemove', e => { if(!drawing) return; ctx.lineWidth=8; ctx.strokeStyle='blue'; ctx.lineTo(e.clientX, e.clientY); ctx.stroke(); });
 canvas.addEventListener('mouseup', () => { drawing=false; });
""")
time.sleep(0.5)

raw_before = base64.b64decode(ctrl.js("document.getElementById('test-canvas').toDataURL('image/png')").split(',')[1])
hash_before = hashlib.md5(raw_before).hexdigest()
print(f" BEFORE canvas hash : {hash_before}")
print(f" BEFORE canvas size : {len(raw_before):,} bytes")

pos = ctrl.js("""
 (function() {
 const c = document.getElementById('test-canvas');
 const r = c.getBoundingClientRect();
 return {left: r.left, top: r.top};
 })()
""")
sx = int(pos["left"]) + 50
sy = int(pos["top"]) + 100

ctrl._send("Input.dispatchMouseEvent", {"type":"mousePressed","x":sx,"y":sy,"button":"left","clickCount":1})
for i in range(30):
    ctrl._send("Input.dispatchMouseEvent", {"type":"mouseMoved","x":sx+(i*15),"y":sy+(i*3),"button":"left","buttons":1})
    time.sleep(0.02)
ctrl._send("Input.dispatchMouseEvent", {"type":"mouseReleased","x":sx+450,"y":sy+90,"button":"left"})
time.sleep(1.0)

raw_after = base64.b64decode(ctrl.js("document.getElementById('test-canvas').toDataURL('image/png')").split(',')[1])
hash_after = hashlib.md5(raw_after).hexdigest()
non_white = ctrl.js("""
 (function() {
 const c = document.getElementById('test-canvas');
 const d = c.getContext('2d').getImageData(0,0,c.width,c.height).data;
 let n = 0;
 for(let i=0;i<d.length;i+=4) if(d[i]<240||d[i+1]<240||d[i+2]<240) n++;
 return n;
 })()
""") or 0

with open("/tmp/final_ca1.png","wb") as f: f.write(raw_after)
size = os.path.getsize("/tmp/final_ca1.png")

print(f" AFTER canvas hash : {hash_after}")
print(f" AFTER canvas size : {len(raw_after):,} bytes")
print(f" Non-white pixels : {non_white:,}")
print(f" screenshot : {size:,} bytes")

assert hash_before != hash_after, "FAIL CA.1: canvas hash unchanged"
assert non_white > 100, f"FAIL CA.1: only {non_white} non-white pixels"
assert len(raw_after) > len(raw_before), "FAIL CA.1: canvas data did not grow"
print(f"✅ CA.1 PASSED — {non_white:,} non-white pixels drawn")
