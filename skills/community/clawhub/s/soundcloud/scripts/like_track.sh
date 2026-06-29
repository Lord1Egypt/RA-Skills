#!/bin/bash
# Like or unlike a SoundCloud track (requires user token)
# Usage: ./like_track.sh TRACK_ID [--unlike]

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/auth_token.sh"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

usage() {
    echo "Usage: $0 TRACK_ID_OR_URL [options]"
    echo ""
    echo "Options:"
    echo "  --unlike    Unlike the track instead of liking it"
    echo "  --help      Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 123456789"
    echo "  $0 https://soundcloud.com/artist/track --unlike"
    echo "  $0 123456789 --unlike"
}

[ $# -eq 0 ] && { usage; exit 1; }

TRACK_INPUT="$1"; shift
UNLIKE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --unlike) UNLIKE=true; shift ;;
        --help) usage; exit 0 ;;
        *) echo -e "${RED}Unknown: $1${NC}"; usage; exit 1 ;;
    esac
done

# Resolve track ID
if [[ "$TRACK_INPUT" =~ ^[0-9]+$ ]]; then
    TRACK_ID="$TRACK_INPUT"
elif [[ "$TRACK_INPUT" =~ soundcloud\.com ]]; then
    echo -e "${YELLOW}Resolving URL...${NC}"
    RESOLVED=$(sc_api_get "/resolve?url=${TRACK_INPUT}")
    TRACK_ID=$(echo "$RESOLVED" | jq -r '.id')
    [ -z "$TRACK_ID" ] || [ "$TRACK_ID" = "null" ] && {
        echo -e "${RED}Error: Could not resolve URL${NC}"
        exit 1
    }
else
    echo -e "${RED}Error: Provide a track ID or SoundCloud URL${NC}"
    exit 1
fi

echo -e "${GREEN}Track ID: $TRACK_ID${NC}"

# Get user token
USER_TOKEN=$(get_user_token) || exit 1

if [ "$UNLIKE" = true ]; then
    echo -e "${YELLOW}Unliking track...${NC}"
    METHOD="DELETE"
else
    echo -e "${YELLOW}Liking track...${NC}"
    METHOD="PUT"
fi

RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X "$METHOD" \
    "https://api.soundcloud.com/me/favorites/${TRACK_ID}" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -H "accept: application/json; charset=utf-8")

if [ "$RESPONSE" -eq 200 ] || [ "$RESPONSE" -eq 201 ]; then
    if [ "$UNLIKE" = true ]; then
        echo -e "${GREEN}✓ Track unliked${NC}"
    else
        echo -e "${GREEN}✓ Track liked!${NC}"
    fi
else
    echo -e "${RED}Error: Request failed (HTTP $RESPONSE)${NC}"
    exit 1
fi
