#!/usr/bin/env bash
# firecrawl.sh - Scrape brand data and visual assets from a website using Firecrawl API
# Usage: firecrawl.sh <url> [output-dir]
#
# Returns structured brand data + downloads reusable assets (logo, OG image, screenshot).
# If output-dir is provided, assets are saved there. Otherwise only JSON is printed.
# Requires FIRECRAWL_API_KEY in environment or .env

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$(dirname "$SKILL_DIR")")"

# Load .env from multiple locations
for envfile in "$WORKSPACE_DIR/.env" "$SKILL_DIR/.env" .env; do
  if [ -f "$envfile" ]; then
    set -a; source "$envfile"; set +a
  fi
done

URL="${1:?Usage: firecrawl.sh <url> [output-dir]}"
OUTPUT_DIR="${2:-}"

if [ -z "${FIRECRAWL_API_KEY:-}" ]; then
  echo "Error: FIRECRAWL_API_KEY not set" >&2
  exit 1
fi

RESPONSE=$(curl -s -X POST 'https://api.firecrawl.dev/v1/scrape' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" \
  -d "$(cat <<PAYLOAD
{
  "url": "$URL",
  "formats": ["markdown", "extract", "screenshot"],
  "extract": {
    "schema": {
      "type": "object",
      "properties": {
        "brandName": {"type": "string"},
        "tagline": {"type": "string"},
        "headline": {"type": "string"},
        "description": {"type": "string"},
        "features": {"type": "array", "items": {"type": "string"}},
        "logoUrl": {"type": "string", "description": "URL of the brand logo image"},
        "faviconUrl": {"type": "string", "description": "URL of the favicon"},
        "primaryColors": {"type": "array", "items": {"type": "string"}, "description": "Brand colors as hex codes (e.g. #FF4444), extract from buttons, headers, accents, gradients — not just background colors"},
        "ctaText": {"type": "string"},
        "socialLinks": {"type": "object"},
        "imageUrls": {"type": "array", "items": {"type": "string"}, "description": "All meaningful image URLs on the page: hero images, product screenshots, illustrations, mascots. Exclude tiny icons and tracking pixels."}
      }
    }
  }
}
PAYLOAD
)")

echo "$RESPONSE"

# Download assets if output directory was given
if [ -n "$OUTPUT_DIR" ]; then
  mkdir -p "$OUTPUT_DIR"
  echo "" >&2
  echo "--- Downloading assets to $OUTPUT_DIR ---" >&2

  # Helper: download a URL if non-empty
  dl() {
    local url="$1" dest="$2"
    if [ -n "$url" ] && [ "$url" != "null" ]; then
      echo "  ↓ $dest" >&2
      curl -sL "$url" -o "$OUTPUT_DIR/$dest" 2>/dev/null || true
    fi
  }

  # Portable JSON string extraction (no jq or grep -P needed)
  extract_json_string() {
    python3 -c "
import json, sys
data = json.load(sys.stdin)
keys = '$1'.split('.')
obj = data
for k in keys:
    if isinstance(obj, dict) and k in obj:
        obj = obj[k]
    else:
        sys.exit(0)
if isinstance(obj, str):
    print(obj)
" <<< "$RESPONSE" 2>/dev/null || true
  }

  extract_json_array() {
    python3 -c "
import json, sys
data = json.load(sys.stdin)
keys = '$1'.split('.')
obj = data
for k in keys:
    if isinstance(obj, dict) and k in obj:
        obj = obj[k]
    else:
        sys.exit(0)
if isinstance(obj, list):
    for item in obj:
        if isinstance(item, str):
            print(item)
" <<< "$RESPONSE" 2>/dev/null || true
  }

  dl "$(extract_json_string 'data.screenshot')" "screenshot.png"
  dl "$(extract_json_string 'data.metadata.og:image')" "og-image.png"
  dl "$(extract_json_string 'data.metadata.favicon')" "favicon.png"
  dl "$(extract_json_string 'data.extract.logoUrl')" "logo.png"

  IDX=1
  while IFS= read -r img_url; do
    [ -z "$img_url" ] && continue
    EXT="${img_url##*.}"
    EXT="${EXT%%\?*}"
    [ ${#EXT} -gt 4 ] && EXT="png"
    dl "$img_url" "image-${IDX}.${EXT}"
    IDX=$((IDX + 1))
  done < <(extract_json_array 'data.extract.imageUrls')

  echo "--- Done: $(ls "$OUTPUT_DIR" | wc -l | tr -d ' ') files saved ---" >&2
fi