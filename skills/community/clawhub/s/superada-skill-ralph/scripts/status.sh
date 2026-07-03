#!/bin/bash
# Check Ralph loop status for a project
# Usage: ./status.sh [project_dir]

PROJECT_DIR="${1:-$(pwd)}"
PRD_FILE="$PROJECT_DIR/scripts/ralph/prd.json"

if [ ! -f "$PRD_FILE" ]; then
  echo "❌ No prd.json found in $PROJECT_DIR/scripts/ralph/"
  exit 1
fi

echo "📊 Ralph Status: $PROJECT_DIR"
echo ""

# Get counts
TOTAL=$(jq '.userStories | length' "$PRD_FILE")
DONE=$(jq '[.userStories[] | select(.passes == true)] | length' "$PRD_FILE")
REMAINING=$((TOTAL - DONE))
PERCENT=$((DONE * 100 / TOTAL))

echo "Progress: $DONE/$TOTAL ($PERCENT%)"
echo ""

# Show progress bar
BAR_WIDTH=40
FILLED=$((DONE * BAR_WIDTH / TOTAL))
EMPTY=$((BAR_WIDTH - FILLED))
printf "["
printf "%0.s█" $(seq 1 $FILLED 2>/dev/null) || true
printf "%0.s░" $(seq 1 $EMPTY 2>/dev/null) || true
printf "]\n\n"

# List remaining stories
if [ "$REMAINING" -gt 0 ]; then
  echo "📝 Remaining stories:"
  jq -r '.userStories[] | select(.passes == false) | "  [\(.priority)] \(.title)"' "$PRD_FILE" | head -10
  
  if [ "$REMAINING" -gt 10 ]; then
    echo "  ... and $((REMAINING - 10)) more"
  fi
else
  echo "🎉 ALL STORIES COMPLETE!"
fi

echo ""
echo "📄 Last progress entry:"
tail -5 "$PROJECT_DIR/scripts/ralph/progress.txt" 2>/dev/null || echo "  (no progress.txt)"
