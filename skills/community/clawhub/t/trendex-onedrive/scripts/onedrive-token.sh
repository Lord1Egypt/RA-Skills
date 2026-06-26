#!/usr/bin/env bash
# onedrive-token.sh — Manage Microsoft OAuth2 access tokens for OneDrive
# Usage: onedrive-token.sh [get|refresh|test|info|me|set|clear]

set -euo pipefail

CONFIG_DIR="${ONEDRIVE_MCP_CONFIG_DIR:-$HOME/.onedrive-mcp}"
CONFIG_FILE="$CONFIG_DIR/config.json"
CREDS_FILE="$CONFIG_DIR/credentials.json"

# get_token: load from $ONEDRIVE_ACCESS_TOKEN first, else creds file
get_token() {
    if [ -n "${ONEDRIVE_ACCESS_TOKEN:-}" ]; then
        echo "$ONEDRIVE_ACCESS_TOKEN"
        return 0
    fi
    if [ ! -f "$CREDS_FILE" ]; then
        echo "Error: no credentials file at $CREDS_FILE — run onedrive-setup.sh or set ONEDRIVE_ACCESS_TOKEN" >&2
        exit 1
    fi
    jq -r '.access_token // empty' "$CREDS_FILE"
}

ensure_config() {
    [ -f "$CONFIG_FILE" ] || { echo "Error: missing $CONFIG_FILE — run onedrive-setup.sh" >&2; exit 1; }
    [ -f "$CREDS_FILE" ] || { echo "Error: missing $CREDS_FILE — run onedrive-setup.sh" >&2; exit 1; }
}

cmd_get() {
    get_token
}

cmd_refresh() {
    ensure_config
    local cid csec tenant scopes rt
    cid=$(jq -r '.client_id' "$CONFIG_FILE")
    csec=$(jq -r '.client_secret' "$CONFIG_FILE")
    tenant=$(jq -r '.tenant // "common"' "$CONFIG_FILE")
    scopes=$(jq -r '.scopes' "$CONFIG_FILE")
    rt=$(jq -r '.refresh_token // empty' "$CREDS_FILE")

    if [ -z "$rt" ]; then
        echo "Error: no refresh_token in $CREDS_FILE — re-run onedrive-setup.sh" >&2
        exit 1
    fi

    local response
    response=$(curl -s -X POST "https://login.microsoftonline.com/$tenant/oauth2/v2.0/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        --data-urlencode "client_id=$cid" \
        --data-urlencode "client_secret=$csec" \
        --data-urlencode "refresh_token=$rt" \
        --data-urlencode "grant_type=refresh_token" \
        --data-urlencode "scope=$scopes")

    if echo "$response" | jq -e '.access_token' >/dev/null 2>&1; then
        local now exp
        now=$(date +%s)
        exp=$(echo "$response" | jq -r '.expires_in // 3600')
        echo "$response" | jq --argjson now "$now" --argjson exp "$exp" \
            '. + {acquired_at: $now, expires_at: ($now + $exp)}' > "$CREDS_FILE"
        chmod 600 "$CREDS_FILE"
        echo "{\"status\":\"refreshed\",\"expires_in\":$exp}"
    else
        echo "$response" | jq '{error: (.error // "unknown"), description: (.error_description // .)}' >&2
        exit 1
    fi
}

cmd_test() {
    local token
    token=$(get_token)
    local r
    r=$(curl -s -o /dev/null -w "%{http_code}" "https://graph.microsoft.com/v1.0/me/drive" \
        -H "Authorization: Bearer $token")
    if [ "$r" = "200" ]; then
        echo '{"status":"ok"}'
    else
        echo "{\"status\":\"failed\",\"http_code\":$r}" >&2
        exit 1
    fi
}

cmd_info() {
    [ -f "$CREDS_FILE" ] || { echo "Error: missing $CREDS_FILE" >&2; exit 1; }
    jq '{
        token_type,
        scope,
        expires_in,
        acquired_at,
        expires_at,
        seconds_remaining: ((.expires_at // 0) - now | floor),
        has_refresh_token: (.refresh_token != null)
    }' "$CREDS_FILE"
}

cmd_me() {
    local token
    token=$(get_token)
    curl -s "https://graph.microsoft.com/v1.0/me" \
        -H "Authorization: Bearer $token" \
        | jq '{id, displayName, userPrincipalName, mail, givenName, surname, jobTitle, officeLocation}'
}

cmd_set() {
    # onedrive-token.sh set <access_token> [refresh_token]
    local at="${1:-}" rt="${2:-}"
    if [ -z "$at" ]; then
        echo "Usage: onedrive-token.sh set <access_token> [refresh_token]" >&2
        exit 1
    fi
    mkdir -p "$CONFIG_DIR" && chmod 700 "$CONFIG_DIR"
    local now=$(date +%s)
    jq -n --arg at "$at" --arg rt "$rt" --argjson now "$now" \
        '{access_token:$at, refresh_token:(if $rt=="" then null else $rt end), token_type:"Bearer", expires_in:3600, acquired_at:$now, expires_at:($now+3600)}' \
        > "$CREDS_FILE"
    chmod 600 "$CREDS_FILE"
    echo "{\"status\":\"saved\",\"file\":\"$CREDS_FILE\"}"
}

cmd_clear() {
    rm -f "$CREDS_FILE"
    echo "{\"status\":\"cleared\"}"
}

case "${1:-}" in
    get)     cmd_get ;;
    refresh) cmd_refresh ;;
    test)    cmd_test ;;
    info)    cmd_info ;;
    me)      cmd_me ;;
    set)     shift; cmd_set "$@" ;;
    clear)   cmd_clear ;;
    *)
        cat <<EOF
Usage: onedrive-token.sh <command>

  get       Print current access token
  refresh   Exchange refresh_token for a new access_token
  test      Verify token against /me/drive (HTTP 200 = ok)
  info      Show token type, scopes, expiration
  me        Show signed-in user (displayName, email, ...)
  set <at> [<rt>]  Manually store an access (and optional refresh) token
  clear     Remove the credentials file

Env overrides:
  ONEDRIVE_ACCESS_TOKEN — short-circuit to use this token (read-only)
  ONEDRIVE_MCP_CONFIG_DIR   — directory for config + credentials (default ~/.onedrive-mcp)
EOF
        ;;
esac
