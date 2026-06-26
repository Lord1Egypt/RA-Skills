#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <rid-file|retrieval-id>" >&2
  exit 1
fi

INPUT="$1"
if [[ -f "$INPUT" ]]; then
  RID=$(tr -d '\n' < "$INPUT")
  BASE_PATH="${INPUT%.rid}"
else
  RID="$INPUT"
  BASE_PATH=""
fi

CURL_BIN="${CURL_BIN:-curl}"
X_API_KEY="${CRYPTOWERK_X_API_KEY:-}"
require_command "$CURL_BIN"
require_command python3
if [[ -z "$X_API_KEY" ]]; then
  echo "set CRYPTOWERK_X_API_KEY before calling get-seal.sh" >&2
  exit 1
fi

RESPONSE=$($CURL_BIN --silent --show-error --fail-with-body -X POST "https://aiagent.cryptowerk.com/platform/API/v8/getseal" \
  -H "Accept: application/json" \
  -H "X-API-Key: $X_API_KEY" \
  --get \
  --data-urlencode "retrievalId=$RID" \
  --data-urlencode "provideVerificationInfos=true")
printf '%s' "$RESPONSE" | validate_json

if ! printf '%s' "$RESPONSE" | python3 -c '
import json,sys
obj=json.load(sys.stdin)
if obj.get("seal"):
    raise SystemExit(0)
docs=obj.get("documents") or []
if docs and docs[0].get("seal"):
    raise SystemExit(0)
raise SystemExit(1)
'; then
  echo "seal not ready in getseal response" >&2
  printf '%s\n' "$RESPONSE"
  exit 3
fi

if [[ -n "$BASE_PATH" ]]; then
  printf '%s\n' "$RESPONSE" > "$BASE_PATH.seal"
fi
printf '%s\n' "$RESPONSE"
