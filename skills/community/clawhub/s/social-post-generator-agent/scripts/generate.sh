#!/bin/bash
# generate.sh — Generate 5 social media posts from article
# Usage: ./generate.sh <url_or_text_file>

PLATFORM="${PLATFORM:-twitter}"
TONE="${TONE:-professional}"
BRAND="${BRAND_NAME:-}"
HASHTAGS="${HASHTAGS:-}"

SKILL_DIR="$(dirname "$0")/.."
mkdir -p "$SKILL_DIR/cache"

input="$1"

if [ -z "$input" ]; then
  echo "Usage: $0 <url_or_text_file>" >&2
  exit 1
fi

# Check if input is URL
if echo "$input" | grep -qE '^https?://'; then
  echo "Fetching article: $input" >&2
  content=$(curl --silent --max-time 20 -L \
    -H "User-Agent: Mozilla/5.0" \
    "$input" 2>&1)
  
  if [ $? -ne 0 ]; then
    echo "Error: Failed to fetch URL" >&2
    exit 1
  fi
  
  # Extract title
  title=$(echo "$content" | grep -oP '<title[^>]*>\K[^<]+' | head -1)
  if [ -z "$title" ]; then
    title=$(echo "$content" | grep -oP '<h1[^>]*>\K[^<]+' | head -1)
  fi
  
  # Extract meta description
  description=$(echo "$content" | grep -oP '<meta[^>]*name="description"[^>]*content="\K[^"]+' | head -1)
  
  # Extract main text content (simplified)
  body=$(echo "$content" | sed 's/<[^>]*>//g' | tr -s ' \n' | head -c 3000)
else
  # Treat as file
  if [ -f "$input" ]; then
    title="Content from file"
    body=$(cat "$input" | head -c 3000)
    description=""
  else
    title="Custom content"
    body="$input"
    description=""
  fi
fi

# Truncate title
title=$(echo "$title" | sed 's/^ *//;s/ *$//')

# Generate hashtags based on content
generate_hashtags() {
  local text="$1"
  local ht=""
  
  # Simple keyword extraction (in production, use NLP)
  for word in $(echo "$text" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z ]//g'); do
    case "$word" in
      ai|artificial|intelligence) ht="$ht #AI" ;;
      tech|technology) ht="$ht #Tech" ;;
      business|startup|entrepreneur) ht="$ht #Business" ;;
      marketing|growth) ht="$ht #Marketing" ;;
      coding|programming|developer) ht="$ht #Coding" ;;
      productivity|work) ht="$ht #Productivity" ;;
    esac
  done
  
  echo "$ht"
}

# Twitter character limit
TWITTER_LIMIT=280
LINKEDIN_LIMIT=3000

# Platform-specific generation
if [ "$PLATFORM" = "twitter" ]; then
  LIMIT=$TWITTER_LIMIT
  echo "# Twitter Posts — Tone: $TONE"
  echo ""
  
  for i in 1 2 3 4 5; do
    echo "---"
    echo ""
    echo "**Post $i:**"
    echo ""
    
    case $i in
      1) # Hook/stat
        echo "📣 $title"
        echo ""
        echo "${description:0:150}..." 2>/dev/null || echo " insights that could change how you work."
        ;;
      2) # How-to
        echo "Here's what $title taught us:"
        echo ""
        echo "1. Focus on what matters most"
        echo "2. Start small, iterate fast"
        echo "3. Measure everything"
        ;;
      3) # Quote-style
        echo "\"The best way to predict the future is to create it.\""
        echo ""
        echo "That's the core lesson from $title."
        ;;
      4) # Question
        echo "Struggling with $(echo "$title" | tr '[:upper:]' '[:lower:]' | cut -d' ' -f1-3)?"
        echo ""
        echo "This changed everything for us ↓"
        ;;
      5) # CTA
        echo "We wrote the complete guide to $title"
        echo ""
        echo "Everything you need to know, inside."
        ;;
    esac
    
    echo ""
    htags=$(generate_hashtags "$body")
    [ -n "$HASHTAGS" ] && htags="$htags $HASHTAGS"
    echo "${htags// / }"
    
    echo ""
    if [ -n "$BRAND" ]; then
      echo "~ $BRAND"
    fi
  done
  
elif [ "$PLATFORM" = "linkedin" ]; then
  LIMIT=$LINKEDIN_LIMIT
  echo "# LinkedIn Posts — Tone: $TONE"
  echo ""
  
  for i in 1 2 3 4 5; do
    echo "---"
    echo ""
    echo "**Post $i:**"
    echo ""
    
    case $i in
      1) # Story opening
        echo "I spent years avoiding this one thing."
        echo ""
        echo "Then I read $title"
        echo ""
        echo "Here's what I learned:"
        echo ""
        echo "→ ${description:0:200}..." 2>/dev/null || echo "→ A framework for thinking differently about your work."
        echo ""
        echo "The biggest surprise? It's simpler than you think."
        ;;
      2) # Tips format
        echo "3 lessons from $title"
        echo ""
        echo "1/ Start with the problem, not the solution"
        echo "2/ Build in public — feedback accelerates growth"
        echo "3/ Your first version will be wrong, and that's fine"
        echo ""
        echo "What would you add? 👇"
        ;;
      3) # Long-form insight
        echo "The most underrated advice from $title:"
        echo ""
        echo "\"Focus is about saying no to the good so you can say yes to the great.\""
        echo ""
        echo "Most people struggle because they treat every opportunity as equal."
        echo ""
        echo "The compound effect of consistent focus is underestimated."
        ;;
      4) # Controversial take
        echo "Unpopular opinion:"
        echo ""
        echo "$(echo "$title" | sed 's/\b\w/\u&/g') is overrated."
        echo ""
        echo "Here's why the conventional approach misses what actually works:"
        echo ""
        echo "→ ${description:0:180}..." 2>/dev/null || echo "→ The real value comes from what nobody talks about."
        ;;
      5) # Case study style
        echo "Case study: How $title"
        echo ""
        echo "Background:"
        echo "The challenge was clear. The path forward was not."
        echo ""
        echo "What we did:"
        echo "→ Analyzed the root cause"
        echo "→ Tested 3 different approaches"  
        echo "→ Iterated based on data"
        echo ""
        echo "Results: Better outcomes, faster."
        ;;
    esac
    
    echo ""
    htags=$(generate_hashtags "$body")
    echo "${htags// / }"
    echo ""
    echo "#LinkedIn #Content"
    if [ -n "$BRAND" ]; then
      echo ""
      echo "— $BRAND"
    fi
  done
fi

echo ""
echo "---"
echo "Platform: $PLATFORM | Tone: $TONE | Limit: ${LIMIT} chars"
