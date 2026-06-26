#!/usr/bin/env bash
#
# Three-layer deterministic monitor for Claude Code sessions in tmux.
#
# Detection priority (checked in this order every iteration):
#   1. Done-file   -- task completed (exit monitor)
#   2. PID liveness -- process crashed (resume via wrapper.sh)
#   3. Output staleness -- process hung (grace period, then resume via wrapper.sh)
#
# Features:
#   - Configurable intervals via MONITOR_BASE_INTERVAL, MONITOR_MAX_INTERVAL,
#     MONITOR_DEADLINE, MONITOR_GRACE_PERIOD, MONITOR_MAX_RETRIES env vars
#   - Exponential backoff on consecutive failures (capped at MAX_INTERVAL)
#   - Manifest status updates: crashed (Layer 2), hung (Layer 3), abandoned (EXIT trap)
#   - Resume dispatched via scripts/wrapper.sh for full lifecycle management
#   - EXIT trap: updates manifest, fires openclaw notification, cleans up tmux session
#
# Usage:
#   ./scripts/monitor.sh <tmux-session> <task-tmpdir>

set -uo pipefail

# Source shared manifest helpers
_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$_SCRIPT_DIR/lib.sh"

# _log: structured log write that bypasses stdio buffering. nohup
# redirects stdout to a file, which block-buffers through libc -- so
# echo output from a still-running monitor is invisible in the log
# file until the process exits. Writing via explicit file append on
# every call sidesteps that: kernel writes are immediately visible.
# Each line also goes to stdout so normal nohup capture still works.
_log() {
  local msg="[monitor $(date -u +%H:%M:%S) pid=$$] $*"
  echo "$msg"
  if [ -n "${TASK_TMPDIR:-}" ] && [ -d "${TASK_TMPDIR:-}" ]; then
    echo "$msg" >> "$TASK_TMPDIR/monitor.trace" 2>/dev/null || true
  fi
}

# --- Cross-platform helpers ---

# get_mtime: return epoch seconds of file mtime
# Tries GNU stat first (Linux), then BSD stat (macOS). Validates the
# result is numeric because Linux `stat -f` is --file-system and outputs
# non-numeric text instead of failing -- capturing that output would
# break downstream arithmetic under set -u.
# Returns 0 if file does not exist or output is non-numeric.
get_mtime() {
  local file="$1"
  local mtime
  mtime=$(stat -c %Y "$file" 2>/dev/null) || mtime=$(stat -f %m "$file" 2>/dev/null)
  case "$mtime" in
    ''|*[!0-9]*) echo 0 ;;
    *) echo "$mtime" ;;
  esac
}

# compute_interval: exponential backoff capped at max and remaining time
compute_interval() {
  local base="$1" retries="$2" max="$3" remaining="$4"
  local interval=$(( base * (2 ** retries) ))
  [ "$interval" -gt "$max" ] && interval=$max
  [ "$interval" -gt "$remaining" ] && [ "$remaining" -gt 0 ] && interval=$remaining
  echo "$interval"
}

# --- Pane state classification ---
#
# Inspects tmux pane contents for states that pipe-pane + file mtime
# cannot detect reliably. The classifier is advisory -- the done-file
# remains the source of truth for completion. Only waiting_for_input
# is acted on immediately (abandon); other states are recorded in the
# manifest for observability.
#
# States: waiting_for_input, crash_text, upgrade_nag, unknown

# classify_pane_state SESSION — capture pane and classify
# Never fails; returns "unknown" on any capture error.
classify_pane_state() {
  local session="$1"
  local pane
  pane=$(tmux capture-pane -t "$session" -p -S -30 2>/dev/null) || { echo unknown; return; }
  _classify_pane_text "$pane"
}

