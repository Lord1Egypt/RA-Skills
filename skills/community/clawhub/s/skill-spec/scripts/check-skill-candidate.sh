#!/bin/bash
# Stop hook: log candidate to data/candidates.md when threshold exceeded
# Pure shell — 0 token cost. Claude only involved at review time.
THRESHOLD=${SKILL_CANDIDATE_THRESHOLD:-15}
SKILL_DIR="$HOME/.claude/skills/skill-spec"
CANDIDATES_FILE="$SKILL_DIR/data/candidates.md"

INPUT=$(cat /dev/stdin 2>/dev/null || echo '{}')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "default"' 2>/dev/null)

COUNTER_FILE="/tmp/claude_skill_counter_${SESSION_ID}"
TOOLS_FILE="/tmp/claude_skill_tools_${SESSION_ID}"

if [ ! -f "$COUNTER_FILE" ]; then
  exit 0
fi

count=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)

if [ "$count" -ge "$THRESHOLD" ]; then
  # Get unique tool list
  if [ -f "$TOOLS_FILE" ]; then
    tools=$(sort "$TOOLS_FILE" | uniq | tr '\n' ',' | sed 's/,$//')
    unique_count=$(sort "$TOOLS_FILE" | uniq | wc -l | tr -d ' ')
  else
    tools="unknown"
    unique_count=0
  fi

  # Get current date
  date_str=$(date +%Y-%m-%d)

  # Ensure candidates file exists with header
  if [ ! -f "$CANDIDATES_FILE" ]; then
    echo "# Skill Candidates" > "$CANDIDATES_FILE"
    echo "" >> "$CANDIDATES_FILE"
  fi

  # Append candidate entry
  cat >> "$CANDIDATES_FILE" << ENTRY

## ${date_str} | ${count} calls | ${unique_count} tool types
- **Session:** ${SESSION_ID}
- **Tools:** ${tools}
- **Status:** pending
ENTRY

fi

# Cleanup temp files
rm -f "$COUNTER_FILE" "$TOOLS_FILE"

# Only inject prompt if threshold exceeded — use systemMessage (Stop hooks don't support hookSpecificOutput)
if [ "$count" -ge "$THRESHOLD" ]; then
  cat << EOF
{"systemMessage": "[skill-spec] Session logged to candidates (${count} calls, ${unique_count} tools). If this was repeatable work, consider running /skill-spec to review."}
EOF
fi
