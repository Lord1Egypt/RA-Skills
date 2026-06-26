#!/usr/bin/env bash
# Relationship OS — Initialize .relationship/ state directory
# Usage: bash init.sh [workspace_dir]
#   workspace_dir defaults to two levels above the script directory (parent of skill root)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE="${1:-$(dirname "$SKILL_DIR")/..}"
WORKSPACE="$(cd "$WORKSPACE" && pwd)"
REL_DIR="$WORKSPACE/.relationship"

echo "=== Relationship OS Initialization ==="
echo "Workspace: $WORKSPACE"
echo "State dir: $REL_DIR"

# Create directory structure
mkdir -p "$REL_DIR/timeline"
mkdir -p "$REL_DIR/threads"

# state.json — Relationship meta-state
if [ ! -f "$REL_DIR/state.json" ]; then
  cat > "$REL_DIR/state.json" << 'STATEJSON'
{
  "stage": "initial",
  "stageStarted": "",
  "interactionCount": 0,
  "emotionBaseline": { "valence": 0.0, "arousal": 0.0 },
  "userPatterns": {
    "activeHours": [],
    "avgMessagesPerDay": 0,
    "lastSeen": ""
  },
  "milestones": [],
  "stageHistory": []
}
STATEJSON
  # Populate stageStarted with jq (if available)
  if command -v jq &>/dev/null; then
    NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    jq --arg now "$NOW" '.stageStarted = $now' "$REL_DIR/state.json" > "$REL_DIR/state.json.tmp" \
      && mv "$REL_DIR/state.json.tmp" "$REL_DIR/state.json"
  fi
  echo "  [+] state.json"
else
  echo "  [=] state.json (already exists)"
fi

# secrets.json — Exclusive memories
if [ ! -f "$REL_DIR/secrets.json" ]; then
  cat > "$REL_DIR/secrets.json" << 'SECRETSJSON'
{
  "nicknames": {
    "user_calls_agent": [],
    "agent_calls_user": []
  },
  "inside_jokes": [],
  "shared_goals": [],
  "agreements": []
}
SECRETSJSON
  echo "  [+] secrets.json"
else
  echo "  [=] secrets.json (already exists)"
fi

# stance.json — Agent stances
if [ ! -f "$REL_DIR/stance.json" ]; then
  cat > "$REL_DIR/stance.json" << 'STANCEJSON'
{
  "values": [],
  "preferences": []
}
STANCEJSON
  echo "  [+] stance.json"
else
  echo "  [=] stance.json (already exists)"
fi

echo ""
echo "=== Initialization Complete ==="
echo "Directory structure:"
find "$REL_DIR" -type f | sort | while read -r f; do
  echo "  $(basename "$f")"
done
echo ""
echo "Timeline: $REL_DIR/timeline/ (empty, awaiting events)"
echo "Threads:  $REL_DIR/threads/  (empty, awaiting follow-ups)"
