#!/bin/bash

# Open high-engagement AI tweets so user/automation can quote them
# Helps growth by quoting trending discussions

QUERY=${1:-"AI agents OR OpenAI OR Anthropic OR LLM"}

ENCODED=$(python3 - <<EOF
import urllib.parse
print(urllib.parse.quote("$QUERY"))
EOF
)

URL="https://x.com/search?q=${ENCODED}&src=typed_query&f=top"

open "$URL"

echo "Opened high-engagement AI tweets."
echo "Look for tweets with strong engagement and quote them with insight."
echo ""
echo "Example quote tweet:"
echo ""
echo "Interesting take on AI agents."
echo ""
echo "What matters most now:"
echo "• reliability"
echo "• tool use"
echo "• long context"
echo ""
echo "Agents are getting closer to real-world deployment."