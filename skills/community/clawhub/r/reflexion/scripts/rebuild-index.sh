#!/usr/bin/env bash
# reflexion/scripts/rebuild-index.sh
# Rebuilds the keyword index from all entries. Run after manual edits.
set -euo pipefail

PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
REFLEX_DIR="$PROJECT_ROOT/.reflexion"
INDEX_FILE="$REFLEX_DIR/index.txt"

[ -d "$REFLEX_DIR/entries" ] || { echo "No .reflexion/entries/ directory found."; exit 1; }

# Wipe and rebuild
> "$INDEX_FILE"

declare -A KW_MAP 2>/dev/null || {
  # bash 3 fallback: use temp file approach
  TMPFILE="$(mktemp)"
  trap "rm -f '$TMPFILE'" EXIT

  for entry_file in "$REFLEX_DIR/entries"/RFX-*.json; do
    [ -f "$entry_file" ] || continue
    ENTRY_ID="$(basename "$entry_file" .json)"
    # Extract keywords field
    KEYWORDS="$(grep -oP '"keywords"\s*:\s*"[^"]+"' "$entry_file" 2>/dev/null | sed 's/.*: *"//;s/"$//' || true)"
    if [ -z "$KEYWORDS" ] && command -v python3 &>/dev/null; then
      KEYWORDS="$(python3 -c "
import json
try:
    d = json.load(open('$entry_file'))
    kws = d.get('keywords', [])
    if isinstance(kws, list): print(','.join(kws))
    else: print(kws)
except: pass
" 2>/dev/null)"
    fi
    IFS=',' read -ra KW_ARRAY <<< "$KEYWORDS"
    for kw in "${KW_ARRAY[@]}"; do
      kw="$(echo "$kw" | tr -d ' "' | tr '[:upper:]' '[:lower:]')"
      [ -n "$kw" ] && echo "${kw}:${ENTRY_ID}" >> "$TMPFILE"
    done
  done

  # Merge duplicate keywords
  sort "$TMPFILE" | awk -F: '{
    if ($1 == prev) {
      ids = ids "," $2
    } else {
      if (prev != "") print prev ":" ids
      prev = $1; ids = $2
    }
  } END { if (prev != "") print prev ":" ids }' > "$INDEX_FILE"

  ENTRY_COUNT="$(find "$REFLEX_DIR/entries" -name 'RFX-*.json' 2>/dev/null | wc -l | tr -d ' ')"
  KW_COUNT="$(wc -l < "$INDEX_FILE" | tr -d ' ')"
  echo "[reflexion] Index rebuilt: $KW_COUNT keywords from $ENTRY_COUNT entries."
  exit 0
}

# bash 4+ path with associative arrays
for entry_file in "$REFLEX_DIR/entries"/RFX-*.json; do
  [ -f "$entry_file" ] || continue
  ENTRY_ID="$(basename "$entry_file" .json)"

  KEYWORDS=""
  if command -v python3 &>/dev/null; then
    KEYWORDS="$(python3 -c "
import json
try:
    d = json.load(open('$entry_file'))
    kws = d.get('keywords', [])
    if isinstance(kws, list): print(','.join(kws))
    else: print(kws)
except: pass
" 2>/dev/null)"
  else
    KEYWORDS="$(grep -oP '"keywords"\s*:\s*"[^"]+"' "$entry_file" 2>/dev/null | sed 's/.*: *"//;s/"$//' || true)"
  fi

  IFS=',' read -ra KW_ARRAY <<< "$KEYWORDS"
  for kw in "${KW_ARRAY[@]}"; do
    kw="$(echo "$kw" | tr -d ' "' | tr '[:upper:]' '[:lower:]')"
    [ -n "$kw" ] || continue
    if [ -n "${KW_MAP[$kw]:-}" ]; then
      KW_MAP["$kw"]="${KW_MAP[$kw]},$ENTRY_ID"
    else
      KW_MAP["$kw"]="$ENTRY_ID"
    fi
  done
done

for kw in $(echo "${!KW_MAP[@]}" | tr ' ' '\n' | sort); do
  echo "${kw}:${KW_MAP[$kw]}" >> "$INDEX_FILE"
done

ENTRY_COUNT="$(find "$REFLEX_DIR/entries" -name 'RFX-*.json' 2>/dev/null | wc -l | tr -d ' ')"
KW_COUNT="$(wc -l < "$INDEX_FILE" | tr -d ' ')"
echo "[reflexion] Index rebuilt: $KW_COUNT keywords from $ENTRY_COUNT entries."
