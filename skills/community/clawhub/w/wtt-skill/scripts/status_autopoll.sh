#!/usr/bin/env bash
set -euo pipefail

os="$(uname -s)"

if [[ "$os" == "Darwin" ]]; then
  echo "== launchd service =="
  launchctl list | grep com.openclaw.wtt.autopoll || true
elif [[ "$os" == "Linux" ]]; then
  echo "== systemd --user service =="
  systemctl --user status wtt-autopoll.service --no-pager || true
else
  echo "Unsupported OS: $os"
fi

echo "== recent logs =="
tail -n 40 /tmp/wtt_autopoll.log 2>/dev/null || echo "(no /tmp/wtt_autopoll.log yet)"
