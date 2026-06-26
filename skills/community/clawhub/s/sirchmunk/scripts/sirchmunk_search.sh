#!/bin/bash

# Sirchmunk Search - Simple wrapper

# Usage: sirchmunk_search.sh "your query here" ["paths"]

QUERY="$1"
PATHS="$2"

if [ -z "$QUERY" ]; then
    echo "Usage: sirchmunk_search.sh \"your query\" [\"paths\"]"
    exit 1
fi

# Set PATHS to empty array if not provided
if [ -z "$PATHS" ]; then
    PATHS_JSON="[]"
else
    PATHS_JSON="[\"$PATHS\"]"
fi

curl -s -X POST "http://localhost:8584/api/v1/search" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"$QUERY\",
    \"paths\": $PATHS_JSON,
    \"mode\": \"FAST\"
  }" | python3 -m json.tool 2>/dev/null || cat
