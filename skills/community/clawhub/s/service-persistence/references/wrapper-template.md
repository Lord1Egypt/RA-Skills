# Wrapper Daemon Script 模板

```bash
#!/bin/zsh
set -euo pipefail

export HOME="{{HOME}}"
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

SESSION="{{SESSION_NAME}}"
WORKDIR="{{WORKDIR}}"
COMMAND='{{COMMAND}}'
LOG="{{HOME}}/.openclaw/logs/{{LOG_PREFIX}}-wrapper.log"
MAX_FAILURES={{MAX_FAILURES}}
CHECK_INTERVAL={{CHECK_INTERVAL}}
STARTUP_WAIT={{STARTUP_WAIT}}

fail_count=0

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$LOG"; }

start_service() {
  tmux kill-session -t "$SESSION" 2>/dev/null || true
  sleep 1
  tmux new-session -d -s "$SESSION" -c "$WORKDIR"
  sleep 2
  tmux send-keys -t "$SESSION" "cd $WORKDIR && $COMMAND" Enter
  log "sent command (workdir: $WORKDIR), waiting ${STARTUP_WAIT}s..."
  sleep "$STARTUP_WAIT"

  # Handle trust/confirmation prompts
  local pane_out
  pane_out=$(tmux capture-pane -pt "$SESSION:0.0" 2>/dev/null || echo "")
  if echo "$pane_out" | grep -q "trust this folder"; then
    log "trust prompt detected, confirming..."
    tmux send-keys -t "$SESSION" Enter
    sleep 10
  fi

  log "started $SESSION"
}

is_alive() {
  if ! tmux has-session -t "$SESSION" 2>/dev/null; then
    log "  check: session does not exist"
    return 1
  fi

  # 關鍵：檢查 pane process，不只檢查 session 存在
  local pane_cmd
  pane_cmd=$(tmux list-panes -t "$SESSION" -F '#{pane_current_command}' 2>/dev/null || echo "")
  case "$pane_cmd" in
    zsh|bash|fish|sh|login)
      log "  check: pane running shell ($pane_cmd) = service exited"
      return 1
      ;;
  esac
  return 0
}

log "wrapper starting, waiting {{BOOT_DELAY}}s for network..."
sleep {{BOOT_DELAY}}
log "entering monitor loop (every ${CHECK_INTERVAL}s, max ${MAX_FAILURES} failures before cooldown)"

while true; do
  if is_alive; then
    if (( fail_count > 0 )); then
      log "service recovered (was at attempt $fail_count)"
    fi
    fail_count=0
  else
    fail_count=$((fail_count + 1))
    if (( fail_count > MAX_FAILURES )); then
      log "COOLDOWN: $MAX_FAILURES consecutive failures, sleeping {{COOLDOWN}}s"
      sleep {{COOLDOWN}}
      fail_count=0
      log "cooldown over, resuming"
      continue
    fi
    start_service
    continue
  fi
  sleep "$CHECK_INTERVAL"
done
```

## Wrapper 的三個檢查狀態

| 狀況 | pane_current_command | 動作 |
|---|---|---|
| session 不存在 | — | 重建 + 啟動 |
| session 在，pane = zsh/bash | shell | 程式退出了 → kill + 重建 |
| session 在，pane = 程式名/版本號 | 非 shell | 正常，不動 |

## 為什麼要檢查 pane process？

只檢查 `tmux has-session` 有盲區：程式 crash 了但 tmux session 殘留（回到 shell prompt），
`has-session` 會說存在，但程式已經死了。檢查 `pane_current_command` 能區分。
