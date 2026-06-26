#!/usr/bin/env bash
# vw-create-note.sh — create a secure note
# Assigns to collection if available, personal vault otherwise
# Usage: echo <content> | vw-create-note.sh <n>

set -euo pipefail
source "$(dirname "$0")/_vw-session.sh"
_vw_load_session

: "${1:?Usage: echo <content> | vw-create-note.sh <n>}"

CONTENT=$(cat /dev/stdin)
if [ -z "$CONTENT" ]; then
    echo "error: no content provided on stdin" >&2
    exit 1
fi

COLLECTION_ID=$(_vw_collection_id)

ITEM=$(bw get template item.secureNote | jq \
    --arg name "$1" \
    --arg notes "$CONTENT" \
    '.name=$name | .notes=$notes')

if [ -n "$COLLECTION_ID" ]; then
    ITEM=$(echo "$ITEM" | jq --arg col "$COLLECTION_ID" '.collectionIds=[$col]')
fi

RESULT=$(echo "$ITEM" | bw encode | bw create item)
ITEM_ID=$(echo "$RESULT" | jq -r '.id')

echo "ok: created note '$1' (id: $ITEM_ID)"
_vw_log "create-note" "$1" "ok:$ITEM_ID"
