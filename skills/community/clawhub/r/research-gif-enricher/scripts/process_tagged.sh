#!/usr/bin/env bash
# process_tagged.sh — Batch-enrich Bear notes tagged 「待整理」 with GIFs
set -euo pipefail

TOKEN_FILE="${GRIZZLY_TOKEN_FILE:-$HOME/.config/grizzly/token}"
TAG="待整理"
DELAY=1  # seconds between API calls

if ! command -v grizzly &>/dev/null; then
  echo "❌ grizzly not found. Install: go install github.com/tylerwince/grizzly/cmd/grizzly@latest"
  exit 1
fi

if [ ! -f "$TOKEN_FILE" ]; then
  echo "❌ Bear token not found at $TOKEN_FILE"
  exit 1
fi

echo "🔍 Fetching notes tagged #$TAG..."
NOTES_JSON=$(grizzly open-tag --name "$TAG" --enable-callback --json --token-file "$TOKEN_FILE" 2>/dev/null || echo '{"notes":[]}')

# Extract note IDs — grizzly JSON format varies; try common shapes
NOTE_IDS=$(echo "$NOTES_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
notes = data if isinstance(data, list) else data.get('notes', data.get('note', []))
if isinstance(notes, dict): notes = [notes]
for n in notes:
    nid = n.get('identifier', n.get('id', n.get('ID', '')))
    if nid: print(nid)
" 2>/dev/null || true)

if [ -z "$NOTE_IDS" ]; then
  echo "✅ No notes tagged #$TAG found. Nothing to do."
  exit 0
fi

PROCESSED=0
SKIPPED=0

while IFS= read -r NOTE_ID; do
  [ -z "$NOTE_ID" ] && continue
  echo "📝 Processing note $NOTE_ID..."

  # Read note content
  NOTE_JSON=$(grizzly open-note --id "$NOTE_ID" --enable-callback --json --token-file "$TOKEN_FILE" 2>/dev/null || echo '{}')
  TITLE=$(echo "$NOTE_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
note = data if isinstance(data, dict) and 'title' in data else data.get('note', data)
print(note.get('title', ''))
" 2>/dev/null || echo "")
  CONTENT=$(echo "$NOTE_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
note = data if isinstance(data, dict) and 'text' in data else data.get('note', data)
print(note.get('text', ''))
" 2>/dev/null || echo "")

  # Derive search keywords from title (first 3 meaningful words)
  QUERY=$(echo "$TITLE" | python3 -c "
import sys, re
title = sys.stdin.read().strip()
words = re.findall(r'[a-zA-Z\u4e00-\u9fff]+', title)
print(' '.join(words[:3]) if words else title[:30])
" 2>/dev/null || echo "${TITLE:0:30}")

  if [ -z "$QUERY" ]; then
    echo "  ⚠️  No query derived, skipping."
    SKIPPED=$((SKIPPED + 1))
    sleep "$DELAY"
    continue
  fi

  echo "  🔎 Searching GIF for: $QUERY"

  # Search GIF via gifgrep (curl to Tenor/Giphy as fallback)
  GIF_URL=""
  if command -v gifgrep &>/dev/null; then
    GIF_URL=$(gifgrep search "$QUERY" --limit 1 --json 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
results = data if isinstance(data, list) else data.get('results', [])
if results: print(results[0].get('url', results[0].get('media', [{}])[0].get('gif', {}).get('url', '')))
" 2>/dev/null || echo "")
  fi

  # Fallback: search via web
  if [ -z "$GIF_URL" ]; then
    GIF_URL=$(curl -s "https://tenor.googleapis.com/v2/search?q=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")&key=AIzaSyAyimkuYQYF_FXVALexPuGQctUWRURdCYQ&limit=1" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
results = data.get('results', [])
if results: print(results[0].get('media_formats', {}).get('gif', {}).get('url', ''))
" 2>/dev/null || echo "")
  fi

  if [ -z "$GIF_URL" ]; then
    echo "  ⚠️  No GIF found, skipping."
    SKIPPED=$((SKIPPED + 1))
    sleep "$DELAY"
    continue
  fi

  # Append GIF to note
  ALT_TEXT="${QUERY} gif"
  printf '\n## Supporting Media\n\n![%s](%s)\n' "$ALT_TEXT" "$GIF_URL" \
    | grizzly add-text --id "$NOTE_ID" --mode append --token-file "$TOKEN_FILE"

  echo "  ✅ GIF appended: $GIF_URL"

  # Strip the tag from note content by rewriting without #待整理
  if echo "$CONTENT" | grep -q '#待整理'; then
    NEW_CONTENT=$(echo "$CONTENT" | sed 's/#待整理//g' | sed '/^$/N;/^\n$/d')
    echo "$NEW_CONTENT" | grizzly add-text --id "$NOTE_ID" --mode replace --token-file "$TOKEN_FILE"
    echo "  🏷️  Tag #$TAG removed"
  fi

  PROCESSED=$((PROCESSED + 1))
  sleep "$DELAY"
done <<< "$NOTE_IDS"

echo ""
echo "📊 Done: $PROCESSED processed, $SKIPPED skipped"
