#!/bin/bash
# scan.sh — Search Reddit for posts matching keywords
# Usage: ./scan.sh <keywords> [subreddits]
# Output: List of Reddit post titles with URLs
#
# METHOD: Uses Bing search as primary, falls back to Google, then Reddit JSON API
# Fixes: DuckDuckGo blocks automated queries — replaced with Bing/Brave approach

CACHE_DIR="$(dirname "$0")/../cache"
mkdir -p "$CACHE_DIR"

SUBREDDITS="${REDDIT_SUBREDDITS:-}"
KEYWORDS="${1:-${REDDIT_KEYWORDS:-}}"
SEARCH_ENGINE="${REDDIT_SEARCH_ENGINE:-bing}"  # bing, google, reddit

if [ -z "$KEYWORDS" ]; then
  echo "Error: No keywords provided. Set REDDIT_KEYWORDS env var or pass as argument." >&2
  echo "Usage: $0 <keywords> [subreddits]" >&2
  exit 1
fi

if [ -n "$2" ]; then
  SUBREDDITS="$2"
fi

echo "Searching Reddit for: $KEYWORDS" >&2
echo "Subreddits: ${SUBREDDITS:-all}" >&2
echo "Search engine: $SEARCH_ENGINE" >&2
echo "---" >&2

# Try multiple search engines with fallback
search_reddit() {
  local query="$1"
  local engine="$2"
  local url=""
  local response=""

  case "$engine" in
    bing)
      # Bing search — less aggressive bot blocking
      url="https://www.bing.com/search?q=$(echo "$query" | sed 's/ /+/g')"
      response=$(curl --silent --max-time 15 -L \
        -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
        -H "Accept: text/html,application/xhtml+xml" \
        -H "Accept-Language: en-US,en;q=0.9" \
        "$url" 2>&1)
      # Extract Bing result URLs
      echo "$response" | grep -oP '(?<=href=")[^"]*reddit[^"]*' | grep -oP 'https?://[^&"]+' | head -20
      ;;
    google)
      # Google search via html.duckduckgo lite (more reliable than google.com)
      url="https://html.duckduckgo.com/html/?q=$(echo "$query" | sed 's/ /+/g')"
      response=$(curl --silent --max-time 15 -L \
        -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
        "$url" 2>&1)
      echo "$response" | grep -oP '(?<=<a class="result__a" href=")[^"]+' | grep "reddit.com" | head -20
      ;;
    reddit)
      # Direct Reddit search via their JSON API
      local encoded_query=$(echo "$query" | sed 's/ /%20/g')
      url="https://www.reddit.com/search.json?q=${encoded_query}&sort=relevance&t=month&limit=20"
      response=$(curl --silent --max-time 15 -L \
        -H "User-Agent: Mozilla/5.0 (compatible; research bot 1.0)" \
        "$url" 2>&1)
      echo "$response" | python3 -c "
import sys, json, re
try:
    data = json.load(sys.stdin)
    for post in data.get('data', {}).get('children', []):
        p = post['data']
        title = p.get('title', 'Reddit Post')
        url = p.get('url', '')
        permalink = 'https://reddit.com' + p.get('permalink', '')
        # Prefer self posts and discussion URLs
        print(f\"[{title}]({permalink})\")
except: pass
" 2>/dev/null
      ;;
  esac
}

# Build search query
search_query="${KEYWORDS} site:reddit.com"
if [ -n "$SUBREDDITS" ]; then
  subs_space=$(echo "$SUBREDDITS" | tr ',' ' ')
  search_query="${KEYWORDS} reddit ${subs_space}"
fi

# Try primary engine (bing), capture results
results=""
results=$(search_reddit "$search_query" "bing")

# Fallback to reddit JSON API if bing returned nothing
if [ -z "$results" ] || [ "$(echo "$results" | wc -l)" -lt 3 ]; then
  echo "(bing returned few results, trying Reddit JSON API...)" >&2
  results=$(search_reddit "$search_query" "reddit")
fi

# Final fallback to google if still nothing
if [ -z "$results" ]; then
  echo "(trying Google fallback...)" >&2
  results=$(search_reddit "$search_query" "google")
fi

if [ -z "$results" ]; then
  echo "No results found. All search engines blocked." >&2
  echo "Suggestions:" >&2
  echo "  - Set REDDIT_SEARCH_ENGINE=reddit for direct API access" >&2
  echo "  - Check network connectivity" >&2
  echo "  - The query may genuinely have no recent Reddit posts" >&2
  exit 1
fi

echo "$results" | head -20
echo "---" >&2
count=$(echo "$results" | grep -c "reddit.com" || echo 0)
echo "Found ~$count results" >&2

exit 0
