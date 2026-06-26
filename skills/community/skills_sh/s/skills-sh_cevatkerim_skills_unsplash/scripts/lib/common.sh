#!/bin/bash
# Shared functions for all Unsplash scripts

UNSPLASH_API_BASE="https://api.unsplash.com"

# Load .env from project root if it exists
# Project root is 4 levels up from scripts/lib/ (.claude/skills/unsplash/scripts/lib)
load_env() {
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local project_root="$(cd "$script_dir/../../../../.." && pwd)"

    if [ -f "$project_root/.env" ]; then
        # Source .env file, only exporting lines that look like KEY=value
        while IFS='=' read -r key value || [ -n "$key" ]; do
            # Skip comments and empty lines
            [[ "$key" =~ ^#.*$ ]] && continue
            [[ -z "$key" ]] && continue
            # Remove leading/trailing whitespace and quotes from value
            value="${value#\"}"
            value="${value%\"}"
            value="${value#\'}"
            value="${value%\'}"
            # Export the variable
            export "$key=$value"
        done < "$project_root/.env"
    fi
}

# Load .env on source
load_env

# Validate API key exists
validate_api_key() {
    if [ -z "${UNSPLASH_ACCESS_KEY:-}" ]; then
        echo "ERROR: UNSPLASH_ACCESS_KEY not set" >&2
        echo "" >&2
        echo "Setup: Create a .env file in your project root with:" >&2
        echo "  UNSPLASH_ACCESS_KEY=your_access_key_here" >&2
        echo "" >&2
        echo "Get your free API key from: https://unsplash.com/developers" >&2
        return 1
    fi
    return 0
}

# Make API request with error handling
# Usage: api_request "endpoint" "query_params"
api_request() {
    local endpoint="$1"
    local params="$2"

    local response
    response=$(curl -s -w "\n%{http_code}" \
        -H "Accept-Version: v1" \
        -H "Authorization: Client-ID $UNSPLASH_ACCESS_KEY" \
        --max-time 30 \
        "${UNSPLASH_API_BASE}${endpoint}?${params}" 2>&1)

    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    case "$http_code" in
        200) echo "$body" ;;
        401) echo "ERROR: Invalid API key" >&2; return 1 ;;
        403) echo "ERROR: Rate limit exceeded (50/hour in demo mode)" >&2; return 1 ;;
        404) echo "ERROR: Resource not found" >&2; return 1 ;;
        *) echo "ERROR: API request failed ($http_code)" >&2; return 1 ;;
    esac
}

# Format photo JSON with attribution
# Converts raw Unsplash API response to our standardized format
format_photos() {
    jq -c 'if type == "array" then . else [.] end | .[] | {
        id: .id,
        description: .description,
        alt_description: .alt_description,
        urls: .urls,
        width: .width,
        height: .height,
        color: .color,
        blur_hash: .blur_hash,
        photographer_name: .user.name,
        photographer_username: .user.username,
        photographer_url: ("https://unsplash.com/@" + .user.username + "?utm_source=claude_skill&utm_medium=referral"),
        photo_url: (.links.html + "?utm_source=claude_skill&utm_medium=referral"),
        attribution_text: ("Photo by " + .user.name + " on Unsplash"),
        attribution_html: ("Photo by <a href=\"https://unsplash.com/@" + .user.username + "?utm_source=claude_skill&utm_medium=referral\">" + .user.name + "</a> on <a href=\"https://unsplash.com/?utm_source=claude_skill&utm_medium=referral\">Unsplash</a>")
    }'
}
