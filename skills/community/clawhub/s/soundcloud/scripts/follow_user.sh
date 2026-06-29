#!/bin/bash
# Follow or unfollow a SoundCloud user (requires user token)
# Usage: ./follow_user.sh USERNAME_OR_ID [--unfollow]

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/auth_token.sh"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'

usage() {
    echo "Usage: $0 USERNAME_OR_ID [options]"
    echo ""
    echo "Options:"
    echo "  --unfollow    Unfollow the user instead of following"
    echo "  --help        Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 chillhop"
    echo "  $0 1234567 --unfollow"
}

[ $# -eq 0 ] && { usage; exit 1; }

USER_INPUT="$1"; shift
UNFOLLOW=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --unfollow) UNFOLLOW=true; shift ;;
        --help) usage; exit 0 ;;
        *) echo -e "${RED}Unknown: $1${NC}"; usage; exit 1 ;;
    esac
done

# Resolve user ID
if [[ "$USER_INPUT" =~ ^[0-9]+$ ]]; then
    USER_ID="$USER_INPUT"
else
    echo -e "${YELLOW}Resolving username: $USER_INPUT${NC}"
    RESOLVED=$(sc_api_get "/resolve?url=https://soundcloud.com/${USER_INPUT}")
    USER_ID=$(echo "$RESOLVED" | jq -r '.id')
    if [ -z "$USER_ID" ] || [ "$USER_ID" = "null" ]; then
        echo -e "${RED}Error: Could not resolve username${NC}"
        exit 1
    fi
    USERNAME=$(echo "$RESOLVED" | jq -r '.username')
    echo -e "${GREEN}Resolved: $USERNAME (ID: $USER_ID)${NC}"
fi

# Get user token
USER_TOKEN=$(get_user_token) || exit 1

if [ "$UNFOLLOW" = true ]; then
    echo -e "${YELLOW}Unfollowing user $USER_ID...${NC}"
    METHOD="DELETE"
else
    echo -e "${YELLOW}Following user $USER_ID...${NC}"
    METHOD="PUT"
fi

RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X "$METHOD" \
    "https://api.soundcloud.com/me/followings/${USER_ID}" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -H "accept: application/json; charset=utf-8")

if [ "$RESPONSE" -eq 200 ] || [ "$RESPONSE" -eq 201 ]; then
    if [ "$UNFOLLOW" = true ]; then
        echo -e "${GREEN}✓ Unfollowed${NC}"
    else
        echo -e "${GREEN}✓ Following!${NC}"
    fi
else
    echo -e "${RED}Error: Request failed (HTTP $RESPONSE)${NC}"
    exit 1
fi
