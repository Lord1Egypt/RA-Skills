#!/bin/bash
# Validate hook script outputs against Claude Code's expected schemas.
# Run this before committing changes to hook scripts.
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PASS=0
FAIL=0

echo "=== Hook Output Validation ==="
echo ""

# --- PostToolUse hook ---
echo "[PostToolUse] count-tool-use.sh"
OUTPUT=$(echo '{"session_id": "test-validate", "tool_name": "Bash"}' | "$SCRIPT_DIR/count-tool-use.sh")
# Must be valid JSON with only allowed top-level keys
VALID_KEYS='["continue","suppressOutput","stopReason","decision","reason","systemMessage","hookSpecificOutput"]'
if echo "$OUTPUT" | jq -e '. | keys[] as $k | if ($k | IN("continue","suppressOutput","stopReason","decision","reason","systemMessage","hookSpecificOutput")) then true else error("invalid key: \($k)") end' > /dev/null 2>&1; then
  echo "  PASS: valid keys"
  PASS=$((PASS + 1))
else
  echo "  FAIL: invalid keys in output: $OUTPUT"
  FAIL=$((FAIL + 1))
fi

# If hookSpecificOutput exists, validate hookEventName matches allowed values for PostToolUse
if echo "$OUTPUT" | jq -e '.hookSpecificOutput' > /dev/null 2>&1; then
  EVENT=$(echo "$OUTPUT" | jq -r '.hookSpecificOutput.hookEventName // ""')
  if [ "$EVENT" = "PostToolUse" ] || [ "$EVENT" = "PostToolBatch" ]; then
    echo "  PASS: hookEventName=$EVENT (valid for PostToolUse)"
    PASS=$((PASS + 1))
  else
    echo "  FAIL: hookEventName=$EVENT (must be PostToolUse or PostToolBatch)"
    FAIL=$((FAIL + 1))
  fi
fi
echo ""

# Cleanup PostToolUse temp files
rm -f /tmp/claude_skill_counter_test-validate /tmp/claude_skill_tools_test-validate

# --- Stop hook (below threshold) ---
echo "[Stop] check-skill-candidate.sh (below threshold)"
OUTPUT=$(echo '{"session_id": "test-validate-stop"}' | "$SCRIPT_DIR/check-skill-candidate.sh")
if [ -z "$OUTPUT" ]; then
  echo "  PASS: no output when below threshold"
  PASS=$((PASS + 1))
else
  echo "  FAIL: should produce no output below threshold, got: $OUTPUT"
  FAIL=$((FAIL + 1))
fi
echo ""

# --- Stop hook (above threshold) ---
echo "[Stop] check-skill-candidate.sh (above threshold)"
echo 20 > /tmp/claude_skill_counter_test-validate-stop
printf "Bash\nEdit\nWrite\n" > /tmp/claude_skill_tools_test-validate-stop
OUTPUT=$(echo '{"session_id": "test-validate-stop"}' | "$SCRIPT_DIR/check-skill-candidate.sh")

# Stop hooks MUST NOT use hookSpecificOutput
if echo "$OUTPUT" | jq -e '.hookSpecificOutput' > /dev/null 2>&1; then
  echo "  FAIL: Stop hooks cannot use hookSpecificOutput!"
  echo "  Output: $OUTPUT"
  FAIL=$((FAIL + 1))
else
  echo "  PASS: no hookSpecificOutput (correct for Stop)"
  PASS=$((PASS + 1))
fi

# Validate only allowed top-level keys for Stop
if echo "$OUTPUT" | jq -e '. | keys[] as $k | if ($k | IN("continue","suppressOutput","stopReason","decision","reason","systemMessage")) then true else error("invalid key: \($k)") end' > /dev/null 2>&1; then
  echo "  PASS: valid keys for Stop hook"
  PASS=$((PASS + 1))
else
  echo "  FAIL: invalid keys in Stop output: $OUTPUT"
  FAIL=$((FAIL + 1))
fi

# Must be valid JSON
if echo "$OUTPUT" | jq . > /dev/null 2>&1; then
  echo "  PASS: valid JSON"
  PASS=$((PASS + 1))
else
  echo "  FAIL: invalid JSON: $OUTPUT"
  FAIL=$((FAIL + 1))
fi
echo ""

# --- Summary ---
echo "=== Results: $PASS passed, $FAIL failed ==="
if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
