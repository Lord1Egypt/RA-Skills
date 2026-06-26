#!/usr/bin/env bash
set -euo pipefail

export LC_ALL=C

BASE_URL="${SKYLIGHT_URL:-https://app.ourskylight.com}"
COOKIE_JAR="${SKYLIGHT_COOKIE_JAR:-$(mktemp -t skylight-cookies.XXXXXX)}"
STATE="${SKYLIGHT_OAUTH_STATE:-Ko5P20HH4D}"
DEVICE_FINGERPRINT="${SKYLIGHT_DEVICE_FINGERPRINT:-f98d88f8-91df-4e71-b405-219dbcf3e0e6}"

cleanup() {
  if [[ -z "${SKYLIGHT_COOKIE_JAR:-}" && -f "$COOKIE_JAR" ]]; then
    rm -f "$COOKIE_JAR"
  fi
}
trap cleanup EXIT

resolve_secret() {
  local value="$1"
  local ref="$2"
  local label="$3"

  if [[ -n "$value" ]]; then
    if [[ "$value" == op://* ]]; then
      command -v op >/dev/null || {
        echo "$label is a 1Password reference but 'op' is not installed" >&2
        exit 1
      }
      op read "$value"
    else
      printf '%s\n' "$value"
    fi
    return
  fi

  if [[ -n "$ref" ]]; then
    command -v op >/dev/null || {
      echo "$label reference was provided but 'op' is not installed" >&2
      exit 1
    }
    op read "$ref"
    return
  fi

  echo "Missing $label. Set it directly or set ${label}_OP_REF to an op:// reference." >&2
  exit 1
}

SKYLIGHT_EMAIL_VALUE="$(resolve_secret "${SKYLIGHT_EMAIL:-}" "${SKYLIGHT_EMAIL_OP_REF:-${SKYLIGHT_EMAIL_1PASSWORD_REF:-}}" "SKYLIGHT_EMAIL")"
SKYLIGHT_PASSWORD_VALUE="$(resolve_secret "${SKYLIGHT_PASSWORD:-}" "${SKYLIGHT_PASSWORD_OP_REF:-${SKYLIGHT_PASSWORD_1PASSWORD_REF:-}}" "SKYLIGHT_PASSWORD")"

COMMON_HEADERS=(
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
)

# Skylight's web/mobile OAuth flow currently accepts this random challenge value.
code_challenge="$(openssl rand -hex 20)"

curl -fsS -c "$COOKIE_JAR" \
  "${COMMON_HEADERS[@]}" \
  -H 'referer: https://ourskylight.com/' \
  "$BASE_URL/oauth/authorize?code_challenge=$code_challenge&prompt=login&code_challenge_method=S256&redirect_uri=https%3A%2F%2Fourskylight.com%2Fwelcome&client_id=skylight-mobile&response_type=code&state=$STATE&scope=everything" \
  >/dev/null

html="$(curl -fsS -c "$COOKIE_JAR" \
  -b "$COOKIE_JAR" \
  "${COMMON_HEADERS[@]}" \
  "$BASE_URL/auth/session/new")"

authenticity_token="$(printf '%s' "$html" | python3 -c '
from html.parser import HTMLParser
import sys

class TokenParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.token = ""

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "input":
            return
        values = dict(attrs)
        if values.get("name") == "authenticity_token":
            self.token = values.get("value", "")

parser = TokenParser()
parser.feed(sys.stdin.read())
print(parser.token)
')"

if [[ -z "$authenticity_token" ]]; then
  echo "Failed to extract authenticity_token" >&2
  exit 1
fi

headers="$(curl -fsS -i \
  "$BASE_URL/auth/session" \
  -b "$COOKIE_JAR" -c "$COOKIE_JAR" \
  "${COMMON_HEADERS[@]}" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Origin: https://app.ourskylight.com' \
  -H 'Referer: https://app.ourskylight.com/auth/session/new' \
  --data-urlencode "authenticity_token=$authenticity_token" \
  --data-urlencode "email=$SKYLIGHT_EMAIL_VALUE" \
  --data-urlencode "password=$SKYLIGHT_PASSWORD_VALUE")"

first_location="$(printf '%s\n' "$headers" \
  | awk 'BEGIN{IGNORECASE=1} /^location:/ {sub(/\r$/,"",$2); print $2; exit}')"

if [[ -z "$first_location" ]]; then
  echo "No first Location header found" >&2
  exit 1
fi

second_headers="$(curl -fsS -i \
  -b "$COOKIE_JAR" \
  -c "$COOKIE_JAR" \
  "${COMMON_HEADERS[@]}" \
  "$first_location")"

second_location="$(printf '%s\n' "$second_headers" \
  | awk 'BEGIN{IGNORECASE=1} /^location:/ {sub(/\r$/,"",$2); print $2; exit}')"

if [[ -z "$second_location" ]]; then
  echo "No second Location header found" >&2
  exit 1
fi

code="$(python3 -c '
import sys, urllib.parse
url = sys.argv[1]
qs = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
print(qs.get("code", [""])[0])
' "$second_location")"

if [[ -z "$code" ]]; then
  echo "No OAuth code found in redirect" >&2
  exit 1
fi

at_response="$(curl -fsS "$BASE_URL/oauth/token" \
  -H 'content-type: application/x-www-form-urlencoded' \
  -H 'origin: https://ourskylight.com' \
  -H 'referer: https://ourskylight.com/' \
  --data-urlencode 'grant_type=authorization_code' \
  --data-urlencode 'client_id=skylight-mobile' \
  --data-urlencode 'scope=everything' \
  --data-urlencode "skylight_api_client_device_fingerprint=$DEVICE_FINGERPRINT" \
  --data-urlencode 'skylight_api_client_device_platform=web' \
  --data-urlencode 'skylight_api_client_device_name=unknown' \
  --data-urlencode 'skylight_api_client_device_os_version=10.15.7' \
  --data-urlencode 'skylight_api_client_device_app_version=unknown' \
  --data-urlencode 'skylight_api_client_device_hardware=Macintosh' \
  --data-urlencode 'source=js-mobile' \
  --data-urlencode 'redirect_uri=https://ourskylight.com/welcome' \
  --data-urlencode "code=$code")"

access_token="$(printf '%s' "$at_response" | python3 -c '
import json, sys
try:
    print(json.load(sys.stdin).get("access_token", ""))
except Exception:
    print("")
')"

if [[ -z "$access_token" ]]; then
  echo "Failed to extract access_token from oauth/token response" >&2
  exit 1
fi

printf 'Bearer %s\n' "$access_token"
