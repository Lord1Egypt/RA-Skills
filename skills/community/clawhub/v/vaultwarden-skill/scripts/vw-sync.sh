#!/usr/bin/env bash
# vw-sync.sh — sync local bw cache with Vaultwarden server
# Run before reads if vault may have been modified by another client or the web UI
# Also clears cached collection ID so it is re-resolved after sync

set -euo pipefail
source "$(dirname "$0")/_vw-session.sh"
_vw_load_session

bw sync --quiet

# Invalidate collection ID cache — may have changed
rm -f "$SESSION_DIR/.collection_id"

echo "ok: vault synced"
_vw_log "sync" "vault" "ok"
