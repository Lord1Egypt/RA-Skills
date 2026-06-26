#!/usr/bin/env bash
# vw-unlock.sh — authenticate and unlock Vaultwarden session
# Required bw CLI version: 2023.10.0
# CLI 2024.x+ breaks with "User Decryption Options are required" on Vaultwarden

set -euo pipefail

SESSION_DIR="${VW_SESSION_DIR:-/run/openclaw/vw}"
SESSION_FILE="$SESSION_DIR/.bw_session"

: "${BW_CLIENTID:?BW_CLIENTID not set}"
: "${BW_CLIENTSECRET:?BW_CLIENTSECRET not set}"
: "${BW_PASSWORD:?BW_PASSWORD not set}"

# Version check before attempting anything
VERSION=$(bw --version 2>/dev/null || echo "0.0.0")
MAJOR=$(echo "$VERSION" | cut -d. -f1)
if [ "$MAJOR" -ge 2024 ]; then
    echo "error: bw CLI $VERSION is incompatible with Vaultwarden"
    echo "error: install correct version: npm install -g @bitwarden/cli@2023.10.0"
    exit 1
fi

if [ ! -d "$SESSION_DIR" ]; then
    mkdir -p "$SESSION_DIR"
    chmod 700 "$SESSION_DIR"
fi

# Check existing session
if [ -f "$SESSION_FILE" ]; then
    export BW_SESSION=$(cat "$SESSION_FILE")
    STATUS=$(bw status | jq -r '.status' 2>/dev/null || echo "error")
    if [ "$STATUS" = "unlocked" ]; then
        echo "ok: session already unlocked"
        exit 0
    fi
    rm -f "$SESSION_FILE" "$SESSION_DIR/.collection_id"
fi

# Verify server configured
SERVER_URL=$(bw status 2>/dev/null | jq -r '.serverUrl // empty')
if [ -z "$SERVER_URL" ]; then
    echo "error: server not configured — run: bw config server https://vaultwarden.mbojer.dk"
    exit 1
fi

# Login via API key if needed
STATUS=$(bw status | jq -r '.status' 2>/dev/null || echo "unauthenticated")
if [ "$STATUS" = "unauthenticated" ]; then
    if ! bw login --apikey --quiet 2>/dev/null; then
        echo "error: API key login failed — check BW_CLIENTID and BW_CLIENTSECRET"
        echo "error: if error contains 'User Decryption Options', downgrade CLI: npm install -g @bitwarden/cli@2023.10.0"
        exit 1
    fi
fi

SESSION=$(bw unlock --passwordenv BW_PASSWORD --raw 2>/dev/null || true)
if [ -z "$SESSION" ]; then
    echo "error: unlock failed — check BW_PASSWORD"
    exit 1
fi

echo "$SESSION" > "$SESSION_FILE"
chmod 600 "$SESSION_FILE"

export BW_SESSION="$SESSION"
echo "ok: unlocked (bw $VERSION)"
