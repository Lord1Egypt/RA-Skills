#!/usr/bin/env bash
# Detect content duplication across workspace files
# Usage: bash scripts/audit-duplication.sh
set -euo pipefail

WS="${WS:-$HOME/.openclaw/workspace}"

echo "=== Workspace Duplication Audit ==="
echo ""

# Collect existing workspace files
EXISTING=()
for f in AGENTS.md TOOLS.md MEMORY.md USER.md SOUL.md IDENTITY.md HEARTBEAT.md; do
  [ -f "$WS/$f" ] && EXISTING+=("$WS/$f")
done

echo "📄 Files found: ${#EXISTING[@]}"
echo ""

# Check for duplicate section headers across files
echo "--- Duplicate Section Headers ---"
DUPS=0

# Use Python for portable associative array behavior
python3 -c "
import os, sys

ws = os.environ.get('WS', os.path.expanduser('~/.openclaw/workspace'))
files = [f for f in sys.argv[1:] if os.path.exists(f)]

header_map = {}
dups = 0
for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith('#') and not line.startswith('####'):
                clean = line.lstrip('#').strip().lower()
                if clean and clean in header_map:
                    print(f'  ⚠️  \"{clean}\" in {fname} AND {header_map[clean]}')
                    dups += 1
                else:
                    header_map[clean] = fname

if dups == 0:
    print('  ✅ No duplicate headers')
" "${EXISTING[@]}" 2>/dev/null || echo "  ⚠️  Header check failed"

echo ""
echo "--- Role Overlap Check ---"

python3 -c "
import re, os

ws = os.environ.get('WS', os.path.expanduser('~/.openclaw/workspace'))
files = {}
for name in ['AGENTS.md', 'TOOLS.md', 'MEMORY.md', 'USER.md', 'SOUL.md', 'IDENTITY.md']:
    path = os.path.join(ws, name)
    if os.path.exists(path):
        files[name] = open(path).read()

# Check for credential patterns outside TOOLS.md
cred_pattern = re.compile(r'(1Password|op item|API.?[Kk]ey|env[: ]|gateway env|OP_SERVICE)', re.IGNORECASE)
issues = 0
for name, content in files.items():
    if name == 'TOOLS.md':
        continue
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if cred_pattern.search(line):
            # Skip cross-references to TOOLS.md
            if 'TOOLS.md' in line:
                continue
            # MEMORY.md can reference 1Password rules briefly (security policy)
            if name == 'MEMORY.md' and any(k in line for k in ['NEVER share', 'vault', 'read-only']):
                continue
            print(f'  ⚠️  {name}:{i+1} — credential-adjacent content: {line.strip()[:80]}')
            issues += 1

if issues == 0:
    print('  ✅ Credentials properly confined to TOOLS.md')
else:
    print(f'  ⚠️  {issues} credential reference(s) outside TOOLS.md')

# Check for personality content outside SOUL.md/IDENTITY.md
personality = re.compile(r'\b(terse|no.?filler|no.?fluff|sycophancy|bullet.?points)\b', re.IGNORECASE)
p_issues = 0
for name, content in files.items():
    if name in ('SOUL.md', 'IDENTITY.md', 'USER.md'):
        continue
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if personality.search(line):
            print(f'  ℹ️  {name}:{i+1} — personality-adjacent: {line.strip()[:80]}')
            p_issues += 1

if p_issues == 0:
    print('  ✅ Personality content properly confined to SOUL.md/IDENTITY.md')
" 2>/dev/null || echo "  ⚠️  Role overlap check failed"

echo ""
echo "=== Done ==="
