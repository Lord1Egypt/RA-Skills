#!/usr/bin/env python3
import subprocess
import time

def osascript(script):
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"osascript error: {result.stderr.strip()}")
        raise RuntimeError("osascript failed")
    return result.stdout.strip()

print("1. Activating WeChat...")
osascript('tell application "WeChat" to activate')
time.sleep(1)

print("2. Pressing Cmd+F...")
osascript('tell application "System Events" to keystroke "f" using command down')
time.sleep(0.5)

print("3. Copying text to clipboard...")
text = "文件传输助手"
subprocess.run(["pbcopy"], input=text.encode(), check=True)
time.sleep(0.2)

print("4. Pasting (Cmd+V)...")
osascript('tell application "System Events" to keystroke "v" using command down')
time.sleep(1)

print("5. Pressing Return...")
osascript('tell application "System Events" to keystroke return')
print("Done!")