# _classify_pane_text TEXT — pure classifier for testability
_classify_pane_text() {
  local pane="$1"

  # Prompts live at the bottom of a pane, not scattered throughout scrollback.
  # Matching the whole capture causes false positives when normal output
  # contains phrases like "continue?" in code, docs, or tool output.
  local tail
  tail=$(printf '%s\n' "$pane" | tail -n 5)

  # Approval/trust prompts -- unexpected with --dangerously-skip-permissions
  # but trust-on-first-use or edge-case dialogs can still appear. Patterns
  # target actual prompt shapes (trailing (y/N), Claude's specific trust
  # dialog text) rather than loose keyword matching.
  if printf '%s' "$tail" | grep -qE '\([YyNn]/[YyNn]\)[[:space:]]*$|\[[YyNn]/[YyNn]\][[:space:]]*$'; then
    echo waiting_for_input
    return
  fi
  if printf '%s' "$tail" | grep -qiE 'do you trust the files|trust the authors'; then
    echo waiting_for_input
    return
  fi

  # Crash text -- process may still be alive but in a broken state.
  # Layer 2 will catch it if/when the PID dies; this is observability.
  # Covers: Go ("panic:"), Rust ("panicked at"), segfault, core dump.
  if printf '%s' "$pane" | grep -qE 'panic:|panicked at|Segmentation fault|core dumped'; then
    echo crash_text
    return
  fi

  # Upgrade nags -- harmless but noteworthy.
  if printf '%s' "$pane" | grep -qiE 'new version available|update available'; then
    echo upgrade_nag
    return
  fi

  echo unknown
}

# --- Resume dispatch ---

# dispatch_resume: shared handler for crash and hang recovery
# Increments retry count, checks max retries, updates manifest, dispatches wrapper
dispatch_resume() {
  local reason="$1" status="$2"
  RETRY_COUNT=$(( RETRY_COUNT + 1 ))
  TOTAL_RETRY_COUNT=$(( TOTAL_RETRY_COUNT + 1 ))

  # Max retry check uses TOTAL_RETRY_COUNT, which never resets. RETRY_COUNT
  # is reset by fresh-output detection for backoff purposes, but the retry
  # cap must be cumulative so a flapping task cannot escape the budget.
  if [ "$TOTAL_RETRY_COUNT" -gt "$MONITOR_MAX_RETRIES" ]; then
    echo "Max retries ($MONITOR_MAX_RETRIES) exceeded. Abandoning task."
    # Update manifest with abandon reason before EXIT trap fires
    if [ -f "$TASK_TMPDIR/manifest" ]; then
      manifest_set "$TASK_TMPDIR/manifest" \
        status abandoned \
        abandon_reason max_retries_exceeded \
        retry_count "$TOTAL_RETRY_COUNT" \
        abandoned_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    fi
    exit 1  # EXIT trap fires for cleanup
  fi

  echo "$reason Resuming (retry #$TOTAL_RETRY_COUNT)"

  # Update manifest with status (crashed or hung)
  if [ -f "$TASK_TMPDIR/manifest" ]; then
    manifest_set "$TASK_TMPDIR/manifest" \
      status "$status" \
      retry_count "$TOTAL_RETRY_COUNT" \
      last_checked_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  fi

  # Signal wrapper to use resume mode + clear stale PID
  touch "$TASK_TMPDIR/resume"
  rm -f "$TASK_TMPDIR/pid"

  # Dispatch wrapper (resolves mode from resume file). Use printf %q to
  # shell-quote WRAPPER_PATH so paths containing spaces or shell metacharacters
  # (common on macOS under paths like "My Skills/") do not word-split when
  # the pane shell parses the send-keys input.
  local quoted_path
  quoted_path=$(printf '%q' "$WRAPPER_PATH")
  tmux send-keys -t "$SESSION" "bash $quoted_path" Enter
  sleep "${MONITOR_DISPATCH_WAIT:-10}"
}

# --- Cleanup (EXIT trap) ---

cleanup() {
  _log "cleanup starting session=${SESSION:-unset}"
  # Guard: only update manifest if task not already completed
  if [ -f "$TASK_TMPDIR/manifest" ] && [ ! -f "$TASK_TMPDIR/done" ]; then
    # Only set abandoned if not already set by dispatch_resume max-retry path
    local current_status
    current_status="$(manifest_read status "$TASK_TMPDIR/manifest")"
    if [ "$current_status" != "abandoned" ]; then
      manifest_set "$TASK_TMPDIR/manifest" \
        status abandoned \
        abandoned_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    fi
    openclaw system event --text "Task abandoned: $SESSION" --mode now 2>/dev/null || true
  fi
  tmux pipe-pane -t "$SESSION" 2>/dev/null || true
  tmux kill-session -t "$SESSION" 2>/dev/null || true
  rm -f "$TASK_TMPDIR/monitor.pid" 2>/dev/null || true
  _log "cleanup done"
}

# --- Main function ---

