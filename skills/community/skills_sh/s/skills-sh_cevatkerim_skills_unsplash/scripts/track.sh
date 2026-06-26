#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# Usage: track.sh photo_id
photo_id="${1:-}"

if [ -z "$photo_id" ]; then
    echo "ERROR: photo_id required" >&2
    echo "Usage: track.sh photo_id" >&2
    exit 1
fi

validate_api_key || exit 1

# Make API request
response=$(api_request "/photos/$photo_id/download" "") || exit 1

# Extract download URL
echo "$response" | jq -r '.url'
