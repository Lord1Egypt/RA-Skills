#!/bin/bash
# 创建停止标志脚本（用于测试）
# 用法: create-stop-flag.sh <sessionId> [reason]

SESSION_ID="$1"
REASON="${2:-User requested stop}"

if [ -z "$SESSION_ID" ]; then
    echo "Usage: $0 <sessionId> [reason]"
    exit 1
fi

FLAG_FILE="/tmp/agent-stop-${SESSION_ID}.flag"

cat > "$FLAG_FILE" << EOF
{
  "sessionId": "$SESSION_ID",
  "timestamp": $(date +%s000),
  "reason": "$REASON"
}
EOF

echo "Stop flag created for session: $SESSION_ID"
echo "File: $FLAG_FILE"
cat "$FLAG_FILE"
