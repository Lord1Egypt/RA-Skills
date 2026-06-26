#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

DIR_INPUT="${1:-$HOME/Pictures/WallpaperAuto}"
INTERVAL_MINUTES="${2:-60}"
DIR_PATH="$(expand_path "$DIR_INPUT")"

ensure_dir_exists "$DIR_PATH"
if ! [[ "$INTERVAL_MINUTES" =~ ^[0-9]+$ ]] || [[ "$INTERVAL_MINUTES" -lt 1 ]]; then
  echo "ERROR: 轮换间隔必须是正整数分钟" >&2
  exit 1
fi

mkdir -p "$HOME/Library/LaunchAgents"

cat > "$LAUNCHD_PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LAUNCHD_LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>${SCRIPT_DIR}/rotate_once.sh</string>
    <string>${DIR_PATH}</string>
  </array>
  <key>StartInterval</key>
  <integer>$((INTERVAL_MINUTES * 60))</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>${HOME}/Library/Logs/${LAUNCHD_LABEL}.log</string>
  <key>StandardErrorPath</key>
  <string>${HOME}/Library/Logs/${LAUNCHD_LABEL}.err.log</string>
</dict>
</plist>
PLIST

launchctl bootout "gui/$(id -u)" "$LAUNCHD_PLIST" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$LAUNCHD_PLIST"
launchctl enable "gui/$(id -u)/${LAUNCHD_LABEL}" >/dev/null 2>&1 || true
launchctl kickstart -k "gui/$(id -u)/${LAUNCHD_LABEL}" >/dev/null 2>&1 || true

echo "状态: 成功"
echo "目录: $DIR_PATH"
echo "轮换间隔(分钟): $INTERVAL_MINUTES"
echo "plist: $LAUNCHD_PLIST"
echo "卸载命令: bash ${SCRIPT_DIR}/uninstall_launchagent.sh"
