#!/bin/bash
# Create a full conversation snapshot on demand
# Usage: ./save_full_snapshot.sh [optional-topic-name]

# 加载配置
CONFIG_FILE="$(dirname "$0")/../config"
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
fi

# 默认路径
SESSION_DIR="${SESSION_DIR:-/root/.openclaw/agents/main/sessions}"
VAULT_DIR="${VAULT_DIR:-$HOME/Documents/Obsidian/Clawd Markdowns}"

SESSION_FILE=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1)

if [[ ! -f "$SESSION_FILE" ]]; then
    echo "No session file found"
    exit 1
fi

TIMESTAMP=$(date +"%Y-%m-%d-%H%M")
TOPIC="${1:-full-conversation}"
SNAPSHOT_FILE="$VAULT_DIR/$TIMESTAMP-$TOPIC.md"

# Estimate tokens
CHARS=$(wc -c < "$SESSION_FILE")
TOKENS=$((CHARS / 4))

cat > "$SNAPSHOT_FILE" <<EOF
# Full Conversation Snapshot - $TOPIC

**Saved**: $(date '+%Y-%m-%d %H:%M %Z')
**Token estimate**: ${TOKENS}k/1,000,000 ($(( (TOKENS * 100) / 1000000 ))%)
**Session file**: $(basename "$SESSION_FILE")

---

EOF

# Parse JSONL to markdown (Obsidian chat format - FIXED)
cat "$SESSION_FILE" | while IFS= read -r line; do
    echo "$line" | jq -r -f /root/clawd/format_message_v2.jq.txt 2>/dev/null
done >> "$SNAPSHOT_FILE"

echo "✅ Saved full snapshot: $SNAPSHOT_FILE"
