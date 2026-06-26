#!/bin/bash
# Verosight Quick Sentiment Analysis
# Usage: ./quick-sentiment.sh <JWT_TOKEN> <QUERY> [DAYS] [SOURCES]

JWT="$1"
QUERY="$2"
DAYS="${3:-7}"
SOURCES="${4:-x,instagram,tiktok,threads,youtube,news_portal}"

if [ -z "$JWT" ] || [ -z "$QUERY" ]; then
  echo "Usage: $0 <JWT_TOKEN> <QUERY> [DAYS] [SOURCES]" >&2
  exit 1
fi

echo "=== SENTIMENT ANALYSIS: $QUERY ==="
curl -s "https://api.verosight.com/v1/analytics/sentiment?query=$QUERY&sources=$SOURCES&days=$DAYS" \
  -H "Authorization: Bearer $JWT" | python3 -c "
import sys, json
d = json.load(sys.stdin)['data']
print(f'Total: {d[\"total\"]}')
print(f'Positive: {d[\"positive\"]} ({d[\"positive_pct\"]}%)')
print(f'Negative: {d[\"negative\"]} ({d[\"negative_pct\"]}%)')
print(f'Neutral: {d[\"neutral\"]} ({d[\"neutral_pct\"]}%)')
print(f'Weighted Negative: {d.get(\"weighted_negative_pct\",\"?\")}%')
" 2>/dev/null
