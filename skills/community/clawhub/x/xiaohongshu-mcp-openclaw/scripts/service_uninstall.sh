#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${1:-xiaohongshu-mcp}"
DRY_RUN="${XHS_SERVICE_DRY_RUN:-0}"

run_cmd() {
  if [ "$DRY_RUN" = "1" ]; then
    echo "[DRYRUN] $*"
    return 0
  fi
  eval "$@"
}

uninstall_macos() {
  local uid label plist_path
  uid="$(id -u)"
  label="${XHS_MCP_LAUNCHD_LABEL:-ai.openclaw.${SERVICE_NAME}}"
  plist_path="$HOME/Library/LaunchAgents/${label}.plist"

  run_cmd "launchctl disable gui/${uid}/${label} >/dev/null 2>&1 || true"
  run_cmd "launchctl bootout gui/${uid}/${label} >/dev/null 2>&1 || true"
  run_cmd "rm -f '$plist_path'"

  echo "[OK] launchd service removed: $label"
}

uninstall_linux() {
  local user_dir unit_name unit_path
  user_dir="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
  unit_name="${XHS_MCP_SYSTEMD_UNIT:-${SERVICE_NAME}.service}"
  unit_path="$user_dir/$unit_name"

  if command -v systemctl >/dev/null 2>&1; then
    run_cmd "systemctl --user disable --now '$unit_name' >/dev/null 2>&1 || true"
    run_cmd "systemctl --user daemon-reload >/dev/null 2>&1 || true"
  fi
  run_cmd "rm -f '$unit_path'"

  echo "[OK] systemd user service removed: $unit_name"
}

os_name="$(uname -s 2>/dev/null | tr '[:upper:]' '[:lower:]')"
case "$os_name" in
  darwin*)
    uninstall_macos
    ;;
  linux*)
    uninstall_linux
    ;;
  *)
    echo "[ERROR] unsupported OS for service_uninstall.sh: $os_name"
    exit 1
    ;;
esac
