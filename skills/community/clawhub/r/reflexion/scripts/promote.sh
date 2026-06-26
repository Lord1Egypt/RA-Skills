#!/usr/bin/env bash
# reflexion/scripts/promote.sh
# Auto-promotes recurring patterns to CLAUDE.md.
#
# Promotion criteria (ALL must be true):
#   1. occurrences >= 3
#   2. resolution is non-empty
#   3. promoted is false
#   4. first_seen is at least 1 day ago (not a flurry)
#
# Writes concise, actionable rules — not incident reports.
set -euo pipefail

PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
REFLEX_DIR="$PROJECT_ROOT/.reflexion"
CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"
STATS_FILE="$REFLEX_DIR/stats.json"
TODAY="$(date +%Y-%m-%d)"
TODAY_EPOCH="$(date +%s)"

[ -d "$REFLEX_DIR/entries" ] || exit 0

# Require python3 for JSON manipulation
command -v python3 &>/dev/null || exit 0

# --- Find promotion candidates ---
PROMOTED_COUNT=0

for entry_file in "$REFLEX_DIR/entries"/RFX-*.json; do
  [ -f "$entry_file" ] || continue

  # Check promotion criteria using python3
  RESULT="$(python3 -c "
import json, sys
from datetime import datetime, timedelta

try:
    with open('$entry_file') as f:
        e = json.load(f)

    # Must not already be promoted
    if e.get('promoted', False):
        sys.exit(0)

    # Must have 3+ occurrences
    if e.get('occurrences', 1) < 3:
        sys.exit(0)

    # Must have a resolution
    if not e.get('resolution', '').strip():
        sys.exit(0)

    # Must be at least 1 day old
    first = datetime.strptime(e.get('first_seen', '$TODAY'), '%Y-%m-%d')
    if (datetime.now() - first).days < 1:
        sys.exit(0)

    # Output the promotion rule
    resolution = e['resolution'].strip()
    entry_id = e.get('id', 'unknown')
    occurrences = e.get('occurrences', 3)
    entry_type = e.get('type', 'pattern')

    # Create a concise rule
    print(f'- {resolution} (seen {occurrences}x, source: {entry_id})')
except Exception as ex:
    sys.exit(0)
" 2>/dev/null)"

  [ -z "$RESULT" ] && continue

  # --- Append rule to CLAUDE.md ---
  # Create CLAUDE.md if it doesn't exist
  if [ ! -f "$CLAUDE_MD" ]; then
    cat > "$CLAUDE_MD" << 'HEADER'
# Project Guidelines

HEADER
  fi

  # Add the reflexion section header if not present
  if ! grep -qF '<!-- reflexion:auto-promoted -->' "$CLAUDE_MD" 2>/dev/null; then
    cat >> "$CLAUDE_MD" << 'SECTION'

<!-- reflexion:auto-promoted -->
## Reflexion: Learned Rules

Rules auto-promoted from recurring patterns. Do not edit this section manually.

SECTION
  fi

  # Check if this specific entry is already promoted (by ID)
  ENTRY_ID="$(python3 -c "import json; print(json.load(open('$entry_file')).get('id',''))" 2>/dev/null)"
  if grep -qF "$ENTRY_ID" "$CLAUDE_MD" 2>/dev/null; then
    # Already in CLAUDE.md — just mark as promoted in entry
    python3 -c "
import json
with open('$entry_file', 'r') as f:
    e = json.load(f)
e['promoted'] = True
with open('$entry_file', 'w') as f:
    json.dump(e, f, indent=2)
" 2>/dev/null || true
    continue
  fi

  # Append the rule
  echo "$RESULT" >> "$CLAUDE_MD"

  # Mark entry as promoted
  python3 -c "
import json
with open('$entry_file', 'r') as f:
    e = json.load(f)
e['promoted'] = True
with open('$entry_file', 'w') as f:
    json.dump(e, f, indent=2)
" 2>/dev/null || true

  PROMOTED_COUNT=$((PROMOTED_COUNT + 1))
done

# --- Update stats ---
if [ "$PROMOTED_COUNT" -gt 0 ] && [ -f "$STATS_FILE" ]; then
  python3 -c "
import json
try:
    with open('$STATS_FILE', 'r') as f:
        s = json.load(f)
    s['total_promoted'] = s.get('total_promoted', 0) + $PROMOTED_COUNT
    s['last_promotion'] = '$TODAY'
    with open('$STATS_FILE', 'w') as f:
        json.dump(s, f, indent=2)
except:
    pass
" 2>/dev/null || true
fi

# Only output if something was promoted (avoid noise)
if [ "$PROMOTED_COUNT" -gt 0 ]; then
  echo "[reflexion] Promoted $PROMOTED_COUNT pattern(s) to CLAUDE.md"
fi
