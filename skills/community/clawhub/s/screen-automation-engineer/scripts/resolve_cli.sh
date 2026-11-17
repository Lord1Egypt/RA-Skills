#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  printf '%s\n' '{"ok":false,"error":"resolve_cli.sh is for macOS only. On Windows, use scripts/resolve_cli.ps1 in PowerShell."}' >&2
  exit 2
fi

for app in \
  "${SCREEN_AUTOMATION_MAC_APP:-}" \
  "/Applications/Screen Automation Helper.app" \
  "$HOME/Applications/Screen Automation Helper.app"; do
  [[ -n "$app" ]] || continue
  cli="$app/Contents/MacOS/screen-automation-helper"
  if [[ -x "$cli" ]]; then
    printf '%s\n' "$cli"
    exit 0
  fi
done

printf '%s\n' '{"ok":false,"platform":"macos","error":"未找到屏幕自动化小助手。请安装到应用程序目录，或设置 SCREEN_AUTOMATION_MAC_APP。"}' >&2
exit 2
