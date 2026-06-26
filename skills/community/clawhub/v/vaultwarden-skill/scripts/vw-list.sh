#!/usr/bin/env bash
# vw-list.sh — list vault items, scoped to openclaw collection if available
# Falls back to all items on personal vaults (collections not accessible via API key)
# Usage: vw-list.sh [search query]
# Returns: JSON array of {id, name, type}

set -euo pipefail
source "$(dirname "$0")/_vw-session.sh"
_vw_load_session

COLLECTION_ID=$(_vw_collection_id)
QUERY="${1:-}"

if [ -n "$COLLECTION_ID" ]; then
    ARGS=(--collectionid "$COLLECTION_ID")
else
    echo "info: no collection scope — listing all vault items" >&2
    ARGS=()
fi

if [ -n "$QUERY" ]; then
    ARGS+=(--search "$QUERY")
fi

bw list items "${ARGS[@]}" 2>/dev/null | \
    jq '[.[] | {id, name, type: (if .type==1 then "login" elif .type==2 then "note" elif .type==3 then "card" else "identity" end)}]'

_vw_log "list" "${QUERY:-all}" "ok"
