#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

launchctl bootout "gui/$(id -u)" "$LAUNCHD_PLIST" >/dev/null 2>&1 || true
rm -f "$LAUNCHD_PLIST"

echo "状态: 成功"
echo "已卸载: $LAUNCHD_PLIST"
