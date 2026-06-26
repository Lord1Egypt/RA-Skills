#!/bin/bash
set -e

# Default values
QUERY=""
ENGINE="search_pro_quark"
INTENT="false"
COUNT=20
RECENCY="noLimit"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -q|--query) QUERY="$2"; shift ;;
        -e|--engine) ENGINE="$2"; shift ;;
        -i|--intent) INTENT="true" ;;
        -c|--count) COUNT="$2"; shift ;;
        -r|--recency) RECENCY="$2"; shift ;;
        -h|--help)
            echo "Usage: $0 --query <text> [--engine <engine>] [--count <int>] [--intent] [--recency <filter>]"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$QUERY" ]; then
    echo "Error: --query is required" >&2
    exit 1
fi

if [ -z "$ZHIPU_API_KEY" ]; then
    echo "Error: ZHIPU_API_KEY environment variable is not set" >&2
    exit 1
fi

# Escape quotes and backslashes in the query for safe JSON encoding
SAFE_QUERY="${QUERY//\\/\\\\}"
SAFE_QUERY="${SAFE_QUERY//\"/\\\"}"

# Build JSON payload manually
PAYLOAD="{\"search_query\": \"$SAFE_QUERY\", \"search_engine\": \"$ENGINE\", \"search_intent\": $INTENT, \"count\": $COUNT, \"search_recency_filter\": \"$RECENCY\"}"

# Execute cURL request
curl -s --request POST \
  --url https://open.bigmodel.cn/api/paas/v4/web_search \
  --header "Authorization: Bearer $ZHIPU_API_KEY" \
  --header "Content-Type: application/json" \
  --data "$PAYLOAD"
