#!/usr/bin/env bash
# Openclaw AI Bot — Colored Buttons Test Script
# Sends a test message with colored inline keyboard buttons via Telegram Bot API.
#
# Usage:
#   ./SKILL.sh <BOT_TOKEN> <CHAT_ID>
#
# Or set environment variables:
#   export BOT_TOKEN="your-bot-token"
#   export CHAT_ID="your-chat-id"
#   ./SKILL.sh

set -euo pipefail

BOT_TOKEN="${1:-${BOT_TOKEN:-}}"
CHAT_ID="${2:-${CHAT_ID:-}}"

if [[ -z "$BOT_TOKEN" || -z "$CHAT_ID" ]]; then
  echo "Usage: $0 <BOT_TOKEN> <CHAT_ID>"
  echo "Or set BOT_TOKEN and CHAT_ID environment variables."
  exit 1
fi

API_URL="https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"

echo "==> Sending auto-colored choice buttons to chat ${CHAT_ID}..."
echo ""
echo "Button classification:"
echo "  [Approve]       → default (blue)  — safe/recommended action"
echo "  [Reject]        → destructive (red) — irreversible decision"
echo "  [Delete All]    → destructive (red) — permanent data loss"
echo "  [Review Later]  → secondary (gray)  — dismiss/postpone"
echo "  [Skip]          → secondary (gray)  — low-priority escape"
echo ""

RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${CHAT_ID}"'",
    "text": "🎨 <b>Openclaw Auto-Colored Buttons</b>\n\nColors are assigned by criticality:\n\n• Blue = recommended / safe\n• Red = irreversible / destructive\n• Gray = dismiss / low-priority",
    "parse_mode": "HTML",
    "reply_markup": {
      "inline_keyboard": [
        [
          {"text": "✅ Approve", "callback_data": "approve"},
          {"text": "❌ Reject", "callback_data": "reject", "style": "destructive"}
        ],
        [
          {"text": "🗑 Delete All", "callback_data": "delete_all", "style": "destructive"},
          {"text": "⏭ Review Later", "callback_data": "later", "style": "secondary"}
        ],
        [
          {"text": "Skip", "callback_data": "skip", "style": "secondary"}
        ]
      ]
    }
  }')

# Check response
OK=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ok', False))" 2>/dev/null || echo "false")

if [[ "$OK" == "True" ]]; then
  MSG_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['message_id'])" 2>/dev/null)
  echo "✅ Message sent! (message_id: ${MSG_ID})"
  echo ""
  echo "All button colors were auto-assigned based on criticality."
else
  echo "❌ Failed to send message."
  echo "Response: $RESPONSE"
  exit 1
fi
