#!/usr/bin/env bash
set -euo pipefail

CLI="${WORKFLOW_WEAVER_CLI:-workflow-weaver}"
MCP="${WORKFLOW_WEAVER_MCP:-workflow-weaver-mcp}"

ERRORS=0
TEMP_FILES=()

pass() { echo "  ✅ $1"; }
fail() { echo "  ❌ $1"; ERRORS=$((ERRORS + 1)); }
skip() { echo "  ⏭️  $1"; }

# Cleanup trap for background MCP processes and temp files
cleanup() {
  local pids
  pids=$(jobs -p 2>/dev/null) || true
  if [ -n "$pids" ]; then
    kill $pids 2>/dev/null || true
  fi
  wait 2>/dev/null || true
  rm -f "${TEMP_FILES[@]}" 2>/dev/null || true
}
trap cleanup EXIT

# ── Test 0: jq availability ──
echo "Test 0: jq availability"
if command -v jq >/dev/null 2>&1; then
  pass "jq found: $(jq --version 2>&1 | head -1)"
else
  pass "jq not found (optional, used by skill examples)"
fi

# ── Test 1: CLI binary exists and reports version ──
echo "Test 1: CLI --version"
if command -v "$CLI" >/dev/null 2>&1; then
  VERSION_OUTPUT=$($CLI --version 2>&1) && pass "CLI reports version: $VERSION_OUTPUT" || fail "CLI --version failed"
else
  fail "CLI binary '$CLI' not found in PATH"
fi

# ── Test 2: CLI --help works ──
echo "Test 2: CLI --help"
if command -v "$CLI" >/dev/null 2>&1; then
  $CLI --help >/dev/null 2>&1 && pass "CLI --help works" || fail "CLI --help failed"
else
  skip "CLI not found"
fi

# ── Test 3: Unauthenticated auth status returns clear error ──
echo "Test 3: Unauthenticated auth status --json"
if command -v "$CLI" >/dev/null 2>&1; then
  AUTH_RESULT=$(mktemp) && TEMP_FILES+=("$AUTH_RESULT")
  (
    unset WORKFLOW_WEAVER_REFRESH_TOKEN 2>/dev/null || true
    if OUTPUT=$($CLI auth status --json 2>&1); then
      printf 'UNEXPECTED_SUCCESS\t%s\n' "$OUTPUT" > "$AUTH_RESULT"
    else
      EXIT_CODE=$?
      printf 'EXPECTED_ERROR\t%d\t%s\n' "$EXIT_CODE" "$OUTPUT" > "$AUTH_RESULT"
    fi
  )

  if grep -q '^EXPECTED_ERROR' "$AUTH_RESULT" 2>/dev/null; then
    AUTH_OUTPUT=$(cut -f3- "$AUTH_RESULT")
    if echo "$AUTH_OUTPUT" | grep -qiE 'AUTH_FAILED|not authenticated|token|unauthorized|missing|invalid'; then
      pass "Got expected auth error"
    else
      pass "Got error (non-auth-specific, but still an error): $(echo "$AUTH_OUTPUT" | head -c 200)"
    fi
  else
    AUTH_OUTPUT=$(cut -f2- "$AUTH_RESULT")
    fail "Expected error for unauthenticated request, got success: $AUTH_OUTPUT"
  fi
else
  skip "CLI not found"
fi

# ── Test 4: MCP binary exists ──
echo "Test 4: MCP binary presence"
if command -v "$MCP" >/dev/null 2>&1; then
  pass "MCP binary '$MCP' found"
else
  fail "MCP binary '$MCP' not found in PATH"
fi

# ── Test 5: MCP without token exits cleanly ──
echo "Test 5: MCP without token"
if command -v "$MCP" >/dev/null 2>&1; then
  MCP_RESULT=$(mktemp) && TEMP_FILES+=("$MCP_RESULT")
  (
    unset WORKFLOW_WEAVER_REFRESH_TOKEN 2>/dev/null || true
    if MCP_OUTPUT=$($MCP 2>&1); then
      printf 'UNEXPECTED_SUCCESS\t%s\n' "$MCP_OUTPUT" > "$MCP_RESULT"
    else
      MCP_EXIT=$?
      printf 'EXPECTED_ERROR\t%d\n' "$MCP_EXIT" > "$MCP_RESULT"
    fi
  )

  if grep -q '^EXPECTED_ERROR' "$MCP_RESULT" 2>/dev/null; then
    MCP_EXIT=$(cut -f2 "$MCP_RESULT")
    if [ "$MCP_EXIT" -eq 1 ]; then
      pass "MCP exited with code 1 (expected clean error)"
    else
      pass "MCP exited with code $MCP_EXIT (non-zero, acceptable)"
    fi
  else
    MCP_OUTPUT=$(cut -f2- "$MCP_RESULT")
    fail "MCP should exit with error when token is missing, but succeeded: $MCP_OUTPUT"
  fi
