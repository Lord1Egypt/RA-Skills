#!/bin/bash

# Semi‑automatic AI trend → tweet workflow
# 1) Opens X search for AI trends
# 2) Prompts user to generate a tweet
# 3) Optionally posts it automatically

QUERY=${1:-"AI agents OR LLM OR OpenAI OR Anthropic"}

SEARCH_URL="https://x.com/search?q=$(python3 - <<EOF
import urllib.parse
print(urllib.parse.quote('''$QUERY'''))
EOF
)&src=typed_query&f=live"

open "$SEARCH_URL"

echo ""
echo "Opened AI trend search on X."
echo "Scan the latest tweets and create a short summary tweet."
echo ""
echo "Example format:"
echo ""
echo "AI trend today:"
echo ""
echo "• new model releases"
echo "• agent tooling"
echo "• open source momentum"
echo ""
echo "AI ecosystem moving fast."
echo ""

echo "To post a tweet automatically run:"
echo "bash skills/x-auto-growth/scripts/post_tweet.sh \"YOUR TWEET HERE\""
