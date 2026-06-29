#!/bin/bash
# Batch operations on SoundCloud tracks/playlists

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/auth_token.sh"

# Defaults
ACTION=""
INPUT_FILE=""
PLAYLIST_ID=""
DELAY=1
VERBOSE=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    echo "Usage: $0 [action] [file] [options]"
    echo ""
    echo "Actions:"
    echo "  like-tracks           Like multiple tracks from file"
    echo "  unlike-tracks         Unlike multiple tracks from file"
    echo "  add-to-playlist       Add tracks to playlist from file"
    echo "  download-metadata     Download metadata for multiple tracks"
    echo "  check-availability    Check if tracks are still available"
    echo ""
    echo "Options:"
    echo "  --playlist-id ID      Playlist ID (required for add-to-playlist)"
    echo "  --delay SECONDS       Delay between requests (default: 1)"
    echo "  --verbose             Show detailed output"
    echo "  --help                Show this help message"
    echo ""
    echo "File format: One track ID per line, or CSV with IDs in first column"
    echo ""
    echo "Examples:"
    echo "  $0 like-tracks track_ids.txt"
    echo "  $0 add-to-playlist tracks.csv --playlist-id 123456"
    echo "  $0 download-metadata ids.txt --delay 2 --verbose"
    echo ""
    echo "Note: like-tracks, unlike-tracks, and add-to-playlist require a user token."
}

read_track_ids() {
    local file="$1"
    [ -f "$file" ] || { echo -e "${RED}Error: File not found: $file${NC}" >&2; exit 1; }

    if [[ "$file" == *.csv ]]; then
        tail -n +2 "$file" | cut -d',' -f1 | grep -E '^[0-9]+$' || true
    else
        grep -E '^[0-9]+$' "$file" || true
    fi
}

like_tracks() {
    local file="$1"
    local action="$2"  # PUT for like, DELETE for unlike
    local token
    token=$(get_user_token) || exit 1

    local track_ids
    track_ids=$(read_track_ids "$file")
    local total
    total=$(echo "$track_ids" | grep -c . || echo 0)
    local success=0
    local failed=0

    local verb="Liking"
    [ "$action" = "DELETE" ] && verb="Unliking"
    echo -e "${YELLOW}${verb} $total tracks...${NC}"

    while read -r track_id; do
        [ -z "$track_id" ] && continue

        [ "$VERBOSE" = true ] && echo -n "${verb} track $track_id... "

        if [ "$action" = "DELETE" ]; then
            RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE \
                "https://api.soundcloud.com/me/favorites/${track_id}" \
                -H "Authorization: Bearer ${token}" \
                -H "accept: application/json; charset=utf-8")
        else
            RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT \
                "https://api.soundcloud.com/me/favorites/${track_id}" \
                -H "Authorization: Bearer ${token}" \
                -H "accept: application/json; charset=utf-8")
        fi

        if [ "$RESPONSE" -eq 200 ] || [ "$RESPONSE" -eq 201 ]; then
            [ "$VERBOSE" = true ] && echo -e "${GREEN}OK${NC}"
            ((success++))
        else
            [ "$VERBOSE" = true ] && echo -e "${RED}FAILED (HTTP $RESPONSE)${NC}"
            ((failed++))
        fi

        sleep "$DELAY"
    done <<< "$track_ids"

    echo -e "${GREEN}Done: $success succeeded, $failed failed${NC}"
}

add_to_playlist() {
    local file="$1"
    local playlist_id="$2"
    local token
    token=$(get_user_token) || exit 1

    [ -z "$playlist_id" ] && { echo -e "${RED}Error: --playlist-id required${NC}" >&2; exit 1; }

    local track_ids
    track_ids=$(read_track_ids "$file")
    local total
    total=$(echo "$track_ids" | grep -c . || echo 0)
    echo -e "${YELLOW}Adding $total tracks to playlist $playlist_id...${NC}"

    # Get current playlist
    [ "$VERBOSE" = true ] && echo "Fetching current playlist..."
    local current
    current=$(curl -s -X GET "https://api.soundcloud.com/playlists/${playlist_id}" \
        -H "Authorization: Bearer ${token}" \
        -H "accept: application/json; charset=utf-8")

    local existing new_tracks
    existing=$(echo "$current" | jq -r '.tracks[]?.id' 2>/dev/null | tr '\n' ',' | sed 's/,$//')
    new_tracks=$(echo "$track_ids" | tr '\n' ',' | sed 's/,$//')

    local all_tracks
    [ -n "$existing" ] && all_tracks="${existing},${new_tracks}" || all_tracks="$new_tracks"

    local unique_tracks unique_count existing_count
    unique_tracks=$(echo "$all_tracks" | tr ',' '\n' | sort -u | tr '\n' ',' | sed 's/,$//')
    unique_count=$(echo "$unique_tracks" | tr ',' '\n' | grep -c . || echo 0)
    existing_count=$(echo "$existing" | tr ',' '\n' | grep -c . || echo 0)
    local new_count=$((unique_count - existing_count))

    echo -e "${YELLOW}Adding $new_count new tracks (playlist has $existing_count)${NC}"

    local track_json
    track_json=$(echo "$unique_tracks" | tr ',' '\n' | jq -R '{id: . | tonumber}' | jq -s '.')
    local payload
    payload=$(jq -n --argjson tracks "$track_json" '{playlist: {tracks: $tracks}}')

    echo "Updating playlist..."
    local response
    response=$(curl -s -X PUT "https://api.soundcloud.com/playlists/${playlist_id}" \
        -H "Authorization: Bearer ${token}" \
        -H "Content-Type: application/json" \
        -H "accept: application/json; charset=utf-8" \
        -d "$payload")

    if echo "$response" | jq -e '.id' >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Updated playlist with $unique_count tracks${NC}"
        echo -e "${BLUE}URL:${NC} $(echo "$response" | jq -r '.permalink_url')"
    else
        echo -e "${RED}Error: $(echo "$response" | jq -r '.message // "Unknown"')${NC}"
        exit 1
    fi
}

