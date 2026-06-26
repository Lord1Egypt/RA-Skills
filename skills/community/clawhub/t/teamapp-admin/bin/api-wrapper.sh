#!/bin/bash
# teamapp-api-wrapper.sh
# Wrapper script for TeamApp Admin API calls.
# Handles authentication, session bootstrapping, and CSRF token management automatically.

# Usage: ./api-wrapper.sh <METHOD> <URL> [CURL_OPTIONS...]
# Example: ./api-wrapper.sh POST "https://teamappcli.teamapp.com/clubs/941837/articles.json?_post_response=v1" --data-urlencode "article[subject]=Test"

set -e

# Configuration
COOKIE_JAR="/tmp/teamapp_cookies.txt"
CSRF_FILE="/tmp/teamapp_csrf.txt"
USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"

# Ensure Environment Variables
if [ -z "$TA_AUTH_TOKEN" ]; then
    echo "Error: TA_AUTH_TOKEN environment variable is required." >&2
    exit 1
fi

# Helper: Bootstrap Session
bootstrap_session() {
    # echo "Bootstrapping session (fetching dashboard)..." >&2
    # Use the main TeamApp site for bootstrapping to avoid needing a specific club ID
    local dashboard_url="https://www.teamapp.com/"

    # Fetch dashboard to populate cookie jar
    # We follow redirects (-L) because the root URL often redirects to /?_detail=v1
    local dashboard_html
    dashboard_html=$(curl -s -L -c "$COOKIE_JAR" \
        -H "User-Agent: $USER_AGENT" \
        -H "Cookie: ta_auth_token=$TA_AUTH_TOKEN" \
        "$dashboard_url")

    # Extract CSRF Token
    local csrf_token
    csrf_token=$(echo "$dashboard_html" | grep '<meta name="csrf-token"' | sed -n 's/.*content="\([^"]*\)".*/\1/p')

    if [ -z "$csrf_token" ]; then
        echo "Error: Failed to extract CSRF token from $dashboard_url" >&2
        # Debug: dump HTML to a file if needed
        # echo "$dashboard_html" > /tmp/teamapp_debug.html
        exit 1
    fi

    echo "$csrf_token" > "$CSRF_FILE"
    # echo "Session bootstrapped. CSRF Token: ${csrf_token:0:10}..." >&2
}

# Ensure session exists
if [ ! -f "$COOKIE_JAR" ] || [ ! -f "$CSRF_FILE" ]; then
    bootstrap_session
fi

# Read CSRF Token
CSRF_TOKEN=$(cat "$CSRF_FILE")

# Parse Arguments
METHOD="$1"
URL="$2"
shift 2

# Perform Request
# We capture the HTTP code to handle retry logic for expired sessions
HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" -X "$METHOD" "$URL" \
    -b "$COOKIE_JAR" -c "$COOKIE_JAR" \
    -H "User-Agent: $USER_AGENT" \
    -H "Cookie: ta_auth_token=$TA_AUTH_TOKEN" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    "$@")

# Extract Body and Status Code
HTTP_BODY=$(echo "$HTTP_RESPONSE" | sed '$d')
HTTP_STATUS=$(echo "$HTTP_RESPONSE" | tail -n 1)

# Retry Logic for 422 (CSRF Error) or 401 (Unauthorized)
if [[ "$HTTP_STATUS" == "422" || "$HTTP_STATUS" == "401" ]]; then
    echo "Request failed with status $HTTP_STATUS. Refreshing session and retrying..." >&2
    bootstrap_session
    CSRF_TOKEN=$(cat "$CSRF_FILE")
    
    # Retry Request
    curl -s -X "$METHOD" "$URL" \
        -b "$COOKIE_JAR" -c "$COOKIE_JAR" \
        -H "User-Agent: $USER_AGENT" \
        -H "Cookie: ta_auth_token=$TA_AUTH_TOKEN" \
        -H "X-CSRF-Token: $CSRF_TOKEN" \
        "$@"
else
    # Output the original response body
    echo "$HTTP_BODY"
fi
