#!/usr/bin/env bash
# research_logger.sh — Research a topic, match a GIF, fill template, output Bear-ready note.
#
# Usage:
#   bash research_logger.sh "<topic>" "<tags>" [<search_results_file>] [<gif_url>"]
#
# When called by the OpenClaw agent:
#   - The agent first runs web_search/web_fetch and writes results to a temp file
#   - The agent first runs gifgrep and captures the GIF URL
#   - Then calls this script with those inputs
#
# When called standalone (no agent inputs):
#   - Falls back to curl-based web search (DuckDuckGo instant answer API)
#   - Skips GIF matching if no gifgrep result provided

set -euo pipefail

TOPIC="${1:?Usage: $0 <topic> <tags> [search_results_file] [gif_url]}"
TAGS="${2:-research}"
SEARCH_FILE="${3:-}"
GIF_URL="${4:-}"
TEMPLATE_DIR="$(cd "$(dirname "$0")" && pwd)/references"
TEMPLATE="${TEMPLATE_DIR}/research_template.md"

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found at $TEMPLATE" >&2
    exit 1
fi

DATE=$(date +%Y-%m-%d)

# ── Step 1: Gather search results ──────────────────────────────────────────────

if [ -n "$SEARCH_FILE" ] && [ -f "$SEARCH_FILE" ]; then
    # Agent-provided search results (JSON lines: title\turl\tsnippet)
    SUMMARY=$(cut -f3 "$SEARCH_FILE" | head -3 | tr '\n' ' ' | sed 's/ $//')
    FINDING1=$(sed -n '1p' "$SEARCH_FILE" | cut -f1,3 | tr '\t' ': ')
    FINDING2=$(sed -n '2p' "$SEARCH_FILE" | cut -f1,3 | tr '\t' ': ')
    FINDING3=$(sed -n '3p' "$SEARCH_FILE" | cut -f1,3 | tr '\t' ': ')
    LINKS=$(cut -f1,2 "$SEARCH_FILE" | awk -F'\t' '{printf "- [%s](%s)\n", $1, $2}')
else
    # Fallback: use DuckDuckGo instant answer API
    DDG_URL="https://api.duckduckgo.com/?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$TOPIC'))")&format=json&no_html=1"
    DDG_JSON=$(curl -sf "$DDG_URL" 2>/dev/null || echo '{}')

    SUMMARY=$(echo "$DDG_JSON" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('Abstract', 'No summary available.')[:300])
except: print('No summary available.')
" 2>/dev/null) || SUMMARY="No summary available."

    FINDING1=$(echo "$DDG_JSON" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    r = d.get('RelatedTopics', [])
    print(r[0]['text'][:120]) if r and 'text' in r[0] else print('See sources for details.')
except: print('See sources for details.')
" 2>/dev/null) || FINDING1="See sources for details."

    FINDING2=$(echo "$DDG_JSON" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    r = d.get('RelatedTopics', [])
    print(r[1]['text'][:120]) if len(r) > 1 and 'text' in r[1] else print('See sources for details.')
except: print('See sources for details.')
" 2>/dev/null) || FINDING2="See sources for details."

    FINDING3=$(echo "$DDG_JSON" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    r = d.get('RelatedTopics', [])
    print(r[2]['text'][:120]) if len(r) > 2 and 'text' in r[2] else print('See sources for details.')
except: print('See sources for details.')
" 2>/dev/null) || FINDING3="See sources for details."

    LINKS=$(echo "$DDG_JSON" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    url = d.get('AbstractURL', '')
    if url: print(f'- [Source]({url})')
    for t in d.get('RelatedTopics', [])[:5]:
        if 'text' in t and 'FirstURL' in t:
            print(f'- [{t[\"text\"][:60]}]({t[\"FirstURL\"]})')
except: pass
" 2>/dev/null) || LINKS="- No links available"
fi

# ── Step 2: GIF matching ──────────────────────────────────────────────────────

if [ -n "$GIF_URL" ]; then
    MEDIA_ALT="GIF related to ${TOPIC}"
    MEDIA_URL="$GIF_URL"
else
    # Try gifgrep CLI if available
    if command -v gifgrep &>/dev/null; then
        GIF_RESULT=$(gifgrep "$TOPIC" 2>/dev/null | head -1) || true
        if [ -n "$GIF_RESULT" ]; then
            MEDIA_ALT="GIF: $TOPIC"
            MEDIA_URL="$GIF_RESULT"
        else
            MEDIA_ALT="No GIF found"
            MEDIA_URL=""
        fi
    else
        MEDIA_ALT="No GIF matched"
        MEDIA_URL=""
    fi
fi

# ── Step 3: Fill template ─────────────────────────────────────────────────────

OUTPUT="/tmp/research_note.md"

sed \
    -e "s|{topic}|${TOPIC}|g" \
    -e "s|{date}|${DATE}|g" \
    -e "s|{tags}|${TAGS}|g" \
    -e "s|{summary}|${SUMMARY}|g" \
    -e "s|{finding1}|${FINDING1}|g" \
    -e "s|{finding2}|${FINDING2}|g" \
    -e "s|{finding3}|${FINDING3}|g" \
    -e "s|{links}|${LINKS}|g" \
    -e "s|{media_alt}|${MEDIA_ALT}|g" \
    -e "s|{media_url}|${MEDIA_URL}|g" \
    -e "s|{action1}|Follow up on key findings|g" \
    -e "s|{action2}|Share with team|g" \
    -e "s|{action3}|Archive for future reference|g" \
    "$TEMPLATE" > "$OUTPUT"

echo "✅ Research note written to $OUTPUT"
echo "---"
cat "$OUTPUT"
