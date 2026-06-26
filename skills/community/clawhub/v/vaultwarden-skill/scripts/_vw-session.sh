#!/usr/bin/env bash
# _vw-session.sh — sourced by other scripts to load and validate session
# Usage: source "$(dirname "$0")/_vw-session.sh"
#
# Required bw CLI version: 2023.10.0
# CLI 2024.x+ breaks Vaultwarden auth ("User Decryption Options are required")
# Install pinned version: npm install -g @bitwarden/cli@2023.10.0
#
# Collection scoping:
# Personal vault API keys cannot see collections (Bitwarden limitation).
# Scripts fall back to unscoped queries automatically.
# To hardcode a collection ID (org accounts): set VW_COLLECTION_ID env var.

SESSION_DIR="${VW_SESSION_DIR:-/run/openclaw/vw}"
SESSION_FILE="$SESSION_DIR/.bw_session"
AGENT_FILE="$SESSION_DIR/.ssh_agent"
CACHE_DIR="$SESSION_DIR/cache"
LOG_FILE="${VW_LOG_FILE:-/var/log/openclaw/vaultwarden.log}"
CACHE_TTL="${VW_CACHE_TTL:-60}"  # seconds, 0 to disable

_vw_check_version() {
    local version
    version=$(bw --version 2>/dev/null || echo "0.0.0")
    local major
    major=$(echo "$version" | cut -d. -f1)
    if [ "$major" -ge 2024 ]; then
        echo "warning: bw CLI $version may be incompatible with Vaultwarden. Recommended: 2023.10.0" >&2
        echo "warning: install with: npm install -g @bitwarden/cli@2023.10.0" >&2
    fi
}

_vw_load_session() {
    _vw_check_version

    if [ ! -f "$SESSION_FILE" ]; then
        echo "error: no active session — run vw-unlock.sh first" >&2
        exit 1
    fi

    export BW_SESSION=$(cat "$SESSION_FILE")

    STATUS=$(bw status | jq -r '.status' 2>/dev/null || echo "error")
    if [ "$STATUS" != "unlocked" ]; then
        echo "error: session invalid or expired — run vw-unlock.sh" >&2
        rm -f "$SESSION_FILE"
        exit 1
    fi
}

_vw_log() {
    local op="$1"
    local detail="$2"
    local result="$3"
    mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $op: $detail: $result" >> "$LOG_FILE" 2>/dev/null || true
}

# Collection ID resolution — returns empty string if not available (personal vault)
# Priority: VW_COLLECTION_ID env var > cached lookup > empty (fallback to unscoped)
_vw_collection_id() {
    # Hardcoded override — use this for org accounts
    if [ -n "${VW_COLLECTION_ID:-}" ]; then
        echo "$VW_COLLECTION_ID"
        return 0
    fi

    local cache_file="$SESSION_DIR/.collection_id"
    if [ -f "$cache_file" ]; then
        cat "$cache_file"
        return 0
    fi

    local id
    id=$(bw list collections 2>/dev/null | jq -r --arg name "${VW_COLLECTION_NAME:-openclaw}" \
        '.[] | select(.name==$name) | .id' 2>/dev/null || echo "")

    if [ -z "$id" ]; then
        # Personal vault — collections not accessible via API key. Fall back to unscoped.
        echo "" > "$cache_file"  # cache the empty result to avoid repeated lookups
        chmod 600 "$cache_file"
        echo ""
        return 0
    fi

    echo "$id" > "$cache_file"
    chmod 600 "$cache_file"
    echo "$id"
}

# Read cache — TTL-based file cache for item reads
_vw_cache_get() {
    [ "${CACHE_TTL}" -eq 0 ] && return 1
    local key="$1"
    local cache_file="$CACHE_DIR/$(echo "$key" | tr -cs '[:alnum:]' '_')"
    [ ! -f "$cache_file" ] && return 1
    local age=$(( $(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || echo 0) ))
    [ "$age" -gt "${CACHE_TTL}" ] && { rm -f "$cache_file"; return 1; }
    cat "$cache_file"
}

_vw_cache_set() {
    [ "${CACHE_TTL}" -eq 0 ] && cat && return 0
    local key="$1"
    mkdir -p "$CACHE_DIR"
    chmod 700 "$CACHE_DIR"
    local cache_file="$CACHE_DIR/$(echo "$key" | tr -cs '[:alnum:]' '_')"
    tee "$cache_file"
    chmod 600 "$cache_file"
}

_vw_cache_clear() {
    local key="${1:-}"
    if [ -n "$key" ]; then
        rm -f "$CACHE_DIR/$(echo "$key" | tr -cs '[:alnum:]' '_')"
    else
        rm -f "$CACHE_DIR"/* 2>/dev/null || true
    fi
}
