#!/bin/bash
# Meta Self-Improvement Error Detector Hook (Optional)
# Conservative detector for explicit infrastructure failures only.
# Reads CLAUDE_TOOL_OUTPUT (when provided by PostToolUse).

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

# If hook context didn't provide output, do nothing.
[ -n "$OUTPUT" ] || exit 0

ERROR_PATTERNS=(
    "failed to load skill"
    "frontmatter"
    "yaml parse"
    "metadata"
    "context length exceeded"
    "token limit exceeded"
    "prompt is too long"
    "malformed"
    "No such file or directory"
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
<meta-error-detected>
A high-signal infrastructure failure pattern was detected.
Log only if the issue required investigation or is likely to recur.
Prefer minimal, reviewed fixes for shared prompt files and hooks.
</meta-error-detected>
EOF
fi
