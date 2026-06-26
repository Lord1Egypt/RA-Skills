#!/usr/bin/env bash
# vw-get-pass.sh — get password for a login item
# Scoped to collection if available, falls back to all items on personal vaults
# Usage: vw-get-pass.sh <item name>

set -euo pipefail
source "$(dirname "$0")/_vw-session.sh"
_vw_load_session

: "${1:?Usage: vw-get-pass.sh <item name>}"

CACHED=$(_vw_cache_get "pass_$1") && { echo "$CACHED"; _vw_log "get-password" "$1" "cache-hit"; exit 0; }

COLLECTION_ID=$(_vw_collection_id)

if [ -n "$COLLECTION_ID" ]; then
    RESULT=$(bw list items --collectionid "$COLLECTION_ID" --search "$1" 2>/dev/null | \
        jq -r --arg name "$1" '.[] | select(.name==$name) | .login.password // empty' | head -1)
else
    RESULT=$(bw list items --search "$1" 2>/dev/null | \
        jq -r --arg name "$1" '.[] | select(.name==$name) | .login.password // empty' | head -1)
fi

if [ -z "$RESULT" ]; then
    echo "error: password for '$1' not found" >&2
    _vw_log "get-password" "$1" "not-found"
    exit 1
fi

echo "$RESULT" | _vw_cache_set "pass_$1"
_vw_log "get-password" "$1" "ok"
