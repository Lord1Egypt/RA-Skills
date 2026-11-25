# Shared helpers for the useapi-gemini-notebook skill scripts. Sourced, not run.
# Needs: curl, jq. Env: USEAPI_TOKEN (required), USEAPI_EMAIL (optional, which connected Google account to use).
# Written for bash 3.2 and later (the macOS default), so no bash 4 features.
set -euo pipefail

API="https://api.useapi.net/v1/gemini-notebook"
: "${USEAPI_TOKEN:?Set USEAPI_TOKEN to your useapi.net API token (https://useapi.net/docs/start-here/setup-useapi)}"
command -v jq > /dev/null || { echo "jq is required (https://jqlang.org/download/)" >&2; exit 1; }

enc() { jq -rn --arg v "$1" '$v|@uri'; }
log() { echo "$(date +%H:%M:%S) $*" >&2; }

# acurl [curl args ...] -> curl with the Authorization header read from stdin (-H @-),
# so the token does not show up in the process list
acurl() { curl "$@" -H @- <<< "Authorization: Bearer $USEAPI_TOKEN"; }

# _call METHOD PATH [JSON_BODY] -> sets CODE (the HTTP status, 000 on a network error) and OUT (a temp file with the body)
_call() {
  local method="$1" path="$2" body="${3:-}"
  OUT=$(mktemp)
  if [ -n "$body" ]; then
    CODE=$(acurl -sS --max-time 320 -o "$OUT" -w '%{http_code}' -H "Content-Type: application/json" -X "$method" "$API/$path" -d "$body") || true
  else
    CODE=$(acurl -sS --max-time 320 -o "$OUT" -w '%{http_code}' -X "$method" "$API/$path") || true
  fi
  CODE="${CODE:-000}"
}

# _finish METHOD PATH -> prints the body of a 2xx answer; anything else prints the error and exits 1
_finish() {
  if [ "${CODE:0:1}" != "2" ]; then
    echo "$1 /$2 -> HTTP $CODE: $(cat "$OUT")" >&2
    rm -f "$OUT"
    exit 1
  fi
  cat "$OUT"
  rm -f "$OUT"
}

# api METHOD PATH [JSON_BODY] -> response body on stdout; a non-2xx answer prints the error and exits 1
api() {
  _call "$@"
  _finish "$1" "$2"
}

# api_poll METHOD PATH -> like api, for the polling loops: a network error or an HTTP 5xx is retried
# up to 3 times, 10 s apart (except 596, which means the Google account needs reconnecting)
api_poll() {
  local try=1
  while true; do
    _call "$@"
    case "$CODE" in
      000|5??)
        if [ "$CODE" != 596 ] && [ "$try" -le 3 ]; then
          log "$1 /$2 -> HTTP $CODE, retry $try of 3 in 10 s"
          rm -f "$OUT"
          try=$((try + 1))
          sleep 10
          continue
        fi ;;
    esac
    break
  done
  _finish "$1" "$2"
}
