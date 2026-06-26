#!/usr/bin/env bash
# Generate a 5-question SAT vocabulary quiz against the Vocab Voyage MCP
# server using a raw JSON-RPC tools/call envelope.
#
# Usage:
#   ./curl-quiz.sh                 # anonymous
#   VV_MCP_TOKEN=vv_mcp_xxx ./curl-quiz.sh   # authenticated

set -euo pipefail

ENDPOINT="https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server"
AUTH_HEADER=()
if [[ -n "${VV_MCP_TOKEN:-}" ]]; then
  AUTH_HEADER=(-H "Authorization: Bearer ${VV_MCP_TOKEN}")
fi

curl -sS -X POST "$ENDPOINT" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  "${AUTH_HEADER[@]}" \
  --data '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "generate_quiz",
      "arguments": { "test_family": "sat", "count": 5 }
    }
  }' | jq .