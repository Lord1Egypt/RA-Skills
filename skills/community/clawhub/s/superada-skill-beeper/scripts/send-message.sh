#!/usr/bin/env bash
# Send a message through Beeper Desktop API by matching a chat title or participant.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -lt 2 ]]; then
  echo "Usage: send-message.sh <recipient-or-chat-title> <message>" >&2
  exit 1
fi

RECIPIENT="$1"
MESSAGE="$2"

CHAT_ID="$("$SCRIPT_DIR/beeper.sh" raw "/v1/chats/search?query=$(jq -sRr @uri <<<"$RECIPIENT")" | \
  jq -r --arg name "$RECIPIENT" \
    '.items[] | select(((.title // .name // "") | ascii_downcase | contains($name | ascii_downcase)) or ([.participants.items[]?.fullName?] | join(" ") | ascii_downcase | contains($name | ascii_downcase))) | .id' | \
  head -1)"

if [[ -z "$CHAT_ID" ]]; then
  echo "No chat found with: $RECIPIENT" >&2
  exit 1
fi

ENCODED_CHAT_ID="$(jq -sRr @uri <<<"$CHAT_ID")"
PAYLOAD="$(jq -n --arg text "$MESSAGE" '{text: $text}')"
RESULT="$("$SCRIPT_DIR/beeper.sh" raw "/v1/chats/${ENCODED_CHAT_ID}/messages" POST "$PAYLOAD")"
PENDING_ID="$(jq -r '.pendingMessageID // .messageID // .id // empty' <<<"$RESULT")"

if [[ -n "$PENDING_ID" ]]; then
  echo "Message sent. Message ID: $PENDING_ID"
else
  echo "Failed to send message:" >&2
  echo "$RESULT" >&2
  exit 1
fi