else
  skip "MCP not found"
fi

# ── Test 6: MCP protocol handshake with invalid token ──
echo "Test 6: MCP protocol handshake (invalid token)"
if command -v "$MCP" >/dev/null 2>&1; then
  RESULT_FILE=$(mktemp) && TEMP_FILES+=("$RESULT_FILE")
  export WORKFLOW_WEAVER_REFRESH_TOKEN="smoke-test-invalid-token"

  # Feed JSON-RPC initialize + initialized notification to MCP, capture output
  {
    echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke-test","version":"1.0.0"}}}'
    sleep 0.5
    echo '{"jsonrpc":"2.0","method":"notifications/initialized"}'
  } | $MCP > "$RESULT_FILE" 2>&1 &
  MCP_PID=$!

  # Poll for up to 5 seconds
  MCP_ALIVE=true
  for ((_i=1; _i<=50; _i++)); do
    if ! kill -0 "$MCP_PID" 2>/dev/null; then
      MCP_ALIVE=false
      break
    fi
    if [ -s "$RESULT_FILE" ] && grep -q "jsonrpc" "$RESULT_FILE"; then
      break
    fi
    sleep 0.1
  done

  # Clean up MCP if still running — SIGTERM first, then SIGKILL after grace period
  if [ "$MCP_ALIVE" = true ]; then
    kill "$MCP_PID" 2>/dev/null || true
    sleep 0.5
    kill -0 "$MCP_PID" 2>/dev/null && kill -9 "$MCP_PID" 2>/dev/null || true
    wait "$MCP_PID" 2>/dev/null || true
  fi

  # Unset leaked env var so tests 7-8 skip correctly
  unset WORKFLOW_WEAVER_REFRESH_TOKEN 2>/dev/null || true

  # Evaluate: must contain a valid JSON-RPC response or a clear auth error
  if [ -s "$RESULT_FILE" ] && grep -q '"jsonrpc":"2.0"' "$RESULT_FILE" && grep -q '"id":1' "$RESULT_FILE"; then
    pass "MCP responded to protocol handshake with valid initialize response"
  elif [ -s "$RESULT_FILE" ] && grep -qiE 'AUTH_FAILED|not authenticated|token|unauthorized|missing|invalid|error' "$RESULT_FILE"; then
    pass "MCP rejected invalid token (expected auth error)"
  else
    fail "MCP did not respond with valid JSON-RPC or clear error"
  fi
else
  skip "MCP not found"
fi

# ── Test 7: Live auth status (token required) ──
echo "Test 7: Live auth status"
if [ -n "${WORKFLOW_WEAVER_REFRESH_TOKEN:-}" ]; then
  AUTH_LIVE_RESULT=$(mktemp) && TEMP_FILES+=("$AUTH_LIVE_RESULT")
  (
    if AUTH_OUTPUT=$($CLI auth status --json 2>&1); then
      printf 'SUCCESS\n' > "$AUTH_LIVE_RESULT"
    else
      printf 'FAIL\t%s\n' "$AUTH_OUTPUT" > "$AUTH_LIVE_RESULT"
    fi
  )

  if grep -q '^SUCCESS' "$AUTH_LIVE_RESULT" 2>/dev/null; then
    pass "Live auth status returned successfully"
  else
    AUTH_LIVE_OUTPUT=$(cut -f2- "$AUTH_LIVE_RESULT")
    fail "Live auth status failed: $AUTH_LIVE_OUTPUT"
  fi
else
  skip "No WORKFLOW_WEAVER_REFRESH_TOKEN set"
fi

# ── Test 8: Live billing status (token required) ──
echo "Test 8: Live billing status"
if [ -n "${WORKFLOW_WEAVER_REFRESH_TOKEN:-}" ]; then
  BILLING_LIVE_RESULT=$(mktemp) && TEMP_FILES+=("$BILLING_LIVE_RESULT")
  (
    if BILLING_OUTPUT=$($CLI billing status --json 2>&1); then
      printf 'SUCCESS\n' > "$BILLING_LIVE_RESULT"
    else
      printf 'FAIL\t%s\n' "$BILLING_OUTPUT" > "$BILLING_LIVE_RESULT"
    fi
  )

  if grep -q '^SUCCESS' "$BILLING_LIVE_RESULT" 2>/dev/null; then
    pass "Live billing status returned successfully"
  else
    BILLING_LIVE_OUTPUT=$(cut -f2- "$BILLING_LIVE_RESULT")
    fail "Live billing status failed: $BILLING_LIVE_OUTPUT"
  fi
else
  skip "No WORKFLOW_WEAVER_REFRESH_TOKEN set"
fi

# ── Summary ──
echo ""
if [ "$ERRORS" -eq 0 ]; then
  echo "=== ✅ All checks passed ==="
  exit 0
else
  echo "=== ❌ $ERRORS check(s) failed ==="
  exit 1
fi
