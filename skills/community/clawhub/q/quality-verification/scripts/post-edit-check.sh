#!/usr/bin/env bash
# post-edit-check.sh — PostToolUse hook for Write/Edit: run diagnostics immediately
# Returns additionalContext with lint/type errors if found.

set -euo pipefail

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""')

# Only trigger on file-editing tools
case "$TOOL" in
  Write|Edit|MultiEdit) ;;
  *) exit 0 ;;
esac

FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.filePath // ""')
[ -z "$FILE" ] && exit 0
[ -f "$FILE" ] || exit 0

ERRORS=""

case "$FILE" in
  *.py)
    if command -v ruff &>/dev/null; then
      LINT=$(ruff check "$FILE" --no-fix 2>&1 | head -5) || true
      [ -n "$LINT" ] && ERRORS="${ERRORS}ruff: ${LINT}\n"
    fi
    if command -v pyright &>/dev/null; then
      TYPE=$(pyright "$FILE" 2>&1 | grep -E 'error|Error' | head -3) || true
      [ -n "$TYPE" ] && ERRORS="${ERRORS}pyright: ${TYPE}\n"
    fi
    ;;
  *.ts|*.tsx)
    if command -v npx &>/dev/null && { [ -f "$(dirname "$FILE")/tsconfig.json" ] || [ -f "tsconfig.json" ]; }; then
      TYPE=$(npx tsc --noEmit "$FILE" 2>&1 | grep -E 'error TS' | head -3) || true
      [ -n "$TYPE" ] && ERRORS="${ERRORS}tsc: ${TYPE}\n"
    fi
    ;;
  *.rs)
    if command -v cargo &>/dev/null; then
      CHECK=$(cargo check 2>&1 | grep -E '^error' | head -3) || true
      [ -n "$CHECK" ] && ERRORS="${ERRORS}cargo: ${CHECK}\n"
    fi
    ;;
  *.go)
    if command -v go &>/dev/null; then
      VET=$(go vet "$FILE" 2>&1 | head -3) || true
      [ -n "$VET" ] && ERRORS="${ERRORS}go vet: ${VET}\n"
    fi
    ;;
  *.sh)
    if command -v shellcheck &>/dev/null; then
      SC=$(shellcheck "$FILE" 2>&1 | head -5) || true
      [ -n "$SC" ] && ERRORS="${ERRORS}shellcheck: ${SC}\n"
    fi
    ;;
esac

if [ -n "$ERRORS" ]; then
  MSG=$(echo -e "$ERRORS" | head -10 | tr '\n' ' ')
  jq -n --arg ctx "Post-edit diagnostics found issues: $MSG" \
    '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":$ctx}}'
fi
