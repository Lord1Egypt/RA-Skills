#!/usr/bin/env bash
# research_logger.sh — Search, fetch, GIF-match, and log to Bear
set -euo pipefail

TOPIC="${1:?Usage: research_logger.sh <topic> [tags]}"
TAGS="${2:-research}"

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
TEMPLATE="$WORKSPACE/notes/research_template.md"
DATE=$(date +%Y-%m-%d)

if [ ! -f "$TEMPLATE" ]; then
  echo "ERROR: Template not found at $TEMPLATE" >&2
  exit 1
fi

# ── Step 1: Web search ──────────────────────────────────────────
echo "🔍 Searching for: $TOPIC"
SEARCH_RESULTS=$(web_search "$TOPIC" 2>/dev/null || echo "")

if [ -z "$SEARCH_RESULTS" ]; then
  echo "ERROR: web_search returned no results" >&2
  exit 1
fi

# Parse top 3 URLs and titles from search results
# Expected format: lines with "URL: ..." or just extract first 3 URLs
URLS=$(echo "$SEARCH_RESULTS" | grep -oP 'https?://[^\s)]+' | head -3)
TOP_URL=$(echo "$URLS" | head -1)

if [ -z "$TOP_URL" ]; then
  echo "ERROR: No URLs found in search results" >&2
  exit 1
fi

# ── Step 2: Fetch content from top result ───────────────────────
echo "📄 Fetching: $TOP_URL"
PAGE_CONTENT=$(web_fetch "$TOP_URL" 2>/dev/null || echo "Could not fetch content.")

# Extract a summary (first 500 chars, stripped of markdown)
SUMMARY=$(echo "$PAGE_CONTENT" | head -20 | tr -d '#' | sed 's/^ *//')

# Extract key findings (first 3 non-empty lines after the summary)
FINDINGS=$(echo "$PAGE_CONTENT" | tail -n +5 | grep -v '^$' | grep -v '^#' | head -3)

# Build links section
LINKS=""
i=1
for URL in $URLS; do
  LINKS="${LINKS}  ${i}. ${URL}
"
  i=$((i + 1))
done

# ── Step 3: GIF search via gifgrep ─────────────────────────────
echo "🎞️  Searching GIF for: $TOPIC"
GIF_RESULT=$(gifgrep "$TOPIC" 2>/dev/null || echo "")
GIF_URL=""
GIF_ALT="$TOPIC"

if [ -n "$GIF_RESULT" ]; then
  # gifgrep typically returns a URL or markdown image
  GIF_URL=$(echo "$GIF_RESULT" | grep -oP 'https?://[^\s)]+\.(gif|mp4|webm)' | head -1)
  if [ -z "$GIF_URL" ]; then
    # Try extracting any URL from the result
    GIF_URL=$(echo "$GIF_RESULT" | grep -oP 'https?://[^\s)]+' | head -1)
  fi
fi

if [ -z "$GIF_URL" ]; then
  GIF_URL="https://media.giphy.com/media/3o7btNa0RUYa5E7ihq/giphy.gif"
  GIF_ALT="$TOPIC (default GIF)"
  echo "⚠️  No GIF found, using placeholder"
fi

# ── Step 4: Fill template ──────────────────────────────────────
echo "📝 Filling template..."

# Read findings into array
F1=$(echo "$FINDINGS" | sed -n '1p' | sed 's/^ *- *//')
F2=$(echo "$FINDINGS" | sed -n '2p' | sed 's/^ *- *//')
F3=$(echo "$FINDINGS" | sed -n '3p' | sed 's/^ *- *//')

# Default action items
A1="Follow up on $TOPIC research"
A2="Review sources for credibility"
A3="Summarize findings for team"

FILLED=$(sed \
  -e "s|{topic}|$TOPIC|g" \
  -e "s|{date}|$DATE|g" \
  -e "s|{tags}|$TAGS|g" \
  -e "s|{summary}|$SUMMARY|g" \
  -e "s|{finding1}|${F1:-No finding extracted}|g" \
  -e "s|{finding2}|${F2:-No finding extracted}|g" \
  -e "s|{finding3}|${F3:-No finding extracted}|g" \
  -e "s|{links}|$LINKS|g" \
  -e "s|{media_alt}|$GIF_ALT|g" \
  -e "s|{media_url}|$GIF_URL|g" \
  -e "s|{action1}|$A1|g" \
  -e "s|{action2}|$A2|g" \
  -e "s|{action3}|$A3|g" \
  "$TEMPLATE")

# ── Step 5: Create Bear note ───────────────────────────────────
echo "🐻 Creating Bear note..."
echo "$FILLED" | grizzly create --title "$TOPIC Research" --tag "$TAGS" 2>/dev/null

if [ $? -eq 0 ]; then
  echo "✅ Research note created in Bear: $TOPIC Research"
else
  # Fallback: save to file if grizzly fails
  OUTFILE="$WORKSPACE/notes/${TOPIC// /_}_research.md"
  echo "$FILLED" > "$OUTFILE"
  echo "⚠️  Bear unavailable, saved to $OUTFILE"
fi
