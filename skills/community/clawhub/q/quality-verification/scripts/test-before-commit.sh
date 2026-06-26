#!/usr/bin/env bash
# test-before-commit.sh — PreToolUse hook: run tests before git commit
# Intercepts git commit commands and runs test suite first.
# Configurable via TEST_BEFORE_COMMIT env var (default: disabled).

set -euo pipefail

INPUT=$(head -c 20000)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null)

# Only intercept Bash
[ "$TOOL" != "Bash" ] && echo '{"continue":true}' && exit 0

# Check if enabled
[ "${TEST_BEFORE_COMMIT:-0}" != "1" ] && echo '{"continue":true}' && exit 0

COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null)
[ -z "$COMMAND" ] && echo '{"continue":true}' && exit 0

# Check for git commit (not --amend)
if ! echo "$COMMAND" | grep -qE 'git\s+commit\b' || echo "$COMMAND" | grep -qE '\-\-amend'; then
  echo '{"continue":true}'
  exit 0
fi

# Find test runner
TEST_CMD=""
if [ -f "package.json" ] && jq -e '.scripts.test' package.json &>/dev/null; then
  TEST_CMD="npm test"
elif [ -f "pytest.ini" ] || [ -f "pyproject.toml" ] || [ -d "tests" ]; then
  TEST_CMD="python3 -m pytest -q"
elif [ -f "Cargo.toml" ]; then
  TEST_CMD="cargo test"
elif [ -f "go.mod" ]; then
  TEST_CMD="go test ./..."
elif [ -f "Makefile" ] && grep -q '^test:' Makefile; then
  TEST_CMD="make test"
fi

# No test runner found — allow
if [ -z "$TEST_CMD" ]; then
  echo '{"continue":true}'
  exit 0
fi

# Run tests with optional timeout
TIMEOUT_CMD=""
if command -v timeout &>/dev/null; then
  TIMEOUT_CMD="timeout 120"
elif command -v gtimeout &>/dev/null; then
  TIMEOUT_CMD="gtimeout 120"
fi

TEST_EXIT=0
TEST_OUTPUT=$(${TIMEOUT_CMD} ${TEST_CMD} 2>&1 | tail -20) || TEST_EXIT=$?

if [ "$TEST_EXIT" -ne 0 ]; then
  jq -n --arg reason "Tests failed (exit code ${TEST_EXIT}). Fix tests before committing. Output: ${TEST_OUTPUT:0:500}" \
    '{"hookSpecificOutput":{"permissionDecision":"deny","reason":$reason}}'
else
  echo '{"continue":true}'
fi
