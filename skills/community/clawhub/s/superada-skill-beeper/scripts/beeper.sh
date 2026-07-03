#!/usr/bin/env bash
# Beeper Desktop API CLI
# Usage: beeper.sh <command> [args]

set -euo pipefail

BEEPER_API_BASE="${BEEPER_API_BASE:-http://127.0.0.1:23373}"
BEEPER_CONFIG_DIR="${BEEPER_CONFIG_DIR:-$HOME/.config/beeper}"
BEEPER_API_KEY="${BEEPER_API_KEY:-}"
BEEPER_SSH_HOST="${BEEPER_SSH_HOST:-}"

if [[ -z "$BEEPER_API_KEY" && -f "$BEEPER_CONFIG_DIR/api-key" ]]; then
  BEEPER_API_KEY="$(tr -d '\n' < "$BEEPER_CONFIG_DIR/api-key")"
elif [[ -z "$BEEPER_API_KEY" && -f "$BEEPER_CONFIG_DIR/config.json" ]]; then
  BEEPER_API_KEY="$(jq -r '.api_key // .apiKey // empty' "$BEEPER_CONFIG_DIR/config.json")"
fi

if [[ -z "$BEEPER_API_KEY" ]]; then
  echo "No Beeper API key found. Set BEEPER_API_KEY or write it to $BEEPER_CONFIG_DIR/api-key." >&2
  exit 1
fi

urlencode() {
  jq -sRr @uri <<<"$1"
}

beeper_api() {
  local endpoint="$1"
  local method="${2:-GET}"
  local data="${3:-}"
  local url="${BEEPER_API_BASE}${endpoint}"

  if [[ -n "$BEEPER_SSH_HOST" ]]; then
    if [[ "$method" == "POST" ]]; then
      ssh "$BEEPER_SSH_HOST" "curl -sS --max-time 30 '$url' -X POST -H 'Authorization: Bearer $BEEPER_API_KEY' -H 'Content-Type: application/json' --data-binary @-" <<<"$data"
    else
      ssh "$BEEPER_SSH_HOST" "curl -sS --max-time 20 -H 'Authorization: Bearer $BEEPER_API_KEY' '$url'"
    fi
  else
    if [[ "$method" == "POST" ]]; then
      curl -sS --max-time 30 "$url" -X POST -H "Authorization: Bearer $BEEPER_API_KEY" -H "Content-Type: application/json" --data-binary "$data"
    else
      curl -sS --max-time 20 -H "Authorization: Bearer $BEEPER_API_KEY" "$url"
    fi
  fi
}

case "${1:-help}" in
  test)
    result="$(beeper_api "/v1/accounts" | jq -r 'if type == "array" then length elif has("accounts") then (.accounts | length) else (.message // "unknown") end' 2>/dev/null || true)"
    if [[ "$result" =~ ^[0-9]+$ ]]; then
      echo "Connected. Found $result accounts."
    else
      echo "API error: ${result:-unknown}" >&2
      exit 1
    fi
    ;;

  accounts)
    beeper_api "/v1/accounts" | jq -r '(if type == "array" then . else .accounts end)[] | "• \(.network // .service // "?"): \(.user.displayText // .user.fullName // .name // .id)"'
    ;;

  chats)
    limit="${2:-20}"
    beeper_api "/v1/chats?limit=$limit" | jq -r '.items[] | "• [\(.network // .account.network // "?")] \(.title // .name // .participants.items[0].fullName // .id) - \(.id)"'
    ;;

  messages)
    chat_id="${2:-}"
    limit="${3:-50}"
    if [[ -z "$chat_id" ]]; then
      echo "Usage: beeper.sh messages <chatID> [limit]" >&2
      exit 1
    fi
    encoded_chat_id="$(urlencode "$chat_id")"
    beeper_api "/v1/chats/$encoded_chat_id/messages?limit=$limit" | jq -r '.items[] | "[\(.createdAt // .timestamp // "?")] \(.sender.displayName // .sender.name // .sender.id // "?"): \((.text // .body // "")[:500])"'
    ;;

  search)
    query="${2:-}"
    if [[ -z "$query" ]]; then
      echo "Usage: beeper.sh search <query>" >&2
      exit 1
    fi
    beeper_api "/v1/messages/search?query=$(urlencode "$query")" | jq -r '.items[:20][] | "[\(.chat.title // .chatTitle // "?")] \(.sender.displayName // .sender.name // "?"): \((.text // .body // "")[:220])"'
    ;;

  raw)
    endpoint="${2:-}"
    method="${3:-GET}"
    data="${4:-}"
    if [[ -z "$endpoint" ]]; then
      echo "Usage: beeper.sh raw /v1/path [GET|POST] [json]" >&2
      exit 1
    fi
    beeper_api "$endpoint" "$method" "$data"
    ;;

  *)
    cat <<'EOF'
Beeper CLI

Commands:
  test                  Test API connection
  accounts              List connected accounts
  chats [limit]         List recent chats
  messages <id> [n]     Get messages from a chat
  search <query>        Search messages
  raw /v1/path [method] [json]
                        Call a raw Beeper API path

Environment:
  BEEPER_API_BASE       Default: http://127.0.0.1:23373
  BEEPER_API_KEY        Beeper Desktop API key
  BEEPER_CONFIG_DIR     Default: ~/.config/beeper
  BEEPER_SSH_HOST       Optional user@host for remote curl over SSH
EOF
    ;;
esac
