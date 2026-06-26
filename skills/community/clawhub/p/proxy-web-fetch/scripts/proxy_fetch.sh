#!/bin/bash
set -e

# Proxy Web Page Fetch - Routes through OpenClaw Manager Web Fetch Proxy
# Usage: proxy_fetch.sh --url <url> [options]

# Proxy URL from env var (required)
if [ -z "$WEB_FETCH_PROXY_URL" ]; then
    echo "Error: WEB_FETCH_PROXY_URL environment variable is not set" >&2
    exit 1
fi
PROXY_URL="$WEB_FETCH_PROXY_URL"

# Default values
URL=""
TIMEOUT=20
NO_CACHE="false"
RETURN_FORMAT="markdown"
RETAIN_IMAGES="true"
NO_GFM="false"
KEEP_IMG_DATA_URL="false"
WITH_IMAGES_SUMMARY="false"
WITH_LINKS_SUMMARY="false"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -u|--url) URL="$2"; shift ;;
        -t|--timeout) TIMEOUT="$2"; shift ;;
        -f|--format) RETURN_FORMAT="$2"; shift ;;
        --no-cache) NO_CACHE="true" ;;
        --no-images) RETAIN_IMAGES="false" ;;
        --no-gfm) NO_GFM="true" ;;
        --keep-img-data-url) KEEP_IMG_DATA_URL="true" ;;
        --images-summary) WITH_IMAGES_SUMMARY="true" ;;
        --links-summary) WITH_LINKS_SUMMARY="true" ;;
        -h|--help)
            echo "Usage: $0 --url <url> [options]"
            echo ""
            echo "Options:"
            echo "  -u, --url <url>        URL to fetch (required)"
            echo "  -t, --timeout <sec>    Request timeout in seconds (default: 20)"
            echo "  -f, --format <fmt>     Return format: markdown|text (default: markdown)"
            echo "  --no-cache             Disable caching"
            echo "  --no-images            Do not retain images in output"
            echo "  --no-gfm              Disable GitHub Flavored Markdown"
            echo "  --keep-img-data-url    Keep image data URLs"
            echo "  --images-summary       Include images summary"
            echo "  --links-summary        Include links summary"
            echo "  -h, --help             Show this help message"
            echo ""
            echo "Environment:"
            echo "  WEB_FETCH_PROXY_URL  Proxy URL (required, no default)"
            exit 0
            ;;
        *) echo "Unknown parameter: $1" >&2; exit 1 ;;
    esac
    shift
done

# Validate required parameters
if [ -z "$URL" ]; then
    echo "Error: --url is required" >&2
    exit 1
fi

# Escape special characters in URL for safe JSON encoding
SAFE_URL="${URL//\\/\\\\}"
SAFE_URL="${SAFE_URL//\"/\\\"}"

# Build JSON payload
PAYLOAD=$(cat <<EOF
{
  "url": "$SAFE_URL",
  "timeout": $TIMEOUT,
  "no_cache": $NO_CACHE,
  "return_format": "$RETURN_FORMAT",
  "retain_images": $RETAIN_IMAGES,
  "no_gfm": $NO_GFM,
  "keep_img_data_url": $KEEP_IMG_DATA_URL,
  "with_images_summary": $WITH_IMAGES_SUMMARY,
  "with_links_summary": $WITH_LINKS_SUMMARY
}
EOF
)

# Execute cURL request to Web Fetch Proxy (no auth needed)
curl -s --request POST \
  --url "${PROXY_URL}/" \
  --header "Content-Type: application/json" \
  --data "$PAYLOAD"
