#!/usr/bin/env bash
#
# Wrapper for Claude Code sessions in tmux.
#
# Handles three modes:
#   - First run:  launch claude -p with prompt
#   - Resume:     launch claude -c (continue last conversation)
#   - Completed:  done-file exists, exit early
#
# Reads TASK_TMPDIR from environment (set by tmux new-session -e).
# Reads model and project_dir from manifest.
#
# Usage: called via tmux send-keys from the orchestrator or monitor.

set -uo pipefail

# Source shared manifest helpers
_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$_SCRIPT_DIR/lib.sh"

TASK_TMPDIR="${TASK_TMPDIR:?TASK_TMPDIR not set}"

# Validate TASK_TMPDIR
if [ ! -d "$TASK_TMPDIR" ]; then
  echo "TASK_TMPDIR not a directory: $TASK_TMPDIR" >&2
  exit 1
fi

# --- Mode detection ---

# Already completed: exit early
if [ -f "$TASK_TMPDIR/done" ]; then
  echo "Task already completed (done-file exists). Exiting."
  exit 0
fi

# Read model and project_dir from manifest
MODEL="$(manifest_read model "$TASK_TMPDIR/manifest")"
PROJECT_DIR="$(manifest_read project_dir "$TASK_TMPDIR/manifest")"

# Map short aliases to full model names
case "$MODEL" in
  opus)   MODEL="claude-opus-4-6" ;;
  sonnet) MODEL="claude-sonnet-4-6" ;;
esac

cd "$PROJECT_DIR" || exit 1

if [ -f "$TASK_TMPDIR/resume" ]; then
  # Resume mode: monitor signaled a resume
  rm -f "$TASK_TMPDIR/resume"
  claude --dangerously-skip-permissions -c --model "$MODEL" &
else
  # First run: launch with prompt via stdin (avoids exposing prompt in process args)
  claude --dangerously-skip-permissions -p --model "$MODEL" - < "$TASK_TMPDIR/prompt" &
fi

# --- Lifecycle management (same for both modes) ---

CLAUDE_PID=$!
echo "$CLAUDE_PID" > "$TASK_TMPDIR/pid.tmp" \
  && mv "$TASK_TMPDIR/pid.tmp" "$TASK_TMPDIR/pid"

# Update manifest with real PID + running status (atomic)
manifest_set "$TASK_TMPDIR/manifest" \
  pid "$CLAUDE_PID" \
  status running

# Wait for Claude to finish
wait $CLAUDE_PID
ECODE=$?

# Write exit_code atomically
echo "$ECODE" > "$TASK_TMPDIR/exit_code.tmp" \
  && mv "$TASK_TMPDIR/exit_code.tmp" "$TASK_TMPDIR/exit_code"

# Determine status
if [ "$ECODE" -eq 0 ]; then
  STATUS=completed
else
  STATUS=failed
fi

# Update manifest with completion data (atomic)
manifest_set "$TASK_TMPDIR/manifest" \
  finished_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  exit_code "$ECODE" \
  status "$STATUS"

# Done-file written immediately after manifest so the monitor sees
# completion before any slow notification step. Any delay between PID
# exit and done creates a race where the monitor may classify success
# as a crash.
touch "$TASK_TMPDIR/done"

# Tell the monitor to exit immediately so cleanup happens without
# polling latency. We use SIGTERM: the monitor's trap is installed
# before monitor.pid is written, so there is no race window, and the
# trap's handle_term function distinguishes completion (done exists,
# exit 0) from external termination (exit 143). Observability is
# written to the manifest so silent failures are visible.
_signal_outcome="unknown"
if [ -f "$TASK_TMPDIR/monitor.pid" ]; then
  MONITOR_PID="$(cat "$TASK_TMPDIR/monitor.pid" 2>/dev/null || true)"
  if [ -z "$MONITOR_PID" ]; then
    _signal_outcome="monitor_pid_empty"
  elif ! kill -0 "$MONITOR_PID" 2>/dev/null; then
    _signal_outcome="monitor_not_live:$MONITOR_PID"
  elif kill -TERM "$MONITOR_PID" 2>/dev/null; then
    _signal_outcome="signaled:$MONITOR_PID"
  else
    _signal_outcome="kill_failed:$MONITOR_PID"
  fi
else
  _signal_outcome="monitor_pid_missing"
fi
manifest_set "$TASK_TMPDIR/manifest" monitor_signal "$_signal_outcome"

# Fire-and-forget notification (after signal so monitor doesn't wait on us)
openclaw system event --text "Claude done: $(manifest_read task_name "$TASK_TMPDIR/manifest")" --mode now || true
