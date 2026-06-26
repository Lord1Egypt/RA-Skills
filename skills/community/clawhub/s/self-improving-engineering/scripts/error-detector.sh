#!/bin/bash
# Engineering Error Detector Hook (Optional)
# Conservative detector for clear engineering failures only.
# Reads CLAUDE_TOOL_OUTPUT and emits a short reminder; no file writes, no network calls.

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
    "build failed"
    "BUILD FAILED"
    "test failed"
    "FAIL "
    "vulnerability"
    "CVE-"
    "regression"
    "timeout"
    "out of memory"
    "npm ERR!"
    "gyp ERR!"
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
<engineering-error-detected>
A high-signal engineering failure pattern was detected.
Log only if it required real investigation or is likely to recur:
- Build/test failure with non-obvious cause
- Dependency vulnerability (CVE)
- Performance regression with measured impact
</engineering-error-detected>
EOF
fi
