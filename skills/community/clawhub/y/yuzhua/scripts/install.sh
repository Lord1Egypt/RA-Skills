#!/usr/bin/env bash

set -euo pipefail

YUZHUA_HOME="${YUZHUA_HOME:-$HOME/.openclaw/workspace/apps/Yuzhua}"
YUZHUA_REPO_URL="${YUZHUA_REPO_URL:-https://github.com/juguangyuan520-dotcom/Yuzhua.git}"

log() {
  echo "[yuzhua-skill] $*"
}

ensure_git() {
  if ! command -v git >/dev/null 2>&1; then
    log "git not found. Please install git first."
    exit 1
  fi
}

clone_or_update() {
  if [ -d "${YUZHUA_HOME}/.git" ]; then
    log "Yuzhua already exists: ${YUZHUA_HOME}"
    log "Updating repository..."
    git -C "${YUZHUA_HOME}" pull --ff-only || {
      log "git pull failed. Keeping existing local files."
    }
    return
  fi

  if [ -d "${YUZHUA_HOME}" ] && [ ! -f "${YUZHUA_HOME}/start.sh" ]; then
    log "Directory exists but not a valid Yuzhua repo: ${YUZHUA_HOME}"
    log "Please set YUZHUA_HOME to a clean path, or remove the directory."
    exit 1
  fi

  log "Cloning Yuzhua from: ${YUZHUA_REPO_URL}"
  mkdir -p "$(dirname "${YUZHUA_HOME}")"
  git clone "${YUZHUA_REPO_URL}" "${YUZHUA_HOME}"
}

prepare_env() {
  if [ ! -f "${YUZHUA_HOME}/.env" ] && [ -f "${YUZHUA_HOME}/.env.example" ]; then
    cp "${YUZHUA_HOME}/.env.example" "${YUZHUA_HOME}/.env"
    log "Created .env from .env.example"
    log "Please edit ${YUZHUA_HOME}/.env if token is not auto-discovered."
  fi
}

main() {
  ensure_git
  clone_or_update

  if [ ! -f "${YUZHUA_HOME}/start.sh" ]; then
    log "Missing start.sh under ${YUZHUA_HOME}"
    exit 1
  fi

  chmod +x "${YUZHUA_HOME}/start.sh" || true
  prepare_env
  log "Install done."
  log "Next: YUZHUA_HOME=\"${YUZHUA_HOME}\" ./scripts/start.sh"
}

main "$@"
