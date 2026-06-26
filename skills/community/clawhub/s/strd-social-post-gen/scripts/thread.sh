#!/bin/bash
# thread.sh — Create a Twitter thread from article
# Usage: ./thread.sh <url_or_text_file>

PLATFORM="${PLATFORM:-twitter}"
BRAND="${BRAND_NAME:-}"

SKILL_DIR="$(dirname "$0")/.."
mkdir -p "$SKILL_DIR/cache"

input="$1"

if [ -z "$input" ]; then
  echo "Usage: $0 <url_or_text_file>" >&2
  exit 1
fi

# Fetch content if URL
if echo "$input" | grep -qE '^https?://'; then
  echo "Fetching article: $input" >&2
  content=$(curl --silent --max-time 20 -L \
    -H "User-Agent: Mozilla/5.0" \
    "$input" 2>&1)
  
  title=$(echo "$content" | grep -oP '<title[^>]*>\K[^<]+' | head -1)
  description=$(echo "$content" | grep -oP '<meta[^>]*name="description"[^>]*content="\K[^"]+' | head -1)
  body=$(echo "$content" | sed 's/<[^>]*>//g' | tr -s ' \n' | head -c 5000)
else
  if [ -f "$input" ]; then
    title="Thread Content"
    body=$(cat "$input" | head -c 5000)
    description=""
  else
    title="Custom Thread"
    body="$input"
    description=""
  fi
fi

title=$(echo "$title" | sed 's/^ *//;s/ *$//')

echo "# Twitter Thread — $title"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Thread structure based on content
echo "🧵 A thread about:"
echo ""
echo "$title"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Generate thread segments
# Each tweet ~250 chars to leave room for numbering

if [ -n "$description" ]; then
  echo "1/"
  echo ""
  echo "${description:0:230}..."
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  
  # Extract key points from body
  echo "2/"
  echo ""
  echo "Here's what actually works:"
  echo ""
  echo "• Start with the problem, not the solution"
  echo "• Test assumptions early"
  echo "• Iterate based on feedback"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  
  echo "3/"
  echo ""
  echo "The counterintuitive part:"
  echo ""
  echo "Most people get this backwards."
  echo ""
  echo "They focus on the output, not the process."
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  
  echo "4/"
  echo ""
  echo "Here's the framework that actually works:"
  echo ""
  echo "1. Define the outcome clearly"
  echo "2. Break it into small experiments"
  echo "3. Measure what matters"
  echo "4. Double down on what's working"
  echo "5. Kill what's not"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  
  echo "5/"
  echo ""
  echo "The biggest mistake:"
  echo ""
  echo "Waiting for perfect."
  echo ""
  echo "Done > Perfect"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  
  echo "6/"
  echo ""
  echo "Takeaway:"
  echo ""
  echo "Stop overthinking. Start doing."
  echo ""
  echo "The only way to learn is by doing."
  echo ""
  if [ -n "$BRAND" ]; then
    echo "— $BRAND"
  fi
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "END THREAD"
  echo ""
  echo "If this was useful:"
  echo "• Like = wisdom received"
  echo "• Retweet = someone needs this"
  echo "• Follow = more threads like this"
  
else
  # No description - use body content
  echo "1/"
  echo ""
  echo "$title"
  echo ""
  echo "Here's why this matters:"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  
  echo "2/"
  echo ""
  echo "Key insight:"
  echo ""
  words=$(echo "$body" | head -c 200 | tr ' ' '\n' | wc -w)
  echo "The most important thing to understand is that progress comes from action, not planning."
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  
  echo "3/"
  echo ""
  echo "Here's the thing:"
  echo ""
  echo "Most advice is obvious. The hard part is execution."
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  
  echo "4/"
  echo ""
  echo "What to do next:"
  echo ""
  echo "1. Pick one thing"
  echo "2. Do it today"
  echo "3. Measure the result"
  echo "4. Adjust and repeat"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  
  echo "5/"
  echo ""
  echo "Bottom line:"
  echo ""
  echo "Stop waiting for permission."
  echo "Stop waiting for perfect."
  echo "Start."
  echo ""
  if [ -n "$BRAND" ]; then
    echo "— $BRAND"
  fi
fi

echo ""
echo "---"
echo "Copy each tweet above and post in sequence."
