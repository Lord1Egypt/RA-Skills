#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_NAME="${1:-xiaohongshu-mcp}"
PORT="${XHS_MCP_PORT:-18060}"
HEADLESS="${XHS_MCP_HEADLESS:-true}"
STATE_DIR="${XHS_MCP_STATE_DIR:-$HOME/.openclaw/state/xiaohongshu-mcp}"
LOG_DIR="${XHS_MCP_LOG_DIR:-$HOME/.openclaw/logs}"
LOG_FILE="$LOG_DIR/xiaohongshu-mcp-server.log"
DRY_RUN="${XHS_SERVICE_DRY_RUN:-0}"

MCP_BIN="${XHS_MCP_BIN:-xiaohongshu-mcp}"
if ! command -v "$MCP_BIN" >/dev/null 2>&1; then
  if [ -x "$HOME/go/bin/$MCP_BIN" ]; then
    MCP_BIN="$HOME/go/bin/$MCP_BIN"
  else
    echo "[ERROR] $MCP_BIN not found in PATH or \$HOME/go/bin."
    echo "[INFO] run setup first: bash $BASE_DIR/scripts/setup.sh"
    exit 1
  fi
fi

run_cmd() {
  if [ "$DRY_RUN" = "1" ]; then
    echo "[DRYRUN] $*"
    return 0
  fi
  eval "$@"
}

install_macos() {
  local uid label plist_dir plist_path
  uid="$(id -u)"
  label="${XHS_MCP_LAUNCHD_LABEL:-ai.openclaw.${SERVICE_NAME}}"
  plist_dir="$HOME/Library/LaunchAgents"
  plist_path="$plist_dir/${label}.plist"

  mkdir -p "$plist_dir" "$STATE_DIR" "$LOG_DIR"

  local plist_content
  plist_content="$(cat <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${label}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${MCP_BIN}</string>
    <string>-headless=${HEADLESS}</string>
    <string>-port</string>
    <string>:${PORT}</string>
  </array>
  <key>WorkingDirectory</key>
  <string>${STATE_DIR}</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>${LOG_FILE}</string>
  <key>StandardErrorPath</key>
  <string>${LOG_FILE}</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>HOME</key>
    <string>${HOME}</string>
    <key>PATH</key>
    <string>${PATH}</string>
  </dict>
</dict>
</plist>
EOF
)"

  if [ "$DRY_RUN" = "1" ]; then
    echo "[DRYRUN] write plist to $plist_path"
  else
    printf "%s\n" "$plist_content" >"$plist_path"
  fi

  run_cmd "launchctl bootout gui/${uid}/${label} >/dev/null 2>&1 || true"
  run_cmd "launchctl bootstrap gui/${uid} '$plist_path'"
  run_cmd "launchctl enable gui/${uid}/${label}"
  run_cmd "launchctl kickstart -k gui/${uid}/${label}"

  echo "[OK] launchd service installed: $label"
  echo "[INFO] plist: $plist_path"
  echo "[INFO] status: launchctl print gui/${uid}/${label}"
}

install_linux() {
  local user_dir unit_name unit_path
  user_dir="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
  unit_name="${XHS_MCP_SYSTEMD_UNIT:-${SERVICE_NAME}.service}"
  unit_path="$user_dir/$unit_name"

  mkdir -p "$user_dir" "$STATE_DIR" "$LOG_DIR"

  local unit_content
  unit_content="$(cat <<EOF
[Unit]
Description=Xiaohongshu MCP service for OpenClaw
After=network.target

[Service]
Type=simple
WorkingDirectory=${STATE_DIR}
ExecStart=${MCP_BIN} -headless=${HEADLESS} -port :${PORT}
Restart=always
RestartSec=3
Environment=HOME=%h

[Install]
WantedBy=default.target
EOF
)"

  if [ "$DRY_RUN" = "1" ]; then
    echo "[DRYRUN] write unit to $unit_path"
  else
    printf "%s\n" "$unit_content" >"$unit_path"
  fi

  if ! command -v systemctl >/dev/null 2>&1; then
    echo "[WARN] systemctl not found. unit file is created at:"
    echo "       $unit_path"
    echo "[INFO] start manually if needed."
    return 0
  fi

  run_cmd "systemctl --user daemon-reload"
  run_cmd "systemctl --user enable --now '$unit_name'"

  echo "[OK] systemd user service installed: $unit_name"
  echo "[INFO] unit: $unit_path"
  echo "[INFO] status: systemctl --user status $unit_name --no-pager"
}

os_name="$(uname -s 2>/dev/null | tr '[:upper:]' '[:lower:]')"
case "$os_name" in
  darwin*)
    install_macos
    ;;
  linux*)
    install_linux
    ;;
  *)
    echo "[ERROR] unsupported OS for service_install.sh: $os_name"
    echo "[INFO] use scripts/start_server.sh manually on this OS."
    exit 1
    ;;
esac

echo "[NEXT] register MCP config:"
echo "       bash $BASE_DIR/scripts/register.sh $SERVICE_NAME"
