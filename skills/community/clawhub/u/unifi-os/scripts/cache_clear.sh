#!/usr/bin/env bash
# cache_clear.sh — inspect and clear UniFi OS skill cache
# No args / --status : show cached keys, ages, sizes
# --all              : clear all cache
# <key>              : clear specific cache key

source "$(dirname "$0")/lib.sh"
# Note: load_config intentionally not called — cache ops don't need credentials

MODE="${1:-}"

case "${MODE}" in
  --all)
    rm -f "${CACHE_DIR}"/*.json
    echo "Cache cleared."
    ;;
  ""| --status)
    echo "# Cache status (${CACHE_DIR})"
    if [[ ! -d "${CACHE_DIR}" ]] || ! ls "${CACHE_DIR}"/*.json &>/dev/null; then
      echo "  empty"
      exit 0
    fi
    printf "  %-30s %8s %8s\n" "key" "age" "size"
    printf "  %-30s %8s %8s\n" "---" "---" "----"
    for f in "${CACHE_DIR}"/*.json; do
      [[ -f "${f}" ]] || continue
      key=$(basename "${f}" .json)
      age=$(( $(date +%s) - $(stat -c %Y "${f}") ))
      size=$(stat -c %s "${f}")
      printf "  %-30s %7ss %7sB\n" "${key}" "${age}" "${size}"
    done
    echo ""
    echo "Use --all to clear all, or pass a key name to clear one."
    echo "Force live fetch without clearing: UNIFI_FORCE=1 bash scripts/<script>.sh"
    ;;
  *)
    target="${CACHE_DIR}/${MODE}.json"
    if [[ -f "${target}" ]]; then
      rm -f "${target}"
      echo "Cleared: ${MODE}"
    else
      echo "No cache entry for: ${MODE}"
      echo "Run with no args to see available keys."
    fi
    ;;
esac
