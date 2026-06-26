#!/bin/bash
# Self-Optimization Error Detector Hook
# Emits a reminder when tool output looks like a meaningful failure.

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

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
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

if [ "$contains_error" = true ]; then
    cat << 'EOF'
<self-optimization-error>
Meaningful failure detected. If it required investigation or may recur:
- log it to .learnings/ERRORS.md
- link related incidents
- promote stable fixes into repo guidance

Use the error format: [ERR-YYYYMMDD-XXX]
</self-optimization-error>
EOF
fi
