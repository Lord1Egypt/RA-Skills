#!/usr/bin/env bash
# research_logger.sh — Research a topic, auto-match a GIF, and log to Bear
#
# Pipeline:
#   1. Web search via Brave API (requires BRAVE_API_KEY)
#   2. Fetch & extract top 3 results
#   3. Find related GIF via Giphy API (requires GIPHY_API_KEY, optional)
#   4. Fill notes/research_template.md with gathered data
#   5. Create Bear note via grizzly
#
# Usage:
#   bash research_logger.sh "quantum computing trends" [--tags tech,quantum]
#
# Exit codes: 0=ok, 1=args, 2=template, 3=search, 4=bear
set -euo pipefail

# ── Args ──
TOPIC=""
TAGS="research"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tags) TAGS="$2"; shift 2 ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *)  TOPIC="$1"; shift ;;
  esac
done

if [[ -z "$TOPIC" ]]; then
  echo "Usage: $0 <topic> [--tags comma,separated,tags]" >&2
  exit 1
fi

# ── Paths ──
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEMPLATE="$WORKSPACE_ROOT/notes/research_template.md"

if [[ ! -f "$TEMPLATE" ]]; then
  echo "ERROR: Template not found at $TEMPLATE" >&2
  exit 2
fi

DATE="$(date +%Y-%m-%d)"

# Sanitize topic for filename: keep only alphanumeric, dashes, underscores
SAFE_TOPIC="$(echo "$TOPIC" | tr -c '[:alnum:] _-' '_' | tr -s '_' | head -c 80)"
OUTPUT="$WORKSPACE_ROOT/notes/research_${SAFE_TOPIC}_${DATE}.md"

# ── Step 1: Web Search ──
echo "🔍 Searching: $TOPIC"

BRAVE_KEY="${BRAVE_API_KEY:-}"
SUMMARY="(No search performed — set BRAVE_API_KEY)"
FINDING1="N/A"
FINDING2="N/A"
FINDING3="N/A"
LINKS="- (none)"

if [[ -n "$BRAVE_KEY" ]]; then
  # URL-encode topic safely via env var
  ENCODED_Q="$(TOPIC="$TOPIC" python3 -c 'import os,urllib.parse;print(urllib.parse.quote(os.environ["TOPIC"]))')"

  # Fetch search results and extract findings in one pipeline
  curl -sf \
    -H "Accept: application/json" \
    -H "Accept-Encoding: gzip" \
    -H "X-Subscription-Token: $BRAVE_KEY" \
    "https://api.search.brave.com/res/v1/web/search?q=${ENCODED_Q}&count=5" \
    2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    results = data.get('web', {}).get('results', [])[:3]
    descs = [r.get('description', 'No description')[:200] for r in results]
    urls = [r.get('url', '') for r in results]
    for d in descs:
        print(d)
    print('---LINKS---')
    for i, u in enumerate(urls, 1):
        if u: print(f'- [Source {i}]({u})')
except Exception:
    pass
" > /tmp/research_logger_results.txt 2>/dev/null || true

  if [[ -s /tmp/research_logger_results.txt ]]; then
    FINDING1="$(sed -n '1p' /tmp/research_logger_results.txt | head -c 200 || echo 'No result')"
    FINDING2="$(sed -n '2p' /tmp/research_logger_results.txt | head -c 200 || echo 'No result')"
    FINDING3="$(sed -n '3p' /tmp/research_logger_results.txt | head -c 200 || echo 'No result')"
    LINKS="$(sed -n '/^---LINKS---$/,$ p' /tmp/research_logger_results.txt | tail -n +2 || echo '- (none)')"
    SUMMARY="Research on '$TOPIC' — ${FINDING1:0:100}"
  fi
  rm -f /tmp/research_logger_results.txt
fi

# ── Step 2: GIF Match ──
echo "🎞️  Searching GIF: $TOPIC"

MEDIA_ALT="No media"
MEDIA_URL=""

