#!/bin/zsh
set -euo pipefail

export HOME="/Users/btai"
export PATH="/Users/btai/.bun/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

SESSION="Agent-Son-Claude-Telegram-Channel"
WORKDIR="/Users/btai/.claude/workspace-telegram"
CLAUDE_CMD="cd $WORKDIR && claude --channels plugin:telegram@claude-plugins-official --dangerously-skip-permissions --permission-mode bypassPermissions"
LOG="/Users/btai/.openclaw/logs/claude-telegram-wrapper.log"
MAX_FAILURES=3
CHECK_INTERVAL=30
STARTUP_WAIT=25

fail_count=0

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$LOG"; }

start_claude() {
  tmux kill-session -t "$SESSION" 2>/dev/null || true
  sleep 1
  tmux new-session -d -s "$SESSION" -c "$WORKDIR"
  sleep 2
  tmux send-keys -t "$SESSION" "$CLAUDE_CMD" Enter
  log "sent claude command (workdir: $WORKDIR), waiting ${STARTUP_WAIT}s..."
  sleep "$STARTUP_WAIT"

  # Handle "trust this folder" prompt if it appears
  local pane_out
  pane_out=$(tmux capture-pane -pt "$SESSION:0.0" 2>/dev/null || echo "")
  if echo "$pane_out" | grep -q "trust this folder"; then
    log "trust prompt detected, confirming..."
    tmux send-keys -t "$SESSION" Enter
    sleep 10
  fi

  log "started $SESSION"
}

is_claude_alive() {
  if ! tmux has-session -t "$SESSION" 2>/dev/null; then
    log "  check: session does not exist"
    return 1
  fi

  local pane_cmd
  pane_cmd=$(tmux list-panes -t "$SESSION" -F '#{pane_current_command}' 2>/dev/null || echo "")

  case "$pane_cmd" in
    zsh|bash|fish|sh|login)
      log "  check: pane running shell ($pane_cmd) = claude exited"
      return 1
      ;;
  esac

  return 0
}

log "wrapper starting, waiting 15s for network..."
sleep 15

log "entering monitor loop (check every ${CHECK_INTERVAL}s, max ${MAX_FAILURES} consecutive failures before cooldown)"

while true; do
  if is_claude_alive; then
    if (( fail_count > 0 )); then
      log "claude recovered (was at attempt $fail_count)"
    fi
    fail_count=0
  else
    fail_count=$((fail_count + 1))

    if (( fail_count > MAX_FAILURES )); then
      log "COOLDOWN: $MAX_FAILURES consecutive failures, sleeping 1 hour before retry"
      log "Manual restart: tmux new-session -d -s $SESSION -c $WORKDIR && tmux send-keys -t $SESSION '$CLAUDE_CMD' Enter"
      sleep 3600
      fail_count=0
      log "cooldown over, resuming monitor"
      continue
    fi

    start_claude
    continue
  fi

  sleep "$CHECK_INTERVAL"
done
