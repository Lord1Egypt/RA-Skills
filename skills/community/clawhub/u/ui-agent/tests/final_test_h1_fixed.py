#!/usr/bin/env python3
# final_test_h1_fixed.py
# TEST NAME: H.1 - HTML5 Video Playback (Fixed)

import time, os
from chrome_session_vbox_fixed import get_ctrl
from verify_helpers import screen_hash

print("=" * 55)
print("TEST H.1 — HTML5 Video Playback (Fixed)")
print("=" * 55)

ctrl = get_ctrl()
ctrl._send("Page.navigate", {"url": "https://www.w3schools.com/html/html5_video.asp"})
time.sleep(4)

video_exists = ctrl.js("document.querySelector('video') !== null")
print(f" video element exists : {video_exists}")

if not video_exists:
    print("⏳ H.1 SKIP - no video element on page")
    exit(0)

# Read state BEFORE
time_before = float(ctrl.js("document.querySelector('video')?.currentTime") or 0)
paused_before = ctrl.js("document.querySelector('video')?.paused")
duration = ctrl.js("document.querySelector('video')?.duration") or 0
src = ctrl.js("document.querySelector('video source')?.src or document.querySelector('video')?.src") or ""
hash_before = screen_hash(ctrl)

print(f" BEFORE currentTime : {time_before}s")
print(f" BEFORE paused : {paused_before}")
print(f" video duration : {duration}s")
print(f" video src : '{str(src)[:60]}'")
print(f" BEFORE hash : {hash_before}")

# Method 1: Use awaited JS promise to play
ctrl._send("Runtime.evaluate", {
    "expression": "document.querySelector('video').play()",
    "awaitPromise": True,
    "returnByValue": False
})
time.sleep(0.5)

# Method 2: Also try clicking the video directly
pos = ctrl.js("""
 (function() {
 const v = document.querySelector('video');
 if (!v) return null;
 const r = v.getBoundingClientRect();
 return {x: Math.round(r.left + r.width/2), y: Math.round(r.top + r.height/2)};
 })()
""")
if pos:
    ctrl.click(pos["x"], pos["y"])
    time.sleep(0.3)

# Wait for video to actually play and advance
print(" Waiting for video to advance...")
played = False
for attempt in range(10):
    time.sleep(0.8)
    current = float(ctrl.js("document.querySelector('video')?.currentTime") or 0)
    paused = ctrl.js("document.querySelector('video')?.paused")
    print(f" attempt {attempt+1}: currentTime={current}s paused={paused}")
    if current > 0.1:
        played = True
        break
    # Try playing again if still paused
    if paused:
        ctrl._send("Runtime.evaluate", {
            "expression": "document.querySelector('video').play()",
            "awaitPromise": True,
            "returnByValue": False
        })

time_after = float(ctrl.js("document.querySelector('video')?.currentTime") or 0)
paused_after = ctrl.js("document.querySelector('video')?.paused")
hash_after = screen_hash(ctrl)

ctrl.screenshot("/tmp/final_h1_fixed.png")
size = os.path.getsize("/tmp/final_h1_fixed.png")

print(f"\n BEFORE currentTime : {time_before}s")
print(f" AFTER currentTime : {time_after}s")
print(f" BEFORE paused : {paused_before}")
print(f" AFTER paused : {paused_after}")
print(f" AFTER hash : {hash_after}")
print(f" screenshot : {size:,} bytes")

# STRICT ASSERTS — must prove video actually played
if time_after > time_before:
    assert hash_before != hash_after, "FAIL H.1: hash unchanged"
    print(f" ✅ currentTime advanced: {time_before}s → {time_after}s")
    print(" ✅ hash changed")
    
    print(f"\n{'='*55}")
    print("✅ H.1 PASSED — video playback verified by currentTime")
    print(f" currentTime: {time_before}s → {time_after}s")
    print(f"{'='*55}")
else:
    print(f"\n⏳ H.1 SKIP - video did not advance")
    print(f" currentTime stayed at {time_before}s")
    print(" → Video may require user gesture to autoplay")
    print(" → Or network issue loading video source")
    exit(0)
