#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source "$SCRIPT_DIR/../../reference/config.sh"
source "$SCRIPT_DIR/../../reference/runtime.sh"

is_valid_api_path() {
    local path="$1"
    if [ -z "$path" ]; then
        return 1
    fi
    case "$path" in
        *"://"* ) return 1 ;;
        *$'\n'*|*$'\r'*|*$'\t'*|*" "* ) return 1 ;;
    esac
    [[ "$path" =~ ^/api/ ]] || return 1
    return 0
}

is_allowed_endpoint() {
    local method="$1"
    local path="$2"

    if [ "$method" != "GET" ] && [ "$method" != "POST" ] && [ "$method" != "PUT" ]; then
        return 1
    fi

    if [ "$method" = "GET" ]; then
        [[ "$path" =~ ^/api/positions/(\?.*)?$ ]] && return 0
        [[ "$path" =~ ^/api/analytics/summary(\?.*)?$ ]] && return 0
        [[ "$path" =~ ^/api/markets/search/stocks(\?.*)?$ ]] && return 0
        [[ "$path" =~ ^/api/markets/stocks/[^/?]+/price(\?.*)?$ ]] && return 0
        [[ "$path" =~ ^/api/brokers/(\?.*)?$ ]] && return 0
        return 1
    fi

    if [ "$method" = "POST" ]; then
        [[ "$path" =~ ^/api/brokers/seed-defaults(\?.*)?$ ]] && return 0
        [[ "$path" =~ ^/api/brokers/calculate-commission(\?.*)?$ ]] && return 0
        [[ "$path" =~ ^/api/trades/(\?.*)?$ ]] && return 0
        return 1
    fi

    if [ "$method" = "PUT" ]; then
        [[ "$path" =~ ^/api/positions/[0-9]+/edit(\?.*)?$ ]] && return 0
        return 1
    fi

    return 1
}

requires_json_body() {
    local method="$1"
    local path="$2"
    if [ "$method" = "PUT" ]; then
        [[ "$path" =~ ^/api/positions/[0-9]+/edit(\?.*)?$ ]] && return 0
    fi
    if [ "$method" != "POST" ]; then
        return 1
    fi
    [[ "$path" =~ ^/api/brokers/calculate-commission(\?.*)?$ ]] && return 0
    [[ "$path" =~ ^/api/trades/(\?.*)?$ ]] && return 0
    return 1
}

API_PATH=$1
HTTP_METHOD=${2:-GET}
JSON_DATA=$3

if [ -z "$API_PATH" ]; then
    echo "Error: API_PATH is required."
    exit 1
fi

if ! is_valid_api_path "$API_PATH"; then
    echo "Error: Invalid API_PATH. It must start with /api/ and must not contain whitespace or scheme."
    exit 1
fi

if ! is_allowed_endpoint "$HTTP_METHOD" "$API_PATH"; then
    echo "Error: Endpoint not allowed by this skill wrapper."
    exit 1
fi

if requires_json_body "$HTTP_METHOD" "$API_PATH" && [ -z "$JSON_DATA" ]; then
    echo "Error: JSON body is required for $HTTP_METHOD $API_PATH"
    exit 1
fi

se_request "$HTTP_METHOD" "$API_PATH" "$JSON_DATA"
