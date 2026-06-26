#!/bin/bash
# W-Spaces project management script

set -euo pipefail

API_BASE="${WSPACES_API_URL:-https://api.wspaces.app}"

if [ -z "${WSPACES_API_KEY:-}" ]; then
    echo "Error: WSPACES_API_KEY not set"
    exit 1
fi

# Parse arguments
ACTION=""
PROJECT_NAME=""
PROJECT_ID=""
CATEGORY=""
DESCRIPTION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --create) ACTION="create"; shift ;;
        --list) ACTION="list"; shift ;;
        --get) ACTION="get"; shift ;;
        --name) PROJECT_NAME="$2"; shift 2 ;;
        --id) PROJECT_ID="$2"; shift 2 ;;
        --category) CATEGORY="$2"; shift 2 ;;
        --description) DESCRIPTION="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

case "$ACTION" in
    create)
        if [ -z "$PROJECT_NAME" ]; then
            echo "Error: --name required"
            exit 1
        fi
        BODY="{\"name\":\"$PROJECT_NAME\""
        [ -n "$CATEGORY" ] && BODY="$BODY,\"category\":\"$CATEGORY\""
        [ -n "$DESCRIPTION" ] && BODY="$BODY,\"description\":\"$DESCRIPTION\""
        BODY="$BODY}"

        curl -s -X POST "$API_BASE/api/v1/projects" \
            -H "X-API-Key: $WSPACES_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" | jq .
        ;;

    list)
        curl -s -X GET "$API_BASE/api/v1/projects" \
            -H "X-API-Key: $WSPACES_API_KEY" | jq .
        ;;

    get)
        if [ -z "$PROJECT_ID" ]; then
            echo "Error: --id required"
            exit 1
        fi
        curl -s -X GET "$API_BASE/api/v1/projects/$PROJECT_ID" \
            -H "X-API-Key: $WSPACES_API_KEY" | jq .
        ;;

    *)
        echo "Usage: wspaces_project.sh <action> [options]"
        echo ""
        echo "Actions:"
        echo "  --create  --name <name> [--category <cat>] [--description <desc>]"
        echo "  --list"
        echo "  --get     --id <project-id>"
        exit 1
        ;;
esac
