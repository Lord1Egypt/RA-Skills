#!/bin/bash
# Invoke the triz_analysis MCP tool
# Usage: ./call_triz_analysis.sh <analysis_name> "<user_input>"

MCP_URL="https://qa-eureka-service.zhihuiya.com/eureka-rd-agent-mcp/rd-agent-mcp-triz-mind/mcp"

ANALYSIS_NAME="$1"
USER_INPUT="$2"

if [ -z "$ANALYSIS_NAME" ] || [ -z "$USER_INPUT" ]; then
    echo "Usage: ./call_triz_analysis.sh <analysis_name> <user_input>"
    exit 1
fi

curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  --data "$(jq -n \
    --arg analysis_name "$ANALYSIS_NAME" \
    --arg user_input "$USER_INPUT" \
    '{
      "jsonrpc": "2.0",
      "id": 1,
      "method": "tools/call",
      "params": {
        "name": "triz_analysis",
        "arguments": {
          "analysis_name": $analysis_name,
          "user_input": $user_input
        }
      }
    }')"
