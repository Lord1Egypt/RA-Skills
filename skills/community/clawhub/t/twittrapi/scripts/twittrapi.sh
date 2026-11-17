#!/usr/bin/env bash
# Calls a TwittrAPI read endpoint with the simple format and prints the JSON body.
#   scripts/twittrapi.sh /user/by/username/XDevelopers
#   scripts/twittrapi.sh /search searchItem='from:XDevelopers lang:en' category=Latest count=20
#   scripts/twittrapi.sh /user/44196397/followers cursor=<nextCursor>
# Needs TWITTRAPI_API_KEY. TWITTRAPI_BASE_URL overrides https://api.twittrapi.com.
# Prints balance and price headers to stderr; exits 1 on HTTP errors (the body is still printed).
set -euo pipefail

if [[ $# -lt 1 || "$1" != /* ]]; then
	echo "usage: $0 /path [name=value ...]" >&2
	exit 2
fi
if [[ -z "${TWITTRAPI_API_KEY:-}" ]]; then
	echo "TWITTRAPI_API_KEY is not set. Get a key at https://twittrapi.com/start" >&2
	exit 2
fi

path="$1"
shift
args=(--get --data-urlencode "format=simple")
for kv in "$@"; do
	args+=(--data-urlencode "$kv")
done

headers="$(mktemp)"
body="$(mktemp)"
trap 'rm -f "$headers" "$body"' EXIT
status="$(curl -sS -o "$body" -D "$headers" -w '%{http_code}' \
	-H "X-API-KEY: ${TWITTRAPI_API_KEY}" -H "Accept: application/json" \
	"${args[@]}" "${TWITTRAPI_BASE_URL:-https://api.twittrapi.com}${path}")"
cat "$body"
echo
grep -iE '^(x-remaining-balance|x-price-per-call|x-refunded):' "$headers" >&2 || true
if [[ ! "$status" =~ ^2 ]]; then
	echo "HTTP $status" >&2
	exit 1
fi
