#!/bin/bash
# Save a memory entry
# Usage: ./save.sh "topic" "content" [tags...]
# Env: AGENT_MEMORY_DIR (default: ~/.agent-memory)
#      MEMORY_IMPORTANCE (default: normal) — low/normal/high/critical

set -e

TOPIC="${1:?Usage: $0 \"topic\" \"content\" [tags...]}"
CONTENT="${2:?Usage: $0 \"topic\" \"content\" [tags...]}"
shift 2
TAGS="$*"

IMPORTANCE="${MEMORY_IMPORTANCE:-normal}"
MEMORY_DIR="${AGENT_MEMORY_DIR:-$HOME/.agent-memory}"
YEAR=$(date -u +%Y)
MONTH=$(date -u +%m)
DAY=$(date -u +%d)

mkdir -p "$MEMORY_DIR/$YEAR/$MONTH"

node -e "
const entry = {
  ts: Date.now(),
  topic: process.argv[1],
  content: process.argv[2],
  tags: process.argv[3] ? process.argv[3].split(' ').filter(Boolean) : [],
  importance: process.argv[4] || 'normal'
};
process.stdout.write(JSON.stringify(entry) + '\n');
" "$TOPIC" "$CONTENT" "$TAGS" "$IMPORTANCE" >> "$MEMORY_DIR/$YEAR/$MONTH/$DAY.jsonl"

echo "✓ Memory saved: [$TOPIC] $(echo "$CONTENT" | head -c 80)"
