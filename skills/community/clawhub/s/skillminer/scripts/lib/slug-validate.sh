#!/usr/bin/env bash
# skillminer slug validator
# Usage: validate_slug "<slug>" [<context-label>]
# Exits 4 on invalid slug with a clear error to stderr.

SKILLMINER_SLUG_REGEX='^[a-z0-9]+(-[a-z0-9]+){1,3}$'

validate_slug() {
  local slug="${1:-}"
  local ctx="${2:-slug}"
  if [[ -z "$slug" ]]; then
    echo "[skillminer] ERROR: empty $ctx" >&2
    return 4
  fi
  if [[ ! "$slug" =~ $SKILLMINER_SLUG_REGEX ]]; then
    echo "[skillminer] ERROR: invalid $ctx '$slug' - must match ${SKILLMINER_SLUG_REGEX}" >&2
    return 4
  fi
  return 0
}
