#!/bin/zsh
# wine-send-label-telegram.sh — look up a wine label and print the send payload.
#
# Usage: wine-send-label-telegram.sh <chat_id> <thread_id> <reply_to> <query...>
#
# Outputs JSON from wine-telegram-bridge.js. When action === "send-media",
# the agent uses the returned mediaPath and caption to send the message via
# the openclaw CLI:
#   openclaw message send --channel telegram --target <chat_id> \
#     --thread-id <thread_id> --reply-to <reply_to> \
#     --media <mediaPath> --message <caption>
set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "usage: wine-send-label-telegram.sh <chat_id> <thread_id> <reply_to> <query...>" >&2
  exit 1
fi

# Capture args before shifting (for documentation / agent use)
CHAT_ID="$1"
THREAD_ID="$2"
REPLY_TO="$3"
shift 3
QUERY="$*"

SCRIPT_DIR="${0:A:h}"
cd "${SCRIPT_DIR}/.."

# Output JSON for the agent to act on
node scripts/wine-telegram-bridge.js --text "Show me the ${QUERY} label"
