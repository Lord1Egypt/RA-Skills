#!/usr/bin/env bash

set -euo pipefail

PORT="${YUZHUA_PORT:-8080}"

log() {
  echo "[yuzhua-skill] $*"
}

stop_with_lsof() {
  if ! command -v lsof >/dev/null 2>&1; then
    return 1
  fi

  local pids
  pids="$(lsof -ti tcp:"${PORT}" || true)"
  if [ -z "${pids}" ]; then
    return 1
  fi

  log "Stopping process on port ${PORT}: ${pids}"
  kill ${pids} || true
  sleep 1
  pids="$(lsof -ti tcp:"${PORT}" || true)"
  if [ -n "${pids}" ]; then
    log "Force killing: ${pids}"
    kill -9 ${pids} || true
  fi
  return 0
}

main() {
  if stop_with_lsof; then
    log "Stop done."
    exit 0
  fi
  log "No running process found on port ${PORT}."
}

main "$@"
