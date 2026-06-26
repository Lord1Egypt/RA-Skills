#!/bin/bash
# W-Spaces deployment script

set -euo pipefail

API_BASE="${WSPACES_API_URL:-https://api.wspaces.app}"

if [ -z "${WSPACES_API_KEY:-}" ]; then
    echo "Error: WSPACES_API_KEY not set"
    exit 1
fi

# Parse arguments
ACTION="deploy"
PROJECT_ID=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --project) PROJECT_ID="$2"; shift 2 ;;
        --list) ACTION="list"; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ -z "$PROJECT_ID" ]; then
    echo "Error: --project required"
    exit 1
fi

case "$ACTION" in
    deploy)
        echo "Deploying project $PROJECT_ID..."
        RESULT=$(curl -s -X POST "$API_BASE/api/v1/projects/$PROJECT_ID/deploy" \
            -H "X-API-Key: $WSPACES_API_KEY")
        echo "$RESULT" | jq .

        URL=$(echo "$RESULT" | jq -r '.url // empty')
        if [ -n "$URL" ]; then
            echo ""
            echo "Live at: $URL"
        fi
        ;;

    list)
        curl -s -X GET "$API_BASE/api/v1/projects/$PROJECT_ID/deployments" \
            -H "X-API-Key: $WSPACES_API_KEY" | jq .
        ;;
esac
