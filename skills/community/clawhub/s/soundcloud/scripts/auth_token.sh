#!/bin/bash
# SoundCloud Token Manager
# Manages two token types:
#   1. App token (client_credentials) — auto-acquired, cached, for public read ops
#   2. User token (authorization_code) — user-provided, for write ops (playlists, likes)
# Can be sourced: source "$(dirname "$0")/auth_token.sh"

set -e

# Configuration
TOKEN_CACHE_DIR="${HOME}/.cache/soundcloud"
APP_TOKEN_FILE="${TOKEN_CACHE_DIR}/app_token.json"
USER_TOKEN_FILE="${TOKEN_CACHE_DIR}/user_token.json"
TOKEN_ENDPOINT="https://api.soundcloud.com/oauth2/token"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

mkdir -p "$TOKEN_CACHE_DIR"

# ── Internal helpers ──────────────────────────────────────────

_token_is_valid() {
    local file="$1"
    [ -f "$file" ] || return 1
    local expires_at
    expires_at=$(jq -r '.expires_at // 0' "$file" 2>/dev/null)
    [ "$expires_at" -gt 0 ] || return 1
    local now
    now=$(date +%s)
    [ "$now" -lt $((expires_at - 60)) ]
}

_refresh_token() {
    local refresh_token="$1"
    local output_file="$2"

    if [ -z "$SOUNDCLOUD_CLIENT_ID" ] || [ -z "$SOUNDCLOUD_CLIENT_SECRET" ]; then
        return 1
    fi

    local response
    response=$(curl -s -X POST "$TOKEN_ENDPOINT" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "client_id=${SOUNDCLOUD_CLIENT_ID}" \
        -d "client_secret=${SOUNDCLOUD_CLIENT_SECRET}" \
        -d "grant_type=refresh_token" \
        -d "refresh_token=${refresh_token}" 2>/dev/null)

    if echo "$response" | jq -e '.access_token' >/dev/null 2>&1; then
        _save_token_response "$response" "$output_file"
        return 0
    fi
    return 1
}

_fetch_client_credentials() {
    if [ -z "$SOUNDCLOUD_CLIENT_ID" ] || [ -z "$SOUNDCLOUD_CLIENT_SECRET" ]; then
        echo -e "${RED}Error: SOUNDCLOUD_CLIENT_ID and SOUNDCLOUD_CLIENT_SECRET must be set${NC}" >&2
        return 1
    fi

    local response
    response=$(curl -s -X POST "$TOKEN_ENDPOINT" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "client_id=${SOUNDCLOUD_CLIENT_ID}" \
        -d "client_secret=${SOUNDCLOUD_CLIENT_SECRET}" \
        -d "grant_type=client_credentials" 2>/dev/null)

    if echo "$response" | jq -e '.access_token' >/dev/null 2>&1; then
        _save_token_response "$response" "$APP_TOKEN_FILE"
        return 0
    fi

    echo -e "${RED}Error: Failed to get app access token${NC}" >&2
    echo "Response: $response" >&2
    return 1
}

_save_token_response() {
    local response="$1"
    local output_file="$2"

    local access_token expires_in refresh_token
    access_token=$(echo "$response" | jq -r '.access_token')
    expires_in=$(echo "$response" | jq -r '.expires_in // 3600')
    refresh_token=$(echo "$response" | jq -r '.refresh_token // empty')

    local now expires_at
    now=$(date +%s)
    expires_at=$((now + expires_in))

    jq -n \
        --arg access_token "$access_token" \
        --argjson expires_at "$expires_at" \
        --arg refresh_token "${refresh_token}" \
        --arg token_type "bearer" \
        '{
            access_token: $access_token,
            expires_at: $expires_at,
            refresh_token: $refresh_token,
            token_type: $token_type
        }' > "$output_file"

    chmod 600 "$output_file"
}

# ── Public token getters ──────────────────────────────────────

