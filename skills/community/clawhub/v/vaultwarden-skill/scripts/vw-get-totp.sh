#!/usr/bin/env bash
# vw-get-totp.sh — get current TOTP code for an item
# Usage: vw-get-totp.sh <n>

set -euo pipefail
source "$(dirname "$0")/_vw-session.sh"
_vw_load_session

: "${1:?Usage: vw-get-totp.sh <n>}"

RESULT=$(bw get totp "$1" 2>/dev/null)
if [ -z "$RESULT" ]; then
    echo "error: TOTP for '$1' not found" >&2
    _vw_log "get-totp" "$1" "not-found"
    exit 1
fi

echo "$RESULT"
_vw_log "get-totp" "$1" "ok"
