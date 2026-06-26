#!/usr/bin/env bash
# reflexion/scripts/status.sh
# Dashboard showing learning stats and recent entries.
set -euo pipefail

PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
REFLEX_DIR="$PROJECT_ROOT/.reflexion"

if [ ! -d "$REFLEX_DIR/entries" ]; then
  echo "No .reflexion/ directory found. Run init.sh or let capture.sh auto-initialize."
  exit 0
fi

# --- Count entries ---
TOTAL="$(find "$REFLEX_DIR/entries" -name 'RFX-*.json' 2>/dev/null | wc -l | tr -d ' ')"
ERRORS="$(grep -rl '"type".*"error"' "$REFLEX_DIR/entries/" 2>/dev/null | wc -l | tr -d ' ')"
CORRECTIONS="$(grep -rl '"type".*"correction"' "$REFLEX_DIR/entries/" 2>/dev/null | wc -l | tr -d ' ')"
INSIGHTS="$(grep -rl '"type".*"insight"' "$REFLEX_DIR/entries/" 2>/dev/null | wc -l | tr -d ' ')"
PATTERNS="$(grep -rl '"type".*"pattern"' "$REFLEX_DIR/entries/" 2>/dev/null | wc -l | tr -d ' ')"
PROMOTED="$(grep -rl '"promoted".*true' "$REFLEX_DIR/entries/" 2>/dev/null | wc -l | tr -d ' ')"
WITH_RESOLUTION="$(grep -rl '"resolution"\s*:\s*"[^"]' "$REFLEX_DIR/entries/" 2>/dev/null | wc -l | tr -d ' ')"
UNRESOLVED=$((TOTAL - WITH_RESOLUTION - PROMOTED))
[ "$UNRESOLVED" -lt 0 ] && UNRESOLVED=0

# --- Count keywords ---
KW_COUNT=0
[ -f "$REFLEX_DIR/index.txt" ] && KW_COUNT="$(wc -l < "$REFLEX_DIR/index.txt" | tr -d ' ')"

# --- Read stats ---
TOTAL_CAPTURED=0
TOTAL_RECALLED=0
TOTAL_PROMOTED_STAT=0
LAST_CAPTURE="never"
LAST_RECALL="never"
if [ -f "$REFLEX_DIR/stats.json" ] && command -v python3 &>/dev/null; then
  eval "$(python3 -c "
import json
try:
    s = json.load(open('$REFLEX_DIR/stats.json'))
    print(f'TOTAL_CAPTURED={s.get(\"total_captured\",0)}')
    print(f'TOTAL_RECALLED={s.get(\"total_recalled\",0)}')
    print(f'TOTAL_PROMOTED_STAT={s.get(\"total_promoted\",0)}')
    lc = s.get('last_capture') or 'never'
    lr = s.get('last_recall') or 'never'
    print(f'LAST_CAPTURE={lc}')
    print(f'LAST_RECALL={lr}')
except:
    pass
" 2>/dev/null)"
fi

# --- Promotion candidates ---
CANDIDATES=0
for f in "$REFLEX_DIR/entries"/RFX-*.json; do
  [ -f "$f" ] || continue
  if python3 -c "
import json, sys
e = json.load(open('$f'))
if not e.get('promoted') and e.get('occurrences',1) >= 2 and e.get('resolution','').strip():
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
    CANDIDATES=$((CANDIDATES + 1))
  fi
done

# --- High-occurrence unresolved ---
HOT_ERRORS=""
if command -v python3 &>/dev/null; then
  HOT_ERRORS="$(python3 -c "
import json, os, glob
entries = []
for f in glob.glob('$REFLEX_DIR/entries/RFX-*.json'):
    try:
        e = json.load(open(f))
        if not e.get('resolution','').strip() and e.get('occurrences',1) >= 2:
            entries.append(e)
    except: pass
entries.sort(key=lambda x: x.get('occurrences',1), reverse=True)
for e in entries[:3]:
    print(f\"  [{e['id']}] {e.get('type','error')} (seen {e.get('occurrences',1)}x): {e.get('trigger','')[:80]}\")
" 2>/dev/null)"
fi

# --- Output ---
cat << DASHBOARD

  ╔══════════════════════════════════════════════╗
  ║          reflexion status dashboard          ║
  ╠══════════════════════════════════════════════╣
  ║                                              ║
  ║  Entries:  $TOTAL total
  ║    errors: $ERRORS  corrections: $CORRECTIONS  insights: $INSIGHTS  patterns: $PATTERNS
  ║    resolved: $WITH_RESOLUTION  unresolved: $UNRESOLVED  promoted: $PROMOTED
  ║                                              ║
  ║  Index:    $KW_COUNT keywords
  ║                                              ║
  ║  Activity:                                   ║
  ║    captures:   $TOTAL_CAPTURED (last: $LAST_CAPTURE)
  ║    recalls:    $TOTAL_RECALLED (last: $LAST_RECALL)
  ║    promotions: $TOTAL_PROMOTED_STAT
  ║                                              ║
  ║  Promotion candidates (2+ occurrences): $CANDIDATES
  ╚══════════════════════════════════════════════╝

DASHBOARD

if [ -n "$HOT_ERRORS" ]; then
  echo "  Hot unresolved errors (recurring, no fix yet):"
  echo "$HOT_ERRORS"
  echo ""
fi

# --- Recent entries (last 5) ---
echo "  Recent entries:"
find "$REFLEX_DIR/entries" -name 'RFX-*.json' -printf '%T@ %f\n' 2>/dev/null \
  | sort -rn | head -5 | while read -r _ts fname; do
    fpath="$REFLEX_DIR/entries/$fname"
    if command -v python3 &>/dev/null; then
      python3 -c "
import json
try:
    e = json.load(open('$fpath'))
    status = 'promoted' if e.get('promoted') else ('resolved' if e.get('resolution','').strip() else 'open')
    print(f\"  [{e['id']}] {e.get('type','?'):10s} {status:8s} (x{e.get('occurrences',1)}) {e.get('trigger','')[:60]}\")
except: pass
" 2>/dev/null
    else
      echo "  $(basename "$fname" .json)"
    fi
  done

echo ""
