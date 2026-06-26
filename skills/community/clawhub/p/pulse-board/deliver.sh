#!/usr/bin/env bash
# Pulse Board — deliver.sh
# Sends a composed digest to the configured channel.
# Called by digest-agent.sh — not meant for direct use.
# Writes delivered message to last-delivered.md. Never touches last-digest.md.
# No sudo. No root.

set -euo pipefail

PULSE_HOME="${PULSE_HOME:-$HOME/.pulse-board}"
CONFIG_FILE="$PULSE_HOME/config/pulse.yaml"

[[ -f "$HOME/.openclaw/shared/secrets/openclaw-secrets.env" ]] && \
  { set +u; source "$HOME/.openclaw/shared/secrets/openclaw-secrets.env"; set -u; }

# ── Helpers ───────────────────────────────────────────────────────────────────
g() { printf "\033[0;32m%s\033[0m\n" "$*" >&2; }
y() { printf "\033[0;33m%s\033[0m\n" "$*" >&2; }
r() { printf "\033[0;31m%s\033[0m\n" "$*" >&2; }

cfg()       { grep -E "^[[:space:]]*${1}[[:space:]]*:" "$CONFIG_FILE" 2>/dev/null | head -1 | sed 's/.*:[[:space:]]*//' | sed "s/^[\"']\(.*\)[\"']$/\1/"; }
cfg_under() { awk "/^[[:space:]]*${1}:/{f=1} f && /^[[:space:]]*${2}:/{ sub(/.*:[[:space:]]*/,\"\"); gsub(/[\"' ]/,\"\"); print; exit }" "$CONFIG_FILE" 2>/dev/null; }
expand()    { echo "${1/#\~/$HOME}"; }
json_str()  { python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$1"; }

# ── Read message ──────────────────────────────────────────────────────────────
MESSAGE_FILE="${1:-}"
[[ -z "$MESSAGE_FILE" || ! -f "$MESSAGE_FILE" ]] && { r "deliver.sh: message file required."; exit 1; }
MESSAGE="$(cat "$MESSAGE_FILE")"
[[ -z "$MESSAGE" ]] && { y "deliver.sh: empty message — skipping."; exit 0; }

# ── Audit trail ───────────────────────────────────────────────────────────────
LAST_DELIVERED="$(expand "$PULSE_HOME/logs/last-delivered.md")"
mkdir -p "$(dirname "$LAST_DELIVERED")"
echo "$MESSAGE" > "$LAST_DELIVERED"

# ── Deliver ───────────────────────────────────────────────────────────────────
CHANNEL="$(cfg 'channel')"; CHANNEL="${CHANNEL:-log}"
TEXT="$(json_str "$MESSAGE")"

case "$CHANNEL" in
  telegram)
    BOT_TOKEN="$(cfg_under 'telegram' 'bot_token')"
    [[ -z "$BOT_TOKEN" ]] && BOT_TOKEN="${PULSE_TELEGRAM_BOT_TOKEN:-}"
    CHAT_ID="$(cfg_under 'telegram' 'chat_id')"
    THREAD_ID="$(cfg_under 'telegram' 'thread_id')"
    [[ -z "$BOT_TOKEN" ]] && { r "Telegram: bot_token not set."; exit 1; }
    [[ -z "$CHAT_ID"   ]] && { r "Telegram: chat_id not set.";   exit 1; }
    PAYLOAD="{\"chat_id\":\"$CHAT_ID\",\"text\":$TEXT,\"parse_mode\":\"Markdown\"}"
    [[ -n "$THREAD_ID" ]] && \
      PAYLOAD="{\"chat_id\":\"$CHAT_ID\",\"message_thread_id\":$THREAD_ID,\"text\":$TEXT,\"parse_mode\":\"Markdown\"}"
    curl -sf -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
      -H "Content-Type: application/json" -d "$PAYLOAD" --max-time 15 > /dev/null \
      && g "✓ Delivered to Telegram" || { r "Telegram delivery failed."; exit 1; }
    ;;
  discord)
    WEBHOOK="$(cfg_under 'discord' 'webhook_url')"
    [[ -z "$WEBHOOK" ]] && WEBHOOK="${PULSE_DISCORD_WEBHOOK_URL:-}"
    [[ -z "$WEBHOOK" ]] && { r "Discord: webhook_url not set."; exit 1; }
    curl -sf -X POST "$WEBHOOK" \
      -H "Content-Type: application/json" \
      -d "{\"content\":$TEXT}" --max-time 15 > /dev/null \
      && g "✓ Delivered to Discord" || { r "Discord delivery failed."; exit 1; }
    ;;
  log|none)
    g "✓ Digest written to last-delivered.md"
    ;;
  *)
    y "Unknown channel '$CHANNEL' — saved to last-delivered.md only."
    ;;
esac
