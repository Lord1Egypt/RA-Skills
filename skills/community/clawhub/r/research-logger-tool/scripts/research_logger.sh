#!/usr/bin/env bash
# research_logger.sh — Search, GIF-match, and log to Bear
set -euo pipefail

TOPIC="${1:?Usage: research_logger.sh <topic> [tags]}"
TAGS="${2:-research}"
WORKSPACE="${WORKSPACE:-$(cd "$(dirname "$0")/../../.." && pwd)}"
TEMPLATE="$WORKSPACE/notes/research_template.md"
DATE=$(date +%Y-%m-%d)

if [ ! -f "$TEMPLATE" ]; then
  echo "ERROR: Template not found at $TEMPLATE" >&2
  exit 1
fi

# ── Step 1: Web search ──────────────────────────────────────────
echo "🔍 Searching for: $TOPIC"
SEARCH_RESULTS=$(web_search "$TOPIC" 2>/dev/null || echo "{}")

# Extract top 3 links and snippets
LINK1=$(echo "$SEARCH_RESULTS" | jq -r '.[0].url // empty' 2>/dev/null || echo "")
LINK2=$(echo "$SEARCH_RESULTS" | jq -r '.[1].url // empty' 2>/dev/null || echo "")
LINK3=$(echo "$SEARCH_RESULTS" | jq -r '.[2].url // empty' 2>/dev/null || echo "")
SNIPPET1=$(echo "$SEARCH_RESULTS" | jq -r '.[0].snippet // empty' 2>/dev/null || echo "")
SNIPPET2=$(echo "$SEARCH_RESULTS" | jq -r '.[1].snippet // empty' 2>/dev/null || echo "")
SNIPPET3=$(echo "$SEARCH_RESULTS" | jq -r '.[2].snippet // empty' 2>/dev/null || echo "")

# Build links section
LINKS=""
[ -n "$LINK1" ] && LINKS="${LINKS}- [Source 1]($LINK1)
"
[ -n "$LINK2" ] && LINKS="${LINKS}- [Source 2]($LINK2)
"
[ -n "$LINK3" ] && LINKS="${LINKS}- [Source 3]($LINK3)
"

# Build findings from snippets
FINDING1="${SNIPPET1:-No finding available}"
FINDING2="${SNIPPET2:-No finding available}"
FINDING3="${SNIPPET3:-No finding available}"

# Build summary from first snippet
SUMMARY="${SNIPPET1:-Research results for $TOPIC}"

# ── Step 2: GIF match via gifgrep ───────────────────────────────
echo "🎞️  Searching GIF for: $TOPIC"
GIF_RESULT=$(gifgrep "$TOPIC" 2>/dev/null || echo "")
GIF_URL=$(echo "$GIF_RESULT" | head -1)
GIF_ALT="${TOPIC} GIF"

if [ -z "$GIF_URL" ]; then
  GIF_ALT="No GIF found"
  GIF_URL=""
fi

# ── Step 3: Fill template ───────────────────────────────────────
echo "📝 Filling template..."
CONTENT=$(sed \
  -e "s|{topic}|$TOPIC|g" \
  -e "s|{date}|$DATE|g" \
  -e "s|{tags}|$TAGS|g" \
  -e "s|{summary}|$SUMMARY|g" \
  -e "s|{finding1}|$FINDING1|g" \
  -e "s|{finding2}|$FINDING2|g" \
  -e "s|{finding3}|$FINDING3|g" \
  -e "s|{links}|$LINKS|g" \
  -e "s|{media_alt}|$GIF_ALT|g" \
  -e "s|{media_url}|$GIF_URL|g" \
  -e "s|{action1}|Review sources and verify claims|g" \
  -e "s|{action2}|Summarize key takeaways|g" \
  -e "s|{action3}|Share findings with team|g" \
  "$TEMPLATE")

# ── Step 4: Create Bear note ────────────────────────────────────
echo "🐻 Creating Bear note..."
BEAR_TAGS=$(echo "$TAGS" | tr ',' ' ')
TAG_FLAGS=""
for tag in $BEAR_TAGS; do
  TAG_FLAGS="$TAG_FLAGS --tag $tag"
done

echo "$CONTENT" | grizzly create --title "$TOPIC Research" $TAG_FLAGS

echo "✅ Research note created for: $TOPIC"
