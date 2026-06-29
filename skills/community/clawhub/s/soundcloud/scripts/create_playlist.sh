#!/bin/bash
# Create a SoundCloud playlist (requires user token)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/auth_token.sh"

# Default values
DESCRIPTION=""
TRACKS=""
SHARING="public"
GENRE=""
TAGS=""
CONFIRM=true

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    echo "Usage: $0 \"Playlist Name\" [options]"
    echo ""
    echo "Options:"
    echo "  --description \"text\"    Playlist description"
    echo "  --tracks \"id1,id2,id3\"  Comma-separated track IDs to add"
    echo "  --sharing \"public|private\"  Sharing setting (default: public)"
    echo "  --genre \"genre\"         Set playlist genre"
    echo "  --tags \"tag1,tag2\"      Comma-separated tags"
    echo "  --no-confirm           Skip confirmation prompt"
    echo "  --help                 Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 \"My Chill Mix\" --description \"Relaxing tracks\" --tracks \"12345,67890\""
    echo "  $0 \"Private Collection\" --sharing private --no-confirm"
    echo ""
    echo "Note: Requires a user token. Run ./scripts/auth_soundcloud.sh first."
}

validate_tracks() {
    local tracks="$1"
    [ -z "$tracks" ] && return 0

    IFS=',' read -ra TRACK_ARRAY <<< "$tracks"
    for track in "${TRACK_ARRAY[@]}"; do
        if ! [[ "$track" =~ ^[0-9]+$ ]]; then
            echo -e "${RED}Error: Invalid track ID '$track'. Must be numeric.${NC}" >&2
            return 1
        fi
    done
    return 0
}

build_playlist_payload() {
    local title="$1"
    # Use jq to build proper JSON safely
    jq -n \
        --arg title "$title" \
        --arg description "$DESCRIPTION" \
        --arg sharing "$SHARING" \
        --arg genre "$GENRE" \
        --arg tag_list "$TAGS" \
        '{
            playlist: {
                title: $title,
                sharing: $sharing
            }
            + (if $description != "" then {description: $description} else {} end)
            + (if $genre != "" then {genre: $genre} else {} end)
            + (if $tag_list != "" then {tag_list: $tag_list} else {} end)
        }'
}

add_tracks_to_playlist() {
    local playlist_id="$1"
    local tracks="$2"
    local token="$3"

    [ -z "$tracks" ] && return 0

    # Get current playlist tracks
    local current
    current=$(curl -s -X GET "https://api.soundcloud.com/playlists/${playlist_id}" \
        -H "Authorization: Bearer ${token}" \
        -H "accept: application/json; charset=utf-8")

    local existing_tracks
    existing_tracks=$(echo "$current" | jq -r '.tracks[]?.id' 2>/dev/null | tr '\n' ',' | sed 's/,$//')

    local all_tracks
    if [ -n "$existing_tracks" ]; then
        all_tracks="${existing_tracks},${tracks}"
    else
        all_tracks="$tracks"
    fi

    # Deduplicate
    local unique_tracks
    unique_tracks=$(echo "$all_tracks" | tr ',' '\n' | sort -u | tr '\n' ',' | sed 's/,$//')

    # Build track array JSON
    local track_json
    track_json=$(echo "$unique_tracks" | tr ',' '\n' | jq -R '{id: . | tonumber}' | jq -s '.')

    local update_payload
    update_payload=$(jq -n --argjson tracks "$track_json" '{playlist: {tracks: $tracks}}')

    # Use app token for PUT (playlist update requires user token actually)
    curl -s -X PUT "https://api.soundcloud.com/playlists/${playlist_id}" \
        -H "Authorization: Bearer ${token}" \
        -H "Content-Type: application/json" \
        -H "accept: application/json; charset=utf-8" \
        -d "$update_payload"
}

# --- Main ---
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

PLAYLIST_TITLE="$1"
shift

while [[ $# -gt 0 ]]; do
    case $1 in
        --description) DESCRIPTION="$2"; shift 2 ;;
        --tracks) TRACKS="$2"; shift 2 ;;
        --sharing)
            SHARING="$2"
            if [[ ! "$SHARING" =~ ^(public|private)$ ]]; then
                echo -e "${RED}Error: Sharing must be 'public' or 'private'${NC}"
                exit 1
            fi
            shift 2 ;;
        --genre) GENRE="$2"; shift 2 ;;
        --tags) TAGS="$2"; shift 2 ;;
        --no-confirm) CONFIRM=false; shift ;;
        --help) usage; exit 0 ;;
        *) echo -e "${RED}Unknown option: $1${NC}"; usage; exit 1 ;;
    esac
done

# Validate
if ! validate_tracks "$TRACKS"; then
    exit 1
fi

# Get user token (playlist creation requires user auth)
USER_TOKEN=$(get_user_token) || exit 1

# Confirm
if [ "$CONFIRM" = true ]; then
    echo -e "${BLUE}=== Playlist Creation ===${NC}"
    echo -e "${YELLOW}Title:${NC} $PLAYLIST_TITLE"
    echo -e "${YELLOW}Description:${NC} ${DESCRIPTION:-(none)}"
    echo -e "${YELLOW}Sharing:${NC} $SHARING"
    echo -e "${YELLOW}Genre:${NC} ${GENRE:-(none)}"
    echo -e "${YELLOW}Tags:${NC} ${TAGS:-(none)}"
    if [ -n "$TRACKS" ]; then
        TRACK_COUNT=$(echo "$TRACKS" | tr ',' '\n' | wc -l)
        echo -e "${YELLOW}Tracks:${NC} $TRACK_COUNT track(s)"
    else
        echo -e "${YELLOW}Tracks:${NC} (empty playlist)"
    fi
    echo ""
    read -p "Create this playlist? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Cancelled${NC}"
        exit 0
    fi
fi

# Create playlist
PAYLOAD=$(build_playlist_payload "$PLAYLIST_TITLE")
echo -e "${YELLOW}Creating playlist...${NC}"

RESPONSE=$(curl -s -X POST "https://api.soundcloud.com/playlists" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -H "Content-Type: application/json" \
    -H "accept: application/json; charset=utf-8" \
    -d "$PAYLOAD")

if ! echo "$RESPONSE" | jq -e '.id' >/dev/null 2>&1; then
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.message // .error // "Unknown error"')
    echo -e "${RED}Error: Failed to create playlist${NC}"
    echo "Response: $RESPONSE"
    exit 1
fi

PLAYLIST_ID=$(echo "$RESPONSE" | jq -r '.id')
PLAYLIST_URL=$(echo "$RESPONSE" | jq -r '.permalink_url')

echo -e "${GREEN}✓ Playlist created!${NC}"
echo -e "${BLUE}ID:${NC} $PLAYLIST_ID"
echo -e "${BLUE}URL:${NC} $PLAYLIST_URL"

# Add tracks if specified
if [ -n "$TRACKS" ]; then
    echo -e "${YELLOW}Adding tracks...${NC}"
    if add_tracks_to_playlist "$PLAYLIST_ID" "$TRACKS" "$USER_TOKEN"; then
        echo -e "${GREEN}✓ Tracks added${NC}"
    else
        echo -e "${YELLOW}⚠ Playlist created but tracks could not be added${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Done: $PLAYLIST_URL${NC}"
