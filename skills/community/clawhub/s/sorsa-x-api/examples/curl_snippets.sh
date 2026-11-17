#!/usr/bin/env bash
# Sorsa API v3 - common requests. Set SORSA_API_KEY first.
#   export SORSA_API_KEY=your_key   # https://api.sorsa.io/overview
set -euo pipefail

BASE="https://api.sorsa.io/v3"
AUTH="ApiKey: ${SORSA_API_KEY}"
JSON="Content-Type: application/json"

# Profile
curl -s -H "$AUTH" "$BASE/info?username=elonmusk"

# Profiles in batch (up to 100)
curl -s -H "$AUTH" "$BASE/info-batch?usernames=elonmusk&usernames=jack"

# Followers (paginated, up to 200 per page)
curl -s -H "$AUTH" "$BASE/followers?username=elonmusk"

# A user's tweets (POST)
curl -s -X POST -H "$AUTH" -H "$JSON" "$BASE/user-tweets" \
  -d '{"username": "elonmusk"}'

# Search tweets with operators (POST)
curl -s -X POST -H "$AUTH" -H "$JSON" "$BASE/search-tweets" \
  -d '{"query": "from:elonmusk min_faves:1000", "order": "popular"}'

# Mentions with filters (POST)
curl -s -X POST -H "$AUTH" -H "$JSON" "$BASE/mentions" \
  -d '{"query": "elonmusk", "min_likes": 100, "since_date": "2026-01-01"}'

# One tweet's full data (POST)
curl -s -X POST -H "$AUTH" -H "$JSON" "$BASE/tweet-info" \
  -d '{"tweet_link": "https://x.com/elonmusk/status/1782368585664626774"}'

# Crypto influence score (Sorsa Info)
curl -s -H "$AUTH" "$BASE/score?username=vitalikbuterin"

# Trending topics for a location (WOEID 1 = worldwide)
curl -s -H "$AUTH" "$BASE/trends?woeid=1"

# Twitter/X Space details by ID
curl -s -H "$AUTH" "$BASE/spaces?id=1lPKqBajQrWGb"

# Remaining quota for this key
curl -s -H "$AUTH" "$BASE/key-usage-info"
