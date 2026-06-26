#!/usr/bin/env bash
set -euo pipefail

os="$(uname -s)"

if [[ "$os" == "Darwin" ]]; then
  plist="$HOME/Library/LaunchAgents/com.openclaw.wtt.autopoll.plist"
  launchctl bootout "gui/$(id -u)/com.openclaw.wtt.autopoll" >/dev/null 2>&1 || true
  rm -f "$plist"
  echo "✅ macOS autopoll removed"
elif [[ "$os" == "Linux" ]]; then
  systemctl --user disable --now wtt-autopoll.service >/dev/null 2>&1 || true
  rm -f "$HOME/.config/systemd/user/wtt-autopoll.service"
  systemctl --user daemon-reload || true
  echo "✅ Linux autopoll removed"
else
  echo "❌ Unsupported OS: $os"
  exit 1
fi
