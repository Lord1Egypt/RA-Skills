#!/bin/bash
# Local Tunnel Helper Script
# Usage: ./tunnel.sh <port> [method]
# Methods: ngrok (default), localhost.run, cloudflared

PORT=${1:-3000}
METHOD=${2:-localhost.run}

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🚀 Starting tunnel for localhost:${PORT}...${NC}"

# Check if local server is running
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${PORT}" 2>/dev/null)
if [[ "$HTTP_CODE" != "200" && "$HTTP_CODE" != "304" && "$HTTP_CODE" != "301" && "$HTTP_CODE" != "302" ]]; then
    echo -e "${RED}⚠️  Warning: No server detected on port ${PORT} (HTTP ${HTTP_CODE})${NC}"
    echo "Make sure your local server is running first."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

case $METHOD in
    "ngrok")
        if ! command -v ngrok &> /dev/null; then
            echo -e "${RED}ngrok not installed.${NC}"
            echo "Install: brew install ngrok (macOS) or npm i -g ngrok"
            exit 1
        fi
        echo -e "${GREEN}Using ngrok — dashboard at http://127.0.0.1:4040${NC}"
        ngrok http ${PORT}
        ;;
    "localhost.run"|"lr")
        echo -e "${GREEN}Using localhost.run (SSH tunnel, no install needed)${NC}"
        echo "Look for URL like: https://XXXXX.lhr.life"
        echo "---"
        ssh -o StrictHostKeyChecking=no -R 80:localhost:${PORT} nokey@localhost.run
        ;;
    "cloudflared"|"cf")
        if ! command -v cloudflared &> /dev/null; then
            echo -e "${RED}cloudflared not installed.${NC}"
            echo "Install: brew install cloudflared"
            exit 1
        fi
        echo -e "${GREEN}Using cloudflared${NC}"
        cloudflared tunnel --url http://localhost:${PORT}
        ;;
    *)
        echo -e "${RED}Unknown method: ${METHOD}${NC}"
        echo "Available: ngrok (default), localhost.run (lr), cloudflared (cf)"
        exit 1
        ;;
esac
