#!/usr/bin/env bash
set -euo pipefail

export PATH=/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

usage() {
  cat <<'EOF'
Usage:
  list-commands.sh [--group plugin]

Examples:
  list-commands.sh
  list-commands.sh --group plugin
EOF
}

GROUP=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --group)
      GROUP="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if ! command -v wp >/dev/null 2>&1; then
  echo "wp not found in PATH" >&2
  exit 1
fi

if [[ -n "$GROUP" ]]; then
  wp help "$GROUP"
else
  wp help
fi
