#!/usr/bin/env bash
# research-assistant: fetch Bear notes tagged "待整理", insert topic-relevant GIFs
set -euo pipefail

TOKEN_FILE="${GRIZZLY_TOKEN_FILE:-$HOME/.config/grizzly/token}"
TAG="待整理"

if [ ! -f "$TOKEN_FILE" ]; then
  echo "Error: Bear token not found at $TOKEN_FILE"
  exit 1
fi

echo "🔍 Fetching notes with tag: $TAG"
NOTES_JSON=$(grizzly open-tag --name "$TAG" --enable-callback --json --token-file "$TOKEN_FILE" 2>/dev/null || echo '[]')

NOTE_COUNT=$(echo "$NOTES_JSON" | jq 'if type == "array" then length elif type == "object" then 1 else 0 end')
echo "Found $NOTE_COUNT note(s) to process"

echo "$NOTES_JSON" | jq -c '.[] | .identifier' 2>/dev/null | while read -r NOTE_ID; do
  echo "📄 Processing note: $NOTE_ID"
  NOTE_DATA=$(grizzly open-note --id "$NOTE_ID" --enable-callback --json --token-file "$TOKEN_FILE" 2>/dev/null || echo '{}')
  TITLE=$(echo "$NOTE_DATA" | jq -r '.title // "untitled"')
  echo "   Title: $TITLE"
  # Keyword extraction and GIF search are handled by the agent using web_search/gifgrep
  echo "   → Agent should extract keywords from: $TITLE and search for a GIF"
done

echo "✅ Note listing complete. Agent handles GIF insertion and tag removal."
