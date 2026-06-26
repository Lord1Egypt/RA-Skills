#!/usr/bin/env bash
#
# Local smoke test for the resilient agent skill.
#
# Runs the real wrapper.sh and monitor.sh against a mock `claude`
# binary that writes a test file and exits 0. Verifies:
#   - file was written to project dir
#   - manifest shows status=completed, exit_code=0
#   - monitor process exited
#   - tmux session was cleaned up
#   - monitor.pid was removed
#
# Use this to iterate on wrapper/monitor changes without going through
# ClawHub or consuming Claude API credits.
#
# Usage: bash scripts/local-smoke-test.sh

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SESSION="claude-smoke-$$"
FAIL=0

_cleanup() {
  tmux kill-session -t "$SESSION" 2>/dev/null || true
  [ -n "${MONITOR_PID:-}" ] && kill -9 "$MONITOR_PID" 2>/dev/null || true
  [ -n "${MOCK_BIN:-}" ] && rm -rf "$MOCK_BIN" 2>/dev/null || true
  [ -n "${PROJECT_DIR:-}" ] && rm -rf "$PROJECT_DIR" 2>/dev/null || true
  # Leave TASK_TMPDIR on failure so the user can inspect it
  if [ $FAIL -eq 0 ] && [ -n "${TASK_TMPDIR:-}" ]; then
    rm -rf "$TASK_TMPDIR" 2>/dev/null || true
  fi
}
trap _cleanup EXIT

echo "=== Local smoke test for resilient agent skill ==="
echo "Skill dir: $SKILL_DIR"
echo "Session: $SESSION"
echo

# --- Setup: mock binaries ---

MOCK_BIN=$(mktemp -d)
cat > "$MOCK_BIN/claude" << 'MOCK'
#!/usr/bin/env bash
# Mock claude: consume stdin prompt, write test file, exit 0.
cat > /dev/null
echo "mock claude: running in $PWD"
echo "smoke ok" > "$PWD/smoke-test.txt"
echo "mock claude: wrote smoke-test.txt"
exit 0
MOCK
chmod +x "$MOCK_BIN/claude"

cat > "$MOCK_BIN/openclaw" << 'MOCK'
#!/usr/bin/env bash
# Mock openclaw: swallow events silently.
exit 0
MOCK
chmod +x "$MOCK_BIN/openclaw"

export PATH="$MOCK_BIN:$PATH"

# --- Setup: task directories ---

PROJECT_DIR=$(mktemp -d)
TASK_TMPDIR=$(mktemp -d)
chmod 700 "$TASK_TMPDIR"

# --- Setup: manifest and prompt ---

cat > "$TASK_TMPDIR/manifest" << EOF
task_name=smoke-test
model=sonnet
project_dir=$PROJECT_DIR
session_name=$SESSION
pid=0
tmpdir=$TASK_TMPDIR
started_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
status=running
EOF

echo "write smoke-test.txt with content 'smoke ok'" > "$TASK_TMPDIR/prompt"

echo "TASK_TMPDIR=$TASK_TMPDIR"
echo "PROJECT_DIR=$PROJECT_DIR"
echo "MOCK_BIN=$MOCK_BIN"
echo

# --- Run: tmux session + wrapper ---

tmux new-session -d -s "$SESSION" \
  -e "TASK_TMPDIR=$TASK_TMPDIR" \
  -e "PATH=$PATH"

tmux pipe-pane -t "$SESSION" -O "cat >> $TASK_TMPDIR/output.log"

tmux send-keys -t "$SESSION" "bash $SKILL_DIR/scripts/wrapper.sh" Enter

# --- Run: monitor (fast intervals for test speed) ---

MONITOR_BASE_INTERVAL=2 \
MONITOR_GRACE_PERIOD=5 \
MONITOR_DISPATCH_WAIT=2 \
  nohup bash "$SKILL_DIR/scripts/monitor.sh" "$SESSION" "$TASK_TMPDIR" \
  > "$TASK_TMPDIR/monitor.log" 2>&1 &
MONITOR_PID=$!
echo "Launched monitor pid=$MONITOR_PID"
echo

# --- Wait: done file ---

echo "Waiting for done file..."
for i in $(seq 1 30); do
  if [ -f "$TASK_TMPDIR/done" ]; then
    echo "  done file appeared after ${i}s"
    break
  fi
  sleep 1
done

# --- Wait: monitor exit ---

echo "Waiting for monitor to exit..."
for i in $(seq 1 15); do
  if ! kill -0 "$MONITOR_PID" 2>/dev/null; then
    echo "  monitor exited after ${i}s"
    break
  fi
  sleep 1
done

# --- Assertions ---

echo
echo "=== Assertions ==="

_check() {
  local name="$1" cond="$2"
  if eval "$cond"; then
    echo "  PASS: $name"
  else
    echo "  FAIL: $name"
    FAIL=1
  fi
}

_check "done file exists" '[ -f "$TASK_TMPDIR/done" ]'
_check "test file was written" '[ -f "$PROJECT_DIR/smoke-test.txt" ]'
_check "test file has correct content" '[ "$(cat "$PROJECT_DIR/smoke-test.txt" 2>/dev/null)" = "smoke ok" ]'

STATUS=$(grep '^status=' "$TASK_TMPDIR/manifest" 2>/dev/null | head -1 | cut -d= -f2-)
_check "manifest status is completed (got: $STATUS)" '[ "$STATUS" = "completed" ]'

EXIT_CODE=$(grep '^exit_code=' "$TASK_TMPDIR/manifest" 2>/dev/null | head -1 | cut -d= -f2-)
_check "manifest exit_code is 0 (got: $EXIT_CODE)" '[ "$EXIT_CODE" = "0" ]'

_check "monitor process is gone" '! kill -0 "$MONITOR_PID" 2>/dev/null'
_check "tmux session is gone" '! tmux has-session -t "$SESSION" 2>/dev/null'
_check "monitor.pid cleaned up" '[ ! -f "$TASK_TMPDIR/monitor.pid" ]'

SIGNAL_OUTCOME=$(grep '^monitor_signal=' "$TASK_TMPDIR/manifest" 2>/dev/null | head -1 | cut -d= -f2-)
echo "  INFO: wrapper signal outcome: $SIGNAL_OUTCOME"

# --- Diagnostics ---

echo
echo "=== Diagnostics ==="
echo
echo "--- monitor.trace (direct file writes, always flushed) ---"
if [ -f "$TASK_TMPDIR/monitor.trace" ]; then
  cat "$TASK_TMPDIR/monitor.trace"
else
  echo "(no monitor.trace)"
fi
echo
echo "--- monitor.log (nohup stdout capture, may be buffered) ---"
if [ -f "$TASK_TMPDIR/monitor.log" ]; then
  cat "$TASK_TMPDIR/monitor.log"
else
  echo "(no monitor.log)"
fi
echo
echo "--- tmux pipe-pane output (wrapper run) ---"
if [ -f "$TASK_TMPDIR/output.log" ]; then
  cat "$TASK_TMPDIR/output.log"
else
  echo "(no output.log)"
fi
echo
echo "--- final manifest ---"
cat "$TASK_TMPDIR/manifest"

# --- Verdict ---

echo
if [ $FAIL -eq 0 ]; then
  echo "=== SMOKE TEST PASSED ==="
  exit 0
else
  echo "=== SMOKE TEST FAILED ==="
  echo "Inspect state at: $TASK_TMPDIR"
  exit 1
fi
