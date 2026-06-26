#!/usr/bin/env bash

set -euo pipefail

YUZHUA_HOME="${YUZHUA_HOME:-$HOME/.openclaw/workspace/apps/Yuzhua}"

log() {
  echo "[yuzhua-skill] $*"
}

main() {
  if [ ! -f "${YUZHUA_HOME}/start.sh" ]; then
    log "start.sh not found in ${YUZHUA_HOME}"
    log "Run ./scripts/install.sh first, or export YUZHUA_HOME to your repo path."
    exit 1
  fi

  log "Starting Yuzhua from: ${YUZHUA_HOME}"
  cd "${YUZHUA_HOME}"
  exec ./start.sh
}

main "$@"
