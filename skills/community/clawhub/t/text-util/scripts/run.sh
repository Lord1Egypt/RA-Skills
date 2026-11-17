#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-}"
shift || true
TEXT="$*"

case "$CMD" in
  upper)
    echo "$TEXT" | tr '[:lower:]' '[:upper:]'
    ;;
  lower)
    echo "$TEXT" | tr '[:upper:]' '[:lower:]'
    ;;
  reverse)
    echo "$TEXT" | rev
    ;;
  count)
    chars=$(echo -n "$TEXT" | wc -m)
    words=$(echo -n "$TEXT" | wc -w)
    lines=$(echo -n "$TEXT" | wc -l)
    # handle trailing newline edge: wc -l misses the last line without newline
    if [[ -n "$TEXT" && "${TEXT: -1}" != $'\n' ]]; then
      lines=$((lines + 1))
    fi
    echo "chars: $chars  words: $words  lines: $lines"
    ;;
  *)
    echo "Usage: run.sh {upper|lower|reverse|count} <text>" >&2
    exit 1
    ;;
esac
