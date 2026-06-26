#!/usr/bin/env bash
# research_logger.sh — Research a topic, find a related GIF, and log to Bear
# Usage: research_logger.sh "<topic>" "<tags>" "<template_path>"
# Expects: web_search, gifgrep, grizzly (Bear CLI) to be available

set -euo pipefail

TOPIC="${1:?Usage: research_logger.sh <topic> [tags] [template_path]}"
TAGS="${2:-research}"
TEMPLATE_PATH="${3:-notes/research_template.md}"
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"

# --- Step 1: Web search for the topic ---
echo "🔍 Searching the web for: $TOPIC"
SEARCH_RESULTS=$(web_search "$TOPIC" 2>/dev/null || echo "{}")

# Parse search results — extract top links and snippets
# web_search returns JSON; pull first 3 results
LINK1=$(echo "$SEARCH_RESULTS" | jq -r '.results[0].url // empty' 2>/dev/null || echo "")
LINK2=$(echo "$SEARCH_RESULTS" | jq -r '.results[1].url // empty' 2>/dev/null || echo "")
LINK3=$(echo "$SEARCH_RESULTS" | jq -r '.results[2].url // empty' 2>/dev/null || echo "")
SNIPPET1=$(echo "$SEARCH_RESULTS" | jq -r '.results[0].snippet // empty' 2>/dev/null || echo "")
SNIPPET2=$(echo "$SEARCH_RESULTS" | jq -r '.results[1].snippet // empty' 2>/dev/null || echo "")
SNIPPET3=$(echo "$SEARCH_RESULTS" | jq -r '.results[2].snippet // empty' 2>/dev/null || echo "")

# --- Step 2: Fetch the top result for deeper content ---
echo "🌐 Fetching top result for summary..."
SUMMARY=""
if [ -n "$LINK1" ]; then
  SUMMARY=$(web_fetch "$LINK1" --max-chars 2000 2>/dev/null | head -c 1500 || echo "Summary unavailable.")
fi

# --- Step 3: Find a related GIF via gifgrep ---
echo "🎬 Finding a related GIF..."
GIF_URL=""
GIF_ALT=""
# gifgrep returns a GIF URL; use the topic as search term
GIF_RESULT=$(gifgrep "$TOPIC" 2>/dev/null || echo "")
if [ -n "$GIF_RESULT" ]; then
  GIF_URL="$GIF_RESULT"
  GIF_ALT="GIF related to $TOPIC"
else
  GIF_URL="https://media.giphy.com/media/3o7btNa0RUYa5E7ihq/giphy.gif"
  GIF_ALT="Research GIF placeholder"
fi

# --- Step 4: Read and fill the template ---
echo "📝 Filling research template..."
if [ ! -f "$WORKSPACE/$TEMPLATE_PATH" ]; then
  echo "⚠️  Template not found at $WORKSPACE/$TEMPLATE_PATH, using inline default"
  TEMPLATE="# {topic} Research
Date: {date}
Tags: {tags}

## Executive Summary
{summary}

## Key Findings
- {finding1}
- {finding2}
- {finding3}

## Sources
{links}

## Supporting Media
![{media_alt}]({media_url})

## Action Items
- [ ] {action1}
- [ ] {action2}
- [ ] {action3}"
else
  TEMPLATE=$(cat "$WORKSPACE/$TEMPLATE_PATH")
fi

DATE=$(date +"%Y-%m-%d %H:%M")
FINDING1="${SNIPPET1:-No finding available}"
FINDING2="${SNIPPET2:-No finding available}"
FINDING3="${SNIPPET3:-No finding available}"
LINKS_BLOCK="- [Source 1]($LINK1)"
[ -n "$LINK2" ] && LINKS_BLOCK="$LINKS_BLOCK
- [Source 2]($LINK2)"
[ -n "$LINK3" ] && LINKS_BLOCK="$LINKS_BLOCK
- [Source 3]($LINK3)"
[ -z "$LINK1" ] && LINKS_BLOCK="- No sources found"

NOTE_CONTENT=$(echo "$TEMPLATE" | \
  sed "s|{topic}|$TOPIC|g" | \
  sed "s|{date}|$DATE|g" | \
  sed "s|{tags}|$TAGS|g" | \
  sed "s|{summary}|${SUMMARY:-No summary available}|g" | \
  sed "s|{finding1}|$FINDING1|g" | \
  sed "s|{finding2}|$FINDING2|g" | \
  sed "s|{finding3}|$FINDING3|g" | \
  sed "s|{links}|$LINKS_BLOCK|g" | \
  sed "s|{media_alt}|$GIF_ALT|g" | \
  sed "s|{media_url}|$GIF_URL|g" | \
  sed "s|{action1}|Review findings for $TOPIC|g" | \
  sed "s|{action2}|Follow up on key sources|g" | \
  sed "s|{action3}|Summarize for team|g")

# --- Step 5: Write to Bear ---
echo "🐻 Creating Bear note..."
BEAR_TAG=$(echo "$TAGS" | tr ',' '\n' | while read -r tag; do
  [ -n "$tag" ] && echo -n " --tag $(echo "$tag" | xargs)"
done)

echo "$NOTE_CONTENT" | grizzly create --title "$TOPIC Research" $BEAR_TAG 2>/dev/null && \
  echo "✅ Research note created in Bear!" || \
  echo "❌ Failed to create Bear note. Content saved to /tmp/research_${TOPIC// /_}.md" && \
  echo "$NOTE_CONTENT" > "/tmp/research_${TOPIC// /_}.md"