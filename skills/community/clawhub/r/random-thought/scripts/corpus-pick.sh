#!/usr/bin/env bash
# corpus-pick.sh — Select a random file from the workspace corpus.
# Respects freshness gate: won't re-select files visited within N days.
#
# Usage: bash corpus-pick.sh [workspace_root] [config_path]
#   workspace_root  — directory to scan (default: current directory)
#   config_path     — path to random-thought.config.json (default: workspace_root/random-thought.config.json)
#
# Outputs: absolute path of selected file

set -uo pipefail

WORKSPACE="${1:-$(pwd)}"
WORKSPACE=$(cd "$WORKSPACE" && pwd)  # resolve to absolute
CONFIG="${2:-$WORKSPACE/random-thought.config.json}"

# ── Read config (with jq-free python fallback) ───────────────────────
read_config() {
  local key="$1" default="$2"
  if [ -f "$CONFIG" ]; then
    python3 -c "
import json, functools, operator
c = json.load(open('$CONFIG'))
keys = '$key'.split('.')
try:
    val = functools.reduce(operator.getitem, keys, c)
    print(val if not isinstance(val, bool) else str(val).lower())
except (KeyError, TypeError):
    print('$default')
" 2>/dev/null || echo "$default"
  else
    echo "$default"
  fi
}

FRESHNESS_ENABLED=$(read_config "freshness.enabled" "true")
FRESHNESS_DAYS=$(read_config "freshness.days" "7")
HISTORY_FILE=$(read_config "freshness.historyFile" ".random-thought-history")
HISTORY_PATH="$WORKSPACE/$HISTORY_FILE"

# ── Build candidate list ─────────────────────────────────────────────
CANDIDATES=$(find "$WORKSPACE" \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/.git-*/*" \
  -not -path "*/.next/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/venv/*" \
  -not -path "*/__pycache__/*" \
  -not -name "*.png" -not -name "*.jpg" -not -name "*.gif" -not -name "*.webp" \
  -not -name "*.mp3" -not -name "*.ogg" -not -name "*.m4a" -not -name "*.wav" \
  -not -name "*.mp4" -not -name "*.mov" -not -name "*.avi" \
  -not -name "*.pdf" -not -name "*.zip" -not -name "*.tar" -not -name "*.gz" \
  -not -name "*.env" -not -name "*.pem" -not -name "*.key" \
  -not -name "package-lock.json" -not -name "yarn.lock" -not -name "pnpm-lock.yaml" \
  -not -name "*.lock" \
  -not -name ".random-thought-history" \
  -not -name ".DS_Store" \
  -type f \
  -size +100c -size -500k \
  2>/dev/null) || true

if [ -z "$CANDIDATES" ]; then
  echo "ERROR: No candidate files found in $WORKSPACE" >&2
  exit 1
fi

# ── Apply freshness gate ─────────────────────────────────────────────
if [ "$FRESHNESS_ENABLED" = "true" ] && [ -f "$HISTORY_PATH" ]; then
  CUTOFF=$(date -v-${FRESHNESS_DAYS}d +%s 2>/dev/null || date -d "${FRESHNESS_DAYS} days ago" +%s 2>/dev/null || echo "0")

  FILTERED=$(python3 -c "
import sys

cutoff = int('$CUTOFF')
history_path = '$HISTORY_PATH'

# Load recently visited files
recent = set()
with open(history_path) as f:
    for line in f:
        parts = line.strip().split('\t', 1)
        if len(parts) == 2:
            try:
                ts = int(parts[0])
                if ts >= cutoff:
                    recent.add(parts[1])
            except ValueError:
                continue

# Filter candidates
for line in sys.stdin:
    path = line.strip()
    if path and path not in recent:
        print(path)
" <<< "$CANDIDATES" 2>/dev/null) || true

  if [ -n "$FILTERED" ]; then
    CANDIDATES="$FILTERED"
  fi
  # If all filtered out, fall back to full list
fi

# ── Pick random ──────────────────────────────────────────────────────
SELECTED=$(echo "$CANDIDATES" | grep -v '^$' | sort -R | head -1)

if [ -z "$SELECTED" ]; then
  echo "ERROR: No file selected" >&2
  exit 1
fi

# ── Record visit ─────────────────────────────────────────────────────
if [ "$FRESHNESS_ENABLED" = "true" ]; then
  echo "$(date +%s)	$SELECTED" >> "$HISTORY_PATH"
fi

echo "$SELECTED"
