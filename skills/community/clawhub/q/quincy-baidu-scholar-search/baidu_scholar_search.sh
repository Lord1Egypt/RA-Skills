#!/bin/bash

# Academic Scholar Search Skill Implementation
# Powered by SkillBoss API Hub

set -e

# Check if required environment variable is set
if [ -z "$SKILLBOSS_API_KEY" ]; then
    echo '{"error": "SKILLBOSS_API_KEY environment variable not set"}'
    exit 1
fi

WD="$1"
if [ -z "$WD" ]; then
    echo '{"error": "Missing wd parameter"}'
    exit 1
fi

pageNum="${2:-0}"
enable_abstract="${3:-false}"

curl -s -X POST \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"search\", \"inputs\": {\"query\": \"$WD\"}, \"prefer\": \"balanced\"}" \
  "https://api.heybossai.com/v1/pilot"
# Response path: .result.results
