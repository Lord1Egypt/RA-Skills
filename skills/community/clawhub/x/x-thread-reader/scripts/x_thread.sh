#!/bin/bash
# x_thread.sh — Fetch full text or download PDF from an X/Twitter thread
# Primary method: curl twitter-thread.com/pdf/{id} and extract from HTML meta description
# No browser or JS rendering required.
#
# Usage:
#   x_thread.sh text <tweet_url_or_id>         # Print full thread text to stdout
#   x_thread.sh pdf  <tweet_url_or_id> [path]  # Download PDF (requires Chrome or agent-browser)

set -e

MODE="${1:-text}"
INPUT="$2"
OUTPUT="$3"

if [ -z "$INPUT" ]; then
  echo "Usage: x_thread.sh <text|pdf> <tweet_url_or_id> [output_path]" >&2
  exit 1
fi

# Extract tweet ID from URL or use raw ID
if [[ "$INPUT" =~ status/([0-9]+) ]]; then
  TWEET_ID="${BASH_REMATCH[1]}"
elif [[ "$INPUT" =~ ^[0-9]+$ ]]; then
  TWEET_ID="$INPUT"
else
  echo "ERROR: Could not extract tweet ID from: $INPUT" >&2
  exit 1
fi

PDF_PAGE_URL="https://twitter-thread.com/pdf/${TWEET_ID}"
THREAD_URL="https://twitter-thread.com/t/${TWEET_ID}"

case "$MODE" in
  text)
    # ── Primary: curl the /pdf/ page and extract article from HTML meta description ──
    # twitter-thread.com embeds the full article text in <meta name="description" content="...">
    # even though the page itself requires JS to render visually.
    echo "Fetching from twitter-thread.com/pdf/${TWEET_ID} ..." >&2

    HTML=$(curl -sL --max-time 30 "$PDF_PAGE_URL")

    if [ -z "$HTML" ]; then
      echo "ERROR: Empty response from twitter-thread.com" >&2
      exit 1
    fi

    # Check for "Thread Not Found" in the HTML title
    if echo "$HTML" | grep -q "Thread Not Found"; then
      echo "ERROR: Thread not found on twitter-thread.com. The thread may not be indexed yet, or it may have been deleted." >&2
      echo "TIP: Visit $THREAD_URL in a browser first to trigger indexing, then retry." >&2
      exit 1
    fi

    # Extract title from <title> tag (macOS-compatible, no PCRE)
    TITLE=$(echo "$HTML" | grep -o '<title>[^<]*</title>' | sed 's/<[^>]*>//g' | sed 's/ - PDF Version | Twitter Thread Reader//' | head -1)

    # Extract author from title (format: "Title by @handle(Name)")
    AUTHOR=$(echo "$TITLE" | grep -oE '@[a-zA-Z0-9_]+' | head -1)

    # Extract full article from meta description
    # The content attribute may contain HTML entities that need decoding
    ARTICLE=$(echo "$HTML" | python3 -c "
import sys, re, html
content = sys.stdin.read()
match = re.search(r'<meta name=\"description\" content=\"(.*?)\"', content, re.DOTALL)
if match:
    print(html.unescape(match.group(1)))
else:
    sys.exit(1)
" 2>/dev/null)

    if [ -z "$ARTICLE" ]; then
      echo "ERROR: Could not extract article text from HTML. The page structure may have changed." >&2
      exit 1
    fi

    # Output with metadata header
    echo "---"
    echo "Title: ${TITLE:-unknown}"
    echo "Author: ${AUTHOR:-unknown}"
    echo "Source: https://x.com/i/status/${TWEET_ID}"
    echo "Thread: ${THREAD_URL}"
    echo "PDF: ${PDF_PAGE_URL}"
    echo "---"
    echo ""
    echo "$ARTICLE"
    ;;

  pdf)
    # ── Download PDF via Chrome headless or agent-browser ──
    # The /pdf/ page requires JS to generate the actual PDF, so we need a browser.
    if [ -z "$OUTPUT" ]; then
      OUTPUT="$HOME/Downloads/thread-${TWEET_ID}.pdf"
    fi

    CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if [ -f "$CHROME" ]; then
      echo "Generating PDF via Chrome headless from $PDF_PAGE_URL ..." >&2
      # Give the page time to render the PDF content
      "$CHROME" --headless --print-to-pdf="$OUTPUT" --virtual-time-budget=10000 "$PDF_PAGE_URL" 2>/dev/null
    elif command -v agent-browser &>/dev/null; then
      echo "Generating PDF via agent-browser..." >&2
      agent-browser open "$PDF_PAGE_URL" 2>/dev/null
      sleep 8
      agent-browser pdf "$OUTPUT" 2>/dev/null
      agent-browser close 2>/dev/null
    else
      echo "ERROR: Neither Chrome nor agent-browser available for PDF generation" >&2
      exit 1
    fi

    if [ -f "$OUTPUT" ]; then
      echo "$OUTPUT"
    else
      echo "ERROR: PDF generation failed" >&2
      exit 1
    fi
    ;;

  *)
    echo "ERROR: Unknown mode '$MODE'. Use 'text' or 'pdf'" >&2
    exit 1
    ;;
esac
