#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <tool_name> [json_args]" >&2
  exit 1
fi

TOOL_NAME="$1"
ARGS_JSON='{}'
if [[ $# -ge 2 ]]; then
  ARGS_JSON="$2"
fi

ENDPOINT="${SELL_THE_NEWS_MCP_ENDPOINT:-https://mcp.sellthenews.org/mcp}"
TMP_HEADERS="$(mktemp)"
TMP_BODY1="$(mktemp)"
TMP_BODY2="$(mktemp)"
cleanup() {
  rm -f "$TMP_HEADERS" "$TMP_BODY1" "$TMP_BODY2"
}
trap cleanup EXIT

INIT_PAYLOAD=$(python3 - <<'PY'
import json
print(json.dumps({
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "sell-the-news-skill", "version": "1.0.0"}
  }
}))
PY
)

curl -sS -D "$TMP_HEADERS" "$ENDPOINT" \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  --data "$INIT_PAYLOAD" > "$TMP_BODY1"

SESSION_ID="$(awk 'BEGIN{IGNORECASE=1} /^Mcp-Session-Id:/ {gsub(/\r/, "", $2); print $2}' "$TMP_HEADERS" | tail -n1)"

CALL_PAYLOAD=$(python3 - "$TOOL_NAME" "$ARGS_JSON" <<'PY'
import json, sys
name = sys.argv[1]
args = json.loads(sys.argv[2])
print(json.dumps({
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": name,
    "arguments": args
  }
}))
PY
)

CURL_ARGS=(
  -sS
  "$ENDPOINT"
  -H 'Accept: application/json, text/event-stream'
  -H 'Content-Type: application/json'
)

if [[ -n "$SESSION_ID" ]]; then
  CURL_ARGS+=( -H "Mcp-Session-Id: $SESSION_ID" )
fi

curl "${CURL_ARGS[@]}" --data "$CALL_PAYLOAD" > "$TMP_BODY2"

python3 - "$TMP_BODY2" <<'PY'
import json, sys
from pathlib import Path
text = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace')

# Try SSE format first
chunks = []
for line in text.splitlines():
    if line.startswith('data:'):
        payload = line[len('data:'):].strip()
        if payload:
            chunks.append(payload)

candidates = chunks if chunks else [text.strip()]
for candidate in candidates:
    try:
        obj = json.loads(candidate)
        if 'error' in obj:
            print(json.dumps(obj['error'], ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(4)
        print(json.dumps(obj.get('result', obj), ensure_ascii=False, indent=2))
        sys.exit(0)
    except Exception:
        pass

print(text)
sys.exit(0)
PY
