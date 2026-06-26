#!/usr/bin/env bash
# vw-delete.sh — delete an item by ID after confirming name
# Usage: vw-delete.sh <item id> <expected name>
# Both ID and expected name required — prevents accidental deletes
# Note: items are moved to trash, not permanently deleted.
# To permanently delete, log into Vaultwarden web UI and empty trash.

set -euo pipefail
source "$(dirname "$0")/_vw-session.sh"
_vw_load_session

: "${1:?Usage: vw-delete.sh <item id> <expected name>}"
: "${2:?Usage: vw-delete.sh <item id> <expected name>}"

ITEM_ID="$1"
EXPECTED_NAME="$2"

# Fetch and confirm name matches
ACTUAL_NAME=$(bw get item "$ITEM_ID" 2>/dev/null | jq -r '.name')
if [ -z "$ACTUAL_NAME" ] || [ "$ACTUAL_NAME" = "null" ]; then
    echo "error: item '$ITEM_ID' not found" >&2
    _vw_log "delete" "$ITEM_ID" "not-found"
    exit 1
fi

if [ "$ACTUAL_NAME" != "$EXPECTED_NAME" ]; then
    echo "error: name mismatch — expected '$EXPECTED_NAME', got '$ACTUAL_NAME'. Delete aborted." >&2
    _vw_log "delete" "$ITEM_ID" "name-mismatch"
    exit 1
fi

bw delete item "$ITEM_ID"

echo "ok: moved '$ACTUAL_NAME' ($ITEM_ID) to trash"
_vw_log "delete" "$ACTUAL_NAME:$ITEM_ID" "ok"
