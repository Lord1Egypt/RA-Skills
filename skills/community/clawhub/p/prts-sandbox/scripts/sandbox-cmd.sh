#!/bin/bash
# scripts/sandbox-cmd.sh
# Wrapper for PRTS Sandbox API

API_URL="http://protocol-spaces-api:3000"
ACTION=$1
shift

call_api() {
  local method=$1
  local endpoint=$2
  local extra_args=("${@:3}")

  local response
  response=$(curl -s -X "$method" "$API_URL$endpoint" "${extra_args[@]}" 2>&1)
  local curl_exit=$?

  if [ $curl_exit -ne 0 ]; then
    echo "{\"success\":false,\"error\":\"Cannot reach API ($curl_exit): $response\"}"
    return 1
  fi

  echo "$response"
}

case "$ACTION" in
  status)
    result=$(call_api GET /is_sandbox_start) || { echo "false"; exit 1; }
    echo "$result" | jq -r '.is_running'
    ;;

  start)
    call_api POST /start | jq .
    ;;

  stop)
    call_api POST /stop | jq .
    ;;

  reset)
    call_api POST /reset | jq .
    ;;

  exec)
    if [ $# -eq 0 ]; then
      echo '{"success":false,"error":"No command provided"}'
      exit 1
    fi

    JSON_CMD=$(jq -nc --args '$ARGS.positional' -- "$@")

    response=$(call_api POST /execute \
      -H "Content-Type: application/json" \
      -d "{\"cmd\":$JSON_CMD}")
    curl_ok=$?

    # ✅ แก้บัค: เช็ค success flag ก่อน แล้วค่อย print output หรือ error
    success=$(echo "$response" | jq -r '.success')

    if [ "$success" = "true" ]; then
      echo "$response" | jq -r '.output'
    else
      echo "$response" | jq -r '.error' >&2
      exit 1
    fi
    ;;

  *)
    echo "Usage: $0 {status|start|stop|reset|exec <command>}"
    exit 1
    ;;
esac
