#!/usr/bin/env bash
set -euo pipefail

# web-info: Extract structured information from web pages
# Usage: web-info [--json|--links-only|--headers-only] <url>

VERSION="1.0.0"

show_help() {
  cat << EOF
web-info v${VERSION} - Extract information from web pages

Usage:
  web-info [OPTIONS] <url>

Options:
  --json          Output in JSON format
  --links-only    Extract only links
  --headers-only  Extract only headers (H1-H6)
  -h, --help      Show this help message
  -v, --version   Show version

Examples:
  web-info https://example.com
  web-info --json https://github.com
  web-info --links-only https://news.ycombinator.com
EOF
}

# Parse arguments
MODE="default"
URL=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --json)
      MODE="json"
      shift
      ;;
    --links-only)
      MODE="links"
      shift
      ;;
    --headers-only)
      MODE="headers"
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    -v|--version)
      echo "web-info v${VERSION}"
      exit 0
      ;;
    http://*|https://*)
      URL="$1"
      shift
      ;;
    *)
      echo "Error: Unknown option or invalid URL: $1" >&2
      echo "Try 'web-info --help' for more information." >&2
      exit 1
      ;;
  esac
done

if [[ -z "$URL" ]]; then
  echo "Error: URL is required" >&2
  show_help >&2
  exit 1
fi

# Check for curl
if ! command -v curl &> /dev/null; then
  echo "Error: curl is required but not installed" >&2
  exit 1
fi

# Fetch the webpage
HTML=$(curl -sL -A "Mozilla/5.0 (compatible; web-info/${VERSION})" "$URL" 2>/dev/null)

if [[ -z "$HTML" ]]; then
  echo "Error: Failed to fetch URL or page is empty" >&2
  exit 1
fi

# Extract title
extract_title() {
  echo "$HTML" | sed -n 's/.*<title>\(.*\)<\/title>.*/\1/p' | head -1 || echo "No title found"
}

# Extract meta description
extract_description() {
  echo "$HTML" | sed -n 's/.*<meta name="description" content="\([^"]*\)".*/\1/p' | head -1 || \
  echo "$HTML" | sed -n 's/.*<meta property="og:description" content="\([^"]*\)".*/\1/p' | head -1 || \
  echo "No description found"
}

# Extract headers
extract_headers() {
  local level=$1
  echo "$HTML" | grep -io "<h${level}>[^<]*</h${level}>" | sed -E "s/<h${level}>|<\/h${level}>//gi" || true
}

# Extract links
extract_links() {
  echo "$HTML" | grep -io '<a[^>]*href="[^"]*"[^>]*>[^<]*</a>' | \
    sed -E 's/<a[^>]*href="([^"]*)"[^>]*>([^<]*)<\/a>/\1|\2/gi' || true
}

# Extract images
extract_images() {
  echo "$HTML" | grep -io '<img[^>]*src="[^"]*"[^>]*alt="[^"]*"[^>]*>' | \
    sed -E 's/<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*/\1|\2/gi' || true
}

# Count words (approximate)
count_words() {
  # Remove HTML tags and count words
  echo "$HTML" | sed 's/<[^>]*>//g' | wc -w | tr -d ' '
}

# Main output logic
case $MODE in
  json)
    TITLE=$(extract_title)
    DESC=$(extract_description)
    H1S=$(extract_headers 1 | sed 's/"/\\"/g' | awk '{printf "\"%s\",", $0}' | sed 's/,$//')
    H2S=$(extract_headers 2 | sed 's/"/\\"/g' | awk '{printf "\"%s\",", $0}' | sed 's/,$//')
    LINKS=$(extract_links | awk -F'|' '{printf "{\"url\":\"%s\",\"text\":\"%s\"},", $1, $2}' | sed 's/,$//')
    WORD_COUNT=$(count_words)

    cat << EOF
{
  "url": "$URL",
  "title": "$TITLE",
  "description": "$DESC",
  "headers": {
    "h1": [$H1S],
    "h2": [$H2S]
  },
  "links": [$LINKS],
  "wordCount": $WORD_COUNT
}
EOF
    ;;

  links)
    echo "Links from $URL:"
    echo ""
    extract_links | while IFS='|' read -r url text; do
      echo "  - $text ($url)"
    done
    ;;

  headers)
    echo "Headers from $URL:"
    echo ""
    for level in {1..6}; do
      HEADERS=$(extract_headers $level)
      if [[ -n "$HEADERS" ]]; then
        echo "$HEADERS" | while read -r header; do
          echo "  H${level}: $header"
        done
      fi
    done
    ;;

  default)
    TITLE=$(extract_title)
    DESC=$(extract_description)
    WORD_COUNT=$(count_words)

    cat << EOF
Title: $TITLE
Description: $DESC
URL: $URL

Headers:
EOF
    for level in {1..3}; do
      HEADERS=$(extract_headers $level)
      if [[ -n "$HEADERS" ]]; then
        echo "$HEADERS" | while read -r header; do
          echo "  H${level}: $header"
        done
      fi
    done

    echo ""
    echo "Links:"
    extract_links | head -10 | while IFS='|' read -r url text; do
      echo "  - $text ($url)"
    done

    echo ""
    echo "Statistics:"
    echo "  - Word count: $WORD_COUNT"
    echo "  - Total links: $(extract_links | wc -l | tr -d ' ')"
    ;;
esac
