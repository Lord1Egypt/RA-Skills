#!/bin/bash
# Search hotels via voyager MCP API
# Usage: search-hotels.sh <queryJsonArray>
# Example: search-hotels.sh '[{"subQuery":"大阪酒店推荐","checkInDate":"2026-04-01","checkOutDate":"2026-04-07","city":"大阪","country":"日本","nearby":"梅田"}]'

set -e

# Parameters
QUERY_JSON="$1"

# Parse and validate JSON using jq
PARSED_JSON=$(echo "$QUERY_JSON" | jq .)

# Make API call
curl --silent --location --request POST \
  'https://ivguserprod.alipay.com/ivgavatarcn/api/v1/voyager/mcp/RECALL_hotel' \
  --header 'Content-Type: application/json' \
  --data "$PARSED_JSON"
