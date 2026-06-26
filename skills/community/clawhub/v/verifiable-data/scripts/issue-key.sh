#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

OUTPUT_FILE="${1:-}"
CURL_BIN="${CURL_BIN:-curl}"
require_command "$CURL_BIN"
require_command python3

RESPONSE=$($CURL_BIN --silent --show-error --fail-with-body -X POST "https://www.cryptowerk.com/api/issue-key" \
  -H "Content-Type: application/json")

printf '%s' "$RESPONSE" | validate_json

TOKEN=$(printf '%s' "$RESPONSE" | python3 -c '
import json,sys
obj=json.load(sys.stdin)
api_key=obj.get("apiKey")
cred=obj.get("apiCredential") or obj.get("credential")
if api_key and cred:
    print(f"{api_key} {cred}")
    raise SystemExit(0)
raise SystemExit("Could not extract issued key pair")
')

if [[ -n "$OUTPUT_FILE" ]]; then
  mkdir -p "$(dirname "$OUTPUT_FILE")"
  umask 077
  printf '%s\n' "$TOKEN" > "$OUTPUT_FILE"
  echo "wrote issued key to $OUTPUT_FILE" >&2
else
  printf '%s\n' "$TOKEN"
fi
