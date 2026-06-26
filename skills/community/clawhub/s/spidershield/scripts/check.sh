#!/usr/bin/env bash
# /spidershield check <skill-name> or <author/skill>
# Queries SpiderRating Skill Trust API and prints rich trust report.
# Supports both "web-search-pro" (fuzzy) and "alice/web-search-pro" (exact).

set -euo pipefail

INPUT="${1:-}"
if [[ -z "$INPUT" ]]; then
  echo "Usage: /spidershield check <skill-name>" >&2
  echo "" >&2
  echo "Examples:" >&2
  echo "  /spidershield check web-search-pro" >&2
  echo "  /spidershield check spclaudehome/web-search-pro" >&2
  exit 1
fi

API_BASE="https://api.spiderrating.com"

# Detect format: author/skill or just skill name
if [[ "$INPUT" == *"/"* ]]; then
  # Exact: author/skill
  AUTHOR=$(echo "$INPUT" | cut -d/ -f1)
  SKILL=$(echo "$INPUT" | cut -d/ -f2-)
  URL="$API_BASE/v1/public/skill-score/$AUTHOR/$SKILL"
else
  # Fuzzy: skill name only
  URL="$API_BASE/v1/public/skill-score/$INPUT"
fi

RESPONSE=$(curl -sf --max-time 10 "$URL") || {
  echo "[SpiderRating] API unavailable — check your connection." >&2
  exit 1
}

# Parse and display rich output
echo "$RESPONSE" | python3 -c "
import sys, json

try:
    d = json.load(sys.stdin)
except json.JSONDecodeError:
    print('[SpiderRating] Invalid response from API.')
    sys.exit(1)

verdict  = d.get('verdict', 'unknown')
score    = d.get('score')
grade    = d.get('grade', '?')
block    = d.get('block', False)
msg      = d.get('message', '')
slug     = d.get('slug', '?')
conf     = d.get('confidence')
scanned  = d.get('scanned_at', '')
caps     = d.get('capabilities', [])
rank     = d.get('ecosystem_rank')
findings = d.get('finding_summary', {})
risks    = d.get('risk_factors', [])
breakdown = d.get('score_breakdown', {})
mp       = d.get('marketplace')
url      = d.get('report_url', '')

score_str = f'{score:.1f} / 10' if score is not None else 'N/A'
conf_label = d.get('confidence_label', f'{conf*100:.0f}%' if conf else 'N/A')

VERDICT_ICONS = {'safe': '\u2705', 'risky': '\u26a0\ufe0f ', 'malicious': '\U0001f6a8', 'unknown': '\u2753'}
icon = VERDICT_ICONS.get(verdict, '\u2753')

CAP_ICONS = {
    'browser_access': '\U0001f310 Browser',
    'installs_deps': '\U0001f4e6 Installs Deps',
    'webhook_calls': '\U0001f517 Webhook',
    'credential_handling': '\U0001f511 Credentials',
    'env_var_access': '\U0001f527 Env Vars',
    'external_network': '\U0001f30d Network',
    'data_mutation': '\U0001f4be Data Mutation',
    'crypto_wallet': '\U0001f4b0 Crypto',
    'downloads_binary': '\u2b07\ufe0f  Binary',
}

# Header
print()
print(f'SpiderRating Skill Trust Report')
print('\u2501' * 40)
print(f'  Skill:      {slug}')
print(f'  Score:      {score_str}   Grade: {grade}')
print(f'  Verdict:    {icon} {verdict.upper()}')
print(f'  Precision:  {conf_label}')
if scanned:
    print(f'  Scanned:    {scanned[:10]}')

# Capabilities
if caps:
    print()
    print(f'  \U0001f4e6 Capabilities:')
    cap_strs = [CAP_ICONS.get(c, c) for c in caps]
    print(f'    {\"  \".join(cap_strs)}')

# Security findings
crit = findings.get('critical', 0)
high = findings.get('high', 0)
med  = findings.get('medium', 0)
low  = findings.get('low', 0)
print()
print(f'  \U0001f50d Security: {crit} critical \u00b7 {high} high \u00b7 {med} medium \u00b7 {low} low')
if risks:
    for r in risks:
        print(f'    {r}')

# Ecosystem ranking
if rank:
    pos = rank.get('position', '?')
    total = rank.get('total', '?')
    pct = rank.get('percentile', '')
    print()
    print(f'  \U0001f4ca Ecosystem: #{pos} / {total} skills ({pct})')

# Score breakdown
if breakdown:
    desc = breakdown.get('description')
    sec  = breakdown.get('security')
    meta = breakdown.get('metadata')
    parts = []
    if desc is not None: parts.append(f'Description {desc:.1f}')
    if sec  is not None: parts.append(f'Security {sec:.1f}')
    if meta is not None: parts.append(f'Metadata {meta:.1f}')
    if parts:
        print(f'    Breakdown: {\" \u00b7 \".join(parts)}')

# Marketplace
if mp and mp.get('downloads'):
    dl = mp['downloads']
    inst = mp.get('installs_current', 0)
    print(f'    Downloads: {dl:,}  Active installs: {inst:,}')

# Recommendation
print()
if msg:
    print(f'  \U0001f4a1 {msg}')
if url:
    print(f'  \U0001f517 {url}')
print()

# Exit code: 2 for malicious (blocked), 1 for risky, 0 for safe/unknown
if block:
    sys.exit(2)
elif verdict == 'risky':
    sys.exit(1)
"
