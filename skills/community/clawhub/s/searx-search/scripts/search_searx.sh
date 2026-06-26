#!/usr/bin/env bash
# Search using a free SearX instance.
# Usage: ./search_searx.sh "search query"

QUERY="$*"
if [[ -z "$QUERY" ]]; then
  echo "请提供搜索关键词。"
  exit 1
fi

# Fetch instance list (JSON) and extract URLs.
INSTANCE_LIST=$(curl -s https://searx.space/data/instances.json 2>/dev/null)
if [[ -z "$INSTANCE_LIST" ]]; then
  # Fallback to a hard‑coded list of known public instances when the fetch fails.
  INSTANCES=(
    "https://searx.be"
    "https://searx.org"
    "https://searx.xyz"
  )
else
  # Extract HTTPS URLs from the JSON using node for accuracy.
  INSTANCES=($(echo "$INSTANCE_LIST" | node -e "const data = JSON.parse(require('fs').readFileSync(0, 'utf8')); const urls = Object.keys(data.instances || {}).filter(u => u.startsWith('https://')); console.log(urls.slice(0, 20).join('\n'));"))
  if [[ ${#INSTANCES[@]} -eq 0 ]]; then
    echo "未找到可用的 SearX 实例。"
    exit 1
  fi
fi

MAX_ATTEMPTS=10
ATTEMPT=0
for URL in "${INSTANCES[@]}"; do
  ((ATTEMPT++))
  if (( ATTEMPT > MAX_ATTEMPTS )); then
    break
  fi
  # Encode query for URL.
  ENCODED_QUERY=$(node -e "console.log(encodeURIComponent(process.argv[1]))" "$QUERY" 2>/dev/null)
  if [[ -z "$ENCODED_QUERY" ]]; then
    # Fallback: simple space replacement
    ENCODED_QUERY=$(echo "$QUERY" | sed 's/ /%20/g')
  fi
  SEARCH_URL="${URL%/}/search?q=${ENCODED_QUERY}&format=json"
  RESPONSE=$(curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "${SEARCH_URL}" 2>/dev/null)
  if [[ -z "$RESPONSE" ]]; then
    sleep 1
    continue
  fi
  # Check for common error messages.
  if echo "$RESPONSE" | grep -q "Too Many Requests"; then
    sleep 2
    continue
  fi
  if echo "$RESPONSE" | grep -q "403 Forbidden"; then
    sleep 2
    continue
  fi
  if echo "$RESPONSE" | grep -qi "Making sure you.*not a bot"; then
    sleep 2
    continue
  fi
  # Extract up to 5 results (title and url) using a simple regex.
  RESULTS=$(echo "$RESPONSE" | grep -oE '"title":"[^"]+","url":"[^"]+"' | head -n 5 | while read -r LINE; do
    TITLE=$(echo "$LINE" | sed -E 's/.*"title":"([^\"]+)".*/\1/')
    URL=$(echo "$LINE" | sed -E "s/.*\"url\":\"([^\"]+)\".*/\1/")
    echo "${TITLE} - ${URL}"
  done)
  # Output results if any.
  if [[ -n "$RESULTS" ]]; then
    echo "$RESULTS"
    exit 0
  fi
  sleep 1
done

echo "搜索失败，请稍后重试。"
exit 1
