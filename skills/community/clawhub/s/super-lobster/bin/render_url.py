#!/usr/bin/env python3
import subprocess
import sys

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} <url>", file=sys.stderr)
    sys.exit(2)

url = sys.argv[1]
cmd = [
    "/usr/bin/google-chrome-stable",
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--virtual-time-budget=15000",
    "--dump-dom",
    url,
]
proc = subprocess.run(cmd, text=True, capture_output=True)
if proc.returncode != 0:
    sys.stderr.write(proc.stderr)
    sys.exit(proc.returncode)
print(proc.stdout, end="")
