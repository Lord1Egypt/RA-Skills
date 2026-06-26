#!/bin/bash
set -e

# Proxy Web Search - Routes through OpenClaw Manager Web Search Proxy
# Usage: proxy_search.sh --query "search text" [--engine search_pro_quark] [--count 25] [--intent] [--recency noLimit]

# Proxy URL from env var (required)
if [ -z "$WEB_SEARCH_PROXY_URL" ]; then
    echo "Error: WEB_SEARCH_PROXY_URL environment variable is not set" >&2
    exit 1
fi
PROXY_URL="$WEB_SEARCH_PROXY_URL"

# Default values
QUERY=""
ENGINE="search_pro_quark"
INTENT="false"
COUNT=25
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
            echo ""
            echo "Options:"
            echo "  -q, --query    Search query (required)"
            echo "  -e, --engine   Search engine: search_std, search_pro, search_pro_sogou, search_pro_quark (default: search_pro_quark)"
            echo "  -c, --count    Result count, 1-50 (default: 25)"
            echo "  -i, --intent   Enable search intent recognition"
            echo "  -r, --recency  Time filter: oneDay, oneWeek, oneMonth, oneYear, noLimit (default: noLimit)"
            echo ""
            echo "Environment:"
            echo "  WEB_SEARCH_PROXY_URL  Proxy URL (required, no default)"
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

# Escape quotes and backslashes in the query for safe JSON encoding
SAFE_QUERY="${QUERY//\\/\\\\}"
SAFE_QUERY="${SAFE_QUERY//\"/\\\"}"

# Build JSON payload
PAYLOAD="{\"search_query\": \"$SAFE_QUERY\", \"search_engine\": \"$ENGINE\", \"search_intent\": $INTENT, \"count\": $COUNT, \"search_recency_filter\": \"$RECENCY\"}"

# Execute cURL request to Web Search Proxy (no auth needed)
curl -s --request POST \
  --url "${PROXY_URL}/" \
  --header "Content-Type: application/json" \
  --data "$PAYLOAD"
