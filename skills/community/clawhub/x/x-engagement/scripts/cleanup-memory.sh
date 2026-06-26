#!/bin/bash
set -euo pipefail

# Preview or apply cleanup inside the dedicated x-engagement memory subtree.

MODE="dry-run"
if [ "${1:-}" = "--apply" ]; then
  MODE="apply"
elif [ "${1:-}" != "" ]; then
  echo "Usage: $0 [--apply]"
  exit 1
fi

MEMORY_DIR="${HOME}/memory/daily/hotspots"
ALLOWED_PREFIX="${HOME}/memory/daily/hotspots"

case "${MEMORY_DIR}" in
  "${ALLOWED_PREFIX}"|"${ALLOWED_PREFIX}/"*) ;;
  *)
    echo "Refusing to run outside allowed memory path: ${ALLOWED_PREFIX}"
    exit 1
    ;;
esac

if [ -L "${MEMORY_DIR}" ]; then
  echo "Refusing to operate on symlinked memory directory: ${MEMORY_DIR}"
  exit 1
fi

if [ ! -d "${MEMORY_DIR}" ]; then
  echo "Memory directory does not exist: ${MEMORY_DIR}"
  exit 0
fi

echo "=== x-engagement memory cleanup (${MODE}) $(date) ==="

cleanup_dir() {
  local label="$1"
  local dir="$2"
  local days="$3"

  echo ""
  echo "${label}: ${dir} (older than ${days} days)"

  if [ ! -d "${dir}" ]; then
    echo "  skipped: directory missing"
    return 0
  fi

  mapfile -t matches < <(find "${dir}" -type f -mtime +"${days}" -print 2>/dev/null | sort)

  if [ "${#matches[@]}" -eq 0 ]; then
    echo "  nothing to clean"
    return 0
  fi

  printf '  %s\n' "${matches[@]}"

  if [ "${MODE}" = "apply" ]; then
    find "${dir}" -type f -mtime +"${days}" -delete 2>/dev/null
    echo "  deleted: ${#matches[@]} files"
  else
    echo "  preview only: rerun with --apply to delete"
  fi
}

cleanup_dir "评论历史" "${MEMORY_DIR}/history/comments" 30
cleanup_dir "每日日志" "${MEMORY_DIR}/history/daily" 30
cleanup_dir "热点表格" "${MEMORY_DIR}/tables" 7

echo ""
echo "Cleanup complete."