main() {
  SESSION="${1:?Usage: monitor.sh <tmux-session> <task-tmpdir>}"
  TASK_TMPDIR="${2:?Usage: monitor.sh <tmux-session> <task-tmpdir>}"

  # Sanitize session name: only allow alphanumeric, dash, underscore, dot
  if ! printf '%s' "$SESSION" | grep -Eq '^[A-Za-z0-9._-]+$'; then
    echo "Invalid session name: $SESSION (only alphanumeric, dash, underscore, dot allowed)" >&2
    exit 1
  fi

  # Validate TASK_TMPDIR is a directory
  if [ ! -d "$TASK_TMPDIR" ]; then
    echo "TASK_TMPDIR not a directory: $TASK_TMPDIR" >&2
    exit 1
  fi

  # Resolve wrapper path
  WRAPPER_PATH="$_SCRIPT_DIR/wrapper.sh"

  # SIGTERM handler: distinguishes wrapper-sent completion signal from
  # external termination. The wrapper sends SIGTERM after touching done;
  # if we see done when the signal arrives, it's normal completion.
  # All output is line-buffered via stdbuf-like redirect to make logs
  # observable immediately (nohup otherwise block-buffers stdout).
  handle_term() {
    _log "SIGTERM received"
    if [ -f "$TASK_TMPDIR/done" ]; then
      _log "done-file present -- normal completion path"
      exit 0
    fi
    _log "done-file absent -- external termination path"
    exit 143
  }

  # Install signal traps BEFORE writing monitor.pid, so there is no
  # window where a signal sent by the wrapper would hit default signal
  # handlers (which would kill the monitor without running cleanup).
  trap handle_term TERM
  trap 'echo "Received SIGHUP -- shutting down"; exit 129' HUP
  trap 'echo "Received SIGINT -- shutting down"; exit 130' INT
  trap cleanup EXIT

  # Record monitor PID so the wrapper can signal us on completion.
  # Without this, the wrapper's touch-done is only seen on the next
  # poll cycle -- up to MONITOR_BASE_INTERVAL seconds of latency.
  echo $$ > "$TASK_TMPDIR/monitor.pid.tmp" \
    && mv "$TASK_TMPDIR/monitor.pid.tmp" "$TASK_TMPDIR/monitor.pid"
  _log "started session=$SESSION tmpdir=$TASK_TMPDIR"

  # Configurable intervals (override via environment)
  MONITOR_BASE_INTERVAL="${MONITOR_BASE_INTERVAL:-30}"     # seconds; default 30s
  MONITOR_MAX_INTERVAL="${MONITOR_MAX_INTERVAL:-300}"      # seconds; default 5m
  MONITOR_DEADLINE="${MONITOR_DEADLINE:-18000}"             # seconds; default 5h
  MONITOR_GRACE_PERIOD="${MONITOR_GRACE_PERIOD:-30}"       # seconds; default 30s
  MONITOR_MAX_RETRIES="${MONITOR_MAX_RETRIES:-10}"         # max resume attempts
  MONITOR_DISPATCH_WAIT="${MONITOR_DISPATCH_WAIT:-10}"     # seconds; post-resume wait

  # State variables.
  # RETRY_COUNT resets on fresh output (used for backoff interval).
  # TOTAL_RETRY_COUNT never resets (used for the max-retries cap, so a
  # flapping task cannot escape the retry budget by producing output
  # between stalls).
  # WAITING_COUNT is the hysteresis counter for pane_state=waiting_for_input:
  # we only abandon after the classifier reports the same state across
  # consecutive polls, avoiding single-poll false positives.
  RETRY_COUNT=0
  TOTAL_RETRY_COUNT=0
  STALE_SINCE=""
  WAITING_COUNT=0
  START_TS="$(date +%s)"
  DEADLINE_TS=$(( START_TS + MONITOR_DEADLINE ))

  # --- Main loop ---

  while true; do
    NOW_TS="$(date +%s)"

    # Deadline check
    if [ "$NOW_TS" -ge "$DEADLINE_TS" ]; then
      echo "Deadline reached (${MONITOR_DEADLINE}s). Stopping monitor."
      exit 1  # EXIT trap fires
    fi

    # Interval calculation: exponential backoff capped at MAX and REMAINING
    REMAINING=$(( DEADLINE_TS - NOW_TS ))
    INTERVAL=$(compute_interval "$MONITOR_BASE_INTERVAL" "$RETRY_COUNT" "$MONITOR_MAX_INTERVAL" "$REMAINING")

    # Session existence check
    if ! tmux has-session -t "$SESSION" 2>/dev/null; then
      echo "tmux session $SESSION no longer exists. Stopping monitor."
      exit 0
    fi

    # PID file wait -- agent may still be starting
    if [ ! -f "$TASK_TMPDIR/pid" ]; then
      sleep "$INTERVAL"
      continue
    fi
    PID="$(cat "$TASK_TMPDIR/pid")"

    # --- Layer 1: Done-file (task completed) ---
    if [ -f "$TASK_TMPDIR/done" ]; then
      EXIT_CODE="$(cat "$TASK_TMPDIR/exit_code" 2>/dev/null || echo "unknown")"
      echo "Task completed with exit code: $EXIT_CODE"
      exit 0  # EXIT trap fires but guard prevents abandoned update
    fi

    # --- Layer 2: PID liveness (process crashed) ---
    if ! kill -0 "$PID" 2>/dev/null; then
      # Grace window: wrapper may still be writing completion markers
      # (exit_code, manifest, done) after Claude exits. A poll that
      # catches the dead PID before the wrapper touches done would
      # misclassify a successful exit as a crash. Re-check done after
      # a brief pause to close this race.
      sleep 2
      if [ -f "$TASK_TMPDIR/done" ]; then
        EXIT_CODE="$(cat "$TASK_TMPDIR/exit_code" 2>/dev/null || echo "unknown")"
        echo "Task completed with exit code: $EXIT_CODE"
        exit 0
      fi
      STALE_SINCE=""  # Clear stale state on crash
      dispatch_resume "Crash detected (PID $PID gone)." "crashed"
      continue
    fi

    # --- Layer 2.5: Pane state classification (advisory + abandon-on-wait) ---
    PANE_STATE=$(classify_pane_state "$SESSION")
    if [ "$PANE_STATE" != "unknown" ] && [ -f "$TASK_TMPDIR/manifest" ]; then
      manifest_set "$TASK_TMPDIR/manifest" pane_state "$PANE_STATE"
    fi
    if [ "$PANE_STATE" = "waiting_for_input" ]; then
      # Hysteresis: require two consecutive detections before acting.
      # The classifier can false-match on transient tail content (e.g.,
      # Claude writing a code snippet that contains a prompt-shaped line).
      # A single hit is not enough to abandon; persistence across polls
      # is the real signal.
      WAITING_COUNT=$(( WAITING_COUNT + 1 ))
      if [ "$WAITING_COUNT" -ge 2 ]; then
        echo "Task stuck waiting for user input -- abandoning (detected on $WAITING_COUNT consecutive polls)"
        if [ -f "$TASK_TMPDIR/manifest" ]; then
          manifest_set "$TASK_TMPDIR/manifest" \
            status abandoned \
            abandon_reason waiting_for_input \
            abandoned_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
        fi
        exit 1  # EXIT trap fires for cleanup
      else
        echo "Pane shows waiting_for_input -- watching for persistence before abandoning"
      fi
    else
      WAITING_COUNT=0
    fi

    # --- Layer 3: Output staleness (process alive, no done-file) ---
    if [ -f "$TASK_TMPDIR/output.log" ]; then
      OUTPUT_MTIME=$(get_mtime "$TASK_TMPDIR/output.log")
      OUTPUT_AGE=$(( NOW_TS - OUTPUT_MTIME ))
      STALENESS_THRESHOLD=$(( MONITOR_BASE_INTERVAL * 3 ))  # 3x base = 90s default

      if [ "$OUTPUT_AGE" -gt "$STALENESS_THRESHOLD" ]; then
        # Output is stale -- start or check grace period
        if [ -z "$STALE_SINCE" ]; then
          # First detection: record timestamp, do not act yet
          STALE_SINCE="$NOW_TS"
          echo "Output stale (${OUTPUT_AGE}s > ${STALENESS_THRESHOLD}s). Grace period started."
        else
          GRACE_ELAPSED=$(( NOW_TS - STALE_SINCE ))
          if [ "$GRACE_ELAPSED" -ge "$MONITOR_GRACE_PERIOD" ]; then
            # Grace period expired -- treat as hang, resume
            echo "Grace period expired after ${GRACE_ELAPSED}s. Treating as hang -- resuming."
            STALE_SINCE=""
            dispatch_resume "Output hung for ${GRACE_ELAPSED}s." "hung"
            continue
          fi
        fi
      else
        # Output is fresh -- healthy state
        STALE_SINCE=""
        RETRY_COUNT=0
      fi
    fi

    sleep "$INTERVAL"
  done
}

# Source guard: only run main when executed directly (not sourced by tests)
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  main "$@"
fi
