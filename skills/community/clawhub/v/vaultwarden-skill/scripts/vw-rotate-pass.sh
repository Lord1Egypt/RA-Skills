#!/usr/bin/env bash
# vw-rotate-pass.sh — generate a new password and update a login item atomically
# Usage: vw-rotate-pass.sh <item name|id> [password length (default 32)]
# Outputs only the new password on stdout — status messages go to stderr

set -euo pipefail
source "$(dirname "$0")/_vw-session.sh"
_vw_load_session

: "${1:?Usage: vw-rotate-pass.sh <item name|id> [length]}"

LENGTH="${2:-32}"

# Resolve item
ITEM=$(bw get item "$1" 2>/dev/null)
if [ -z "$ITEM" ]; then
    echo "error: item '$1' not found" >&2
    _vw_cache_clear
_vw_log "rotate-pass" "$1" "not-found"
    exit 1
fi

ITEM_ID=$(echo "$ITEM" | jq -r '.id')
ITEM_NAME=$(echo "$ITEM" | jq -r '.name')

# Generate new password
NEW_PASS=$(bw generate --length "$LENGTH" --uppercase --lowercase --number --special)
if [ -z "$NEW_PASS" ]; then
    echo "error: password generation failed" >&2
    exit 1
fi

# Update
UPDATED=$(echo "$ITEM" | jq --arg p "$NEW_PASS" '.login.password=$p')
echo "$UPDATED" | bw encode | bw edit item "$ITEM_ID" > /dev/null

echo "ok: rotated password for '$ITEM_NAME' ($ITEM_ID)" >&2
_vw_cache_clear
_vw_log "rotate-pass" "$ITEM_NAME" "ok"

# New password on stdout only — clean for capture: NEW=$(vw-rotate-pass.sh "MyService")
echo "$NEW_PASS"
