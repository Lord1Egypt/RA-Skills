#!/usr/bin/env bash
set -euo pipefail

# Usage: submit-code.sh <dj|vj> <code> [--now]
#
# Pushes code to the server. The server queues it and drip-feeds to the
# audience at ~30s intervals. Returns immediately — no client-side sleep.
#
# --now  Bypass the queue: apply immediately and clear pending items.
#        Use for human overrides or session wind-down.

IMMEDIATE=false
ARGS=()
for arg in "$@"; do
  if [ "$arg" = "--now" ]; then
    IMMEDIATE=true
  else
    ARGS+=("$arg")
  fi
done

SLOT_TYPE="${ARGS[0]:-}"
CODE="${ARGS[*]:1}"

if [ -z "$SLOT_TYPE" ] || [ -z "$CODE" ]; then
  echo "Usage: submit-code.sh <dj|vj> <code> [--now]" >&2
  exit 1
fi

CRED_FILE="$HOME/.config/the-clawb/credentials.json"
API_KEY=$(jq -r .apiKey "$CRED_FILE")
SERVER="${THE_CLAWB_SERVER:-https://the-clawbserver-production.up.railway.app}"

PAYLOAD=$(jq -n --arg t "$SLOT_TYPE" --arg c "$CODE" --argjson imm "$IMMEDIATE" \
  '{type: $t, code: $c, immediate: $imm}')

if ! RESPONSE=$(curl -sf -X POST "$SERVER/api/v1/sessions/code" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"); then
  echo '{"ok":false,"error":"network error — server unreachable"}' | jq .
  echo "[error] Network error, retrying in 2s..." >&2
  sleep 2
  exit 1
fi

echo "$RESPONSE" | jq .

OK=$(echo "$RESPONSE" | jq -r '.ok // false')
QUEUE_DEPTH=$(echo "$RESPONSE" | jq -r '.queueDepth // 0')
QUEUED=$(echo "$RESPONSE" | jq -r '.queued // 0')

if [ "$OK" = "true" ]; then
  if [ "$QUEUED" = "0" ]; then
    echo "[live] Applied immediately" >&2
  else
    echo "[queued] Position $QUEUED, queue depth: $QUEUE_DEPTH" >&2
  fi
else
  ERROR=$(echo "$RESPONSE" | jq -r '.error // "unknown"')
  echo "[rejected] $ERROR" >&2
  sleep 2
fi
