#!/usr/bin/env bash
# vw-update.sh — update a specific field on an existing item
# Usage: vw-update.sh <item id> <field>
# Value is read from stdin to avoid exposure in process list:
#   echo "newvalue" | vw-update.sh <item id> <field>
# field: password | username | notes | custom:<fieldname>

set -euo pipefail
source "$(dirname "$0")/_vw-session.sh"
_vw_load_session

: "${1:?Usage: echo <value> | vw-update.sh <item id> <field>}"
: "${2:?Usage: echo <value> | vw-update.sh <item id> <field>}"

ITEM_ID="$1"
FIELD="$2"
VALUE=$(cat /dev/stdin)

if [ -z "$VALUE" ]; then
    echo "error: no value provided on stdin" >&2
    exit 1
fi

# Fetch current item
CURRENT=$(bw get item "$ITEM_ID" 2>/dev/null)
if [ -z "$CURRENT" ]; then
    echo "error: item '$ITEM_ID' not found" >&2
    _vw_log "update" "$ITEM_ID:$FIELD" "not-found"
    exit 1
fi

ITEM_NAME=$(echo "$CURRENT" | jq -r '.name')

case "$FIELD" in
    password)
        UPDATED=$(echo "$CURRENT" | jq --arg v "$VALUE" '.login.password=$v')
        ;;
    username)
        UPDATED=$(echo "$CURRENT" | jq --arg v "$VALUE" '.login.username=$v')
        ;;
    notes)
        UPDATED=$(echo "$CURRENT" | jq --arg v "$VALUE" '.notes=$v')
        ;;
    custom:*)
        FNAME="${FIELD#custom:}"
        # Verify field exists before trying to update
        EXISTS=$(echo "$CURRENT" | jq -r --arg fname "$FNAME" '.fields // [] | map(select(.name==$fname)) | length')
        if [ "$EXISTS" = "0" ]; then
            echo "error: custom field '$FNAME' does not exist on item '$ITEM_NAME'" >&2
            _vw_log "update" "$ITEM_NAME:$FIELD" "field-not-found"
            exit 1
        fi
        UPDATED=$(echo "$CURRENT" | jq --arg fname "$FNAME" --arg v "$VALUE" \
            '(.fields[] | select(.name==$fname) | .value) = $v')
        ;;
    *)
        echo "error: unknown field '$FIELD'. Use: password | username | notes | custom:<fieldname>" >&2
        exit 1
        ;;
esac

echo "$UPDATED" | bw encode | bw edit item "$ITEM_ID" > /dev/null

# Invalidate cache for this item
_vw_cache_clear

echo "ok: updated '$ITEM_NAME' ($ITEM_ID) field '$FIELD'"
_vw_log "update" "$ITEM_NAME:$FIELD" "ok"
