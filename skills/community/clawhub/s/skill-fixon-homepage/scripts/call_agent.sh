#!/bin/bash
# Agent 调用包装脚本

MESSAGE="$1"
SESSION_ID="$2"
AGENT_ID="${3:-main}"
GATEWAY_TOKEN="$4"

export OPENCLAW_GATEWAY_TOKEN="$GATEWAY_TOKEN"

/Users/yaoyi/.nvm/versions/node/v22.19.0/bin/openclaw agent \
    --agent "$AGENT_ID" \
    --session-id "$SESSION_ID" \
    --message "$MESSAGE" \
    --json
