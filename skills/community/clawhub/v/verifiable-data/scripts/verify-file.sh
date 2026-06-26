#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <file-path> <seal-file>" >&2
  exit 1
fi

FILE_PATH="$1"
SEAL_FILE="$2"
if [[ ! -f "$FILE_PATH" ]]; then
  echo "file not found: $FILE_PATH" >&2
  exit 1
fi
if [[ ! -f "$SEAL_FILE" ]]; then
  echo "seal file not found: $SEAL_FILE" >&2
  exit 1
fi

CURL_BIN="${CURL_BIN:-curl}"
X_API_KEY="${CRYPTOWERK_X_API_KEY:-}"
require_command "$CURL_BIN"
require_command python3
if [[ -z "$X_API_KEY" ]]; then
  echo "set CRYPTOWERK_X_API_KEY before calling verify-file.sh" >&2
  exit 1
fi

HASH=$(sha256_file "$FILE_PATH")
SEAL=$(python3 - <<'PY' "$SEAL_FILE"
import json,sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    obj=json.load(f)
if 'seal' in obj:
    print(json.dumps(obj['seal'], separators=(',',':')))
else:
    docs=obj.get('documents') or []
    if docs and docs[0].get('seal'):
        print(json.dumps(docs[0]['seal'], separators=(',',':')))
    else:
        raise SystemExit('Could not extract seal object')
PY
)

RESPONSE=$($CURL_BIN --silent --show-error --fail-with-body -X POST "https://aiagent.cryptowerk.com/platform/API/v8/verifyseal" \
  -H "Accept: application/json" \
  -H "X-API-Key: $X_API_KEY" \
  --get \
  --data-urlencode "verifyDocHashes=$HASH" \
  --data-urlencode "seals=$SEAL")
printf '%s' "$RESPONSE" | validate_json
printf '%s\n' "$RESPONSE" > "$FILE_PATH.verify.json"
printf '%s\n' "$RESPONSE"
