#!/bin/bash
# W-Spaces authentication script

set -euo pipefail

API_BASE="${WSPACES_API_URL:-https://api.wspaces.app}"

# Parse arguments
ACTION=""
EMAIL=""
PASSWORD=""
NAME=""
KEY_NAME=""
KEY_ID=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --register) ACTION="register"; shift ;;
        --login) ACTION="login"; shift ;;
        --me) ACTION="me"; shift ;;
        --create-key) ACTION="create-key"; shift ;;
        --list-keys) ACTION="list-keys"; shift ;;
        --revoke-key) ACTION="revoke-key"; shift ;;
        --email) EMAIL="$2"; shift 2 ;;
        --password) PASSWORD="$2"; shift 2 ;;
        --name) NAME="$2"; shift 2 ;;
        --key-name) KEY_NAME="$2"; shift 2 ;;
        --id) KEY_ID="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

case "$ACTION" in
    register)
        if [ -z "$EMAIL" ] || [ -z "$PASSWORD" ] || [ -z "$NAME" ]; then
            echo "Error: --email, --password, and --name required"
            exit 1
        fi
        curl -s -X POST "$API_BASE/api/v1/auth/register" \
            -H "Content-Type: application/json" \
            -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\",\"name\":\"$NAME\"}" | jq .
        ;;

    login)
        if [ -z "$EMAIL" ] || [ -z "$PASSWORD" ]; then
            echo "Error: --email and --password required"
            exit 1
        fi
        curl -s -X POST "$API_BASE/api/v1/auth/login" \
            -H "Content-Type: application/json" \
            -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}" | jq .
        ;;

    me)
        if [ -z "${WSPACES_API_KEY:-}" ]; then
            echo "Error: WSPACES_API_KEY not set"
            exit 1
        fi
        curl -s -X GET "$API_BASE/api/v1/me" \
            -H "X-API-Key: $WSPACES_API_KEY" | jq .
        ;;

    create-key)
        if [ -z "${WSPACES_API_KEY:-}" ]; then
            echo "Error: WSPACES_API_KEY not set"
            exit 1
        fi
        KEY_NAME="${KEY_NAME:-API Key}"
        curl -s -X POST "$API_BASE/api/v1/auth/api-keys" \
            -H "X-API-Key: $WSPACES_API_KEY" \
            -H "Content-Type: application/json" \
            -d "{\"name\":\"$KEY_NAME\"}" | jq .
        ;;

    list-keys)
        if [ -z "${WSPACES_API_KEY:-}" ]; then
            echo "Error: WSPACES_API_KEY not set"
            exit 1
        fi
        curl -s -X GET "$API_BASE/api/v1/auth/api-keys" \
            -H "X-API-Key: $WSPACES_API_KEY" | jq .
        ;;

    revoke-key)
        if [ -z "${WSPACES_API_KEY:-}" ]; then
            echo "Error: WSPACES_API_KEY not set"
            exit 1
        fi
        if [ -z "$KEY_ID" ]; then
            echo "Error: --id required"
            exit 1
        fi
        curl -s -X DELETE "$API_BASE/api/v1/auth/api-keys/$KEY_ID" \
            -H "X-API-Key: $WSPACES_API_KEY"
        echo "Key revoked."
        ;;

    *)
        echo "Usage: wspaces_auth.sh <action> [options]"
        echo ""
        echo "Actions:"
        echo "  --register  --email <email> --password <pass> --name <name>"
        echo "  --login     --email <email> --password <pass>"
        echo "  --me"
        echo "  --create-key [--key-name <name>]"
        echo "  --list-keys"
        echo "  --revoke-key --id <key-id>"
        exit 1
        ;;
esac
