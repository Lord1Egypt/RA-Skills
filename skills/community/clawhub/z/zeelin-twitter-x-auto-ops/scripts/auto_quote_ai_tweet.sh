#!/bin/bash

# auto_quote_ai_tweet.sh
# Opens high‑engagement AI tweets and prepares a quote tweet template

QUERY="AI agents OR OpenAI OR Anthropic OR LLM"

ENCODED=$(python3 - <<EOF
import urllib.parse
print(urllib.parse.quote("""$QUERY"""))
EOF
)

URL="https://x.com/search?q=${ENCODED}&src=typed_query&f=top"

open "$URL"

echo "Opened high‑engagement AI tweets (Top)."
echo "Find a tweet with strong engagement and quote it using a template like:"
echo ""
echo "Interesting perspective on AI agents."
echo ""
echo "What matters next:"
echo "• reasoning reliability"
echo "• tool use"
echo "• long context"
echo ""
echo "Agents are getting closer to real‑world deployment."