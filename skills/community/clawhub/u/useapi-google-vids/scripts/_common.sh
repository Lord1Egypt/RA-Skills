# Shared helpers for the useapi-google-vids skill scripts. Sourced, not run.
# Needs: curl, jq. Env: USEAPI_TOKEN (required), USEAPI_EMAIL (optional, which connected Google account to use).
# Written for bash 3.2 and later (the macOS default), so no bash 4 features.
set -euo pipefail

API="https://api.useapi.net/v1/google-vids"
UA="useapi-clawhub-google-vids/1.0.0"
: "${USEAPI_TOKEN:?Set USEAPI_TOKEN to your useapi.net API token (https://useapi.net/docs/start-here/setup-useapi)}"
command -v jq > /dev/null || { echo "jq is required (https://jqlang.org/download/)" >&2; exit 1; }

enc() { jq -rn --arg v "$1" '$v|@uri'; }
log() { echo "$(date +%H:%M:%S) $*" >&2; }

# acurl [curl args ...] -> curl to api.useapi.net with the skill's User-Agent and the Authorization header
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

# hint CODE BODY_FILE -> one line on what to do about a failed request or a failed job (stderr).
# CODE is the HTTP status, or error.code of a failed job record.
hint() {
  local code="$1" body
  body=$(cat "$2" 2>/dev/null || true)
  case "$code" in
    000) echo "Hint: no answer from the API (network error or timeout). A generation may still have been accepted: do not resend it blindly. Ask the user first." >&2 ;;
    400)
      if grep -Eq 'when spoken' <<< "$body"; then
        echo "Hint: the script runs over 30 seconds when spoken. Shorten it (about 250 to 400 characters, depending on the voice)." >&2
      elif grep -Eq 'extends clips of up to 24' <<< "$body"; then
        echo "Hint: Google Vids extends clips of up to 24 seconds, so the longest clip is about 34 seconds. Nothing was charged." >&2
      elif grep -Eq 'expired' <<< "$body"; then
        echo "Hint: a generated image lasts only a few hours. Make it again with image.sh, or upload the file again." >&2
      elif grep -Eq 'older Vids narrator voice' <<< "$body"; then
        echo "Hint: that avatar uses an old web-app voice the API cannot send. Make a new one with avatar.sh (avatar=<that avatarId> keeps the picture)." >&2
      elif grep -Eq 'not both|lives on' <<< "$body"; then
        echo "Hint: startImage cannot be combined with references, and every input of one request must come from the same Google account. Nothing was charged." >&2
      else
        echo "Hint: a parameter was rejected (the error names it). Nothing was charged. See https://useapi.net/docs/api-google-vids-v1" >&2
      fi ;;
    401) echo "Hint: the API token is wrong or missing. Check USEAPI_TOKEN." >&2 ;;
    403)
      if grep -Eq 'does not belong' <<< "$body"; then
        echo "Hint: that id was made with a different useapi.net API token." >&2
      elif grep -Eq 'smart features' <<< "$body"; then
        echo "Hint: the Google account has Google Workspace smart features turned off. Turn them on: https://useapi.net/docs/start-here/setup-google-vids#turn-on-smart-features" >&2
      else
        echo "Hint: this account's Google plan has no Google Vids allowance for this kind of job. Omni videos and images need Google AI Plus, Pro or Ultra (a free account makes avatars and talking avatar videos only). Nothing was charged." >&2
      fi ;;
    404)
      if grep -Eq 'expired' <<< "$body"; then
        echo "Hint: the file has expired at Google (videos last 24 hours, images a few hours). It cannot be downloaded any more." >&2
      elif grep -Eq 'Avatar not found' <<< "$body"; then
        echo "Hint: that avatar is not in the account's Google Vids document (already deleted?). avatar.sh --list shows what is there." >&2
      elif grep -Eq '"Job ' <<< "$body"; then
        echo "Hint: no such job. Check the job id." >&2
      else
        echo "Hint: that Google account is not connected. Check USEAPI_EMAIL, or see https://useapi.net/docs/start-here/setup-google-vids" >&2
      fi ;;
    410) echo "Hint: the job record has expired (job records are kept for 7 days)." >&2 ;;
    422)
      if grep -Eq 'avatar allowance' <<< "$body"; then
        echo "Hint: Google refused the finished talking avatar video, and still counted it against the month's AI avatar videos. Change the script or use another avatar." >&2
      else
        echo "Hint: Google refused the prompt or the inputs. Nothing was charged. Rephrase the prompt or change the inputs, then try again." >&2
      fi ;;
    429)
      if grep -Eq 'left this month|used up|allowance' <<< "$body"; then
        echo "Hint: the month's Google Vids allowance for this kind of job is used up. It resets at retryAt (the 1st of the month, 00:00 Pacific). Nothing was charged." >&2
      else
        echo "Hint: the account is busy (maxJobs jobs running) or Google is limiting it for about a minute. Nothing was charged. It is safe to send again once after retryAt or a minute. Do not loop on it." >&2
      fi ;;
    500) echo "Hint: an unexpected error at useapi.net. Try again later, and report the job id to support@useapi.net if it repeats." >&2 ;;
    502)
      if grep -Eq 'please retry|Retry shortly' <<< "$body"; then
        echo "Hint: Google did not complete the change. It is safe to try once more." >&2
      else
        echo "Hint: Google answered without a file the API could read. Google MAY HAVE CHARGED this job, so running it again is not free. Do not resubmit automatically: tell the user and report the job id to support@useapi.net." >&2
      fi ;;
    503) echo "Hint: Google answered with a server error or the job could not be queued. Try again in a minute or two." >&2 ;;
    504) echo "Hint: Google did not answer in time. Running it again is the fix, but Google may still have counted the first try: ask the user before resending." >&2 ;;
    596)
      if grep -Eq 'Re-add it' <<< "$body"; then
        echo "Hint: Google signed the account out and it must be reconnected: https://useapi.net/docs/start-here/setup-google-vids" >&2
      else
        echo "Hint: Google reported the account as signed out and it is being re-checked. Retry in about a minute. If it stays that way, reconnect it: https://useapi.net/docs/start-here/setup-google-vids" >&2
      fi ;;
  esac
}

