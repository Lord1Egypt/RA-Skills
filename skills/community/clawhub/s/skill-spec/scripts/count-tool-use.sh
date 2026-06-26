#!/bin/bash
# PostToolUse hook: increment counter + log tool name
# Zero token cost — pure shell, no Claude involvement
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "default"' 2>/dev/null)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null)

COUNTER_FILE="/tmp/claude_skill_counter_${SESSION_ID}"
TOOLS_FILE="/tmp/claude_skill_tools_${SESSION_ID}"

# Increment counter
if [ ! -f "$COUNTER_FILE" ]; then
  echo 1 > "$COUNTER_FILE"
else
  count=$(($(cat "$COUNTER_FILE") + 1))
  echo $count > "$COUNTER_FILE"
fi

# Log tool name
if [ -n "$TOOL_NAME" ] && [ "$TOOL_NAME" != "null" ]; then
  echo "$TOOL_NAME" >> "$TOOLS_FILE"
fi

echo '{"suppressOutput": true}'
