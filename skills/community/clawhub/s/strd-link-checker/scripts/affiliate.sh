#!/bin/bash
# affiliate.sh — Affiliate link report: find and verify affiliate links
# Run this to audit revenue links on affiliate/commission-based sites

set -e

DIR="${1:-${SITE_DIR:-./site}}"
TIMEOUT="${LINK_CHECK_TIMEOUT:-10}"
AFFILIATE_DOMAINS="${AFFILIATE_DOMAINS:-amazon.com,hostname/s/aspx,godaddy.com,bluehost.com,digitalocean.com,heroku.com,shopify.com,awin1.com,ref=,clickbank.com,hostname/s/affiliate}"

echo "# 💰 Affiliate Link Report"
echo "Directory: $DIR"
echo "Generated: $(date '+%Y-%m-%d %H:%M:%S UTC')"
echo ""

python3 - "$DIR" "$TIMEOUT" "$AFFILIATE_DOMAINS" << 'PYEOF'
import sys
import os
import re
import subprocess
from pathlib import Path

dir_path = sys.argv[1]
timeout = int(sys.argv[2])
aff_domains = sys.argv[3].split(",")

# Find all HTML files
html_files = list(Path(dir_path).rglob("*.html"))
print(f"Scanning {len(html_files)} HTML files...")

# Extract all links and filter to affiliate
link_pattern = re.compile(r'href="(https?://[^"]*)"', re.IGNORECASE)

aff_links = []
for html_file in html_files:
    try:
        content = html_file.read_text(errors="ignore")
        for m in link_pattern.finditer(content):
            url = m.group(1)
            for aff in aff_domains:
                if aff.strip() and aff.strip() in url:
                    line_num = content[:m.start()].count("\n") + 1
                    aff_links.append((str(html_file), line_num, url))
                    break
    except Exception:
        pass

total = len(aff_links)
print(f"Affiliate links found: {total}")
print()

if total == 0:
    print("No affiliate links detected.")
    print()
    print("Tip: Set AFFILIATE_DOMAINS env var to include your specific affiliate domains.")
    print("Example: AFFILIATE_DOMAINS='mytracking.affiliate.com,partner.example.com' ./scripts/affiliate.sh")
    sys.exit(0)

print("Verifying link status...")
print()

working = 0
broken = 0

for i, (file, line, url) in enumerate(aff_links):
    if i % 10 == 0:
        print(f"  Verified {i}/{total}...", end="\r")
    
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", str(timeout), "-L", "-I", url],
            capture_output=True, text=True, timeout=timeout + 2
        )
        status = result.stdout.strip() or "000"
    except Exception:
        status = "000"
    
    if status.startswith("2"):
        print(f"✅ `{file}` line {line}: [{url}]({url})")
        working += 1
    elif status.startswith("3"):
        print(f"↪️  `{file}` line {line}: [{url}]({url}) — redirected (HTTP {status})")
        working += 1
    else:
        print(f"❌ `{file}` line {line}: [{url}]({url}) — HTTP {status}")
        broken += 1

print(f"\nVerified {total}/{total} links")
print()
print(f"- Total affiliate links: {total}")
print(f"- Working: {working}")
print(f"- Broken: {broken}")
print()

if broken > 0:
    print(f"⚠️  {broken} affiliate link(s) are broken. Replace before they cost you commissions.")
else:
    print("🎉 All affiliate links are working.")
PYEOF
