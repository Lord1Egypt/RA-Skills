#!/usr/bin/env bash
# add-telegram-group.sh — Add a Telegram group to openclaw.json allow-list
# Usage: add-telegram-group.sh <chat_id> [requireMention] [groupPolicy]
#   chat_id:        negative Telegram group/supergroup ID (e.g. -5254564401)
#   requireMention: true|false (default: false)
#   groupPolicy:    open|allowlist (default: open)

set -euo pipefail

CHAT_ID="${1:?Usage: add-telegram-group.sh <chat_id> [requireMention] [groupPolicy]}"
REQUIRE_MENTION="${2:-false}"
GROUP_POLICY="${3:-open}"

# Find openclaw.json
CONFIG=""
for p in "$HOME/.openclaw/openclaw.json" "/etc/openclaw/openclaw.json"; do
  if [[ -f "$p" ]]; then
    CONFIG="$p"
    break
  fi
done

if [[ -z "$CONFIG" ]]; then
  echo "ERROR: openclaw.json not found" >&2
  exit 1
fi

# Check if group already exists
if jq -e ".channels.telegram.groups[\"$CHAT_ID\"]" "$CONFIG" >/dev/null 2>&1; then
  echo "Group $CHAT_ID already in config:"
  jq ".channels.telegram.groups[\"$CHAT_ID\"]" "$CONFIG"
  exit 0
fi

# Backup
cp "$CONFIG" "${CONFIG}.bak.$(date +%s)"

# Add the group entry
jq --arg id "$CHAT_ID" \
   --argjson mention "$REQUIRE_MENTION" \
   --arg policy "$GROUP_POLICY" \
   '.channels.telegram.groups[$id] = {
      requireMention: $mention,
      groupPolicy: $policy
    }' "$CONFIG" > "${CONFIG}.tmp" && mv "${CONFIG}.tmp" "$CONFIG"

echo "✅ Added group $CHAT_ID to $CONFIG"
echo "   requireMention: $REQUIRE_MENTION"
echo "   groupPolicy: $GROUP_POLICY"
echo ""
echo "⚠️  Restart the gateway to apply: openclaw gateway restart"
