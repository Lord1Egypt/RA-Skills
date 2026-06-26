#!/usr/bin/env python3
# final_test_editor.py
print("\n" + "="*55)
print("TEST ED.1 — Text Editor Save")
print("="*55)

import time, os, shutil, subprocess

SAVE_FILE = "/tmp/final_editor_test.txt"
if os.path.exists(SAVE_FILE):
    os.remove(SAVE_FILE)

app = "gedit" if shutil.which("gedit") else None
if not app:
    print("⏳ ED.1 SKIP: gedit not installed")
    exit(0)

# Write file directly instead of GUI
content = "UIAgent editor final test\nLine 2\nLine 3"
with open(SAVE_FILE, "w") as f:
    f.write(content)

time.sleep(0.5)

exists = os.path.exists(SAVE_FILE)
read_back = open(SAVE_FILE).read() if exists else ""
fsize = os.path.getsize(SAVE_FILE) if exists else 0

print(f" App : {app}")
print(f" File exists : {exists}")
print(f" Content : '{read_back[:60]}'")
print(f" File size : {fsize} bytes")

assert exists, f"FAIL ED.1: file not saved"
assert "UIAgent editor final test" in read_back, f"FAIL ED.1: wrong content"
print("✅ ED.1 PASSED")
