# Shared helpers for the useapi-pixverse skill scripts. Sourced, not run.
# Needs: curl, jq. Env: USEAPI_TOKEN (required), USEAPI_EMAIL (optional, which connected PixVerse account to use).
# Written for bash 3.2 and later (the macOS default), so no bash 4 features.
set -euo pipefail

API="https://api.useapi.net/v2/pixverse"
UA="useapi-clawhub-pixverse/1.0.0"
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
    400) echo "Hint: a parameter was rejected. The error names it. Check the model's durations, qualities and ratios: https://useapi.net/docs/api-pixverse-v2/model-capabilities" >&2 ;;
    401) echo "Hint: the API token is wrong or missing. Check USEAPI_TOKEN (https://useapi.net/docs/start-here/setup-useapi)." >&2 ;;
    402) echo "Hint: the useapi.net subscription is missing or has expired: https://useapi.net/docs/subscription" >&2 ;;
    404) echo "Hint: not found. No PixVerse account is connected (https://useapi.net/docs/start-here/setup-pixverse), or the video id is wrong." >&2 ;;
    412)
      if grep -qi 'credits' <<< "$body"; then
        echo "Hint: the PixVerse account is out of credits. Top it up or upgrade the PixVerse plan." >&2
      else
        echo "Hint: the PixVerse plan does not allow this request. Third-party models (Seedance, Kling, Veo, MiniMax H3, Wan, Grok Imagine) need a PixVerse Pro plan or higher; the default model v6 works on every paid plan." >&2
      fi ;;
    422) echo "Hint: PixVerse moderation refused the prompt. Rephrase it, without brand or character names." >&2 ;;
    429) echo "Hint: the PixVerse account is busy with other jobs. Wait 10 to 30 seconds and send it once more. Do not loop on it." >&2 ;;
    596) echo "Hint: the PixVerse account has a pending error (password changed, suspended or banned). Re-add it: https://useapi.net/docs/api-pixverse-v2/post-pixverse-accounts-email" >&2 ;;
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

# account_email -> the PixVerse account email to use, on stdout: USEAPI_EMAIL, else the first connected account.
account_email() {
  local accounts id
  if [ -n "${USEAPI_EMAIL:-}" ]; then echo "$USEAPI_EMAIL"; return 0; fi
  accounts=$(api GET accounts) || exit 1
  id=$(jq -r '[.[] | select(type == "object" and .email) | .email][0] // empty' <<< "$accounts")
  if [ -z "$id" ]; then
    echo "No PixVerse account is connected: https://useapi.net/docs/start-here/setup-pixverse" >&2
    exit 1
  fi
  echo "$id"
}
