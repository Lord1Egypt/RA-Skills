#!/usr/bin/env bash
set -euo pipefail

base_url="${ZQCC_BASE_URL:-https://zqcc.mkstone.club}"
mcp_url="${base_url%/}/mcp/stream"
chat_url="${base_url%/}/api/v1/chat"

usage() {
  cat <<'EOF'
Usage:
  zqcc.sh tools-list
  zqcc.sh tools-call <tool-name> '<json-arguments>'
  zqcc.sh chat <session-id> <message>
  zqcc.sh config
  zqcc.sh health

Environment:
  ZQCC_APP_KEY   Required for tools-list, tools-call, chat, and config
  ZQCC_BASE_URL  Optional; defaults to https://zqcc.mkstone.club
EOF
}

require_app_key() {
  if [[ -z "${ZQCC_APP_KEY:-}" ]]; then
    printf 'ZQCC_APP_KEY is required. Register at https://zqcc.mkstone.club\n' >&2
    exit 2
  fi
}

post_json() {
  local url="$1"
  local body="$2"

  curl --fail-with-body --silent --show-error \
    --connect-timeout 15 \
    --max-time 300 \
    -X POST "$url" \
    -H "Authorization: Bearer ${ZQCC_APP_KEY}" \
    -H 'Content-Type: application/json' \
    --data "$body"
}

command="${1:-}"
case "$command" in
  tools-list)
    require_app_key
    post_json "$mcp_url" '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | jq .
    ;;
  tools-call)
    require_app_key
    tool_name="${2:-}"
    arguments="${3:-}"
    if [[ -z "$tool_name" || -z "$arguments" ]]; then
      usage >&2
      exit 2
    fi
    if ! jq -e 'type == "object"' >/dev/null 2>&1 <<<"$arguments"; then
      printf 'Tool arguments must be a valid JSON object.\n' >&2
      exit 2
    fi
    body="$(jq -cn --arg name "$tool_name" --argjson arguments "$arguments" \
      '{jsonrpc:"2.0",id:1,method:"tools/call",params:{name:$name,arguments:$arguments}}')"
    post_json "$mcp_url" "$body" | jq .
    ;;
  chat)
    require_app_key
    session_id="${2:-}"
    shift 2 2>/dev/null || true
    message="$*"
    if [[ -z "$session_id" || -z "$message" ]]; then
      usage >&2
      exit 2
    fi
    body="$(jq -cn --arg sessionId "$session_id" --arg message "$message" \
      '{sessionId:$sessionId,message:$message}')"
    post_json "$chat_url" "$body" | jq .
    ;;
  config)
    require_app_key
    jq -n --arg url "$mcp_url" --arg authorization "Bearer ${ZQCC_APP_KEY}" \
      '{mcpServers:{zqcc:{url:$url,headers:{Authorization:$authorization}}}}'
    ;;
  health)
    curl --fail-with-body --silent --show-error \
      --connect-timeout 15 \
      --max-time 30 \
      "${base_url%/}/api/health" | jq .
    ;;
  -h|--help|help|'')
    usage
    ;;
  *)
    printf 'Unknown command: %s\n' "$command" >&2
    usage >&2
    exit 2
    ;;
esac
