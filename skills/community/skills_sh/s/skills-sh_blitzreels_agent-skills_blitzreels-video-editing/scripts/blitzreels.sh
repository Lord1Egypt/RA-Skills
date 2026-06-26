#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BLITZREELS_API_BASE_URL:-https://www.blitzreels.com/api/v1}"
API_KEY="${BLITZREELS_API_KEY:-}"

if [[ -z "$API_KEY" ]]; then
  echo "BLITZREELS_API_KEY is required" >&2
  exit 1
fi

if [[ $# -lt 2 ]]; then
  echo "Usage: blitzreels.sh METHOD PATH [JSON_BODY]" >&2
  echo "Example: blitzreels.sh POST /projects '{\"name\":\"My Video\"}'" >&2
  exit 1
fi

METHOD="$1"
PATH_PART="$2"
BODY="${3:-}"

# Guardrail: require explicit opt-in for expensive operations.
# This prevents agents from accidentally triggering paid generation/export flows.
ALLOW_EXPENSIVE="${BLITZREELS_ALLOW_EXPENSIVE:-}"
is_expensive_path() {
  case "$1" in
    */faceless|*/faceless/*) return 0 ;;
    */export|*/export/*) return 0 ;;
  esac
  return 1
}

if [[ "${METHOD}" =~ ^(POST|PATCH|PUT)$ ]] && is_expensive_path "$PATH_PART"; then
  if [[ "$ALLOW_EXPENSIVE" != "1" && "$ALLOW_EXPENSIVE" != "true" ]]; then
    echo "Refusing to call expensive endpoint: ${PATH_PART}" >&2
    echo "Set BLITZREELS_ALLOW_EXPENSIVE=1 after explicit user approval to proceed." >&2
    exit 2
  fi
fi

if [[ -n "$BODY" ]]; then
  curl -sS -X "$METHOD" "${BASE_URL}${PATH_PART}" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$BODY"
else
  curl -sS -X "$METHOD" "${BASE_URL}${PATH_PART}" \
    -H "Authorization: Bearer $API_KEY"
fi
