#!/usr/bin/env bash
# reflexion/scripts/recall.sh
# UserPromptSubmit hook — searches past learnings relevant to the current prompt
# and injects matching solutions into the agent's context.
#
# Claude Code UserPromptSubmit hooks receive JSON on stdin:
#   { "prompt": "the user's message" }
#
# Output is injected into the conversation as system context.
# If no relevant learnings found, output NOTHING (zero token overhead).
set -euo pipefail

# --- Init ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
REFLEX_DIR="$PROJECT_ROOT/.reflexion"
INDEX_FILE="$REFLEX_DIR/index.txt"

# No reflexion data yet — exit silently
[ -d "$REFLEX_DIR/entries" ] || exit 0
[ -f "$INDEX_FILE" ] || exit 0
# Empty index — exit silently
[ -s "$INDEX_FILE" ] || exit 0

# --- Read user prompt from stdin ---
INPUT=""
if [ ! -t 0 ]; then
  INPUT="$(cat)"
fi
[ -z "$INPUT" ] && exit 0

# Extract the prompt text
PROMPT=""
if command -v python3 &>/dev/null; then
  PROMPT="$(python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    print(d.get('prompt', d.get('message', '')))
except:
    print(sys.stdin.read() if False else '')
" <<< "$INPUT" 2>/dev/null)"
fi
# Fallback: use the raw input as the prompt
[ -z "$PROMPT" ] && PROMPT="$INPUT"
[ -z "$PROMPT" ] && exit 0

# --- Extract keywords from prompt ---
PROMPT_KEYWORDS="$(echo "$PROMPT" \
  | tr '[:upper:]' '[:lower:]' \
  | tr -cs '[:alnum:]_-' '\n' \
  | grep -E '^.{3,}$' \
  | grep -vxF -e 'the' -e 'and' -e 'for' -e 'not' -e 'that' -e 'with' -e 'this' -e 'from' -e 'was' -e 'are' -e 'but' -e 'has' -e 'had' -e 'have' -e 'been' -e 'will' -e 'can' -e 'could' -e 'would' -e 'should' -e 'may' -e 'might' -e 'does' -e 'did' -e 'done' -e 'its' -e 'into' -e 'also' -e 'than' -e 'then' -e 'each' -e 'which' -e 'their' -e 'there' -e 'these' -e 'those' -e 'such' -e 'when' -e 'where' -e 'while' -e 'about' -e 'after' -e 'before' -e 'between' -e 'under' -e 'over' -e 'just' -e 'like' -e 'more' -e 'some' -e 'only' -e 'other' -e 'very' -e 'still' -e 'already' -e 'help' -e 'please' -e 'want' -e 'need' -e 'make' -e 'how' -e 'what' -e 'why' -e 'use' -e 'get' -e 'run' -e 'try' -e 'let' -e 'see' -e 'fix' -e 'add' \
  | sort -u \
  | head -30)"

[ -z "$PROMPT_KEYWORDS" ] && exit 0

# --- Search index for matching entry IDs ---
# Score entries by number of keyword hits (more hits = more relevant)
declare -A ENTRY_SCORES 2>/dev/null || {
  # bash 3 fallback: just collect entry IDs without scoring
  MATCHED_IDS=""
  while IFS= read -r kw; do
    HITS="$(grep -i "^${kw}:" "$INDEX_FILE" 2>/dev/null | head -1 | cut -d: -f2-)"
    if [ -n "$HITS" ]; then
      IFS=',' read -ra IDS <<< "$HITS"
      for id in "${IDS[@]}"; do
        id="$(echo "$id" | tr -d ' ')"
        [ -n "$id" ] && MATCHED_IDS="$MATCHED_IDS $id"
      done
    fi
  done <<< "$PROMPT_KEYWORDS"

  # Deduplicate and take top 3
  TOP_IDS="$(echo "$MATCHED_IDS" | tr ' ' '\n' | sort | uniq -c | sort -rn | head -3 | awk '{print $2}')"
  # Skip to output section
  if [ -z "$TOP_IDS" ]; then
    exit 0
  fi
  # Jump to output
  ENTRY_SCORES_FALLBACK=true
}

