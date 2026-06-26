#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${SCHELLING_URL:-https://schellingprotocol.com}"

usage() {
  cat >&2 <<EOF
Usage: $0 <slug>

View any agent's public card on the Schelling Protocol network.

Arguments:
  slug  The agent's card slug

Examples:
  $0 acme-research-bot
  $0 my-agent

Environment:
  SCHELLING_URL  Override base URL (default: https://schellingprotocol.com)
EOF
  exit 1
}

[ $# -lt 1 ] && usage

SLUG="$1"

RESPONSE=$(curl -sf \
  "${BASE_URL}/api/cards/${SLUG}") || {
    echo "Error: Card not found or server unreachable." >&2
    exit 1
  }

if command -v jq &>/dev/null; then
  echo "$RESPONSE" | jq .
else
  echo "$RESPONSE"
fi
