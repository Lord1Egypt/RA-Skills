#!/bin/bash
# Search SoundCloud tracks with various filters

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/auth_token.sh"

# Default values
LIMIT=20
OUTPUT_FORMAT="human"
GENRE=""
BPM_MIN=""
BPM_MAX=""
DURATION_MIN=""
DURATION_MAX=""
SORT="hotness"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    echo "Usage: $0 \"search query\" [options]"
    echo ""
    echo "Options:"
    echo "  --limit N          Number of results (default: 20)"
    echo "  --genre \"genre\"    Filter by genre"
    echo "  --bpm-min N        Minimum BPM"
    echo "  --bpm-max N        Maximum BPM"
    echo "  --duration-min N   Minimum duration in seconds"
    echo "  --duration-max N   Maximum duration in seconds"
    echo "  --sort \"field\"     Sort by: created_at, hotness, plays, likes (default: hotness)"
    echo "  --json             Output raw JSON"
    echo "  --csv              Output CSV format"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 \"lofi hip hop\" --limit 10 --genre \"lofi\""
    echo "  $0 \"jazz\" --bpm-min 70 --bpm-max 90 --csv"
}

build_url() {
    local query="$1"
    # URL-encode the query
    local encoded_query
    encoded_query=$(echo -n "$query" | jq -sRr '@uri')
    local url="/tracks?q=${encoded_query}&limit=${LIMIT}"

    [ -n "$GENRE" ] && url="${url}&genre=${GENRE}"
    [ -n "$BPM_MIN" ] && url="${url}&bpm[from]=${BPM_MIN}"
    [ -n "$BPM_MAX" ] && url="${url}&bpm[to]=${BPM_MAX}"
    [ -n "$DURATION_MIN" ] && url="${url}&duration[from]=${DURATION_MIN}000"
    [ -n "$DURATION_MAX" ] && url="${url}&duration[to]=${DURATION_MAX}000"
    [ -n "$SORT" ] && url="${url}&order=${SORT}"

    echo "$url"
}

format_duration() {
    local ms=$1
    local seconds=$((ms / 1000))
    local minutes=$((seconds / 60))
    local remaining_seconds=$((seconds % 60))
    printf "%d:%02d" $minutes $remaining_seconds
}

format_human() {
    local json="$1"
    local count
    count=$(echo "$json" | jq '. | length')

    echo -e "${GREEN}Found $count tracks:${NC}"
    echo ""

    # Output one JSON object per line, then format each in bash
    echo "$json" | jq -c '.[]' | while read -r track; do
        local id title artist duration genre plays likes url
        id=$(echo "$track" | jq -r '.id')
        title=$(echo "$track" | jq -r '.title')
        artist=$(echo "$track" | jq -r '.user.username // "Unknown"')
        duration=$(echo "$track" | jq -r '.duration // 0')
        genre=$(echo "$track" | jq -r '.genre // "N/A"')
        plays=$(echo "$track" | jq -r '.playback_count // 0')
        likes=$(echo "$track" | jq -r '.favoritings_count // .likes_count // 0')
        url=$(echo "$track" | jq -r '.permalink_url // ""')

        formatted_duration=$(format_duration "$duration")
        echo -e "${BLUE}ID:${NC} $id"
        echo -e "  ${YELLOW}Title:${NC} $title"
        echo -e "  ${YELLOW}Artist:${NC} $artist"
        echo -e "  ${YELLOW}Duration:${NC} $formatted_duration"
        echo -e "  ${YELLOW}Genre:${NC} $genre"
        echo -e "  ${YELLOW}Plays:${NC} $plays"
        echo -e "  ${YELLOW}Likes:${NC} $likes"
        echo -e "  ${YELLOW}URL:${NC} $url"
        echo ""
    done
}

format_csv() {
    local json="$1"
    echo "id,title,artist,duration_seconds,genre,plays,likes,url"
    echo "$json" | jq -r '.[] | [.id, .title, (.user.username // "Unknown"), (.duration/1000), (.genre // ""), .playback_count, (.favoritings_count // .likes_count // 0), .permalink_url] | @csv'
}

# --- Main ---
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

QUERY="$1"
shift

while [[ $# -gt 0 ]]; do
    case $1 in
        --limit) LIMIT="$2"; shift 2 ;;
        --genre) GENRE="$2"; shift 2 ;;
        --bpm-min) BPM_MIN="$2"; shift 2 ;;
        --bpm-max) BPM_MAX="$2"; shift 2 ;;
        --duration-min) DURATION_MIN="$2"; shift 2 ;;
        --duration-max) DURATION_MAX="$2"; shift 2 ;;
        --sort) SORT="$2"; shift 2 ;;
        --json) OUTPUT_FORMAT="json"; shift ;;
        --csv) OUTPUT_FORMAT="csv"; shift ;;
        --help) usage; exit 0 ;;
        *) echo -e "${RED}Unknown option: $1${NC}"; usage; exit 1 ;;
    esac
done

# Build path and make API call
URL_PATH=$(build_url "$QUERY")
echo -e "${YELLOW}Searching SoundCloud...${NC}" >&2

RESPONSE=$(sc_api_get "$URL_PATH")

# Check if response is valid JSON
if ! echo "$RESPONSE" | jq -e . >/dev/null 2>&1; then
    echo -e "${RED}Error: Invalid JSON response from SoundCloud API${NC}"
    echo "Response: $RESPONSE"
    exit 1
fi

# Check for API errors
if echo "$RESPONSE" | jq -e '.error or .errors' >/dev/null 2>&1; then
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.message // .error // "Unknown error"')
    echo -e "${RED}API Error: $ERROR_MSG${NC}"
    exit 1
fi

# Check if empty
if echo "$RESPONSE" | jq -e 'type == "array" and length == 0' >/dev/null 2>&1; then
    echo -e "${YELLOW}No tracks found${NC}"
    exit 0
fi

# Output
case $OUTPUT_FORMAT in
    human) format_human "$RESPONSE" ;;
    json)   echo "$RESPONSE" | jq '.' ;;
    csv)    format_csv "$RESPONSE" ;;
    *)      format_human "$RESPONSE" ;;
esac
