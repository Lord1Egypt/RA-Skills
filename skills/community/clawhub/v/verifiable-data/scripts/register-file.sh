#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <file-path> [lookup-info]" >&2
  exit 1
fi

FILE_PATH="$1"
if [[ ! -f "$FILE_PATH" ]]; then
  echo "file not found: $FILE_PATH" >&2
  exit 1
fi

CURL_BIN="${CURL_BIN:-curl}"
X_API_KEY="${CRYPTOWERK_X_API_KEY:-}"
require_command "$CURL_BIN"
require_command python3
if [[ -z "$X_API_KEY" ]]; then
  echo "set CRYPTOWERK_X_API_KEY to the exact issued token before calling register-file.sh" >&2
  exit 1
fi

HASH=$(sha256_file "$FILE_PATH")
LOOKUP_INFO="${2:-sha256:$HASH}"
RESPONSE=$($CURL_BIN --silent --show-error --fail-with-body -X POST "https://aiagent.cryptowerk.com/platform/API/v8/register" \
  -H "Accept: application/json" \
  -H "X-API-Key: $X_API_KEY" \
  --get \
  --data-urlencode "hashes=$HASH" \
  --data-urlencode "lookupInfo=$LOOKUP_INFO")

printf '%s' "$RESPONSE" | validate_json
RID=$(printf '%s' "$RESPONSE" | python3 -c '
import json,sys
obj=json.load(sys.stdin)
docs=obj.get("documents") or []
if docs and docs[0].get("retrievalId"):
    print(docs[0]["retrievalId"])
    raise SystemExit(0)
raise SystemExit("Could not extract retrievalId")
')
printf '%s\n' "$RID" > "$FILE_PATH.rid"
python3 - "$FILE_PATH" "$LOOKUP_INFO" "$HASH" "$RID" <<'PY'
import json
import sys
from datetime import datetime, timezone
file_path, lookup_info, sha256, retrieval_id = sys.argv[1:5]
meta={
  "version": 1,
  "sourcePath": file_path,
  "lookupInfo": lookup_info,
  "sha256": sha256,
  "retrievalId": retrieval_id,
  "registeredAt": datetime.now(timezone.utc).isoformat(),
  "sealPath": f"{file_path}.seal",
  "verifyPath": f"{file_path}.verify.json",
  "lastSealReceivedAt": None,
  "lastVerifiedAt": None,
  "lastError": None,
}
with open(f"{file_path}.cw.json","w", encoding="utf-8") as f:
    json.dump(meta,f,indent=2)
    f.write("\n")
PY
printf '%s\n' "$RESPONSE"
