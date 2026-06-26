#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="openclaw-session-memory-flush"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
CRON_MARKER="# openclaw-session-memory-flush"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
OPENCLAW_CONFIG="$OPENCLAW_HOME/openclaw.json"

mkdir -p "$SKILL_DIR/state"
if [ ! -f "$SKILL_DIR/state/flushed_sessions.json" ]; then
  printf '{\n  "flushed_sessions": {}\n}\n' > "$SKILL_DIR/state/flushed_sessions.json"
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
else
  echo "ERROR: python3 not found"
  exit 1
fi

if command -v openclaw >/dev/null 2>&1; then
  OPENCLAW_BIN="$(command -v openclaw)"
else
  echo "ERROR: openclaw not found in current shell PATH"
  echo "Please export PATH correctly before running install.sh, or manually set OPENCLAW_BIN."
  exit 1
fi

read_config_value() {
  local key="$1"
  "$PYTHON_BIN" - "$OPENCLAW_CONFIG" "$key" <<'PY'
import json
import pathlib
import sys

config_path = pathlib.Path(sys.argv[1]).expanduser()
query = sys.argv[2]

if not config_path.exists():
    sys.exit(0)

try:
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)


def get(obj, *path):
    cur = obj
    for part in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def pos_int(value):
    try:
        value = int(str(value).strip())
    except Exception:
        return None
    return value if value > 0 else None

custom = get(cfg, "sessionMemoryFlush")
if not isinstance(custom, dict):
    custom = get(cfg, "skills", "sessionMemoryFlush")
if not isinstance(custom, dict):
    custom = {}

if query == "dm_idle":
    value = (
        pos_int(custom.get("dmIdleMinutes"))
        or pos_int(custom.get("directIdleMinutes"))
        or pos_int(get(custom, "idleMinutes", "dm"))
        or pos_int(get(custom, "idleMinutes", "direct"))
        or pos_int(get(cfg, "session", "resetByType", "direct", "idleMinutes"))
        or pos_int(get(cfg, "session", "resetByType", "dm", "idleMinutes"))
        or pos_int(get(cfg, "session", "reset", "idleMinutes"))
        or pos_int(get(cfg, "session", "idleMinutes"))
        or 5
    )
    print(value)
elif query == "group_idle":
    value = (
        pos_int(custom.get("groupIdleMinutes"))
        or pos_int(get(custom, "idleMinutes", "group"))
        or pos_int(get(cfg, "session", "resetByType", "group", "idleMinutes"))
        or pos_int(get(cfg, "session", "reset", "idleMinutes"))
        or pos_int(get(cfg, "session", "idleMinutes"))
        or 30
    )
    print(value)
elif query == "timer":
    dm_idle = (
        pos_int(custom.get("dmIdleMinutes"))
        or pos_int(custom.get("directIdleMinutes"))
        or pos_int(get(custom, "idleMinutes", "dm"))
        or pos_int(get(custom, "idleMinutes", "direct"))
        or pos_int(get(cfg, "session", "resetByType", "direct", "idleMinutes"))
        or pos_int(get(cfg, "session", "resetByType", "dm", "idleMinutes"))
        or pos_int(get(cfg, "session", "reset", "idleMinutes"))
        or pos_int(get(cfg, "session", "idleMinutes"))
        or 5
    )
    group_idle = (
        pos_int(custom.get("groupIdleMinutes"))
        or pos_int(get(custom, "idleMinutes", "group"))
        or pos_int(get(cfg, "session", "resetByType", "group", "idleMinutes"))
        or pos_int(get(cfg, "session", "reset", "idleMinutes"))
        or pos_int(get(cfg, "session", "idleMinutes"))
        or 30
    )
    value = pos_int(custom.get("timerMinutes")) or pos_int(get(custom, "schedule", "timerMinutes"))
    if value is None:
        value = max(1, min(dm_idle, group_idle) - 1)
    print(value)
elif query == "scan_dm":
    dm_idle = (
        pos_int(custom.get("dmIdleMinutes"))
        or pos_int(custom.get("directIdleMinutes"))
        or pos_int(get(custom, "idleMinutes", "dm"))
        or pos_int(get(custom, "idleMinutes", "direct"))
        or pos_int(get(cfg, "session", "resetByType", "direct", "idleMinutes"))
        or pos_int(get(cfg, "session", "reset", "idleMinutes"))
        or pos_int(get(cfg, "session", "idleMinutes"))
        or 5
    )
    timer = pos_int(custom.get("timerMinutes")) or pos_int(get(custom, "schedule", "timerMinutes")) or max(1, dm_idle - 1)
    value = (
        pos_int(custom.get("dmScanWindowMinutes"))
        or pos_int(custom.get("directScanWindowMinutes"))
        or pos_int(get(custom, "scanWindowMinutes", "dm"))
        or pos_int(get(custom, "scanWindowMinutes", "direct"))
        or min(timer, max(1, dm_idle - 1))
    )
    print(value)
