#!/bin/bash
# Get playlists for a SoundCloud user

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/auth_token.sh"

# Default values
LIMIT=10
WITH_TRACKS=false
OUTPUT_FORMAT="human"
PUBLIC_ONLY=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    echo "Usage: $0 \"username_or_id\" [options]"
    echo ""
    echo "Options:"
    echo "  --limit N          Number of playlists (default: 10)"
    echo "  --with-tracks      Include track details in output"
    echo "  --json             Output raw JSON"
    echo "  --public-only      Only show public playlists"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 \"chillhop\" --limit 5"
    echo "  $0 \"1234567\" --with-tracks --json"
}

# Resolve username to user ID via the resolve endpoint
resolve_user_id() {
    local identifier="$1"

    # Already numeric = user ID
    if [[ "$identifier" =~ ^[0-9]+$ ]]; then
        echo "$identifier"
        return 0
    fi

    local response
    response=$(sc_api_get "/resolve?url=https://soundcloud.com/${identifier}")

    if echo "$response" | jq -e '.id' >/dev/null 2>&1; then
        echo "$response" | jq -r '.id'
        return 0
    else
        echo -e "${RED}Error: Could not resolve username '$identifier'${NC}" >&2
        return 1
    fi
}

format_human() {
    local json="$1"
    local count
    count=$(echo "$json" | jq '. | length')

    echo -e "${GREEN}Found $count playlists:${NC}"
    echo ""

    # Use jq for formatting to avoid TSV/bash parsing issues
    echo "$json" | jq -r '.[] |
        "ID: \(.id)\n" +
        "  Title: \(.title)\n" +
        "  Tracks: \(.track_count // 0)\n" +
        "  Duration: \(
            (.duration // 0) as $ms |
            ($ms / 1000 | floor) as $sec |
            ($sec / 3600 | floor) as $hr |
            (($sec % 3600) / 60 | floor) as $min |
            ($sec % 60) as $s |
            if $hr > 0 then "\($hr):\("0" + ($min|tostring) | .[-2:]):\("0" + ($s|tostring) | .[-2:])"
            else "\($min):\("0" + ($s|tostring) | .[-2:])" end
        )\n" +
        "  Genre: \(.genre // "N/A")\n" +
        "  URL: \(.permalink_url // "")\n" +
        ""' 2>/dev/null

    # If --with-tracks, show track details per playlist
    if [ "$WITH_TRACKS" = true ]; then
        echo "$json" | jq -r '.[] | .id' | while read -r pid; do
            echo -e "  ${YELLOW}Playlist $pid tracks:${NC}"
            echo "$json" | jq -r ".[] | select(.id == $pid) | .tracks[]? | \"    - \\(.title) by \\(.user.username // \"Unknown\")\"" 2>/dev/null || echo "    (No track details available)"
            echo ""
        done
    fi
}

# --- Main ---
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

USER_IDENTIFIER="$1"
shift

while [[ $# -gt 0 ]]; do
    case $1 in
        --limit) LIMIT="$2"; shift 2 ;;
        --with-tracks) WITH_TRACKS=true; shift ;;
        --json) OUTPUT_FORMAT="json"; shift ;;
        --public-only) PUBLIC_ONLY=true; shift ;;
        --help) usage; exit 0 ;;
        *) echo -e "${RED}Unknown option: $1${NC}"; usage; exit 1 ;;
    esac
done

# Resolve user ID
echo -e "${YELLOW}Resolving user: $USER_IDENTIFIER${NC}" >&2
USER_ID=$(resolve_user_id "$USER_IDENTIFIER") || exit 1
echo -e "${GREEN}Resolved to user ID: $USER_ID${NC}" >&2

# Build URL path
URL_PATH="/users/${USER_ID}/playlists?limit=${LIMIT}"
[ "$PUBLIC_ONLY" = true ] && URL_PATH="${URL_PATH}&public=true"
[ "$WITH_TRACKS" = false ] && URL_PATH="${URL_PATH}&show_tracks=false"

# Make API call
echo -e "${YELLOW}Fetching playlists...${NC}" >&2
RESPONSE=$(sc_api_get "$URL_PATH")

# Validate
if ! echo "$RESPONSE" | jq -e . >/dev/null 2>&1; then
    echo -e "${RED}Error: Invalid JSON response${NC}"
    echo "Response: $RESPONSE"
    exit 1
fi

if echo "$RESPONSE" | jq -e '.error or .errors' >/dev/null 2>&1; then
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.message // .error // "Unknown error"')
    echo -e "${RED}API Error: $ERROR_MSG${NC}"
    exit 1
fi

if echo "$RESPONSE" | jq -e 'type == "array" and length == 0' >/dev/null 2>&1; then
    echo -e "${YELLOW}No playlists found for this user${NC}"
    exit 0
fi

# Output
case $OUTPUT_FORMAT in
    human) format_human "$RESPONSE" ;;
    json)   echo "$RESPONSE" | jq '.' ;;
    *)      format_human "$RESPONSE" ;;
esac
