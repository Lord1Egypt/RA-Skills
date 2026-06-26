#!/bin/bash
# Whoop Fetcher - Self-contained WHOOP data fetcher
# All paths are relative to skill directory

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$SKILL_DIR/data"
CRED_FILE="$HOME/.clawdbot/whoop-credentials.env"

# Create data directory
mkdir -p "$DATA_DIR"

# Source credentials
if [ -f "$CRED_FILE" ]; then
    source "$CRED_FILE"
else
    echo "Error: Credentials file not found at $CRED_FILE"
    exit 1
fi

# Check credentials
if [ -z "$WHOOP_CLIENT_ID" ] || [ -z "$WHOOP_CLIENT_SECRET" ] || [ -z "$WHOOP_REFRESH_TOKEN" ]; then
    echo "Error: WHOOP credentials not configured"
    echo "Please set WHOOP_CLIENT_ID, WHOOP_CLIENT_SECRET, WHOOP_REFRESH_TOKEN in $CRED_FILE"
    exit 1
fi

# Token file
TOKEN_FILE="$HOME/.clawdbot/whoop-tokens.json"
mkdir -p "$(dirname "$TOKEN_FILE")"

# Get access token
get_access_token() {
    local response=$(curl -s -X POST "https://api.prod.whoop.com/oauth/oauth2/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "grant_type=refresh_token" \
        -d "refresh_token=$WHOOP_REFRESH_TOKEN" \
        -d "client_id=$WHOOP_CLIENT_ID" \
        -d "client_secret=$WHOOP_CLIENT_SECRET")
    
    echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('access_token',''))" 2>/dev/null
}

# Fetch data
fetch_data() {
    local endpoint="$1"
    local days="${2:-7}"
    local token=$(get_access_token)
    
    if [ -z "$token" ]; then
        echo "Error: Failed to get access token"
        return 1
    fi
    
    curl -s -X GET "https://api.prod.whoop.com/developer/v2/${endpoint}?days=${days}" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json"
}

# Parse arguments
ENDPOINT="${1:-all}"
DAYS="${2:-7}"

if [ "$ENDPOINT" = "all" ]; then
    echo "Fetching cycles..."
    fetch_data "cycles" "$DAYS" > "$DATA_DIR/cycles_raw.json"
    echo "Fetching sleep..."
    fetch_data "sleep" "$DAYS" > "$DATA_DIR/sleep_raw.json"
    echo "Fetching recovery..."
    fetch_data "recovery" "$DAYS" > "$DATA_DIR/recovery_raw.json"
    echo "Done!"
else
    fetch_data "$ENDPOINT" "$DAYS" > "$DATA_DIR/${ENDPOINT}_raw.json"
    echo "Fetched $ENDPOINT data"
fi