# Get a valid app token (client_credentials). Auto-acquires & caches.
# Usage: TOKEN=$(get_app_token)
get_app_token() {
    if _token_is_valid "$APP_TOKEN_FILE"; then
        jq -r '.access_token' "$APP_TOKEN_FILE"
        return 0
    fi

    # Try refresh
    if [ -f "$APP_TOKEN_FILE" ]; then
        local refresh_token
        refresh_token=$(jq -r '.refresh_token // empty' "$APP_TOKEN_FILE")
        if [ -n "$refresh_token" ] && _refresh_token "$refresh_token" "$APP_TOKEN_FILE"; then
            jq -r '.access_token' "$APP_TOKEN_FILE"
            return 0
        fi
    fi

    # New token
    _fetch_client_credentials
    jq -r '.access_token' "$APP_TOKEN_FILE"
}

# Get a user token for write operations.
# Checks: SOUNDCLOUD_USER_TOKEN env → cached file → error with instructions
# Usage: TOKEN=$(get_user_token)
get_user_token() {
    # Check env var first
    if [ -n "$SOUNDCLOUD_USER_TOKEN" ]; then
        echo "$SOUNDCLOUD_USER_TOKEN"
        return 0
    fi

    # Check cached
    if _token_is_valid "$USER_TOKEN_FILE"; then
        jq -r '.access_token' "$USER_TOKEN_FILE"
        return 0
    fi

    # Try refresh
    if [ -f "$USER_TOKEN_FILE" ]; then
        local refresh_token
        refresh_token=$(jq -r '.refresh_token // empty' "$USER_TOKEN_FILE")
        if [ -n "$refresh_token" ] && _refresh_token "$refresh_token" "$USER_TOKEN_FILE"; then
            jq -r '.access_token' "$USER_TOKEN_FILE"
            return 0
        fi
    fi

    echo -e "${RED}Error: No valid user token available${NC}" >&2
    echo "" >&2
    echo "User-level operations (create playlists, like tracks, follow users)" >&2
    echo "require an OAuth user token. To get one:" >&2
    echo "" >&2
    echo "  Option 1: Run the OAuth helper:" >&2
    echo "    ./scripts/auth_soundcloud.sh" >&2
    echo "" >&2
    echo "  Option 2: Set your token in the environment:" >&2
    echo "    export SOUNDCLOUD_USER_TOKEN=\"your_oauth_token\"" >&2
    echo "" >&2
    return 1
}

# Save a user token (called by auth_soundcloud.sh after OAuth flow)
# Usage: save_user_token "access_token" "refresh_token" "expires_in"
save_user_token() {
    local access_token="$1"
    local refresh_token="${2:-}"
    local expires_in="${3:-21599}"

    local now expires_at
    now=$(date +%s)
    expires_at=$((now + expires_in))

    jq -n \
        --arg access_token "$access_token" \
        --argjson expires_at "$expires_at" \
        --arg refresh_token "${refresh_token}" \
        --arg token_type "bearer" \
        '{
            access_token: $access_token,
            expires_at: $expires_at,
            refresh_token: $refresh_token,
            token_type: $token_type
        }' > "$USER_TOKEN_FILE"

    chmod 600 "$USER_TOKEN_FILE"
    echo -e "${GREEN}✓ User token saved${NC}" >&2
}

# ── API call wrappers ─────────────────────────────────────────

# Make an authenticated GET request (uses app token)
sc_api_get() {
    local path="$1"
    local token
    token=$(get_app_token) || return 1

    curl -s -L -X GET "https://api.soundcloud.com${path}" \
        -H "Authorization: Bearer ${token}" \
        -H "accept: application/json; charset=utf-8"
}

# Make an authenticated POST (uses user token for write ops)
sc_api_post() {
    local path="$1"
    local payload="$2"
    local token
    token=$(get_user_token) || return 1

    curl -s -X POST "https://api.soundcloud.com${path}" \
        -H "Authorization: Bearer ${token}" \
        -H "Content-Type: application/json" \
        -H "accept: application/json; charset=utf-8" \
        -d "$payload"
}

# Make an authenticated PUT (uses user token)
sc_api_put() {
    local path="$1"
    local payload="$2"
    local token
    token=$(get_user_token) || return 1

    curl -s -X PUT "https://api.soundcloud.com${path}" \
        -H "Authorization: Bearer ${token}" \
        -H "Content-Type: application/json" \
        -H "accept: application/json; charset=utf-8" \
        -d "$payload"
}

