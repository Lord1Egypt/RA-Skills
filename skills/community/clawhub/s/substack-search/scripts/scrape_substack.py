#!/usr/bin/env python3
"""Scrape Substack search results via agent-browser CLI."""

import json
import subprocess
import sys
import time
from urllib.parse import quote

QUERY = sys.argv[1]
DATE_RANGE = sys.argv[2] if len(sys.argv) > 2 else "day"

URL = f"https://substack.com/search/{quote(QUERY)}?utm_source=global-search&searching=all_posts&dateRange={DATE_RANGE}"


def run(cmd: str, timeout: int = 20) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=False)
    return r.stdout.strip()


# 1. Open page
print(f"[1/4] Opening Substack search: {QUERY}")
run(f"agent-browser open '{URL}'", timeout=30)
time.sleep(2)

# 2. Wait for network idle
print("[2/4] Waiting for page load...")
run("agent-browser wait --load networkidle", timeout=30)

# 3. Snapshot and scroll to capture more results
print("[3/4] Extracting articles...")
articles = []

for scroll_idx in range(4):
    snap = run("agent-browser snapshot -i", timeout=20)
    # Parse link lines that contain article data
    for line in snap.splitlines():
        line = line.strip()
        if not line.startswith('- link '):
            continue
        # Extract content between quotes
        if '"' not in line:
            continue
        text = line.split('"', 1)[1].rsplit('"', 1)[0]
        # Skip nav/header links (too short or duplicate publication names)
        if len(text) < 40:
            continue
        articles.append(text)

    if scroll_idx < 3:
        run("agent-browser scroll down 800", timeout=10)
        time.sleep(1)

# 4. Close browser
print("[4/4] Closing browser...")
run("agent-browser close", timeout=10)

# Deduplicate while preserving order
seen = set()
unique = []
for a in articles:
    if a not in seen:
        seen.add(a)
        unique.append(a)

# Output as JSON
print(json.dumps(unique, ensure_ascii=False, indent=2))
