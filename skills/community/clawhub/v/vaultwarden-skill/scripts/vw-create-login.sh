#!/usr/bin/env bash
# vw-create-login.sh — create a login item
# Assigns to collection if available, personal vault otherwise
# Usage: echo <password> | vw-create-login.sh <n> <username>

set -euo pipefail
source "$(dirname "$0")/_vw-session.sh"
_vw_load_session

: "${1:?Usage: echo <password> | vw-create-login.sh <n> <username>}"
: "${2:?Usage: echo <password> | vw-create-login.sh <n> <username>}"

PASS=$(cat /dev/stdin)
if [ -z "$PASS" ]; then
    echo "error: no password provided on stdin" >&2
    exit 1
fi

COLLECTION_ID=$(_vw_collection_id)

ITEM=$(bw get template item.login | jq \
    --arg name "$1" \
    --arg user "$2" \
    --arg pass "$PASS" \
    '.name=$name | .login.username=$user | .login.password=$pass')

if [ -n "$COLLECTION_ID" ]; then
    ITEM=$(echo "$ITEM" | jq --arg col "$COLLECTION_ID" '.collectionIds=[$col]')
fi

RESULT=$(echo "$ITEM" | bw encode | bw create item)
ITEM_ID=$(echo "$RESULT" | jq -r '.id')

echo "ok: created login '$1' (id: $ITEM_ID)"
_vw_log "create-login" "$1" "ok:$ITEM_ID"
