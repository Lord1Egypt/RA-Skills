#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
START_SCRIPT="$SCRIPT_DIR/start_senseaudio_let_claw_talk.sh"

if [[ ! -x "$START_SCRIPT" ]]; then
  echo "start script not executable: $START_SCRIPT" >&2
  exit 1
fi

quoted_command="bash $(printf '%q' "$START_SCRIPT")"
for arg in "$@"; do
  quoted_command+=" $(printf '%q' "$arg")"
done

/usr/bin/osascript <<EOF
tell application "Terminal"
  activate
  do script "$quoted_command"
end tell
EOF

echo "opened_terminal"