GIPHY_KEY="${GIPHY_API_KEY:-}"
if [[ -n "$GIPHY_KEY" ]]; then
  MEDIA_URL="$(curl -sf \
    "https://api.giphy.com/v1/gifs/search?api_key=${GIPHY_KEY}&q=$(TOPIC="$TOPIC" python3 -c "import os,urllib.parse;print(urllib.parse.quote(os.environ['TOPIC']))")&limit=1&rating=g" \
    | python3 -c "
import json, sys
data = json.load(sys.stdin)
gifs = data.get('data', [])
if gifs:
    print(gifs[0].get('images', {}).get('original', {}).get('url', ''))
" 2>/dev/null || true)"

  if [[ -n "$MEDIA_URL" ]]; then
    MEDIA_ALT="GIF related to $TOPIC"
  fi
fi

if [[ -z "$MEDIA_URL" ]]; then
  echo "ℹ️  No GIF matched (set GIPHY_API_KEY for auto-matching)"
fi

# ── Step 3: Fill Template ──
echo "📝 Filling template..."

# Use Python with env vars for safe substitution (no shell injection)
TOPIC="$TOPIC" DATE="$DATE" TAGS="$TAGS" \
SUMMARY="$SUMMARY" FINDING1="$FINDING1" FINDING2="$FINDING2" FINDING3="$FINDING3" \
LINKS="$LINKS" MEDIA_ALT="$MEDIA_ALT" MEDIA_URL="$MEDIA_URL" \
TEMPLATE_PATH="$TEMPLATE" OUTPUT_PATH="$OUTPUT" \
python3 -c "
import os, re

with open(os.environ.get('OUTPUT_PATH', '/dev/stdout'), 'w') as out:
    with open(os.environ.get('TEMPLATE_PATH', '')) as f:
        result = f.read()

    replacements = {
        '{topic}':    os.environ.get('TOPIC', ''),
        '{date}':     os.environ.get('DATE', ''),
        '{tags}':     os.environ.get('TAGS', ''),
        '{summary}':  os.environ.get('SUMMARY', ''),
        '{finding1}': os.environ.get('FINDING1', ''),
        '{finding2}': os.environ.get('FINDING2', ''),
        '{finding3}': os.environ.get('FINDING3', ''),
        '{links}':    os.environ.get('LINKS', ''),
        '{media_alt}': os.environ.get('MEDIA_ALT', ''),
        '{media_url}': os.environ.get('MEDIA_URL', ''),
        '{action1}':  'Follow up on key findings',
        '{action2}':  'Review sources for deeper analysis',
        '{action3}':  'Share results with team',
    }

    for key, val in replacements.items():
        result = result.replace(key, val)

    # Remove any remaining unfilled placeholders
    result = re.sub(r'\{[a-z0-9_]+\}', '', result)

    out.write(result)
"

echo "✅ Template filled → $OUTPUT"

# ── Step 4: Create Bear Note ──
echo "🐻 Creating Bear note..."

if command -v grizzly &>/dev/null; then
  # Build tag args safely with array (no eval)
  BEAR_ARGS=("create" "--title" "$TOPIC Research")
  OLD_IFS="$IFS"
  IFS=','
  for tag in $TAGS; do
    tag="$(echo "$tag" | xargs)"
    [[ -n "$tag" ]] && BEAR_ARGS+=("--tag" "$tag")
  done
  IFS="$OLD_IFS"

  grizzly "${BEAR_ARGS[@]}" < "$OUTPUT"
  echo "✅ Bear note created: $TOPIC Research"
else
  echo "WARNING: grizzly not found, skipping Bear note creation" >&2
  echo "   Note content saved to: $OUTPUT"
fi

echo ""
echo "🎉 Research log complete!"
echo "   Topic:   $TOPIC"
echo "   Date:    $DATE"
echo "   Tags:    $TAGS"
echo "   Output:  $OUTPUT"
echo "   GIF:     ${MEDIA_URL:-none}"