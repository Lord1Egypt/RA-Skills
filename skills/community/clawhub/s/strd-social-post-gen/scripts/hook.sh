#!/bin/bash
# hook.sh — Create viral hooks for social posts
# Usage: ./hook.sh <url_or_text_file>

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
  body=$(echo "$content" | sed 's/<[^>]*>//g' | tr -s ' \n' | head -c 3000)
else
  if [ -f "$input" ]; then
    title="Content"
    body=$(cat "$input" | head -c 3000)
    description=""
  else
    title="Custom"
    body="$input"
    description=""
  fi
fi

title=$(echo "$title" | sed 's/^ *//;s/ *$//')

echo "# Viral Hooks — $title"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Extract key topic from title
topic=$(echo "$title" | sed 's/[^a-zA-Z0-9 ]//g' | cut -d' ' -f1-3)

echo "## Pattern 1: The Counterintuitive"
echo ""
echo "What everyone gets wrong about $topic:"
echo "The truth will surprise you."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "## Pattern 2: The Bold Claim"
echo ""
echo "I used to think $topic was complicated."
echo "Until I learned this one thing."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "## Pattern 3: The Stat/Number Hook"
echo ""
echo "90% of people fail at $topic."
echo "Here's why (and what to do instead)."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "## Pattern 4: The Question Hook"
echo ""
echo "What's the one thing about $topic"
echo "that nobody talks about?"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "## Pattern 5: The Contrast"
echo ""
echo "Before $topic: Lost."
echo "After $topic: Focused."
echo ""
echo "Here's the difference:"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "## Pattern 6: The Command"
echo ""
echo "Stop doing $topic wrong."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "## Pattern 7: The Story Hook"
echo ""
echo "I made \$50K mistake with $topic."
echo "So you don't have to."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "## Pattern 8: The Curiosity Gap"
echo ""
echo "The $topic secret nobody shares."
echo "(It's simpler than you think.)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "## Pattern 9: The List Hook"
echo ""
echo "3 things about $topic"
echo "that will change how you think."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "## Pattern 10: The Pattern Interrupt"
echo ""
echo "\"$topic is dead.\""
echo ""
echo "Why this matters now more than ever."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -n "$BRAND" ]; then
  echo "— $BRAND"
  echo ""
fi

echo "Tips:"
echo "• Test 2-3 hooks before committing"
echo "• Watch which ones get saves/retweets"
echo "• Iterate based on engagement"
echo ""
echo "Hook format: Open with pattern → deliver value → CTA"
