#!/bin/bash
# mcp-call.sh — Helper to call MCP travel servers
# Usage: mcp-call.sh <provider> <tool> '<json_args>'
# Example: mcp-call.sh kiwi search-flight '{"flyFrom":"Madrid","flyTo":"Rome","departureDate":"10/04/2026","sort":"price","curr":"EUR"}'

set -euo pipefail

PROVIDER="${1:-}"
TOOL="${2:-}"
ARGS="${3:-{}}"

declare -A ENDPOINTS=(
  [kiwi]="https://mcp.kiwi.com"
  [skiplagged]="https://mcp.skiplagged.com/mcp"
  [trivago]="https://mcp.trivago.com/mcp"
  [ferryhopper]="https://mcp.ferryhopper.com/mcp"
)

if [[ -z "$PROVIDER" || -z "$TOOL" ]]; then
  echo "Usage: mcp-call.sh <kiwi|skiplagged|trivago|ferryhopper> <tool> '<json_args>'"
  exit 1
fi

URL="${ENDPOINTS[$PROVIDER]:-}"
if [[ -z "$URL" ]]; then
  echo "Unknown provider: $PROVIDER"
  echo "Available: ${!ENDPOINTS[*]}"
  exit 1
fi

HEADER_FILE=$(mktemp)
trap "rm -f $HEADER_FILE" EXIT

# Initialize session
curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -D "$HEADER_FILE" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"openclaw-travel","version":"1.0"}}}' > /dev/null

# Extract session ID if present
SESSION=$(grep -i "mcp-session-id:" "$HEADER_FILE" 2>/dev/null | awk '{print $2}' | tr -d '\r' || true)

# Call tool
SESSION_ARGS=()
if [[ -n "$SESSION" ]]; then
  SESSION_ARGS=(-H "Mcp-Session-Id: ${SESSION}")
fi

curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  "${SESSION_ARGS[@]}" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/call\",\"params\":{\"name\":\"${TOOL}\",\"arguments\":${ARGS}}}" \
  | sed -n 's/^data: //p'
