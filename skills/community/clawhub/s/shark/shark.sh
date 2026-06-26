#!/usr/bin/env sh
# shark.sh — Ralph-style loop enforcer for the Shark Pattern
# Each iteration = one bounded Claude turn. Never blocks >30s per loop.
# Usage: ./shark.sh "your task description"
#   or:  ./shark.sh  (reads task from SHARK_TASK.md if exists)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_FILE="$SCRIPT_DIR/SKILL.md"
STATE_FILE="$SCRIPT_DIR/shark-exec/state/pending.json"
TIMINGS_FILE="$SCRIPT_DIR/state/timings.jsonl"
MAX_LOOPS=${SHARK_MAX_LOOPS:-50}
LOOP_TIMEOUT=${SHARK_LOOP_TIMEOUT:-25}  # seconds per turn (under 30s hard limit)

# Ensure state dir exists
mkdir -p "$SCRIPT_DIR/state"

if [ -n "$1" ]; then
  TASK="$*"
elif [ -f "$SCRIPT_DIR/SHARK_TASK.md" ]; then
  TASK=$(cat "$SCRIPT_DIR/SHARK_TASK.md")
else
  echo "Usage: ./shark.sh 'task description'"
  echo "  or create SHARK_TASK.md with your task"
  exit 1
fi

# Task hash for correlating loops within a run
TASK_HASH=$(printf '%s%s' "$TASK" "$(date +%Y%m%d%H%M%S)" | md5sum 2>/dev/null | cut -c1-8 || printf '%s%s' "$TASK" "$(date +%Y%m%d%H%M%S)" | md5 2>/dev/null | cut -c1-8 || echo "nohash")

# Write a timing entry to state/timings.jsonl
write_timing() {
  _loop=$1
  _elapsed=$2
  _result=$3
  _ts=$(date +%s)
  printf '{"ts":%s,"loop":%s,"elapsed_s":%s,"timeout_s":%s,"result":"%s","task_hash":"%s"}\n' \
    "$_ts" "$_loop" "$_elapsed" "$LOOP_TIMEOUT" "$_result" "$TASK_HASH" >> "$TIMINGS_FILE"
}

# Build the prompt: skill context + task + state awareness
build_prompt() {
  cat "$SKILL_FILE"
  echo ""
  echo "---"
  echo "## Current Task"
  echo "$TASK"
  echo ""
  echo "## Loop State"
  echo "Loop: $CURRENT_LOOP / $MAX_LOOPS"
  if [ -f "$STATE_FILE" ]; then
    echo "Pending background jobs:"
    cat "$STATE_FILE"
  fi
  echo ""
  echo "## Instructions"
  echo "Follow the Shark Pattern from SKILL.md above."
  echo "Each turn MUST complete in under ${LOOP_TIMEOUT}s."
  echo "If your task requires slow operations (>5s), use shark-exec pattern."
  echo "Write TASK_COMPLETE to a file named .shark-done when finished."
  echo "Write progress to SHARK_LOG.md after each loop."
}

run_claude_with_timeout() {
  _prompt_file=$1
  _timeout_flag=$2

  rm -f "$_timeout_flag"

  claude --print --permission-mode bypassPermissions < "$_prompt_file" &
  _claude_pid=$!

  (
    sleep "$LOOP_TIMEOUT"
    if kill -0 "$_claude_pid" 2>/dev/null; then
      : > "$_timeout_flag"
      kill "$_claude_pid" 2>/dev/null
      sleep 1
      kill -9 "$_claude_pid" 2>/dev/null
    fi
  ) &
  _watchdog_pid=$!

  wait "$_claude_pid"
  _exit_code=$?

  kill "$_watchdog_pid" 2>/dev/null
  wait "$_watchdog_pid" 2>/dev/null

  if [ -f "$_timeout_flag" ]; then
    rm -f "$_timeout_flag"
    return 124
  fi

  return "$_exit_code"
}

CURRENT_LOOP=0
DONE_FILE="$SCRIPT_DIR/.shark-done"
rm -f "$DONE_FILE"

echo "[SHARK] Shark loop starting - task: $TASK"
echo "   Max loops: $MAX_LOOPS | Timeout per turn: ${LOOP_TIMEOUT}s | Run: $TASK_HASH"
echo ""

while [ $CURRENT_LOOP -lt $MAX_LOOPS ]; do
  CURRENT_LOOP=$((CURRENT_LOOP + 1))
  echo "[SHARK] Loop $CURRENT_LOOP/$MAX_LOOPS..."

  LOOP_START=$(date +%s)

  # Run claude with hard timeout — THIS is the 30s enforcement
  TMP_PROMPT=$(mktemp "${TMPDIR:-/tmp}/shark-prompt.XXXXXX")
  TIMEOUT_FLAG="${TMP_PROMPT}.timeout"
  build_prompt > "$TMP_PROMPT"
  run_claude_with_timeout "$TMP_PROMPT" "$TIMEOUT_FLAG"
  EXIT_CODE=$?
  rm -f "$TMP_PROMPT" "$TIMEOUT_FLAG"

  LOOP_END=$(date +%s)
  ELAPSED=$((LOOP_END - LOOP_START))

  if [ $EXIT_CODE -eq 124 ]; then
    echo "[TIMEOUT] Turn $CURRENT_LOOP timed out at ${LOOP_TIMEOUT}s (${ELAPSED}s elapsed) - looping back"
    write_timing "$CURRENT_LOOP" "$ELAPSED" "timeout"
  else
    echo "[TIMING] Turn $CURRENT_LOOP completed in ${ELAPSED}s"
    write_timing "$CURRENT_LOOP" "$ELAPSED" "ok"
  fi

  # Check if task is done
  if [ -f "$DONE_FILE" ]; then
    write_timing "$CURRENT_LOOP" "$ELAPSED" "done"
    echo ""
    echo "[DONE] Task complete after $CURRENT_LOOP loops"
    cat "$DONE_FILE"
    exit 0
  fi
done

echo "[WARN] Max loops ($MAX_LOOPS) reached without completion"
exit 1
