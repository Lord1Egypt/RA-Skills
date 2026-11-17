#!/usr/bin/env bash
# telethon.sh: thin curl wrapper over a running docker-telethon-plus instance.
#
# Drives the JSON HTTP API for the common read/send/delete operations so you
# don't hand-assemble the bearer header + JSON body every time. Talks to a
# REAL Telegram user account. Only point it at an instance you own and only
# for actions that account is authorized to take.
#
# Env:
#   TELETHON_PLUS_URL   base URL (default http://localhost:8080)
#   TELETHON_AUTH_KEY   bearer token (only if the server was started with it)
#
# Usage:
#   telethon.sh health
#   telethon.sh me
#   telethon.sh dialogs [limit]
#   telethon.sh read   <chat> [limit] [search]
#   telethon.sh send   <chat> <text...>
#   telethon.sh sendfile <chat> <file_url> [caption...]
#   telethon.sh delete <chat> <id> [id...]
#   telethon.sh risk
#
# Chat refs: @username | +phone | https://t.me/x | 123456789 | -100123... | me
set -euo pipefail

URL="${TELETHON_PLUS_URL:-http://localhost:8080}"

auth=()
if [[ -n "${TELETHON_AUTH_KEY:-}" ]]; then
  auth=(-H "Authorization: Bearer ${TELETHON_AUTH_KEY}")
fi

die() {
  echo "error: $*" >&2
  exit 1
}

# JSON-encode a single string via jq (handles quotes/newlines/unicode).
jstr() { jq -Rn --arg s "$1" '$s'; }

cmd="${1:-}"
[[ -n "$cmd" ]] || die "usage: telethon.sh <health|me|dialogs|read|send|sendfile|delete|risk> ..."
shift || true

case "$cmd" in
  health)
    curl -fsS "${auth[@]}" "$URL/healthz"
    ;;
  me)
    curl -fsS "${auth[@]}" "$URL/api/me"
    ;;
  risk)
    curl -fsS "${auth[@]}" "$URL/api/account/health"
    ;;
  dialogs)
    limit="${1:-20}"
    curl -fsS "${auth[@]}" "$URL/api/dialogs?limit=${limit}"
    ;;
  read)
    chat="${1:-}"; [[ -n "$chat" ]] || die "read: <chat> required"
    limit="${2:-20}"
    q="chat=$(jq -rn --arg c "$chat" '$c|@uri')&limit=${limit}"
    if [[ -n "${3:-}" ]]; then
      q+="&search=$(jq -rn --arg s "$3" '$s|@uri')"
    fi
    curl -fsS "${auth[@]}" "$URL/api/messages?${q}"
    ;;
  send)
    chat="${1:-}"; [[ -n "$chat" ]] || die "send: <chat> <text...> required"
    shift
    [[ $# -gt 0 ]] || die "send: text required"
    body=$(jq -n --arg chat "$chat" --arg text "$*" '{chat:$chat, text:$text}')
    curl -fsS -X POST "${auth[@]}" -H 'Content-Type: application/json' \
      -d "$body" "$URL/api/messages"
    ;;
  sendfile)
    chat="${1:-}"; url="${2:-}"
    [[ -n "$chat" && -n "$url" ]] || die "sendfile: <chat> <file_url> [caption...] required"
    shift 2
    caption="$*"
    body=$(jq -n --arg chat "$chat" --arg url "$url" --arg cap "$caption" \
      '{chat:$chat, file_url:$url} + (if $cap == "" then {} else {text:$cap} end)')
    curl -fsS -X POST "${auth[@]}" -H 'Content-Type: application/json' \
      -d "$body" "$URL/api/messages"
    ;;
  delete)
    chat="${1:-}"; [[ -n "$chat" ]] || die "delete: <chat> <id> [id...] required"
    shift
    [[ $# -gt 0 ]] || die "delete: at least one message id required"
    ids=$(printf '%s\n' "$@" | jq -R 'tonumber' | jq -s '.')
    body=$(jq -n --arg chat "$chat" --argjson ids "$ids" '{chat:$chat, message_ids:$ids}')
    curl -fsS -X DELETE "${auth[@]}" -H 'Content-Type: application/json' \
      -d "$body" "$URL/api/messages"
    ;;
  *)
    die "unknown command: $cmd"
    ;;
esac
echo
