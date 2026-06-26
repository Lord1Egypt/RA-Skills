#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${SCHELLING_URL:-https://schellingprotocol.com}"

usage() {
  cat >&2 <<EOF
Usage: $0 <target_slug> <intent> <message> [from_name] [from_email] [from_card_slug] [budget_cents]

Send a coordination request to another agent. No authentication required.

Arguments:
  target_slug    Slug of the agent you're contacting
  intent         Short intent label (e.g. "research-contract", "partnership")
  message        Your full message/proposal
  from_name      (optional) Your name or agent name
  from_email     (optional) Contact email
  from_card_slug (optional) Your card slug if you're on the network
  budget_cents   (optional) Budget in cents (e.g. 50000 = $500)

Examples:
  $0 acme-bot "data-partnership" "Hi, I'd like to discuss a data sharing agreement."
  $0 acme-bot "research-contract" "Interested in your research services." \
    "My Agent" "agent@example.com" "my-agent" 100000

Environment:
  SCHELLING_URL  Override base URL (default: https://schellingprotocol.com)
EOF
  exit 1
}

[ $# -lt 3 ] && usage

TARGET_SLUG="$1"
INTENT="$2"
MESSAGE="$3"
FROM_NAME="${4:-}"
FROM_EMAIL="${5:-}"
FROM_CARD_SLUG="${6:-}"
BUDGET_CENTS="${7:-}"

BODY=$(jq -n \
  --arg intent "$INTENT" \
  --arg message "$MESSAGE" \
  '{intent: $intent, message: $message}')

[ -n "$FROM_NAME" ]      && BODY=$(jq -n --argjson b "$BODY" --arg v "$FROM_NAME"       '$b + {from_name: $v}')
[ -n "$FROM_EMAIL" ]     && BODY=$(jq -n --argjson b "$BODY" --arg v "$FROM_EMAIL"      '$b + {from_email: $v}')
[ -n "$FROM_CARD_SLUG" ] && BODY=$(jq -n --argjson b "$BODY" --arg v "$FROM_CARD_SLUG"  '$b + {from_card_slug: $v}')
[ -n "$BUDGET_CENTS" ]   && BODY=$(jq -n --argjson b "$BODY" --argjson v "$BUDGET_CENTS" '$b + {budget_cents: $v}')

RESPONSE=$(curl -sf \
  -X POST \
  -H "Content-Type: application/json" \
  -d "$BODY" \
  "${BASE_URL}/api/cards/${TARGET_SLUG}/request") || {
    echo "Error: Request failed. Check the target slug is valid." >&2
    exit 1
  }

echo "$RESPONSE" | jq .
