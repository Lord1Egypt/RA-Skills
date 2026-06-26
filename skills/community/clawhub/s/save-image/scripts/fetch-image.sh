#!/usr/bin/env bash
# fetch-image.sh — Download an image with proper browser headers
# Usage: fetch-image.sh <url> <output-file> [referer]
# Example: fetch-image.sh "https://i.kym-cdn.com/doge.jpg" ~/Downloads/doge.jpg "https://knowyourmeme.com/"

set -euo pipefail

URL="${1:-}"
OUTPUT="${2:-}"
REFERER="${3:-${URL}}"  # Default Referer to the URL itself if not provided

if [[ -z "$URL" || -z "$OUTPUT" ]]; then
  echo "Usage: fetch-image.sh <url> <output-file> [referer]" >&2
  exit 1
fi

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

echo "Fetching: $URL"
echo "Output:   $OUTPUT"
echo "Referer:  $REFERER"

HTTP_CODE=$(curl -s "$URL" \
  -H "User-Agent: $UA" \
  -H "Referer: $REFERER" \
  -H "Accept: image/webp,image/apng,image/*,*/*;q=0.8" \
  -H "Accept-Language: en-US,en;q=0.9" \
  -o "$OUTPUT" \
  -w "%{http_code}")

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "ERROR: HTTP $HTTP_CODE — download failed" >&2
  exit 1
fi

SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT" 2>/dev/null || echo "?")
TYPE=$(file "$OUTPUT" | cut -d: -f2 | xargs)

echo "Done: HTTP $HTTP_CODE | $SIZE bytes | $TYPE"

# Warn if we got HTML instead of an image
if echo "$TYPE" | grep -qi "html\|text"; then
  echo "WARNING: Output looks like HTML, not an image. CDN may have blocked the request." >&2
  exit 1
fi