elif query == "scan_group":
    group_idle = (
        pos_int(custom.get("groupIdleMinutes"))
        or pos_int(get(custom, "idleMinutes", "group"))
        or pos_int(get(cfg, "session", "resetByType", "group", "idleMinutes"))
        or pos_int(get(cfg, "session", "reset", "idleMinutes"))
        or pos_int(get(cfg, "session", "idleMinutes"))
        or 30
    )
    timer = pos_int(custom.get("timerMinutes")) or pos_int(get(custom, "schedule", "timerMinutes")) or max(1, group_idle - 1)
    value = pos_int(custom.get("groupScanWindowMinutes")) or pos_int(get(custom, "scanWindowMinutes", "group")) or min(timer, max(1, group_idle - 1))
    print(value)
elif query == "output_dir":
    value = custom.get("outputDir")
    if isinstance(value, str) and value.strip():
        print(value.strip())
PY
}

TIMER_MINUTES="${SESSION_MEMORY_TIMER_MINUTES:-$(read_config_value timer)}"
DM_IDLE_MINUTES="${SESSION_MEMORY_DM_IDLE_MINUTES:-$(read_config_value dm_idle)}"
GROUP_IDLE_MINUTES="${SESSION_MEMORY_GROUP_IDLE_MINUTES:-$(read_config_value group_idle)}"
SCAN_WINDOW_DM="${SESSION_MEMORY_SCAN_WINDOW_DM:-$(read_config_value scan_dm)}"
SCAN_WINDOW_GROUP="${SESSION_MEMORY_SCAN_WINDOW_GROUP:-$(read_config_value scan_group)}"
OUTPUT_DIR="${SESSION_MEMORY_OUTPUT_DIR:-$(read_config_value output_dir)}"
OUTPUT_DIR="${OUTPUT_DIR:-$HOME/.openclaw/workspace/memory}"

if command -v systemctl >/dev/null 2>&1 && systemctl --user list-timers >/dev/null 2>&1; then
  mkdir -p "$SYSTEMD_USER_DIR"

  cat > "$SYSTEMD_USER_DIR/$SERVICE_NAME.service" <<EOF
[Unit]
Description=OpenClaw session memory flush
After=network.target

[Service]
Type=oneshot
Environment=OPENCLAW_BIN=$OPENCLAW_BIN
Environment=SESSION_MEMORY_DM_IDLE_MINUTES=$DM_IDLE_MINUTES
Environment=SESSION_MEMORY_GROUP_IDLE_MINUTES=$GROUP_IDLE_MINUTES
Environment=SESSION_MEMORY_SCAN_WINDOW_DM=$SCAN_WINDOW_DM
Environment=SESSION_MEMORY_SCAN_WINDOW_GROUP=$SCAN_WINDOW_GROUP
Environment=SESSION_MEMORY_OUTPUT_DIR=$OUTPUT_DIR
ExecStart=$PYTHON_BIN $SKILL_DIR/watcher.py --once
WorkingDirectory=$SKILL_DIR
EOF

  cat > "$SYSTEMD_USER_DIR/$SERVICE_NAME.timer" <<EOF
[Unit]
Description=Run OpenClaw session memory flush every $TIMER_MINUTES minute(s)

[Timer]
OnBootSec=2min
OnUnitActiveSec=${TIMER_MINUTES}min
Unit=$SERVICE_NAME.service

[Install]
WantedBy=timers.target
EOF

  systemctl --user daemon-reload
  systemctl --user enable --now "$SERVICE_NAME.timer"
  echo "Installed systemd user timer: $SERVICE_NAME.timer"
  systemctl --user status "$SERVICE_NAME.timer" --no-pager || true
else
  if ! command -v crontab >/dev/null 2>&1; then
    echo "ERROR: neither systemd user timer nor crontab is available"
    exit 1
  fi

  TMP_CRON="$(mktemp)"
  crontab -l 2>/dev/null | grep -v "$CRON_MARKER" > "$TMP_CRON" || true
  echo "*/$TIMER_MINUTES * * * * cd $SKILL_DIR && OPENCLAW_BIN=$OPENCLAW_BIN SESSION_MEMORY_DM_IDLE_MINUTES=$DM_IDLE_MINUTES SESSION_MEMORY_GROUP_IDLE_MINUTES=$GROUP_IDLE_MINUTES SESSION_MEMORY_SCAN_WINDOW_DM=$SCAN_WINDOW_DM SESSION_MEMORY_SCAN_WINDOW_GROUP=$SCAN_WINDOW_GROUP SESSION_MEMORY_OUTPUT_DIR=$OUTPUT_DIR $PYTHON_BIN watcher.py --once $CRON_MARKER" >> "$TMP_CRON"
  crontab "$TMP_CRON"
  rm -f "$TMP_CRON"
  echo "Installed crontab job: every $TIMER_MINUTES minute(s)"
fi

echo "Install complete."
echo "Detected OPENCLAW_BIN: $OPENCLAW_BIN"
echo "Timer interval: ${TIMER_MINUTES} minute(s)"
echo "DM idle threshold: ${DM_IDLE_MINUTES} minute(s)"
echo "Group idle threshold: ${GROUP_IDLE_MINUTES} minute(s)"
echo "Output dir: $OUTPUT_DIR"
echo "Manual test: cd $SKILL_DIR && OPENCLAW_BIN=$OPENCLAW_BIN SESSION_MEMORY_OUTPUT_DIR=$OUTPUT_DIR $PYTHON_BIN watcher.py --once --dry-run"
