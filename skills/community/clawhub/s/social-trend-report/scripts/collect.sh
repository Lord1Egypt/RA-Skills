#!/bin/bash
# Social Trend Report — Data Collection Helper
# Usage: ./collect.sh [config.json]
#
# This script is a reference implementation. The agent can also
# call web_fetch/bird/web_search tools directly.

set -euo pipefail

CONFIG="${1:-config.json}"

if [ ! -f "$CONFIG" ]; then
  echo "No config.json found. Create one with your niche settings."
  echo "See SKILL.md for the config format."
  exit 1
fi

NICHE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['niche'])")
OUTPUT_DIR=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('output',{}).get('dir','reports'))")
DATE=$(date +%Y-%m-%d)
OUTFILE="$OUTPUT_DIR/raw-$DATE.json"

mkdir -p "$OUTPUT_DIR"

echo "📊 Collecting data for niche: $NICHE"
echo "📅 Date: $DATE"
echo ""

# --- Reddit ---
echo "🔴 Reddit..."
SUBREDDITS=$(python3 -c "import json; [print(s) for s in json.load(open('$CONFIG'))['reddit']['subreddits']]")
TIMEFRAME=$(python3 -c "import json; print(json.load(open('$CONFIG'))['reddit'].get('timeframe','week'))")
LIMIT=$(python3 -c "import json; print(json.load(open('$CONFIG'))['reddit'].get('limit',10))")

REDDIT_DATA="["
for sub in $SUBREDDITS; do
  echo "  r/$sub (top/$TIMEFRAME, limit $LIMIT)"
  # Note: Use web_fetch tool in agent context; curl may not work behind firewalls
  URL="https://www.reddit.com/r/${sub}/top/.json?t=${TIMEFRAME}&limit=${LIMIT}"
  DATA=$(curl -s -H "User-Agent: SocialTrendReport/1.0" "$URL" 2>/dev/null || echo '{"data":{"children":[]}}')
  REDDIT_DATA="$REDDIT_DATA{\"subreddit\":\"$sub\",\"data\":$DATA},"
done
REDDIT_DATA="${REDDIT_DATA%,}]"

# --- Twitter/X ---
echo ""
echo "🐦 Twitter/X..."
KEYWORDS=$(python3 -c "import json; [print(k) for k in json.load(open('$CONFIG'))['twitter']['keywords']]")

TWITTER_DATA="["
for kw in $KEYWORDS; do
  echo "  Search: $kw"
  RESULT=$(bird search "$kw" --plain 2>/dev/null || echo "No results")
  TWITTER_DATA="$TWITTER_DATA{\"keyword\":\"$kw\",\"results\":\"$(echo "$RESULT" | head -50 | sed 's/"/\\"/g')\"},"
done
TWITTER_DATA="${TWITTER_DATA%,}]"

echo ""
echo "✅ Raw data saved to $OUTFILE"
echo "Next step: Feed this data to the agent for AI analysis."

# Save combined raw data
python3 -c "
import json
data = {
    'date': '$DATE',
    'niche': '$NICHE',
    'reddit': json.loads('''$REDDIT_DATA''') if '''$REDDIT_DATA''' != '[]' else [],
    'twitter_keywords': '$KEYWORDS'.split()
}
with open('$OUTFILE', 'w') as f:
    json.dump(data, f, indent=2)
"