# Make an authenticated DELETE (uses user token)
sc_api_delete() {
    local path="$1"
    local token
    token=$(get_user_token) || return 1

    curl -s -X DELETE "https://api.soundcloud.com${path}" \
        -H "Authorization: Bearer ${token}" \
        -H "accept: application/json; charset=utf-8"
}

# ── Status & management ───────────────────────────────────────

_token_status() {
    local label="$1"
    local file="$2"

    echo -e "${YELLOW}${label}:${NC}"
    if [ -f "$file" ]; then
        local expires_at now remaining
        expires_at=$(jq -r '.expires_at // 0' "$file")
        now=$(date +%s)
        remaining=$((expires_at - now))
        if [ "$remaining" -gt 0 ]; then
            echo -e "  ${GREEN}Status:${NC} Valid (expires in $((remaining / 60))m $((remaining % 60))s)"
        else
            echo -e "  ${RED}Status:${NC} Expired"
        fi
        echo -e "  Refresh token: $([ -n "$(jq -r '.refresh_token // empty' "$file")" ] && echo "${GREEN}available${NC}" || echo "${YELLOW}none${NC}")"
    else
        echo -e "  ${RED}Status:${NC} Not cached"
    fi
}

sc_token_status() {
    echo -e "${YELLOW}=== SoundCloud Token Status ===${NC}"
    _token_status "App token (public reads)" "$APP_TOKEN_FILE"
    echo ""
    _token_status "User token (playlists/likes)" "$USER_TOKEN_FILE"
    if [ -n "$SOUNDCLOUD_USER_TOKEN" ]; then
        echo -e "  ${GREEN}SOUNDCLOUD_USER_TOKEN env var is also set${NC}"
    fi
}

sc_token_refresh() {
    echo -e "${YELLOW}Refreshing app token...${NC}"
    rm -f "$APP_TOKEN_FILE"
    get_app_token > /dev/null
    echo -e "${GREEN}✓ App token refreshed${NC}"
    sc_token_status
}

# ── Direct execution ──────────────────────────────────────────

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    case "${1:-status}" in
        status)  sc_token_status ;;
        refresh) sc_token_refresh ;;
        app)     get_app_token && echo "" ;;
        user)    get_user_token && echo "" ;;
        test)
            echo -e "${YELLOW}Testing app token...${NC}"
            RESPONSE=$(sc_api_get "/tracks?q=test&limit=1")
            if echo "$RESPONSE" | jq -e '.[0].id' >/dev/null 2>&1; then
                echo -e "${GREEN}✓ App token works — public API accessible${NC}"
                echo "Sample: $(echo "$RESPONSE" | jq -r '.[0].title')"
            else
                echo -e "${RED}✗ App token test failed${NC}"
            fi

            echo ""
            echo -e "${YELLOW}Testing user token...${NC}"
            if USER_RESPONSE=$(sc_api_get "/me" 2>/dev/null); then
                :
            fi
            # For user token test we need to use the user token directly
            UT=$(get_user_token 2>/dev/null) || true
            if [ -n "$UT" ]; then
                UR=$(curl -s "https://api.soundcloud.com/me" \
                    -H "Authorization: Bearer ${UT}" \
                    -H "accept: application/json; charset=utf-8")
                if echo "$UR" | jq -e '.id' >/dev/null 2>&1; then
                    echo -e "${GREEN}✓ User token works — authenticated as $(echo "$UR" | jq -r '.username')${NC}"
                else
                    echo -e "${RED}✗ User token test failed${NC}"
                fi
            else
                echo -e "${YELLOW}⚠ No user token available (needed for playlist creation, likes, etc.)${NC}"
                echo "  Run: ./scripts/auth_soundcloud.sh"
            fi
            ;;
        save-user)
            # Internal: save a user token from auth flow
            save_user_token "$2" "$3" "$4"
            ;;
        *)
            echo "Usage: $0 {status|refresh|app|user|test|save-user}"
            exit 1
            ;;
    esac
fi
