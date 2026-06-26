#!/bin/bash
# Tavily Search Script with blocklist filtering
# Usage: ./search.sh "query" [max_results] [include_images]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ===== Key loading =====
if [ -z "$TAVILY_API_KEY" ]; then
    if [ -f "${SCRIPT_DIR}/apikey" ]; then
        TAVILY_API_KEY="$(cat "${SCRIPT_DIR}/apikey" 2>/dev/null)"
    fi
fi

if [ -z "$TAVILY_API_KEY" ]; then
    echo "ERROR: TAVILY_API_KEY is not configured" >&2
    echo "Please either:" >&2
    echo "  1. Set env var: export TAVILY_API_KEY='your-api-key'" >&2
    echo "  2. Create apikey file in the same directory as this script" >&2
    exit 1
fi

TAVILY_ENDPOINT="https://api.tavily.com/search"
TAVILY_USAGE_ENDPOINT="https://api.tavily.com/usage"

# ===== Parse args =====
query="${1:-}"
max_results="${2:-5}"
include_images="${3:-false}"

if [ -z "$query" ]; then
    echo "Usage: ./search.sh \"query\" [max_results] [include_images]" >&2
    exit 1
fi

# ===== Make API call =====
images_flag="false"
if [ "$include_images" = "true" ] || [ "$include_images" = "1" ]; then
    images_flag="true"
fi

# Build JSON payload via jq to avoid shell injection
# query is passed as --arg value (no shell expansion), max_results as tonumber
json_payload=$(jq -n \
    --arg q "$query" \
    --arg mr "$max_results" \
    --arg ii "$images_flag" \
    '{
        query: $q,
        search_depth: "basic",
        max_results: ($mr | tonumber),
        include_images: ($ii == "true")
    }')

response=$(curl -s -w "\n%{http_code}" -X POST "$TAVILY_ENDPOINT" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TAVILY_API_KEY" \
    -d "$json_payload")

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" != "200" ]; then
    echo "{\"error\": \"HTTP $http_code\", \"body\": $body}" >&2
    exit 1
fi

# ===== Get quota =====
quota_response=$(curl -s -X GET "$TAVILY_USAGE_ENDPOINT" \
    -H "Authorization: Bearer $TAVILY_API_KEY")

plan=$(echo "$quota_response" | jq -r '.account.current_plan // "unknown"' 2>/dev/null)
used=$(echo "$quota_response" | jq -r '.account.plan_usage // 0' 2>/dev/null)
total=$(echo "$quota_response" | jq -r '.account.plan_limit // 1000' 2>/dev/null)
remaining=$(echo "$quota_response" | jq -r '(.account.plan_limit // 1000) - (.account.plan_usage // 0)' 2>/dev/null)

quota_info="{\"plan\": \"$plan\", \"total\": $total, \"used\": $used, \"remaining\": $remaining}"

# ===== Build output with quota =====
output=$(echo "$body" | jq --argjson quota "$quota_info" '{query: .query, results: .results, quota_info: $quota, response_time: .response_time}')

# ===== Apply blocklist filter =====
blocklist_file="${SCRIPT_DIR}/blocklist/blocklist.json"
filter_script="${SCRIPT_DIR}/blocklist/filter_blocklist.py"

if [ -f "$blocklist_file" ] && [ -f "$filter_script" ]; then
    # Use random temp file to avoid conflicts
    tmpfile=$(mktemp /tmp/tavily_XXXXXX.json)
    echo "$output" > "$tmpfile"
    filtered=$(python3 "$filter_script" "$blocklist_file" "$tmpfile" 2>&1)
    rm -f "$tmpfile"
    echo "$filtered"
else
    echo "$output"
fi
