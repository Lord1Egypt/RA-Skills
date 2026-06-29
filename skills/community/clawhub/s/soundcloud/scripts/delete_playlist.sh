#!/bin/bash
# Delete a SoundCloud playlist (requires user token)
# Usage: ./delete_playlist.sh PLAYLIST_ID [--force]

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/auth_token.sh"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

usage() {
    echo "Usage: $0 PLAYLIST_ID [--force]"
    echo ""
    echo "Options:"
    echo "  --force   Skip confirmation prompt"
    echo "  --help    Show this help"
    echo ""
    echo "Example:"
    echo "  $0 123456"
    echo "  $0 123456 --force"
}

[ $# -eq 0 ] && { usage; exit 1; }

PLAYLIST_ID="$1"; shift
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --force) FORCE=true; shift ;;
        --help) usage; exit 0 ;;
        *) echo -e "${RED}Unknown: $1${NC}"; usage; exit 1 ;;
    esac
done

USER_TOKEN=$(get_user_token) || exit 1

# Fetch playlist to confirm
echo -e "${YELLOW}Fetching playlist...${NC}"
PLAYLIST=$(curl -s -X GET "https://api.soundcloud.com/playlists/${PLAYLIST_ID}" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -H "accept: application/json; charset=utf-8")

if ! echo "$PLAYLIST" | jq -e '.id' >/dev/null 2>&1; then
    echo -e "${RED}Error: Playlist not found or inaccessible${NC}"
    exit 1
fi

PLAYLIST_TITLE=$(echo "$PLAYLIST" | jq -r '.title')
TRACK_COUNT=$(echo "$PLAYLIST" | jq -r '.track_count')

echo -e "${BLUE}Playlist to delete:${NC}"
echo -e "  ${YELLOW}Title:${NC} $PLAYLIST_TITLE"
echo -e "  ${YELLOW}Tracks:${NC} $TRACK_COUNT"
echo -e "  ${YELLOW}ID:${NC} $PLAYLIST_ID"
echo ""

if [ "$FORCE" != true ]; then
    read -p "Delete this playlist? This cannot be undone. (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Cancelled${NC}"
        exit 0
    fi
fi

echo -e "${YELLOW}Deleting...${NC}"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE \
    "https://api.soundcloud.com/playlists/${PLAYLIST_ID}" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -H "accept: application/json; charset=utf-8")

if [ "$RESPONSE" -eq 200 ] || [ "$RESPONSE" -eq 204 ]; then
    echo -e "${GREEN}✓ Playlist deleted: $PLAYLIST_TITLE${NC}"
else
    echo -e "${RED}Error: Deletion failed (HTTP $RESPONSE)${NC}"
    exit 1
fi
