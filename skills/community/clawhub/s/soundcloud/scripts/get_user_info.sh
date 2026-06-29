#!/bin/bash
# Get SoundCloud user profile information
# Usage: ./get_user_info.sh USERNAME_OR_ID [options]

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/auth_token.sh"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'
PURPLE='\033[0;35m'; CYAN='\033[0;36m'; NC='\033[0m'

usage() {
    echo "Usage: $0 USERNAME_OR_ID [options]"
    echo ""
    echo "Options:"
    echo "  --with-tracks N    Show top N tracks (default: 0)"
    echo "  --with-playlists N Show N playlists (default: 0)"
    echo "  --json             Output raw JSON"
    echo "  --help             Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 chillhop"
    echo "  $0 1234567 --with-tracks 5 --with-playlists 3"
}

[ $# -eq 0 ] && { usage; exit 1; }

USER_INPUT="$1"; shift
WITH_TRACKS=0; WITH_PLAYLISTS=0; JSON_OUT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --with-tracks) WITH_TRACKS="$2"; shift 2 ;;
        --with-playlists) WITH_PLAYLISTS="$2"; shift 2 ;;
        --json) JSON_OUT=true; shift ;;
        --help) usage; exit 0 ;;
        *) echo -e "${RED}Unknown: $1${NC}"; usage; exit 1 ;;
    esac
done

# Resolve user
if [[ "$USER_INPUT" =~ ^[0-9]+$ ]]; then
    USER_ID="$USER_INPUT"
    echo -e "${YELLOW}Fetching user $USER_ID...${NC}"
else
    echo -e "${YELLOW}Resolving username: $USER_INPUT${NC}"
    RESOLVED=$(sc_api_get "/resolve?url=https://soundcloud.com/${USER_INPUT}")
    USER_ID=$(echo "$RESOLVED" | jq -r '.id')
    if [ -z "$USER_ID" ] || [ "$USER_ID" = "null" ]; then
        echo -e "${RED}Error: Could not resolve username${NC}"
        exit 1
    fi
    echo -e "${GREEN}Resolved to ID: $USER_ID${NC}"
fi

# Fetch user profile
echo -e "${YELLOW}Fetching profile...${NC}"
USER_DATA=$(sc_api_get "/users/${USER_ID}")

if ! echo "$USER_DATA" | jq -e '.id' >/dev/null 2>&1; then
    echo -e "${RED}Error: User not found${NC}"
    exit 1
fi

if [ "$JSON_OUT" = true ]; then
    echo "$USER_DATA" | jq '.'
    [ "$WITH_TRACKS" -gt 0 ] && echo "$(sc_api_get "/users/${USER_ID}/tracks?limit=${WITH_TRACKS}")" | jq '.'
    [ "$WITH_PLAYLISTS" -gt 0 ] && echo "$(sc_api_get "/users/${USER_ID}/playlists?limit=${WITH_PLAYLISTS}")" | jq '.'
    exit 0
fi

# Display profile
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}          USER PROFILE${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${CYAN}Username:${NC} $(echo "$USER_DATA" | jq -r '.username')"
echo -e "${CYAN}Full Name:${NC} $(echo "$USER_DATA" | jq -r '.full_name // "(not set)"')"
echo -e "${CYAN}User ID:${NC} $USER_ID"
echo -e "${CYAN}Permalink:${NC} $(echo "$USER_DATA" | jq -r '.permalink_url')"
echo ""

# Stats
echo -e "${YELLOW}=== STATISTICS ===${NC}"
echo -e "${CYAN}Track Count:${NC} $(echo "$USER_DATA" | jq -r '.track_count // 0')"
echo -e "${CYAN}Playlist Count:${NC} $(echo "$USER_DATA" | jq -r '.playlist_count // 0')"
echo -e "${CYAN}Followers:${NC} $(echo "$USER_DATA" | jq -r '.followers_count // 0')"
echo -e "${CYAN}Following:${NC} $(echo "$USER_DATA" | jq -r '.followings_count // 0')"
echo -e "${CYAN}Public Favorites:${NC} $(echo "$USER_DATA" | jq -r '.public_favorites_count // 0')"
echo ""

# Location & Bio
echo -e "${YELLOW}=== ABOUT ===${NC}"
CITY=$(echo "$USER_DATA" | jq -r '.city // empty')
COUNTRY=$(echo "$USER_DATA" | jq -r '.country // empty')
if [ -n "$CITY" ] && [ "$CITY" != "null" ]; then
    echo -e "${CYAN}Location:${NC} ${CITY}$([ -n "$COUNTRY" ] && [ "$COUNTRY" != "null" ] && echo ", ${COUNTRY}")"
fi

DESC=$(echo "$USER_DATA" | jq -r '.description // empty')
if [ -n "$DESC" ] && [ "$DESC" != "null" ]; then
    echo -e "${CYAN}Description:${NC} $DESC"
fi

WEBSITE=$(echo "$USER_DATA" | jq -r '.website // empty')
if [ -n "$WEBSITE" ] && [ "$WEBSITE" != "null" ]; then
    echo -e "${CYAN}Website:${NC} $WEBSITE"
fi
echo ""

# Avatar
AVATAR=$(echo "$USER_DATA" | jq -r '.avatar_url // empty')
if [ -n "$AVATAR" ] && [ "$AVATAR" != "null" ]; then
    echo -e "${CYAN}Avatar:${NC} $AVATAR"
fi

# Dates
echo -e "${YELLOW}=== DATES ===${NC}"
CREATED=$(echo "$USER_DATA" | jq -r '.created_at')
echo -e "${CYAN}Joined:${NC} $(date -d "$CREATED" '+%Y-%m-%d' 2>/dev/null || echo "$CREATED")"

echo -e "${BLUE}========================================${NC}"

# Optional: Show tracks
if [ "$WITH_TRACKS" -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}=== TOP ${WITH_TRACKS} TRACKS ===${NC}"
    TRACKS=$(sc_api_get "/users/${USER_ID}/tracks?limit=${WITH_TRACKS}")
    echo "$TRACKS" | jq -r '.[] | "  • \(.title) — \(.playback_count) plays"' 2>/dev/null || echo "  (none)"
fi

# Optional: Show playlists
if [ "$WITH_PLAYLISTS" -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}=== PLAYLISTS (${WITH_PLAYLISTS}) ===${NC}"
    PLAYLISTS=$(sc_api_get "/users/${USER_ID}/playlists?limit=${WITH_PLAYLISTS}")
    echo "$PLAYLISTS" | jq -r '.[] | "  • \(.title) (\(.track_count) tracks)"' 2>/dev/null || echo "  (none)"
fi
