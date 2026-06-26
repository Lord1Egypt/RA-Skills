#!/usr/bin/env bash

set -euo pipefail

API_URL="${YUZHUA_API_URL:-http://127.0.0.1:8080/api/status}"

log() {
  echo "[yuzhua-skill] $*"
}

main() {
  if ! command -v curl >/dev/null 2>&1; then
    log "curl not found."
    exit 1
  fi

  log "Checking: ${API_URL}"
  if ! response="$(curl -fsS --max-time 5 "${API_URL}")"; then
    log "Yuzhua status endpoint is not reachable."
    log "Please ensure Yuzhua is running: ./scripts/start.sh"
    exit 1
  fi

  if command -v jq >/dev/null 2>&1; then
    echo "${response}" | jq .
  else
    echo "${response}"
  fi
}

main "$@"