if [ "${ENTRY_SCORES_FALLBACK:-}" != "true" ]; then
  # bash 4+ path: proper scoring with associative arrays
  while IFS= read -r kw; do
    HITS="$(grep -i "^${kw}:" "$INDEX_FILE" 2>/dev/null | head -1 | cut -d: -f2-)"
    if [ -n "$HITS" ]; then
      IFS=',' read -ra IDS <<< "$HITS"
      for id in "${IDS[@]}"; do
        id="$(echo "$id" | tr -d ' ')"
        [ -n "$id" ] || continue
        ENTRY_SCORES["$id"]=$(( ${ENTRY_SCORES["$id"]:-0} + 1 ))
      done
    fi
  done <<< "$PROMPT_KEYWORDS"

  # No matches — exit silently (zero overhead)
  [ ${#ENTRY_SCORES[@]} -eq 0 ] && exit 0

  # Sort by score, take top 3
  TOP_IDS="$(for id in "${!ENTRY_SCORES[@]}"; do
    echo "${ENTRY_SCORES[$id]} $id"
  done | sort -rn | head -3 | awk '{print $2}')"
fi

[ -z "$TOP_IDS" ] && exit 0

# --- Read matching entries and build recall context ---
RECALL_ITEMS=""
RECALL_COUNT=0

while IFS= read -r entry_id; do
  [ -z "$entry_id" ] && continue
  ENTRY_FILE="$REFLEX_DIR/entries/${entry_id}.json"
  [ -f "$ENTRY_FILE" ] || continue

  # Skip promoted entries (they're already in CLAUDE.md)
  if grep -q '"promoted".*true' "$ENTRY_FILE" 2>/dev/null; then
    continue
  fi

  # Skip entries with no resolution (unsolved errors aren't helpful for recall)
  RESOLUTION=""
  if command -v python3 &>/dev/null; then
    RESOLUTION="$(python3 -c "
import json, sys
try:
    d = json.load(open('$ENTRY_FILE'))
    print(d.get('resolution', ''))
except:
    pass
" 2>/dev/null)"
  else
    RESOLUTION="$(grep -oP '"resolution"\s*:\s*"[^"]+"' "$ENTRY_FILE" 2>/dev/null | sed 's/.*: *"//;s/"$//' || true)"
  fi

  # Include entries with resolutions (known fixes) or high occurrence count
  OCCURRENCES="$(grep -oP '"occurrences"\s*:\s*\d+' "$ENTRY_FILE" 2>/dev/null | grep -oP '\d+' || echo "1")"

  if [ -z "$RESOLUTION" ] && [ "${OCCURRENCES:-1}" -lt 2 ]; then
    continue
  fi

  # Extract trigger (the error/situation)
  TRIGGER=""
  if command -v python3 &>/dev/null; then
    TRIGGER="$(python3 -c "
import json, sys
try:
    d = json.load(open('$ENTRY_FILE'))
    print(d.get('trigger', '')[:200])
except:
    pass
" 2>/dev/null)"
  else
    TRIGGER="$(grep -oP '"trigger"\s*:\s*"[^"]{0,200}' "$ENTRY_FILE" 2>/dev/null | sed 's/.*: *"//' || true)"
  fi

  TYPE="$(grep -oP '"type"\s*:\s*"[^"]+"' "$ENTRY_FILE" 2>/dev/null | sed 's/.*: *"//;s/"$//' || echo "error")"
  KEYWORDS="$(grep -oP '"keywords"\s*:\s*"[^"]+"' "$ENTRY_FILE" 2>/dev/null | sed 's/.*: *"//;s/"$//' || true)"

  RECALL_ITEMS="${RECALL_ITEMS}
  [$entry_id] (${TYPE}, seen ${OCCURRENCES}x):
    Trigger: ${TRIGGER}
    Resolution: ${RESOLUTION:-UNRESOLVED — this error has occurred ${OCCURRENCES}x without a known fix}
    Keywords: ${KEYWORDS}"

  RECALL_COUNT=$((RECALL_COUNT + 1))
done <<< "$TOP_IDS"

# Nothing useful to recall — exit silently
[ "$RECALL_COUNT" -eq 0 ] && exit 0

# --- Update stats ---
STATS_FILE="$REFLEX_DIR/stats.json"
if [ -f "$STATS_FILE" ] && command -v python3 &>/dev/null; then
  python3 -c "
import json
try:
    with open('$STATS_FILE', 'r') as f:
        s = json.load(f)
    s['total_recalled'] = s.get('total_recalled', 0) + 1
    s['last_recall'] = '$(date +%Y-%m-%d)'
    with open('$STATS_FILE', 'w') as f:
        json.dump(s, f, indent=2)
except:
    pass
" 2>/dev/null || true
fi

# --- Also check if any matched entries should be promoted ---
# Run promote.sh in background (non-blocking)
if [ -x "$SCRIPT_DIR/promote.sh" ]; then
  bash "$SCRIPT_DIR/promote.sh" &>/dev/null &
fi

# --- Output recall context ---
cat << EOF
<reflexion-recall>
${RECALL_COUNT} relevant past learning(s) found:
${RECALL_ITEMS}

Apply known resolutions if they match the current situation.
If a resolution works, increment its occurrences count in the entry file.
If it doesn't apply, ignore it.
</reflexion-recall>
EOF
