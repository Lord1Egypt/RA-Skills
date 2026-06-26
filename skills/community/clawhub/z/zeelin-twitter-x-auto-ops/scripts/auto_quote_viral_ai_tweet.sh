#!/bin/bash

# auto_quote_viral_ai_tweet.sh
# Finds high‑engagement AI tweets (approx viral) and opens them for quoting

QUERY="AI agents OR OpenAI OR Anthropic OR LLM min_faves:500"

ENCODED=$(python3 - <<EOF
import urllib.parse
print(urllib.parse.quote("""$QUERY"""))
EOF
)

URL="https://x.com/search?q=${ENCODED}&src=typed_query&f=top"

open "$URL"

echo "Opened potentially viral AI tweets (>~500 likes)."
echo "Quote one with insight such as:"
echo ""
echo "Big moment for AI agents." 
echo ""
echo "Key unlocks now:" 
echo "• reliable reasoning" 
echo "• tool use" 
echo "• long context" 
echo ""
echo "AI apps are moving from demos → real systems."