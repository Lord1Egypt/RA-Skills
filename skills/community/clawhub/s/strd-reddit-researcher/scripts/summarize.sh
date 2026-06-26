#!/bin/bash
# summarize.sh — Extract pain points and themes from Reddit posts
# Usage: ./summarize.sh <posts_file>

CACHE_DIR="$(dirname "$0")/../cache"
mkdir -p "$CACHE_DIR"

if [ -z "$1" ]; then
  echo "Usage: $0 <posts_file>" >&2
  echo "Posts file should contain one URL per line or markdown links" >&2
  exit 1
fi

POSTS_FILE="$1"

if [ ! -f "$POSTS_FILE" ]; then
  echo "Error: File not found: $POSTS_FILE" >&2
  exit 1
fi

echo "# Reddit Research Summary"
echo ""
echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# Extract URLs from file (handle both plain URLs and markdown links)
urls=$(grep -oE 'https://www\.reddit\.com/[^ ]+' "$POSTS_FILE" | sort -u)

if [ -z "$urls" ]; then
  echo "No Reddit URLs found in file."
  exit 0
fi

echo "## Analyzed Posts"
echo ""

post_count=0
for url in $urls; do
  post_count=$((post_count + 1))
  
  # Skip if URL is just a domain
  if echo "$url" | grep -qE '/r/[^/]+/?$'; then
    continue
  fi
  
  echo "Processing: $url" >&2
  
  # Generate cache filename
  cache_file="$CACHE_DIR/$(echo "$url" | md5sum | cut -d' ' -f1).txt"
  
  # Check cache
  if [ -f "$cache_file" ] && [ $(( $(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || echo 0) )) -lt 86400 ]; then
    echo "  (cached)" >&2
    content=$(cat "$cache_file")
  else
    # Fetch the URL (use old.reddit.com for simpler HTML)
    content=$(curl --silent --max-time 15 -L \
      -H "User-Agent: Mozilla/5.0" \
      "${url}.json" 2>&1)
    
    if [ $? -eq 0 ] && [ -n "$content" ]; then
      echo "$content" > "$cache_file"
    fi
  fi
  
  # Extract post title
  title=$(echo "$content" | grep -oP '"title"\s*:\s*"\K[^"]+' | head -1)
  if [ -z "$title" ]; then
    title="Unknown Post"
  fi
  
  # Extract post body (selftext)
  body=$(echo "$content" | grep -oP '"selftext"\s*:\s*"\K[^"]+' | head -1)
  
  # Extract top comments
  comments=$(echo "$content" | grep -oP '"body"\s*:\s*"\K[^"]+' | head -5)
  
  echo "### $title"
  echo ""
  echo "URL: $url"
  echo ""
  
  if [ -n "$body" ]; then
    echo "**Post:** ${body:0:500}${([ ${#body} -gt 500 ] && echo '...')}"
    echo ""
  fi
  
  if [ -n "$comments" ]; then
    echo "**Top Comments:**"
    echo ""
    echo "$comments" | while read -r comment; do
      # Truncate long comments
      if [ ${#comment} -gt 300 ]; then
        echo "- ${comment:0:300}..."
      else
        echo "- $comment"
      fi
    done
    echo ""
  fi
  
  # Rate limit
  sleep 1
done

echo "---"
echo ""
echo "*Analyzed $post_count posts*"
