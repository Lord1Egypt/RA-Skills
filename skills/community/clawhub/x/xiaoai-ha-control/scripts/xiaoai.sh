#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
  cat <<EOF
Usage:
  $0 say "text to speak"
  $0 exec "directive text"
  $0 play "media url" [media_content_type]

Examples:
  $0 say "你好，我是小叮当。"
  $0 exec "关闭客厅灯"
  $0 play "http://example.com/test.mp3"
EOF
}

if [ $# -lt 2 ]; then
  usage
  exit 1
fi

MODE="$1"
shift

case "$MODE" in
  say)
    bash "${SCRIPT_DIR}/xiaoai_say.sh" "$@"
    ;;
  exec)
    bash "${SCRIPT_DIR}/xiaoai_execute.sh" "$@"
    ;;
  play)
    bash "${SCRIPT_DIR}/xiaoai_play.sh" "$@"
    ;;
  *)
    echo "Unknown mode: $MODE" >&2
    usage
    exit 2
    ;;
esac
