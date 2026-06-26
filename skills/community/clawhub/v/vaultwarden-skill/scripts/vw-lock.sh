#!/usr/bin/env bash
# vw-lock.sh — lock vault and remove session token file

set -euo pipefail

SESSION_DIR="${VW_SESSION_DIR:-/run/openclaw/vw}"
SESSION_FILE="$SESSION_DIR/.bw_session"

if [ -f "$SESSION_FILE" ]; then
    export BW_SESSION=$(cat "$SESSION_FILE")
    bw lock --quiet 2>/dev/null || true
    rm -f "$SESSION_FILE"
fi

rm -f "$SESSION_DIR/.collection_id"
rm -rf "$SESSION_DIR/cache" 2>/dev/null || true
echo "ok: locked"
