#!/usr/bin/env bash
# Search Beeper chats or list recent conversations.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUERY="${1:-}"
LIMIT="${2:-20}"

if [[ -n "$QUERY" ]]; then
  "$SCRIPT_DIR/beeper.sh" raw "/v1/chats/search?query=$(jq -sRr @uri <<<"$QUERY")" | \
    jq -r '.items[] | "[\(.network // .account.network // "?")] \(.title // .name // .participants.items[0].fullName // "(untitled)") - \(.id)"'
else
  "$SCRIPT_DIR/beeper.sh" raw "/v1/chats?limit=$LIMIT" | \
    jq -r '.items[] | "[\(.network // .account.network // "?")] \(.title // .name // .participants.items[0].fullName // "(untitled)") - Last: \(.lastActivity // .lastMessage.receivedAt // "?") - \(.id)"'
fi

