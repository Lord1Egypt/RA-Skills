#!/usr/bin/env bash
# vw-get.sh — get full item JSON by name or ID
# Usage: vw-get.sh <name|id>

set -euo pipefail
source "$(dirname "$0")/_vw-session.sh"
_vw_load_session

: "${1:?Usage: vw-get.sh <name|id>}"

RESULT=$(bw get item "$1" 2>/dev/null)
if [ -z "$RESULT" ]; then
    echo "error: item '$1' not found" >&2
    _vw_log "get-item" "$1" "not-found"
    exit 1
fi

echo "$RESULT"
_vw_log "get-item" "$1" "ok"
