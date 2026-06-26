#!/bin/bash
# W-Spaces code push script

set -euo pipefail

API_BASE="${WSPACES_API_URL:-https://api.wspaces.app}"

if [ -z "${WSPACES_API_KEY:-}" ]; then
    echo "Error: WSPACES_API_KEY not set"
    exit 1
fi

# Parse arguments
PROJECT_ID=""
HTML_CONTENT=""
FILE_PATH=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --project) PROJECT_ID="$2"; shift 2 ;;
        --html) HTML_CONTENT="$2"; shift 2 ;;
        --file) FILE_PATH="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ -z "$PROJECT_ID" ]; then
    echo "Error: --project required"
    exit 1
fi

if [ -z "$HTML_CONTENT" ] && [ -z "$FILE_PATH" ]; then
    echo "Error: --html or --file required"
    exit 1
fi

# Read from file if provided
if [ -n "$FILE_PATH" ]; then
    if [ ! -f "$FILE_PATH" ]; then
        echo "Error: File not found: $FILE_PATH"
        exit 1
    fi
    HTML_CONTENT=$(cat "$FILE_PATH")
fi

# Escape JSON special characters
HTML_ESCAPED=$(echo "$HTML_CONTENT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

curl -s -X PUT "$API_BASE/api/v1/projects/$PROJECT_ID/code" \
    -H "X-API-Key: $WSPACES_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"html\":$HTML_ESCAPED}" | jq .
