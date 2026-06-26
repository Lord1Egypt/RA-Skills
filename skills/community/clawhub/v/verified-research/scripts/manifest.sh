#!/usr/bin/env bash
#===========================================================
# manifest.sh — Build manifest.json from all claim cards
#
# Inputs:
#   CACHE_DIR   — full path to the session cache dir
#   TOPIC       — research topic
#   SESSION_ID  — optional session id
#===========================================================

set -e

CACHE_DIR="${CACHE_DIR:?missing CACHE_DIR}"
TOPIC="${TOPIC:?missing TOPIC}"
SESSION_ID="${SESSION_ID:-unknown}"

CLAIMS_DIR="${CACHE_DIR}/claims"
MANIFEST_PATH="${CACHE_DIR}/manifest.json"

NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

python3 << PYEOF
import os, json, re, glob
from pathlib import Path

cache_dir = os.environ.get('CACHE_DIR', '')
claims_dir = os.path.join(cache_dir, 'claims')
topic = os.environ.get('TOPIC', '')
session_id = os.environ.get('SESSION_ID', 'unknown')
now = os.environ.get('NOW', '')

# Find oldest claim created_at
oldest = now
tiers = {'T1': 0, 'T2': 0, 'T3': 0, 'T4': 0}
claims = []

for fpath in sorted(glob.glob(os.path.join(claims_dir, '*.md'))):
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        raw = f.read()

    # Parse YAML frontmatter
    m = re.match(r'^---\n(.*?)\n---\n', raw, re.DOTALL)
    if not m:
        continue
    frontmatter_raw = m.group(1)
    content = raw[m.end():].strip()

    # Extract frontmatter fields
    def get_field(key):
        match = re.search(rf'^{re.escape(key)}:\s*(.*)$', frontmatter_raw, re.MULTILINE)
        return match.group(1).strip() if match else ''

    cid = get_field('id') or fname.replace('.md','')
    round_n = get_field('round') or '1'
    source = get_field('source') or 'unknown'
    source_tier = get_field('source_tier') or 'T4'
    verification = get_field('verification_status') or 'pending'
    created_at = get_field('created_at') or now

    if created_at < oldest:
        oldest = created_at

    tiers[source_tier] = tiers.get(source_tier, 0) + 1

    claims.append({
        'id': cid,
        'round': round_n,
        'source': source,
        'source_tier': source_tier,
        'verification_status': verification,
        'created_at': created_at,
        'content_preview': content[:500]
    })

total = len(claims)

manifest = {
    'topic': topic,
    'session_id': session_id,
    'created_at': oldest,
    'updated_at': now,
    'total_claims': total,
    'source_tier_counts': tiers,
    'claims': claims
}

with open(os.path.join(cache_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"manifest: wrote {os.path.join(cache_dir, 'manifest.json')} (total_claims={total}, T1={tiers['T1']} T2={tiers['T2']} T3={tiers['T3']} T4={tiers['T4']})")
PYEOF
