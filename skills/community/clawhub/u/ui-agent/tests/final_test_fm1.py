#!/usr/bin/env python3
# final_test_fm1.py
print("\n" + "="*55)
print("TEST FM.1 — File Manager")
print("="*55)

import time, os, subprocess, shutil

if not shutil.which("nautilus"):
    print("⏳ FM.1 SKIP: nautilus not installed")
    exit(0)

# Launch nautilus
proc = subprocess.Popen(
    ["nautilus", "--new-window"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(3)

running = subprocess.run(
    ["pgrep", "-x", "nautilus"],
    capture_output=True
).returncode == 0

pid_result = subprocess.run(
    ["pgrep", "-x", "nautilus"],
    capture_output=True
).stdout.decode().strip()

print(f" Running : {running}")
print(f" PID : {pid_result}")

if running:
    print("✅ FM.1 PASSED")
    subprocess.run(["pkill", "-x", "nautilus"], capture_output=True)
else:
    print(f"❌ FM.1 FAILED - nautilus not running")
