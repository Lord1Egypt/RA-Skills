#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
RUNTIME_DIR="${SKILL_DIR}/runtime"

WARN_MB="${CONTENT_INSIGHT_RUNTIME_WARN_MB:-1536}"
CLEAN_MB="${CONTENT_INSIGHT_RUNTIME_CLEAN_MB:-2048}"
FORCE=0

usage() {
  cat <<'EOF'
Usage: maintain_runtime.sh [--force]

Default behavior:
- print a reminder when runtime size exceeds the warn threshold
- automatically clear runtime/cache and runtime/work when runtime size exceeds the clean threshold
- never remove models or binaries automatically

Environment variables:
- CONTENT_INSIGHT_RUNTIME_WARN_MB   warn threshold in MB (default: 1536)
- CONTENT_INSIGHT_RUNTIME_CLEAN_MB  auto-clean threshold in MB (default: 2048)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

mkdir -p "${RUNTIME_DIR}/cache" "${RUNTIME_DIR}/work"

size_mb() {
  local path="$1"
  if [[ ! -e "${path}" ]]; then
    echo "0"
    return
  fi
  du -sk "${path}" 2>/dev/null | awk '{printf "%d", ($1 + 1023) / 1024}'
}

TOTAL_MB="$(size_mb "${RUNTIME_DIR}")"
CACHE_MB="$(size_mb "${RUNTIME_DIR}/cache")"
WORK_MB="$(size_mb "${RUNTIME_DIR}/work")"

if [[ "${FORCE}" -eq 1 ]]; then
  echo "Runtime maintenance: cleaning cache and work unconditionally." >&2
  "${SCRIPT_DIR}/cleanup_runtime.sh" >/dev/null
  exit 0
fi

if [[ "${TOTAL_MB}" -ge "${CLEAN_MB}" ]]; then
  echo "Runtime maintenance: ${TOTAL_MB}MB exceeds auto-clean threshold ${CLEAN_MB}MB." >&2
  echo "Cleaning runtime/cache (${CACHE_MB}MB) and runtime/work (${WORK_MB}MB)." >&2
  "${SCRIPT_DIR}/cleanup_runtime.sh" >/dev/null
  NEW_TOTAL_MB="$(size_mb "${RUNTIME_DIR}")"
  echo "Runtime maintenance: runtime is now ${NEW_TOTAL_MB}MB." >&2
  exit 0
fi

if [[ "${TOTAL_MB}" -ge "${WARN_MB}" ]]; then
  echo "Runtime maintenance: runtime is ${TOTAL_MB}MB, above warn threshold ${WARN_MB}MB." >&2
  echo "Tip: run scripts/runtime_status.sh or scripts/cleanup_runtime.sh if you want to reclaim space." >&2
fi
