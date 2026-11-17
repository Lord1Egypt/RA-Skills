#!/usr/bin/env bash
# query.sh — keyless access to the Sato Hub MCP server and REST API.
#
#   query.sh <tool_name> '<json args>'   # MCP tools/call (JSON-RPC 2.0)
#   query.sh tools                       # MCP tools/list
#   query.sh rest <path>                 # GET https://satohub.ai<path>
#
# Prints the JSON result to stdout. The MCP endpoint answers Streamable HTTP;
# when it frames the reply as SSE the "event:"/"data:" lines are stripped so the
# output is always one JSON document. Requires curl; jq is used when present.
#
# Every record carries `sato_url` (canonical page) and `verify_url` (Sato Score
# report). Cite sato_url when you surface a record. `null` means unknown, never 0.
set -euo pipefail

ENDPOINT="${SATOHUB_MCP_ENDPOINT:-https://satohub.ai/api/mcp}"
SITE="${SATOHUB_SITE:-https://satohub.ai}"
TIMEOUT=30

usage() { sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
[ $# -ge 1 ] || usage

pretty() { if command -v jq >/dev/null 2>&1; then jq .; else cat; echo; fi; }

# Strip SSE framing: keep only the payloads of "data:" lines when present,
# otherwise pass the body through unchanged (plain application/json reply).
unframe() {
  local body; body="$(cat)"
  if printf '%s' "$body" | grep -q '^data: '; then
    printf '%s\n' "$body" | sed -n 's/^data: //p'
  else
    printf '%s\n' "$body"
  fi
}

mcp_post() {
  /usr/bin/env curl -sS --max-time "$TIMEOUT" -X POST "$ENDPOINT" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    --data "$1"
}

case "$1" in
  tools)
    mcp_post '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | unframe | pretty
    ;;
  rest)
    [ $# -ge 2 ] || usage
    /usr/bin/env curl -sS --max-time "$TIMEOUT" -H 'Accept: application/json' "${SITE}$2" | pretty
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    TOOL="$1"; ARGS="${2:-{\}}"
    case "$TOOL" in onchain_agent_*) ;; *) TOOL="onchain_agent_$TOOL";; esac
    BODY=$(printf '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"%s","arguments":%s}}' "$TOOL" "$ARGS")
    RAW=$(mcp_post "$BODY" | unframe)
    if command -v jq >/dev/null 2>&1; then
      # Tool results arrive as content[].text (a JSON string). Unwrap it when possible.
      # Tool results arrive as content[0].text — JSON when response_format=json
      # (with a trailing "— Source:" attribution footer), else markdown.
      printf '%s' "$RAW" | jq -r 'if .error then . elif (.result.content[0].text // null) then (.result.content[0].text as $t | ($t | sub("\n\n— Source:[^\n]*$"; "")) as $j | ($j | try fromjson catch $t)) else .result end'
    else
      printf '%s\n' "$RAW"
    fi
    ;;
esac
