#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${1:-xiaohongshu-mcp}"

status_macos() {
  local uid label
  uid="$(id -u)"
  label="${XHS_MCP_LAUNCHD_LABEL:-ai.openclaw.${SERVICE_NAME}}"

  echo "[INFO] launchd label: $label"
  if launchctl print "gui/${uid}/${label}" >/tmp/xhs_launchd_status.out 2>/tmp/xhs_launchd_status.err; then
    sed -n '1,120p' /tmp/xhs_launchd_status.out
  else
    echo "[WARN] service not active or not installed."
    cat /tmp/xhs_launchd_status.err || true
  fi
}

status_linux() {
  local unit_name
  unit_name="${XHS_MCP_SYSTEMD_UNIT:-${SERVICE_NAME}.service}"
  echo "[INFO] systemd unit: $unit_name"
  if ! command -v systemctl >/dev/null 2>&1; then
    echo "[WARN] systemctl not found."
    exit 0
  fi
  systemctl --user status "$unit_name" --no-pager || true
}

os_name="$(uname -s 2>/dev/null | tr '[:upper:]' '[:lower:]')"
case "$os_name" in
  darwin*)
    status_macos
    ;;
  linux*)
    status_linux
    ;;
  *)
    echo "[ERROR] unsupported OS for service_status.sh: $os_name"
    exit 1
    ;;
esac
