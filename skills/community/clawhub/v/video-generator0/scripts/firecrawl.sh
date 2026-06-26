#!/usr/bin/env bash
set -euo pipefail

URL="${1:?Usage: firecrawl.sh <url>}"

if [ -z "${FIRECRAWL_API_KEY:-}" ]; then
  echo "Error: FIRECRAWL_API_KEY not set" >&2
  exit 1
fi

curl -s -X POST 'https://api.firecrawl.dev/v1/scrape' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" \
  -d "{\"url\":\"$URL\",\"formats\":[\"markdown\",\"extract\",\"screenshot\"]}"
