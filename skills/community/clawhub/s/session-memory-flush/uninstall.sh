#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="openclaw-session-memory-flush"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
CRON_MARKER="# openclaw-session-memory-flush"

if command -v systemctl >/dev/null 2>&1; then
  systemctl --user disable --now "$SERVICE_NAME.timer" >/dev/null 2>&1 || true
  rm -f "$SYSTEMD_USER_DIR/$SERVICE_NAME.service"
  rm -f "$SYSTEMD_USER_DIR/$SERVICE_NAME.timer"
  systemctl --user daemon-reload >/dev/null 2>&1 || true
fi

if command -v crontab >/dev/null 2>&1; then
  TMP_CRON="$(mktemp)"
  crontab -l 2>/dev/null | grep -v "$CRON_MARKER" > "$TMP_CRON" || true
  crontab "$TMP_CRON" || true
  rm -f "$TMP_CRON"
fi

echo "Uninstall complete."
