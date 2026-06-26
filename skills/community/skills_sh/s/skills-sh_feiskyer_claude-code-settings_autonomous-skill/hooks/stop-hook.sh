#!/bin/bash
#
# Autonomous Skill - Stop Hook
# Intercepts session exit when an autonomous loop is active.
# Checks for task completion (checkboxes + promise tags) and either
# blocks exit (feeding the prompt back) or allows it.
#

set -euo pipefail

HOOK_INPUT=$(cat)
STATE_FILE=".claude/autonomous-loop.local.md"

# No active loop → allow exit
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

# ── Parse state file frontmatter ───────────────────────────────────────
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")

ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')
COMPLETION_PROMISE=$(echo "$FRONTMATTER" | grep '^completion_promise:' | sed 's/completion_promise: *//' | sed 's/^"\(.*\)"$/\1/')
MODE=$(echo "$FRONTMATTER" | grep '^mode:' | sed 's/mode: *//')
TASK_DIR=$(echo "$FRONTMATTER" | grep '^task_dir:' | sed 's/task_dir: *//' | sed 's/^"\(.*\)"$/\1/')

# Validate numeric fields
if [[ ! "$ITERATION" =~ ^[0-9]+$ ]] || [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "Warning: Autonomous loop state corrupted. Stopping." >&2
  rm -f "$STATE_FILE"
  exit 0
fi

# ── Check max iterations ───────────────────────────────────────────────
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "Autonomous loop: Reached max iterations ($MAX_ITERATIONS). Stopping."
  rm -f "$STATE_FILE"
  exit 0
fi

# ── Get transcript and check for completion ────────────────────────────
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path' 2>/dev/null || echo "")

LAST_OUTPUT=""
if [[ -n "$TRANSCRIPT_PATH" ]] && [[ -f "$TRANSCRIPT_PATH" ]]; then
  LAST_LINE=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1 || echo "")
  if [[ -n "$LAST_LINE" ]]; then
    LAST_OUTPUT=$(echo "$LAST_LINE" | jq -r '
      .message.content |
      map(select(.type == "text")) |
      map(.text) |
      join("\n")
    ' 2>/dev/null || echo "")
  fi
fi

# ── Check promise-based completion ─────────────────────────────────────
if [[ -n "$COMPLETION_PROMISE" ]] && [[ "$COMPLETION_PROMISE" != "null" ]] && [[ -n "$LAST_OUTPUT" ]]; then
  PROMISE_TEXT=$(echo "$LAST_OUTPUT" | perl -0777 -pe 's/.*?<promise>(.*?)<\/promise>.*/$1/s; s/^\s+|\s+$//g; s/\s+/ /g' 2>/dev/null || echo "")
  if [[ -n "$PROMISE_TEXT" ]] && [[ "$PROMISE_TEXT" = "$COMPLETION_PROMISE" ]]; then
    echo "Autonomous loop: Completion promise detected — <promise>$COMPLETION_PROMISE</promise>"
    rm -f "$STATE_FILE"
    exit 0
  fi
fi

# ── Check task-list completion (structured mode only) ──────────────────
if [[ "$MODE" != "lightweight" ]] && [[ -n "$TASK_DIR" ]] && [[ -f "$TASK_DIR/task_list.md" ]]; then
  TOTAL=$(grep -c '^\- \[' "$TASK_DIR/task_list.md" 2>/dev/null || echo "0")
  DONE_COUNT=$(grep -c '^\- \[x\]' "$TASK_DIR/task_list.md" 2>/dev/null || echo "0")
  if [[ "$DONE_COUNT" -eq "$TOTAL" ]] && [[ "$TOTAL" -gt 0 ]]; then
    echo "Autonomous loop: All $TOTAL tasks complete."
    rm -f "$STATE_FILE"
    exit 0
  fi
fi

# ── Not complete — continue loop ───────────────────────────────────────
NEXT_ITERATION=$((ITERATION + 1))

# Extract prompt (everything after closing ---)
PROMPT_TEXT=$(awk '/^---$/{i++; next} i>=2' "$STATE_FILE")

if [[ -z "$PROMPT_TEXT" ]]; then
  echo "Warning: Autonomous loop state missing prompt. Stopping." >&2
  rm -f "$STATE_FILE"
  exit 0
fi

# Update iteration counter
TEMP_FILE="${STATE_FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$STATE_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$STATE_FILE"

# Build status message
if [[ "$MODE" == "lightweight" ]]; then
  STATUS_MSG="Autonomous loop iteration $NEXT_ITERATION"
else
  if [[ -n "$TASK_DIR" ]] && [[ -f "$TASK_DIR/task_list.md" ]]; then
    TOTAL=$(grep -c '^\- \[' "$TASK_DIR/task_list.md" 2>/dev/null || echo "?")
    DONE_COUNT=$(grep -c '^\- \[x\]' "$TASK_DIR/task_list.md" 2>/dev/null || echo "?")
    STATUS_MSG="Autonomous loop iteration $NEXT_ITERATION | Progress: $DONE_COUNT/$TOTAL"
  else
    STATUS_MSG="Autonomous loop iteration $NEXT_ITERATION"
  fi
fi

if [[ -n "$COMPLETION_PROMISE" ]] && [[ "$COMPLETION_PROMISE" != "null" ]]; then
  STATUS_MSG="$STATUS_MSG | Complete: output <promise>$COMPLETION_PROMISE</promise>"
fi

# Block exit, feed prompt back
jq -n \
  --arg prompt "$PROMPT_TEXT" \
  --arg msg "$STATUS_MSG" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

exit 0
