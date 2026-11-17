#!/usr/bin/env bash
# wechat.sh — Unified CLI for WeChatLayout skill
# ================================================
# Usage:
#   wechat.sh <command> [options]
#
# Commands:
#   validate <input.html>              Validate HTML for WeChat editor compliance
#   lint                               Scan theme component libraries for anti-patterns
#   extract <url> [--output <name>]    Extract style from WeChat article URL
#   extract --html <file> [--output <name>]  Extract style from local HTML file
#   eval                               Run regression tests on evals/fixtures golden HTML

set -euo pipefail

# 禁止 Python 生成 .pyc / __pycache__，保持 skill 目录干净
export PYTHONDONTWRITEBYTECODE=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

usage() {
  cat <<'EOF'
wechat.sh — WeChatLayout CLI

USAGE:
  wechat.sh <command> [options]

COMMANDS:
  validate <input.html>                   Validate HTML for WeChat editor compliance
  lint                                    Scan theme component libraries for anti-patterns
  extract <url> [--output <name>]         Extract style from WeChat article URL
  extract --html <file> [--output <name>] Extract style from local HTML file
  eval                                    Run regression tests on evals/fixtures golden HTML

FLAGS:
  --help, -h                              Show this help

ENV:
  SKILL_ROOT  Override skill root (default: autodetect)

EOF
}

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 1
fi

CMD="$1"
shift

case "$CMD" in
  validate)
    if [[ $# -lt 1 ]]; then
      echo "[ERR] 'validate' requires <input.html>." >&2
      exit 1
    fi
    exec python3 "$SCRIPT_DIR/validate_output.py" "$@"
    ;;

  lint)
    exec python3 "$SCRIPT_DIR/component_lint.py" "$SKILL_ROOT"
    ;;

  extract)
    exec python3 "$SCRIPT_DIR/style_extractor.py" "$@"
    ;;

  eval)
    exec python3 "$SCRIPT_DIR/run_evals.py" "$@"
    ;;

  --help|-h)
    usage
    exit 0
    ;;

  *)
    echo "[ERR] Unknown command '$CMD'. See 'wechat.sh --help'." >&2
    exit 1
    ;;
esac
