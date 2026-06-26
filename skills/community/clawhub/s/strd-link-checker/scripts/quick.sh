#!/bin/bash
# quick.sh — Fast broken-link scan only (no slow/redirect/affiliate checks)
# Use for rapid pre-publish checks

set -e

DIR="${1:-${SITE_DIR:-./site}}"
TIMEOUT="${LINK_CHECK_TIMEOUT:-10}"

echo "# 🔗 Quick Broken Link Scan"
echo "Directory: $DIR"
echo "Generated: $(date '+%Y-%m-%d %H:%M:%S UTC')"
echo ""

HTML_FILES=$(find "$DIR" -name "*.html" 2>/dev/null | wc -l | tr -d ' ')
echo "Scanning $HTML_FILES HTML files..."
echo ""

# Use Python for reliable HTML parsing + link extraction
python3 - "$DIR" "$TIMEOUT" << 'PYEOF'
import sys
import os
import re
import subprocess
from pathlib import Path

dir_path = sys.argv[1]
timeout = int(sys.argv[2])

# Find all HTML files
html_files = list(Path(dir_path).rglob("*.html"))
print(f"Found {len(html_files)} HTML files")

# Extract all http/https links
link_pattern = re.compile(r'href="(https?://[^"]*)"', re.IGNORECASE)

links = []
for html_file in html_files:
    try:
        content = html_file.read_text(errors="ignore")
        for m in link_pattern.finditer(content):
            url = m.group(1)
            if url.startswith("http"):
                line_num = content[:m.start()].count("\n") + 1
                links.append((str(html_file), line_num, url))
    except Exception:
        pass

total = len(links)
print(f"Total external links: {total}")
print()

broken_count = 0
working = 0
batch = []

for i, (file, line, url) in enumerate(links):
    if i > 0 and i % 50 == 0:
        print(f"  Checked {i}/{total}...", end="\r")
    
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", str(timeout), "-L", "-I", url],
            capture_output=True, text=True, timeout=timeout + 2
        )
        status = result.stdout.strip() or "000"
    except Exception:
        status = "000"
    
    if status.startswith("4") or status.startswith("5") or status == "000":
        print(f"- `{file}` line {line}: [{url}]({url}) — HTTP {status}")
        broken_count += 1
    else:
        working += 1

print(f"\nChecked {total}/{total} links")
print()
if broken_count == 0:
    print(f"✅ No broken links found in {total} links checked.")
    sys.exit(0)
else:
    print(f"🔴 Found {broken_count} broken link(s) out of {total} total links.")
    sys.exit(1)
PYEOF

exit_code=$?
echo ""
if [ $exit_code -eq 0 ]; then
    echo "✅ Scan complete — no broken links."
elif [ $exit_code -eq 1 ]; then
    echo "🔴 Scan complete — broken links found."
else
    echo "⚠️  Scan exited with code $exit_code"
fi
