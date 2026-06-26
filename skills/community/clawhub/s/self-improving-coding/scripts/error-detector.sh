#!/bin/bash
# Coding Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect lint errors, type errors, and runtime exceptions
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
    "SyntaxError"
    "TypeError"
    "ReferenceError"
    "NameError"
    "AttributeError"
    "ValueError"
    "IndexError"
    "KeyError"
    "ImportError"
    "ModuleNotFoundError"
    "NullPointerException"
    "ClassCastException"
    "lint"
    "ESLint"
    "Ruff"
    "Pylint"
    "warning:"
    "error:"
    "Error:"
    "ERROR:"
    "undefined"
    "null"
    "NaN"
    "stack overflow"
    "segfault"
    "Segmentation fault"
    "panic:"
    "PANIC"
    "Traceback"
    "AssertionError"
    "assertion failed"
    "expect("
    "FAIL"
    "TS2322"
    "TS2345"
    "TS2339"
    "borrow checker"
    "lifetime"
    "cannot find module"
    "unresolved import"
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
<coding-error-detected>
A coding error was detected in command output. Consider logging to .learnings/ if:
- Lint violation required a non-obvious fix → BUG_PATTERNS.md [BUG-YYYYMMDD-XXX]
- Type error revealed a design issue → BUG_PATTERNS.md with type_checker trigger
- Runtime exception had a non-trivial root cause → BUG_PATTERNS.md with runtime trigger
- The fix reveals an anti-pattern to avoid → LEARNINGS.md with anti_pattern category
- A better idiom would prevent recurrence → LEARNINGS.md with idiom_gap category

Include before/after code snippets, language, and area tag.
</coding-error-detected>
EOF
fi
