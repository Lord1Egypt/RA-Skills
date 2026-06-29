#!/bin/bash
# Update a SoundCloud playlist (requires user token)
# Usage: ./update_playlist.sh PLAYLIST_ID [options]

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/auth_token.sh"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

usage() {
    echo "Usage: $0 PLAYLIST_ID [options]"
    echo ""
    echo "Options:"
    echo "  --title \"New Title\"       New playlist title"
    echo "  --description \"text\"      New description"
    echo "  --sharing \"public|private\" Change visibility"
    echo "  --genre \"genre\"           Set genre"
    echo "  --tags \"tag1,tag2\"        Set tags"
    echo "  --add-tracks \"id1,id2\"    Add these track IDs"
    echo "  --remove-tracks \"id1,id2\" Remove these track IDs"
    echo "  --set-tracks \"id1,id2\"    Replace all tracks with these"
    echo "  --json                   Output raw JSON response"
    echo "  --help                   Show this help"
    echo ""
    echo "Example:"
    echo "  $0 123456 --title \"My Updated Mix\" --sharing private"
    echo "  $0 123456 --add-tracks \"123,456\""
}

# --- Main ---
[ $# -eq 0 ] && { usage; exit 1; }

PLAYLIST_ID="$1"; shift

[ -z "$PLAYLIST_ID" ] && { echo -e "${RED}Error: Playlist ID required${NC}"; usage; exit 1; }

TITLE=""; DESCRIPTION=""; SHARING=""; GENRE=""; TAGS=""
ADD_TRACKS=""; REMOVE_TRACKS=""; SET_TRACKS=""
JSON_OUT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --title) TITLE="$2"; shift 2 ;;
        --description) DESCRIPTION="$2"; shift 2 ;;
        --sharing) SHARING="$2"; shift 2 ;;
        --genre) GENRE="$2"; shift 2 ;;
        --tags) TAGS="$2"; shift 2 ;;
        --add-tracks) ADD_TRACKS="$2"; shift 2 ;;
        --remove-tracks) REMOVE_TRACKS="$2"; shift 2 ;;
        --set-tracks) SET_TRACKS="$2"; shift 2 ;;
        --json) JSON_OUT=true; shift ;;
        --help) usage; exit 0 ;;
        *) echo -e "${RED}Unknown: $1${NC}"; usage; exit 1 ;;
    esac
done

# Get user token
USER_TOKEN=$(get_user_token) || exit 1

# Fetch current playlist
echo -e "${YELLOW}Fetching current playlist...${NC}"
CURRENT=$(curl -s -X GET "https://api.soundcloud.com/playlists/${PLAYLIST_ID}" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -H "accept: application/json; charset=utf-8")

if ! echo "$CURRENT" | jq -e '.id' >/dev/null 2>&1; then
    echo -e "${RED}Error: Playlist not found or inaccessible${NC}"
    echo "$CURRENT" | jq '.'
    exit 1
fi

# Build update payload from current playlist
PAYLOAD=$(jq -n \
    --arg title "$TITLE" \
    --arg description "$DESCRIPTION" \
    --arg sharing "$SHARING" \
    --arg genre "$GENRE" \
    --arg tag_list "$TAGS" \
    '{
        playlist: {}
        + (if $title != "" then {title: $title} else {} end)
        + (if $description != "" then {description: $description} else {} end)
        + (if $sharing != "" then {sharing: $sharing} else {} end)
        + (if $genre != "" then {genre: $genre} else {} end)
        + (if $tag_list != "" then {tag_list: $tag_list} else {} end)
    }')

# Handle track modifications
TRACK_OP=false
if [ -n "$SET_TRACKS" ] || [ -n "$ADD_TRACKS" ] || [ -n "$REMOVE_TRACKS" ]; then
    TRACK_OP=true
    # Get current track IDs
    CURRENT_TRACKS=$(echo "$CURRENT" | jq -r '.tracks[]?.id' 2>/dev/null | tr '\n' ',' | sed 's/,$//')

    if [ -n "$SET_TRACKS" ]; then
        FINAL_TRACKS="$SET_TRACKS"
    else
        # Start with current tracks
        FINAL_TRACKS="$CURRENT_TRACKS"

        # Add tracks
        if [ -n "$ADD_TRACKS" ]; then
            [ -n "$FINAL_TRACKS" ] && FINAL_TRACKS="${FINAL_TRACKS},${ADD_TRACKS}" || FINAL_TRACKS="$ADD_TRACKS"
        fi

        # Remove tracks
        if [ -n "$REMOVE_TRACKS" ]; then
            IFS=',' read -ra REMOVE_ARRAY <<< "$REMOVE_TRACKS"
            for rid in "${REMOVE_ARRAY[@]}"; do
                FINAL_TRACKS=$(echo "$FINAL_TRACKS" | tr ',' '\n' | grep -v "^${rid}$" | tr '\n' ',' | sed 's/,$//')
            done
        fi
    fi

    # Deduplicate
    FINAL_TRACKS=$(echo "$FINAL_TRACKS" | tr ',' '\n' | sort -u | grep -v '^$' | tr '\n' ',' | sed 's/,$//')

    # Build track JSON and merge into payload
    TRACK_JSON=$(echo "$FINAL_TRACKS" | tr ',' '\n' | grep -v '^$' | jq -R '{id: . | tonumber}' | jq -s '.')
    PAYLOAD=$(echo "$PAYLOAD" | jq --argjson tracks "$TRACK_JSON" '.playlist.tracks = $tracks')
fi

# Update
echo -e "${YELLOW}Updating playlist...${NC}"
RESPONSE=$(curl -s -X PUT "https://api.soundcloud.com/playlists/${PLAYLIST_ID}" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -H "Content-Type: application/json" \
    -H "accept: application/json; charset=utf-8" \
    -d "$PAYLOAD")

if echo "$RESPONSE" | jq -e '.id' >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Playlist updated!${NC}"
    if [ "$JSON_OUT" = true ]; then
        echo "$RESPONSE" | jq '.'
    else
        echo -e "${BLUE}Title:${NC} $(echo "$RESPONSE" | jq -r '.title')"
        echo -e "${BLUE}URL:${NC} $(echo "$RESPONSE" | jq -r '.permalink_url')"
        echo -e "${BLUE}Tracks:${NC} $(echo "$RESPONSE" | jq -r '.track_count')"
    fi
else
    echo -e "${RED}Error: $(echo "$RESPONSE" | jq -r '.message // "Update failed"')${NC}"
    exit 1
fi
