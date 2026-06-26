#!/usr/bin/env bash
# status.sh — Show live status of all workers in a research run
# Usage: status.sh <slug>

set -euo pipefail

SLUG="${1:?Usage: status.sh <slug>}"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
DATA_DIR="$WORKSPACE/skills-data/skilled-deep-research/$SLUG"

if [[ ! -d "$DATA_DIR" ]]; then
  echo "Error: no run found for slug '$SLUG'"
  exit 1
fi

NOW=$(date +%s)

echo "=== Research Run: $SLUG ==="
echo ""

if [[ -f "$DATA_DIR/meta.json" ]]; then
  TOPIC=$(python3 -c "import json,sys; d=json.load(open('$DATA_DIR/meta.json')); print(d.get('topic','?'))" 2>/dev/null)
  STARTED=$(python3 -c "import json,sys; d=json.load(open('$DATA_DIR/meta.json')); print(d.get('started','?'))" 2>/dev/null)
  echo "Topic:   $TOPIC"
  echo "Started: $STARTED"
  echo ""
fi

echo "--- Workers ---"
WORKER_COUNT=0
for pf in "$DATA_DIR"/workers/*-progress.json; do
  [[ -f "$pf" ]] || continue
  WORKER_COUNT=$((WORKER_COUNT + 1))
  python3 - "$pf" "$NOW" <<'PYEOF'
import json, sys
from datetime import datetime

pf = sys.argv[1]
now = int(sys.argv[2])

try:
    d = json.load(open(pf))
except Exception:
    print(f"  [error reading {pf}]")
    sys.exit(0)

name     = d.get("worker", "?")
phase    = d.get("phase", "?")
pct      = d.get("pct", 0)
found    = d.get("urls_found", "?")
fetched  = d.get("urls_fetched", "?")
findings = d.get("findings", "?")
url      = d.get("current_url", "")
hb       = d.get("heartbeat", 0)

age = now - hb if hb else 0
age_str = f"{age}s ago" if age < 3600 else f"{age//60}m ago"

status_icon = "✅" if phase == "complete" else ("⚠️" if age > 300 else "🔄")

print(f"  {status_icon} {name}")
print(f"     Phase: {phase} | Progress: {pct}% | Heartbeat: {age_str}")
print(f"     URLs found: {found} | fetched: {fetched} | findings: {findings}")
if url and phase != "complete":
    print(f"     Current: {url[:80]}")
PYEOF
  echo ""
done

if [[ $WORKER_COUNT -eq 0 ]]; then
  echo "  (no worker progress files found yet)"
  echo ""
fi

# Summary counts
SOURCES=$(grep -c '^### ' "$DATA_DIR/workers/"*-results.md 2>/dev/null | awk -F: '{sum+=$2} END {print sum+0}')
RETRIES=$(grep -c '^- ' "$DATA_DIR/workers/retry-queue.md" 2>/dev/null || echo 0)

echo "--- Totals ---"
echo "  Sources found: $SOURCES"
echo "  Retry queue:   $RETRIES"
echo ""

if [[ -f "$DATA_DIR/report.md" ]]; then
  echo "  📄 Final report: $DATA_DIR/report.md"
fi
