#!/bin/bash
# LDM OS Process Monitor
# Kills zombie npm/ldm processes, cleans stale locks.
# Run via healthcheck (every 3 min) or standalone cron.

LOG="/tmp/ldm-process-monitor.log"
KILLED=0

log() { echo "[$(date '+%H:%M:%S')] $1" >> "$LOG"; }

# 1. Kill npm view/list processes older than 30s
for pid in $(ps -eo pid,etime,args | grep -E "npm (view|list)" | grep -v grep | awk '{
  split($2, t, /[:-]/);
  if (length(t) >= 3) secs = t[1]*3600 + t[2]*60 + t[3];
  else if (length(t) == 2) secs = t[1]*60 + t[2];
  else secs = t[1];
  if (secs > 30) print $1
}'); do
  kill -9 "$pid" 2>/dev/null && KILLED=$((KILLED + 1))
done

# 2. Kill orphaned ldm install (parent is init/launchd)
for pid in $(pgrep -f "ldm install" 2>/dev/null); do
  ppid=$(ps -p "$pid" -o ppid= 2>/dev/null | tr -d ' ')
  if [ "$ppid" = "1" ]; then
    kill -9 "$pid" 2>/dev/null && KILLED=$((KILLED + 1))
  fi
done

# 3. Kill npm install null (should never exist)
for pid in $(pgrep -f "npm install null" 2>/dev/null); do
  kill -9 "$pid" 2>/dev/null && KILLED=$((KILLED + 1))
done

# 4. Kill ldm install --version zombies older than 10s
for pid in $(ps -eo pid,etime,args | grep "ldm install --version" | grep -v grep | awk '{
  split($2, t, /[:-]/);
  if (length(t) >= 2) secs = t[1]*60 + t[2];
  else secs = t[1];
  if (secs > 10) print $1
}'); do
  kill -9 "$pid" 2>/dev/null && KILLED=$((KILLED + 1))
done

# 5. Clean stale lockfile
LOCK="$HOME/.ldm/state/.ldm-install.lock"
if [ -f "$LOCK" ]; then
  lock_pid=$(python3 -c "import json; print(json.load(open('$LOCK'))['pid'])" 2>/dev/null)
  if [ -n "$lock_pid" ] && ! kill -0 "$lock_pid" 2>/dev/null; then
    rm -f "$LOCK"
    log "Cleaned stale lockfile (PID $lock_pid dead)"
    KILLED=$((KILLED + 1))
  fi
fi

# Log if we killed anything
if [ "$KILLED" -gt 0 ]; then
  log "Killed $KILLED zombie process(es)"
fi

# Alert if node count is high
NODE_COUNT=$(pgrep -fl node 2>/dev/null | wc -l | tr -d ' ')
if [ "$NODE_COUNT" -gt 150 ]; then
  log "WARNING: $NODE_COUNT node processes running"
fi
