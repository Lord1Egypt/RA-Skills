# Shared helpers for the useapi-google-flow-music skill scripts. Sourced, not run.
# Needs: curl, jq. Env: USEAPI_TOKEN (required), USEAPI_EMAIL (optional, which connected Google Flow Music account to use).
# Written for bash 3.2 and later (the macOS default), so no bash 4 features.
set -euo pipefail

API="https://api.useapi.net/v1/flowmusic"
UA="useapi-clawhub-google-flow-music/1.0.0"
: "${USEAPI_TOKEN:?Set USEAPI_TOKEN to your useapi.net API token (https://useapi.net/docs/start-here/setup-useapi)}"
command -v jq > /dev/null || { echo "jq is required (https://jqlang.org/download/)" >&2; exit 1; }

enc() { jq -rn --arg v "$1" '$v|@uri'; }
log() { echo "$(date +%H:%M:%S) $*" >&2; }

# acurl [curl args ...] -> curl to api.useapi.net with this skill's User-Agent and the Authorization header
# read from stdin (-H @-), so the token does not show up in the process list
acurl() { curl -A "$UA" "$@" -H @- <<< "Authorization: Bearer $USEAPI_TOKEN"; }

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

# hint CODE BODY_FILE -> one line on what to do about a failed request (stderr)
hint() {
  local code="$1" body
  body=$(cat "$2" 2>/dev/null || true)
  case "$code" in
    400)
      if grep -q 'No healthy' <<< "$body"; then
        echo "Hint: no working Google Flow Music account is connected to this useapi.net token (none added yet, or each one needs reconnecting): https://useapi.net/docs/start-here/setup-flowmusic" >&2
      else
        echo "Hint: a parameter was rejected. The error names it. Every option: https://useapi.net/docs/api-flowmusic-v1/post-flowmusic-music" >&2
      fi ;;
    401) echo "Hint: the API token is wrong or missing. Check USEAPI_TOKEN." >&2 ;;
    402) echo "Hint: the Google Flow Music account is out of credits. Wait for the plan's next top-up, or set USEAPI_EMAIL to another connected account that has credits." >&2 ;;
    403) echo "Hint: that job or clip belongs to another useapi.net account." >&2 ;;
    404) echo "Hint: not found. Check USEAPI_EMAIL (it must be a connected account), the job id or the clip id." >&2 ;;
    409) echo "Hint: the job is not completed yet. Wait for it with wait-job.sh first." >&2 ;;
    422) echo "Hint: the model made no audio for this request, usually a content refusal. Rephrase the prompt or the lyrics." >&2 ;;
    429) echo "Hint: the connected account is already running as many songs as it may at once (maxJobs). Wait until a running song finishes, then send it once more. Do not loop on it." >&2 ;;
    504) echo "Hint: the stem split is still running at Google Flow Music. Send the same request again in a minute: a clip that is already split answers at once." >&2 ;;
    596) echo "Hint: the Google Flow Music account needs to be reconnected: https://useapi.net/docs/start-here/setup-flowmusic" >&2 ;;
  esac
}

# _finish METHOD PATH -> prints the body of a 2xx answer. Anything else prints the error, a hint, and exits 1
_finish() {
  if [ "${CODE:0:1}" != "2" ]; then
    echo "$1 /$2 -> HTTP $CODE: $(cat "$OUT")" >&2
    hint "$CODE" "$OUT"
    rm -f "$OUT"
    exit 1
  fi
  cat "$OUT"
  rm -f "$OUT"
}

# api METHOD PATH [JSON_BODY] -> response body on stdout. A non-2xx answer prints the error and exits 1
api() {
  _call "$@"
  _finish "$1" "$2"
}

# api_poll METHOD PATH -> like api, for the polling loop: a network error or an HTTP 5xx is retried
# up to 3 times, 10 s apart (except 596, which means the account needs reconnecting)
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
