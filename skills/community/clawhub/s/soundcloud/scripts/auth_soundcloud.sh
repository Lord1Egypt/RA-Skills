#!/bin/bash
# SoundCloud OAuth Authentication Helper
# Walks user through authorization_code grant to get a user token
# Required for: playlist creation, liking tracks, following users

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_DIR="${HOME}/.cache/soundcloud"
mkdir -p "$CACHE_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

REDIRECT_URI="http://localhost:8080/callback"
AUTH_ENDPOINT="https://soundcloud.com/connect"
TOKEN_ENDPOINT="https://api.soundcloud.com/oauth2/token"
SCOPES="non-expiring"

# ── Check prerequisites ───────────────────────────────────────

if [ -z "$SOUNDCLOUD_CLIENT_ID" ]; then
    echo -e "${RED}Error: SOUNDCLOUD_CLIENT_ID is not set${NC}"
    echo ""
    echo "You need a SoundCloud app registered at:"
    echo "  https://soundcloud.com/you/apps"
    echo ""
    echo "Then set:"
    echo "  export SOUNDCLOUD_CLIENT_ID=\"your_client_id\""
    echo "  export SOUNDCLOUD_CLIENT_SECRET=\"your_client_secret\""
    exit 1
fi

if [ -z "$SOUNDCLOUD_CLIENT_SECRET" ]; then
    echo -e "${RED}Error: SOUNDCLOUD_CLIENT_SECRET is not set${NC}"
    exit 1
fi

# ── Step 1: Generate authorization URL ────────────────────────

if command -v openssl >/dev/null 2>&1; then
  STATE=$(openssl rand -hex 12 2>/dev/null || echo "sc$(date +%s)")
else
  STATE="sc$(date +%s)$$"
fi

AUTH_URL="${AUTH_ENDPOINT}?client_id=${SOUNDCLOUD_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=${SCOPES}&state=${STATE}"

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}   SoundCloud OAuth Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}Step 1:${NC} Open this URL in your browser:"
echo ""
echo -e "${CYAN}${AUTH_URL}${NC}"
echo ""
echo -e "${YELLOW}Step 2:${NC} Log in and authorize the application"
echo -e "${YELLOW}Step 3:${NC} You'll be redirected to ${CYAN}localhost:8080${NC}"
echo -e "        Copy the ${CYAN}code${NC} parameter from the URL"
echo ""
echo -e "${BLUE}========================================${NC}"
echo ""

# ── Step 2: Start local server to display callback ────────────

echo -e "${YELLOW}Starting a temporary server on port 8080...${NC}"
echo -e "Waiting for the redirect... (press Ctrl+C when done)"
echo ""

# Use Python to catch the callback and display it nicely
python3 -c "
import http.server
import urllib.parse
import sys

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        
        if parsed.path == '/callback':
            code = params.get('code', [None])[0]
            state_val = params.get('state', [None])[0]
            error = params.get('error', [None])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            if error:
                self.wfile.write(f'''
                <html><body style=\"font-family:sans-serif;padding:40px\">
                <h1 style=\"color:red\">Authorization Failed</h1>
                <p>Error: {error}</p>
                <p>You can close this window.</p>
                </body></html>
                '''.encode())
                print(f'ERROR:{error}', flush=True)
            elif code:
                self.wfile.write(f'''
                <html><body style=\"font-family:sans-serif;padding:40px;background:#1a1a1a;color:#fff\">
                <h1 style=\"color:#4CAF50\">✓ Authorization Successful!</h1>
                <p>You can close this window and return to your terminal.</p>
                </body></html>
                '''.encode())
                print(f'CODE:{code}', flush=True)
                if state_val:
                    print(f'STATE:{state_val}', flush=True)
            else:
                self.wfile.write(b'<html><body><h1>No authorization code found</h1></body></html>')
                print('ERROR:no_code', flush=True)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')
    
    def log_message(self, format, *args):
        pass  # Suppress log output

server = http.server.HTTPServer(('127.0.0.1', 8080), Handler)
server.timeout = 120  # 2 min timeout
try:
    server.handle_request()
except KeyboardInterrupt:
    pass
" 2>/dev/null &
SERVER_PID=$!

# Also accept manual paste
echo -e "${YELLOW}Or, paste the authorization code here:${NC}"
echo -n "> "
read -r AUTH_CODE

# Kill server if still running
kill $SERVER_PID 2>/dev/null || true

if [ -z "$AUTH_CODE" ]; then
    echo -e "${RED}No authorization code provided. Aborting.${NC}"
    exit 1
fi

# Clean up the code (remove any whitespace or URL parameters)
AUTH_CODE=$(echo "$AUTH_CODE" | sed 's/&.*//' | xargs)

# ── Step 3: Exchange code for token ───────────────────────────

echo ""
echo -e "${YELLOW}Exchanging code for access token...${NC}"

RESPONSE=$(curl -s -X POST "$TOKEN_ENDPOINT" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "client_id=${SOUNDCLOUD_CLIENT_ID}" \
    -d "client_secret=${SOUNDCLOUD_CLIENT_SECRET}" \
    -d "grant_type=authorization_code" \
    -d "redirect_uri=${REDIRECT_URI}" \
    -d "code=${AUTH_CODE}")

if echo "$RESPONSE" | jq -e '.access_token' >/dev/null 2>&1; then
    ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
    REFRESH_TOKEN=$(echo "$RESPONSE" | jq -r '.refresh_token // empty')
    EXPIRES_IN=$(echo "$RESPONSE" | jq -r '.expires_in // 21599')

    echo -e "${GREEN}✓ Authentication successful!${NC}"
    echo ""

    # Save using auth_token.sh's save-user function
    source "$SCRIPT_DIR/auth_token.sh"
    save_user_token "$ACCESS_TOKEN" "$REFRESH_TOKEN" "$EXPIRES_IN"

    # Also export to current session
    export SOUNDCLOUD_USER_TOKEN="$ACCESS_TOKEN"

    # Verify
    echo -e "${YELLOW}Verifying token...${NC}"
    USER_RESPONSE=$(curl -s "https://api.soundcloud.com/me" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "accept: application/json; charset=utf-8")

    if echo "$USER_RESPONSE" | jq -e '.id' >/dev/null 2>&1; then
        USERNAME=$(echo "$USER_RESPONSE" | jq -r '.username')
        echo -e "${GREEN}✓ Authenticated as:${NC} ${CYAN}${USERNAME}${NC}"
    fi

    echo ""
    echo -e "${GREEN}You can now use all SoundCloud scripts!${NC}"
    echo ""
    echo "To persist the token across sessions, add to your shell config:"
    echo -e "  ${CYAN}export SOUNDCLOUD_USER_TOKEN=\"${ACCESS_TOKEN:0:20}...\"${NC}"
    echo ""
    echo "Or just run the scripts — they'll use the cached token automatically."
else
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.error_description // .error // "Unknown error"')
    echo -e "${RED}✗ Token exchange failed:${NC} $ERROR_MSG"
    echo ""
    echo "Response: $RESPONSE"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Make sure you copied the full authorization code"
    echo "  2. The code expires quickly — try again and paste faster"
    echo "  3. Verify your redirect URI matches your SoundCloud app settings"
    exit 1
fi
