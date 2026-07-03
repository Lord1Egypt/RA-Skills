#!/bin/bash
# Run Ralph loop on a project
# Usage: ./run-ralph.sh [project_dir] [max_iterations] [--tool codex|claude]

set -e

PROJECT_DIR="${1:-$(pwd)}"
MAX_ITERATIONS="${2:-10}"
TOOL="codex"  # Default to Codex CLI

# Parse optional --tool argument
for arg in "$@"; do
  case $arg in
    --tool=*)
      TOOL="${arg#*=}"
      ;;
  esac
done

RALPH_DIR="$PROJECT_DIR/scripts/ralph"
RALPH_SOURCE=~/Code/ralph

# Ensure Ralph is set up in project
if [ ! -d "$RALPH_DIR" ]; then
  echo "📦 Setting up Ralph in $PROJECT_DIR..."
  mkdir -p "$RALPH_DIR"
  cp "$RALPH_SOURCE/ralph.sh" "$RALPH_DIR/"
  cp "$RALPH_SOURCE/prompt.md" "$RALPH_DIR/"
  cp "$RALPH_SOURCE/CLAUDE.md" "$RALPH_DIR/"
  chmod +x "$RALPH_DIR/ralph.sh"
  echo "✅ Ralph installed to $RALPH_DIR"
fi

# Check for prd.json
if [ ! -f "$RALPH_DIR/prd.json" ]; then
  echo "❌ No prd.json found in $RALPH_DIR"
  echo "   Create one with: ~/agent-workspace/skills/ralph/scripts/convert-prd.sh <prd.md>"
  exit 1
fi

cd "$PROJECT_DIR"

echo "🚀 Starting Ralph Loop"
echo "   Project: $PROJECT_DIR"
echo "   Tool: $TOOL"
echo "   Max iterations: $MAX_ITERATIONS"
echo ""

# Show current status
TOTAL=$(jq '.userStories | length' "$RALPH_DIR/prd.json")
DONE=$(jq '[.userStories[] | select(.passes == true)] | length' "$RALPH_DIR/prd.json")
echo "📊 Status: $DONE/$TOTAL stories complete"
echo ""

# Modify ralph.sh to use Codex if specified
if [ "$TOOL" = "codex" ]; then
  # Run with Codex CLI instead of amp/claude
  for i in $(seq 1 $MAX_ITERATIONS); do
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Ralph Iteration $i of $MAX_ITERATIONS (Codex CLI)"
    echo "═══════════════════════════════════════════════════════════════"
    
    # Check if all done
    REMAINING=$(jq '[.userStories[] | select(.passes == false)] | length' "$RALPH_DIR/prd.json")
    if [ "$REMAINING" -eq 0 ]; then
      echo ""
      echo "🎉 ALL STORIES COMPLETE!"
      exit 0
    fi
    
    # Get next story
    NEXT_STORY=$(jq -r '[.userStories[] | select(.passes == false)] | sort_by(.priority) | .[0].title' "$RALPH_DIR/prd.json")
    echo "📝 Next story: $NEXT_STORY"
    
    # Build prompt from template
    PROMPT=$(cat "$RALPH_DIR/prompt.md")
    PROMPT="$PROMPT\n\nCurrent prd.json:\n$(cat $RALPH_DIR/prd.json)"
    
    # Run Codex
    echo "$PROMPT" | codex exec --dangerously-skip-permissions 2>&1 | tee -a "$RALPH_DIR/progress.txt"
    
    # Check for completion
    DONE_NOW=$(jq '[.userStories[] | select(.passes == true)] | length' "$RALPH_DIR/prd.json")
    echo ""
    echo "📊 Progress: $DONE_NOW/$TOTAL stories complete"
    
    if [ "$DONE_NOW" -eq "$TOTAL" ]; then
      echo ""
      echo "🎉 ALL STORIES COMPLETE!"
      exit 0
    fi
  done
else
  # Use original ralph.sh with claude
  "$RALPH_DIR/ralph.sh" --tool claude "$MAX_ITERATIONS"
fi

echo ""
echo "⏸️  Max iterations reached. Run again to continue."
