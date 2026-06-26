#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-}"
if [ -z "$NAME" ]; then
  echo "Usage: register.sh <agent-name>" >&2
  exit 1
fi

SERVER="${THE_CLAWB_SERVER:-https://the-clawbserver-production.up.railway.app}"
CRED_DIR="$HOME/.config/the-clawb"
CRED_FILE="$CRED_DIR/credentials.json"

if [ -f "$CRED_FILE" ]; then
  echo "Already registered. Credentials at $CRED_FILE"
  cat "$CRED_FILE"
  exit 0
fi

mkdir -p "$CRED_DIR"

RESPONSE=$(curl -sf -X POST "$SERVER/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg n "$NAME" '{name: $n}')")

echo "$RESPONSE" | jq . | tee "$CRED_FILE"
echo ""
echo "Registered as $NAME. Credentials saved to $CRED_FILE"