download_metadata() {
    local file="$1"
    local track_ids
    track_ids=$(read_track_ids "$file")
    local total
    total=$(echo "$track_ids" | grep -c . || echo 0)
    local success=0
    local failed=0

    echo -e "${YELLOW}Downloading metadata for $total tracks...${NC}"

    local output_file="soundcloud_metadata_$(date +%Y%m%d_%H%M%S).json"
    echo "[" > "$output_file"

    local first=true
    while read -r track_id; do
        [ -z "$track_id" ] && continue

        [ "$VERBOSE" = true ] && echo -n "Track $track_id... "

        local response
        response=$(sc_api_get "/tracks/${track_id}")

        if echo "$response" | jq -e '.id' >/dev/null 2>&1; then
            [ "$VERBOSE" = true ] && echo -e "${GREEN}OK${NC}"
            [ "$first" = true ] && first=false || echo "," >> "$output_file"
            echo "$response" >> "$output_file"
            ((success++))
        else
            [ "$VERBOSE" = true ] && echo -e "${RED}FAILED${NC}"
            ((failed++))
        fi

        sleep "$DELAY"
    done <<< "$track_ids"

    echo "]" >> "$output_file"

    echo -e "${GREEN}Done: $success succeeded, $failed failed${NC}"
    echo -e "${BLUE}Saved to:${NC} $output_file"
}

check_availability() {
    local file="$1"
    local track_ids
    track_ids=$(read_track_ids "$file")
    local total
    total=$(echo "$track_ids" | grep -c . || echo 0)
    local available=0
    local unavailable=0

    echo -e "${YELLOW}Checking $total tracks...${NC}"

    local output_file="soundcloud_availability_$(date +%Y%m%d_%H%M%S).csv"
    echo "track_id,available,title,artist,plays,likes" > "$output_file"

    while read -r track_id; do
        [ -z "$track_id" ] && continue

        [ "$VERBOSE" = true ] && echo -n "Track $track_id... "

        local response
        response=$(sc_api_get "/tracks/${track_id}")

        if echo "$response" | jq -e '.id' >/dev/null 2>&1; then
            [ "$VERBOSE" = true ] && echo -e "${GREEN}AVAILABLE${NC}"
            local title artist plays likes
            title=$(echo "$response" | jq -r '.title | @csv')
            artist=$(echo "$response" | jq -r '.user.username // "Unknown" | @csv')
            plays=$(echo "$response" | jq -r '.playback_count // 0')
            likes=$(echo "$response" | jq -r '.favoritings_count // 0')
            echo "$track_id,true,$title,$artist,$plays,$likes" >> "$output_file"
            ((available++))
        else
            [ "$VERBOSE" = true ] && echo -e "${RED}UNAVAILABLE${NC}"
            echo "$track_id,false,,,0,0" >> "$output_file"
            ((unavailable++))
        fi

        sleep "$DELAY"
    done <<< "$track_ids"

    echo -e "${GREEN}Done: $available available, $unavailable unavailable${NC}"
    echo -e "${BLUE}Saved to:${NC} $output_file"
}

# --- Main ---
[ $# -eq 0 ] && { usage; exit 1; }

ACTION="$1"; shift
[ $# -eq 0 ] && { echo -e "${RED}Error: Input file required${NC}"; usage; exit 1; }
INPUT_FILE="$1"; shift

while [[ $# -gt 0 ]]; do
    case $1 in
        --playlist-id) PLAYLIST_ID="$2"; shift 2 ;;
        --delay) DELAY="$2"; shift 2 ;;
        --verbose) VERBOSE=true; shift ;;
        --help) usage; exit 0 ;;
        *) echo -e "${RED}Unknown option: $1${NC}"; usage; exit 1 ;;
    esac
done

case "$ACTION" in
    like-tracks)       like_tracks "$INPUT_FILE" "PUT" ;;
    unlike-tracks)     like_tracks "$INPUT_FILE" "DELETE" ;;
    add-to-playlist)   add_to_playlist "$INPUT_FILE" "$PLAYLIST_ID" ;;
    download-metadata) download_metadata "$INPUT_FILE" ;;
    check-availability) check_availability "$INPUT_FILE" ;;
    *) echo -e "${RED}Unknown action: $ACTION${NC}"; usage; exit 1 ;;
esac
