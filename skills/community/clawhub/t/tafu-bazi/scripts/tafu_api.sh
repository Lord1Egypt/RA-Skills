#!/usr/bin/env sh

set -eu

if [ "${1:-}" = "" ] || [ "${2:-}" = "" ]; then
  echo "usage: tafu_api.sh METHOD PATH [JSON_BODY|@JSON_FILE]" >&2
  exit 1
fi

if [ "${TAFU_API_KEY:-}" = "" ]; then
  echo "TAFU_API_KEY is required" >&2
  exit 2
fi

METHOD="$1"
PATH_INPUT="$2"
BODY_INPUT="${3:-}"
BASE_URL="${TAFU_API_BASE_URL:-https://api.tafu.me/api/v1}"

case "$PATH_INPUT" in
  /*) PATH_SUFFIX="$PATH_INPUT" ;;
  *) PATH_SUFFIX="/$PATH_INPUT" ;;
esac

BASE_URL="$(printf '%s' "$BASE_URL" | sed 's:/*$::')"
URL="${BASE_URL}${PATH_SUFFIX}"

if [ "$BODY_INPUT" = "" ]; then
  exec curl -sS --fail-with-body \
    -X "$METHOD" \
    -H "Authorization: Bearer $TAFU_API_KEY" \
    "$URL"
fi

case "$BODY_INPUT" in
  @*)
    BODY_FILE="${BODY_INPUT#@}"
    exec curl -sS --fail-with-body \
      -X "$METHOD" \
      -H "Authorization: Bearer $TAFU_API_KEY" \
      -H "Content-Type: application/json" \
      --data-binary "@${BODY_FILE}" \
      "$URL"
    ;;
  *)
    exec curl -sS --fail-with-body \
      -X "$METHOD" \
      -H "Authorization: Bearer $TAFU_API_KEY" \
      -H "Content-Type: application/json" \
      --data-binary "$BODY_INPUT" \
      "$URL"
    ;;
esac
