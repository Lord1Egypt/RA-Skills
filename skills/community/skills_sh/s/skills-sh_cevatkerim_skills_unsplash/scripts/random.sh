#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# Usage: random.sh [query] [count] [orientation]
query="${1:-}"
count="${2:-1}"
orientation="${3:-}"

validate_api_key || exit 1

# Build query params
params="count=$count&content_filter=low"
[ -n "$query" ] && params="$params&query=$(printf '%s' "$query" | jq -sRr @uri)"
[ -n "$orientation" ] && params="$params&orientation=$orientation"

# Make API request
response=$(api_request "/photos/random" "$params") || exit 1

# Format results (handles both single object and array)
echo "$response" | format_photos