# _finish METHOD PATH -> prints the body of a 2xx answer; anything else prints the error, a hint, and exits 1
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

# api METHOD PATH [JSON_BODY] -> response body on stdout; a non-2xx answer prints the error and exits 1.
# Never retried: a generation request sent twice could be charged twice.
api() {
  _call "$@"
  _finish "$1" "$2"
}

# api_poll METHOD PATH -> like api, for reads only: a network error, an HTTP 429 or a 5xx is retried
# up to 3 times, 10 s apart (except 596, which means the Google account needs attention)
api_poll() {
  local try=1
  while true; do
    _call "$@"
    case "$CODE" in
      000|429|5??)
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

# add_kv BODY KEY=VALUE -> BODY with the option added; a number for duration, strings otherwise
add_kv() {
  local body="$1" kv="$2" k v
  case "$kv" in *=*) ;; *) echo "Expected key=value, got: $kv" >&2; exit 1 ;; esac
  k="${kv%%=*}"
  v="${kv#*=}"
  case "$k" in
    duration)
      case "$v" in ''|*[!0-9]*) echo "duration must be a whole number of seconds, got: $v" >&2; exit 1 ;; esac
      jq --arg k "$k" --argjson v "$v" '.[$k] = $v' <<< "$body" ;;
    *) jq --arg k "$k" --arg v "$v" '.[$k] = $v' <<< "$body" ;;
  esac
}

# id_email ID -> the Google account an asset, image, video or avatar id lives on (user:<n>-<email>-<kind>:...)
id_email() { sed -E -n 's/^user:[0-9]+-(.*)-(asset|image|video|avatar):.*/\1/p' <<< "$1"; }

# file_or_id VALUE -> sets FID to VALUE unchanged, or, when VALUE is an existing local file, to its assetId after
# an upload. The first upload pins USEAPI_EMAIL to its account (exported), so every later input lands on the same
# one. Call it directly (file_or_id "$V"; V="$FID"), not in $( ), or the pinned account is lost.
file_or_id() {
  FID="$1"
  if [ -f "$1" ]; then
    FID=$(bash "$SCRIPTS/upload.sh" "$1") || exit 1
    if [ -z "${USEAPI_EMAIL:-}" ]; then
      USEAPI_EMAIL=$(id_email "$FID")
      export USEAPI_EMAIL
    fi
  fi
}

# start_job PATH BODY -> POSTs an async job (once, never retried) and prints its job id
start_job() {
  local job id
  job=$(api POST "$1" "$(jq '.async = true' <<< "$2")") || exit 1
  id=$(jq -r '.jobid // empty' <<< "$job")
  [ -n "$id" ] || { echo "No job id in the answer: $job" >&2; exit 1; }
  log "job $id"
  echo "$id"
}

SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
