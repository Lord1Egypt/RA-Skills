#!/usr/bin/env python3
# run_final_all.py - Run all final tests and capture complete output

import subprocess
import sys
import os

tests = [
    ("preflight", "preflight.py", "Pre-flight Check"),
    ("C.1", "final_test_c1.py", "Contenteditable Typing"),
    ("E.1", "final_test_e1.py", "Login Form Filling"),
    ("H.1", "final_test_h1.py", "HTML5 Video Playback"),
    ("I.1", "final_test_i1.py", "Google Search"),
    ("J.1", "final_test_j1.py", "Multi-tab Management"),
    ("K.1", "final_test_k1.py", "Keyboard Navigation"),
    ("L.2", "final_test_l2.py", "404 Recovery"),
    ("SD.1", "final_test_sd1.py", "Shadow DOM"),
    ("CF.1", "final_test_cf1.py", "Complex Forms"),
    ("CA.1", "final_test_ca1.py", "Canvas Drawing"),
    ("T.1", "final_test_t1.py", "Terminal"),
    ("ED.1", "final_test_editor.py", "Text Editor"),
    ("FM.1", "final_test_fm1.py", "File Manager"),
    ("SP.1", "test_sp1_official.py", "Session Persistence Across Chrome Restart"),
]

results = {}

for code, script, name in tests:
    print(f"\n{'#'*60}")
    print(f"RUNNING {code}: {name}")
    print(f"{'#'*60}\n")
    
    if not os.path.exists(script):
        results[code] = ("⏭ SKIP", name)
        print(f" Script not found: {script}\n")
        continue
    
    # Run with full output capture
    r = subprocess.run(
        [sys.executable, script],
        capture_output=False,  # Show output directly
        text=True
    )
    
    results[code] = ("✅ PASS" if r.returncode == 0 else "❌ FAIL", name)

print(f"\n{'='*60}")
print("FINAL RESULTS")
print(f"{'='*60}")

passed = failed = skipped = 0

for code, (status, name) in results.items():
    print(f" {status} {code:<8} {name}")
    if "PASS" in status:
        passed += 1
    elif "SKIP" in status:
        skipped += 1
    else:
        failed += 1

print(f"{'='*60}")
print(f" Passed  : {passed}")
print(f" Skipped : {skipped}")
print(f" Failed  : {failed}")
print(f" Total   : {passed + failed}/{passed + failed + skipped}")
print(f"{'='*60}\n")
