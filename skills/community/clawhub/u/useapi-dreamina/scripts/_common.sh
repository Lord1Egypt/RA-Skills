# Shared helpers for the useapi-dreamina skill scripts. Sourced, not run.
# Needs: curl, jq. Env: USEAPI_TOKEN (required), USEAPI_EMAIL (optional, which connected Dreamina account to use).
# Written for bash 3.2 and later (the macOS default), so no bash 4 features.
set -euo pipefail

API="https://api.useapi.net/v1/dreamina"
UA="useapi-clawhub-dreamina/1.0.0"
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
    CODE=$(acurl -sS --max-time 120 -o "$OUT" -w '%{http_code}' -H "Content-Type: application/json" -X "$method" "$API/$path" -d "$body") || true
  else
    CODE=$(acurl -sS --max-time 120 -o "$OUT" -w '%{http_code}' -X "$method" "$API/$path") || true
  fi
  CODE="${CODE:-000}"
}

# hint CODE BODY_FILE -> one line on what to do about a failed request (stderr)
hint() {
  local code="$1" body
  body=$(cat "$2" 2>/dev/null || true)
  case "$code" in
    000) echo "Hint: no answer from api.useapi.net. Check the network connection and try again." >&2 ;;
    400)
      if grep -q 'not available in region' <<< "$body"; then
        echo "Hint: this model or resolution is not offered in the account's region. 4K and seedance-2.5-flash need a Canada (CA) account: set USEAPI_EMAIL to one." >&2
      else
        echo "Hint: a parameter was rejected. The error names it; see https://useapi.net/docs/api-dreamina-v1/post-dreamina-videos" >&2
      fi ;;
    401) echo "Hint: the API token is wrong or missing. Check USEAPI_TOKEN (https://useapi.net/docs/start-here/setup-useapi)." >&2 ;;
    402) echo "Hint: the useapi.net subscription is missing or has expired: https://useapi.net/docs/subscription" >&2 ;;
    403)
      if grep -q '4010' <<< "$body"; then
        echo "Hint: Dreamina wants its one-time \"Before you continue\" confirmation. Retry once. If it persists, sign in at dreamina.capcut.com with this account, start a generation with this model, click Agree, then retry." >&2
      else
        echo "Hint: the Dreamina account has no paid Dreamina plan that includes this model (credits bought separately don't count). Seedance video needs a paid plan." >&2
      fi ;;
    404) echo "Hint: not found. No Dreamina account is connected (https://useapi.net/docs/start-here/setup-dreamina), or the job id is wrong or older than 30 days." >&2 ;;
    412) echo "Hint: the Dreamina account is out of credits, or unlimited=true was sent and the account has no Unlimited for this model and resolution. Top up the account, or send it without unlimited." >&2 ;;
    429) echo "Hint: the Dreamina account is busy with other jobs (or already runs an Unlimited job). Wait for them to finish, then send it once more. Do not loop on it." >&2 ;;
    503) echo "Hint: Dreamina signed the account out and signing in again failed for now. Try again in about 30 seconds." >&2 ;;
    596) echo "Hint: the Dreamina session expired or is in a sign-out pause. Check https://useapi.net/docs/api-dreamina-v1/get-dreamina-accounts and re-add the account if needed: https://useapi.net/docs/start-here/setup-dreamina" >&2 ;;
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
# up to 3 times, 15 s apart (except 596, which means the Dreamina account needs attention)
api_poll() {
  local try=1
  while true; do
    _call "$@"
    case "$CODE" in
      000|5??)
        if [ "$CODE" != 596 ] && [ "$try" -le 3 ]; then
          log "$1 /$2 -> HTTP $CODE, retry $try of 3 in 15 s"
          rm -f "$OUT"
          try=$((try + 1))
          sleep 15
          continue
        fi ;;
    esac
    break
  done
  _finish "$1" "$2"
}

# account_id [REGION] -> the account id (REGION:email, such as CA:user@example.com) to use, on stdout.
# USEAPI_EMAIL may be that id or just the email. Without USEAPI_EMAIL: the first connected account
# (of REGION, US or CA, when given) that has no error and is not in a sign-out pause.
account_id() {
  local want="${1:-}" accounts id
  case "${USEAPI_EMAIL:-}" in
    *:*) echo "$USEAPI_EMAIL"; return 0 ;;
  esac
  accounts=$(api GET accounts) || exit 1
  if [ -n "${USEAPI_EMAIL:-}" ]; then
    id=$(jq -r --arg e "$USEAPI_EMAIL" '[.[] | select((.email // "" | ascii_downcase) == ($e | ascii_downcase))][0].account // empty' <<< "$accounts")
  else
    id=$(jq -r --arg r "$want" '[.[] | select((.error | not) and (.signedOutPauseUntil | not) and ($r == "" or .region == $r))][0].account // empty' <<< "$accounts")
  fi
  if [ -z "$id" ]; then
    echo "No matching Dreamina account${USEAPI_EMAIL:+ for $USEAPI_EMAIL}${want:+ in region $want}. Connected: $(jq -r '[.[].account] | join(", ")' <<< "$accounts")" >&2
    exit 1
  fi
  echo "$id"
}
