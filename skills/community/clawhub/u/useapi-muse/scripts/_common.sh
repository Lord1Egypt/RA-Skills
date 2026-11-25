# Shared helpers for the useapi-muse skill scripts. Sourced, not run.
# Needs: curl, jq. Env: USEAPI_TOKEN (required), USEAPI_EMAIL (optional, which connected Muse account to use).
# Written for bash 3.2 and later (the macOS default), so no bash 4 features.
set -euo pipefail

API="https://api.useapi.net/v1/muse"
UA="useapi-clawhub-muse/1.0.0"
SCRIPTS="$(dirname "${BASH_SOURCE[0]}")"
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

# hint CODE BODY_FILE -> one line on what to do about a failed request or a failed job (stderr).
# CODE is the HTTP status, or error.code of a failed job record.
hint() {
  local code="$1" body
  body=$(cat "$2" 2>/dev/null || true)
  case "$code" in
    000) echo "Hint: no answer from the API (network error or timeout). A job may still have been accepted. Do not resend it blindly: check GET /jobs first." >&2 ;;
    400)
      if grep -q 'names .*was not provided' <<< "$body"; then
        echo "Hint: the prompt names an input (image_N, video_N or audio_N) that was not passed. Pass it, or reword the prompt. Nothing was used." >&2
      elif grep -q 'different accounts\|same account' <<< "$body"; then
        echo "Hint: all inputs of one job must be on the same Muse account. Upload them with the same USEAPI_EMAIL." >&2
      elif grep -q 'configure at least one account' <<< "$body"; then
        echo "Hint: no Muse account is connected yet. Add one: https://useapi.net/docs/start-here/setup-muse" >&2
      else
        echo "Hint: a parameter was rejected (the error names it). Nothing was used. See https://useapi.net/docs/api-muse-v1" >&2
      fi ;;
    401) echo "Hint: the API token is wrong or missing. Check USEAPI_TOKEN." >&2 ;;
    403)
      if grep -q 'does not belong' <<< "$body"; then
        echo "Hint: that id was made with a different useapi.net API token." >&2
      elif grep -q 'country or region' <<< "$body"; then
        echo "Hint: Meta has switched off video for this Muse account in its country or region. Image jobs still work. Once video works for the account again at muse.ai, add it again: https://useapi.net/docs/start-here/setup-muse" >&2
      else
        echo "Hint: Muse refused to make it (its own words are in the message), or asked for a confirmation. Running the same prompt again will not help. Change the prompt or the inputs." >&2
      fi ;;
    404) echo "Hint: the Muse account is not connected (check USEAPI_EMAIL, or https://useapi.net/docs/start-here/setup-muse), the job does not exist, or the file is no longer in the account's Muse Library." >&2 ;;
    409) echo "Hint: Muse says this account already made this request or has it queued, and will not do it again. Nothing was made. Change the prompt." >&2 ;;
    410) echo "Hint: the job is older than 7 days, and job records are kept for 7 days. Its files are still in the Muse Library if you have their assetIds." >&2 ;;
    411|413) echo "Hint: uploads are the raw file, at most 52,428,800 bytes (50 MB)." >&2 ;;
    412) echo "Hint: the account's weekly Muse allowance is used up. Nothing was made. account.sh shows quota.resetsAt, when it starts over." >&2 ;;
    429)
      if grep -q 'video limit' <<< "$body"; then
        echo "Hint: Muse's video limit for the last 24 hours is reached on this account. retryAt says when video jobs try it again. Image jobs still work. Nothing was made." >&2
      else
        echo "Hint: the account is running its maxJobs, or Muse is limiting it for about a minute. Nothing was made: it is safe to send once more after a minute. Do not loop on it." >&2
      fi ;;
    502) echo "Hint: Muse made a file the API could not read, or did not accept the message (for an upload or download: retry that). For a job, do not resubmit automatically: report the job id to useapi.net support." >&2 ;;
    503) echo "Hint: nothing was made (Muse could not be reached, or Muse failed to make it this time and said so). It is safe to run the same request again." >&2 ;;
    504) echo "Hint: Muse did not finish in time, but it MAY HAVE MADE THE FILE. Check GET /jobs/<jobid>?history=true and ask the user before running it again." >&2 ;;
    596) echo "Hint: the Muse account needs attention (a Meta security check, a changed password, or Muse disabled the account's computer). Sign in at https://muse.ai to see what it asks, then add the account again: https://useapi.net/docs/start-here/setup-muse" >&2 ;;
  esac
}

# _finish METHOD PATH -> prints the body of a 2xx answer. Anything else prints the error, a hint, and exits 1.
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

# api METHOD PATH [JSON_BODY] -> response body on stdout. A non-2xx answer prints the error and exits 1.
# Never retried: a generation request sent twice would use the allowance twice.
api() {
  _call "$@"
  _finish "$1" "$2"
}

# api_poll METHOD PATH -> like api, for reads only: a network error, an HTTP 429 or a 5xx is retried
# up to 3 times, 10 s apart (except 596, which means the Muse account needs attention)
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

# add_kv BODY KEY=VALUE -> BODY with the option added (all Muse job options are strings)
add_kv() {
  local body="$1" kv="$2" k v
  case "$kv" in *=*) ;; *) echo "Expected key=value, got: $kv" >&2; exit 1 ;; esac
  k="${kv%%=*}"
  v="${kv#*=}"
  jq --arg k "$k" --arg v "$v" '.[$k] = $v' <<< "$body"
}

# start_job image|video BODY -> POSTs an async job (once, never retried) and prints its job id
start_job() {
  local job id
  job=$(api POST "jobs/$1" "$(jq '.async = true' <<< "$2")")
  id=$(jq -r '.jobid // empty' <<< "$job")
  [ -n "$id" ] || { echo "No job id in the answer: $job" >&2; exit 1; }
  log "job $id"
  echo "$id"
}

# asset_email ASSET_ID -> the Muse account an asset lives on
# (the id embeds it hex-encoded: user:123-email:<hex>-image:...)
asset_email() {
  local hex
  hex=$(sed -n 's/.*-email:\([0-9a-fA-F]*\)-.*/\1/p' <<< "$1")
  [ -n "$hex" ] || return 0
  printf "$(sed 's/../\\x&/g' <<< "$hex")"
}

# resolve_inputs KEY=VALUE ... -> sets ARGS to the same options, with every image_N, video_N or audio_N value that is
# a local file uploaded first and replaced by its assetId. All inputs of one job must be on one Muse account, so without
# USEAPI_EMAIL the uploads go to the account of the first assetId given (or of the first upload).
resolve_inputs() {
  local kv k v id
  ARGS=()
  if [ -z "${USEAPI_EMAIL:-}" ]; then
    for kv in "$@"; do
      v="${kv#*=}"
      case "$v" in user:*-email:*)
        USEAPI_EMAIL=$(asset_email "$v")
        export USEAPI_EMAIL
        break ;;
      esac
    done
  fi
  for kv in "$@"; do
    k="${kv%%=*}"
    v="${kv#*=}"
    case "$k" in
      image_[1-9]|video_[1-3]|audio_[1-3])
        if [ "$k" != "$kv" ] && [ -f "$v" ]; then
          id=$("$SCRIPTS/upload.sh" "$v")
          if [ -z "${USEAPI_EMAIL:-}" ]; then
            USEAPI_EMAIL=$(asset_email "$id")
            export USEAPI_EMAIL
          fi
          kv="$k=$id"
        fi ;;
    esac
    ARGS+=("$kv")
  done
}
