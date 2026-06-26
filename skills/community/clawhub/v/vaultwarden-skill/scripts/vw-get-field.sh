#!/usr/bin/env bash
# vw-get-field.sh — get a custom field value from an item
# Usage: vw-get-field.sh <item name|id> <field name>

set -euo pipefail
source "$(dirname "$0")/_vw-session.sh"
_vw_load_session

: "${1:?Usage: vw-get-field.sh <item name|id> <field name>}"
: "${2:?Usage: vw-get-field.sh <item name|id> <field name>}"

RESULT=$(bw get item "$1" 2>/dev/null | jq -r --arg field "$2" '.fields[] | select(.name==$field) | .value')
if [ -z "$RESULT" ]; then
    echo "error: field '$2' not found on item '$1'" >&2
    _vw_log "get-field" "$1:$2" "not-found"
    exit 1
fi

echo "$RESULT"
_vw_log "get-field" "$1:$2" "ok"
