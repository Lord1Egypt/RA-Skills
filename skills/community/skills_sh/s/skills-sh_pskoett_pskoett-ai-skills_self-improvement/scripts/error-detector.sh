#!/bin/bash
# Self-Improvement Error Detector Hook (agent-agnostic)
#
# Post-tool-use hook for Bash/shell commands. Supported agents:
#   - Claude Code  (PostToolUse, matcher "Bash"):   payload field `tool_response`
#   - Codex CLI    (PostToolUse, matcher "Bash"):   payload field `tool_response`
#   - Copilot CLI  (postToolUse, no matcher):       payload field `toolResult.textResultForLlm`
#
# All three agents send the hook payload as JSON on stdin. There is no
# CLAUDE_TOOL_OUTPUT environment variable.
#
# Output channel differs by agent:
#   - Claude Code and Codex CLI: plain stdout from a post-tool hook is NOT
#     shown to the model; the reminder must be returned as JSON
#     `hookSpecificOutput.additionalContext`. Both agents accept the same shape.
#   - Copilot CLI: hook output is ignored entirely (context injection is not
#     supported); error-capture guidance must live in
#     `.github/copilot-instructions.md` instead. This script is still safe to
#     register there: the JSON output is silently discarded.

set -e

INPUT=$(cat)

json_extract() {
    # $1 = jq expression, $2 = python fallback statement (uses dict `d`)
    if command -v jq >/dev/null 2>&1; then
        printf '%s' "$INPUT" | jq -r "$1" 2>/dev/null || true
    elif command -v python3 >/dev/null 2>&1; then
        printf '%s' "$INPUT" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
    exec(sys.argv[1])
except Exception:
    pass
' "$2" 2>/dev/null || true
    fi
}

# Copilot's postToolUse has no matcher and fires for every tool; filter to
# shell commands in-script. Claude Code / Codex are already filtered by the
# "Bash" matcher, so this check just passes through.
TOOL_NAME=$(json_extract '.tool_name // .toolName // ""' 'print(d.get("tool_name") or d.get("toolName") or "")')
if [ -n "$TOOL_NAME" ] && ! printf '%s' "$TOOL_NAME" | grep -qiE '^bash$|^shell$'; then
    exit 0
fi

# Extract the tool output text across payload shapes.
OUTPUT=$(json_extract '(.tool_response // .toolResult.textResultForLlm // "") | tostring' 'print(json.dumps(d.get("tool_response") or (d.get("toolResult") or {}).get("textResultForLlm") or ""))')
[ -n "$OUTPUT" ] || OUTPUT="$INPUT"

# Copilot reports failures explicitly; treat that as a direct signal.
RESULT_TYPE=$(json_extract '.toolResult.resultType // ""' 'print((d.get("toolResult") or {}).get("resultType") or "")')

# Patterns indicating errors
ERROR_PATTERNS=(
    "error:"
    "Error:"
    "ERROR:"
    "failed"
    "FAILED"
    "command not found"
    "No such file"
    "Permission denied"
    "fatal:"
    "Exception"
    "Traceback"
    "npm ERR!"
    "ModuleNotFoundError"
    "SyntaxError"
    "TypeError"
    "exit code"
    "non-zero"
)

contains_error=false
if [ "$RESULT_TYPE" = "failure" ]; then
    contains_error=true
else
    for pattern in "${ERROR_PATTERNS[@]}"; do
        if [[ "$OUTPUT" == *"$pattern"* ]]; then
            contains_error=true
            break
        fi
    done
fi

# Emit the reminder as additionalContext JSON. Claude Code and Codex CLI both
# accept this exact shape for post-tool hooks; Copilot ignores it.
if [ "$contains_error" = true ]; then
    cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "<error-detected>\nA command error was detected. Consider logging this to .learnings/ERRORS.md if:\n- The error was unexpected or non-obvious\n- It required investigation to resolve\n- It might recur in similar contexts\n- The solution could benefit future sessions\n\nUse the self-improvement skill format: [ERR-YYYYMMDD-XXX]\n</error-detected>"
  }
}
EOF
fi
