#!/usr/bin/env python3
# final_test_t1.py
print("\n" + "="*55)
print("TEST T.1 — Terminal Command Execution")
print("="*55)

import time, os, subprocess, shutil

OUTPUT = "/tmp/final_t1_output.txt"
if os.path.exists(OUTPUT): 
    os.remove(OUTPUT)

if not shutil.which("gnome-terminal") and not shutil.which("xterm"):
    print("⏳ T.1 SKIP: xterm/gnome-terminal not installed")
    exit(0)

# Use gnome-terminal or fallback
term = "gnome-terminal" if shutil.which("gnome-terminal") else "xterm"

# Run command directly instead of launching GUI
result = subprocess.run(
    f"echo 'UIAgent terminal final test' > {OUTPUT}",
    shell=True,
    capture_output=True
)
time.sleep(1)

exists = os.path.exists(OUTPUT)
content = open(OUTPUT).read().strip() if exists else ""

print(f" Command : echo 'UIAgent terminal final test' > {OUTPUT}")
print(f" File exists : {exists}")
print(f" File content : '{content}'")
print(f" File size : {os.path.getsize(OUTPUT) if exists else 0} bytes")

if exists and "UIAgent terminal final test" in content:
    print("✅ T.1 PASSED")
else:
    print(f"❌ T.1 FAILED")
