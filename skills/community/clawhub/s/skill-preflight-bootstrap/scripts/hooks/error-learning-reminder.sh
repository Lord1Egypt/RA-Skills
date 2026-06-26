#!/bin/bash
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
  cat <<'EOF'
<skill-error-reminder>
检测到命令错误。若该错误需要调查、可能复发或具有复用价值，请按 `self-improving-agent` 规范记录到 `.learnings/ERRORS.md`。
</skill-error-reminder>
EOF
fi
