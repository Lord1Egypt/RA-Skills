#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# Usage: search.sh query [page] [per_page] [order_by] [orientation] [color]
query="${1:-}"
page="${2:-1}"
per_page="${3:-10}"
order_by="${4:-relevant}"
orientation="${5:-}"
color="${6:-}"

if [ -z "$query" ]; then
    echo "ERROR: query required" >&2
    echo "Usage: search.sh query [page] [per_page] [order_by] [orientation] [color]" >&2
    exit 1
fi

validate_api_key || exit 1

# Build query params
params="query=$(printf '%s' "$query" | jq -sRr @uri)&page=$page&per_page=$per_page&order_by=$order_by&content_filter=low"
[ -n "$orientation" ] && params="$params&orientation=$orientation"
[ -n "$color" ] && params="$params&color=$color"

# Make API request
response=$(api_request "/search/photos" "$params") || exit 1

# Extract and format results
echo "$response" | jq -r '.results' | format_photos
