#!/usr/bin/env bash
# freshness-gate.sh — Manage the file visit history for Random Thought.
#
# Usage:
#   bash freshness-gate.sh check <file> [config_path]   — exit 0 if OK to visit, 1 if recent
#   bash freshness-gate.sh record <file> [config_path]   — record a file visit
#   bash freshness-gate.sh prune [config_path]            — remove entries older than window
#   bash freshness-gate.sh stats [config_path]            — show history statistics
#
# Config is read from random-thought.config.json if present.

set -euo pipefail

ACTION="${1:-}"
FILE="${2:-}"
CONFIG="${3:-random-thought.config.json}"

# ── Read config ──────────────────────────────────────────────────────
if [ -f "$CONFIG" ]; then
  DAYS=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(c.get('freshness',{}).get('days',7))" 2>/dev/null || echo "7")
  HISTORY_FILE=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(c.get('freshness',{}).get('historyFile','.random-thought-history'))" 2>/dev/null || echo ".random-thought-history")
else
  DAYS=7
  HISTORY_FILE=".random-thought-history"
fi

CUTOFF=$(date -v-${DAYS}d +%s 2>/dev/null || date -d "${DAYS} days ago" +%s 2>/dev/null || echo "0")

case "$ACTION" in
  check)
    if [ -z "$FILE" ]; then
      echo "Usage: freshness-gate.sh check <file>" >&2
      exit 2
    fi
    ABS_FILE=$(cd "$(dirname "$FILE")" 2>/dev/null && echo "$(pwd)/$(basename "$FILE")" || echo "$FILE")
    if [ ! -f "$HISTORY_FILE" ]; then
      exit 0  # No history = fresh
    fi
    # Check if file was visited within the window
    FOUND=$(python3 -c "
cutoff = int('$CUTOFF')
target = '$ABS_FILE'
with open('$HISTORY_FILE') as f:
    for line in f:
        parts = line.strip().split('\t', 1)
        if len(parts) == 2:
            ts, path = int(parts[0]), parts[1]
            if ts >= cutoff and path == target:
                print('found')
                break
" 2>/dev/null || true)
    if [ "$FOUND" = "found" ]; then
      exit 1  # Recently visited
    fi
    exit 0  # Fresh
    ;;

  record)
    if [ -z "$FILE" ]; then
      echo "Usage: freshness-gate.sh record <file>" >&2
      exit 2
    fi
    ABS_FILE=$(cd "$(dirname "$FILE")" 2>/dev/null && echo "$(pwd)/$(basename "$FILE")" || echo "$FILE")
    echo "$(date +%s)	$ABS_FILE" >> "$HISTORY_FILE"
    echo "Recorded: $ABS_FILE"
    ;;

  prune)
    if [ ! -f "$HISTORY_FILE" ]; then
      echo "No history file to prune."
      exit 0
    fi
    BEFORE=$(wc -l < "$HISTORY_FILE" | tr -d ' ')
    python3 -c "
cutoff = int('$CUTOFF')
lines = []
with open('$HISTORY_FILE') as f:
    for line in f:
        parts = line.strip().split('\t', 1)
        if len(parts) == 2 and int(parts[0]) >= cutoff:
            lines.append(line)
with open('$HISTORY_FILE', 'w') as f:
    f.writelines(lines)
print(f'Kept {len(lines)} entries')
" 2>/dev/null
    AFTER=$(wc -l < "$HISTORY_FILE" | tr -d ' ')
    echo "Pruned: $BEFORE → $AFTER entries"
    ;;

  stats)
    if [ ! -f "$HISTORY_FILE" ]; then
      echo "No history file found."
      exit 0
    fi
    TOTAL=$(wc -l < "$HISTORY_FILE" | tr -d ' ')
    ACTIVE=$(python3 -c "
cutoff = int('$CUTOFF')
count = 0
with open('$HISTORY_FILE') as f:
    for line in f:
        parts = line.strip().split('\t', 1)
        if len(parts) == 2 and int(parts[0]) >= cutoff:
            count += 1
print(count)
" 2>/dev/null || echo "?")
    echo "History: $TOTAL total entries, $ACTIVE within ${DAYS}-day window"
    ;;

  *)
    echo "Usage: freshness-gate.sh {check|record|prune|stats} [file] [config_path]" >&2
    exit 2
    ;;
esac
