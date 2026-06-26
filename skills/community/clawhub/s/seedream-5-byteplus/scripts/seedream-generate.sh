#!/usr/bin/env bash
set -euo pipefail

if [[ -f /root/.clawdbot/.env ]]; then
  # shellcheck disable=SC1091
  source /root/.clawdbot/.env
fi

if [[ -z "${SEEDREAM_API_KEY:-}" ]]; then
  echo "Error: SEEDREAM_API_KEY not set" >&2
  exit 1
fi

PROMPT="${1:-}"
OUTFILE="${2:-/root/clawd/output/seedream-image-$(date +%s).jpg}"
MODEL="${SEEDREAM_MODEL:-seedream-5-0-260128}"
SIZE="${SEEDREAM_SIZE:-2K}"

if [[ -z "$PROMPT" ]]; then
  echo "Usage: $0 \"prompt\" [outfile]" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTFILE")"

PAYLOAD=$(python3 - "$MODEL" "$PROMPT" "$SIZE" <<'PY'
import json, sys
model, prompt, size = sys.argv[1], sys.argv[2], sys.argv[3]
print(json.dumps({
  "model": model,
  "prompt": prompt,
  "sequential_image_generation": "disabled",
  "response_format": "url",
  "size": size,
  "stream": False,
  "watermark": False,
}))
PY
)

RESP=$(curl -sS -X POST 'https://ark.ap-southeast.bytepluses.com/api/v3/images/generations' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${SEEDREAM_API_KEY}" \
  -d "$PAYLOAD")

IMAGE_URL=$(python3 - "$RESP" <<'PY'
import json, sys
obj = json.loads(sys.argv[1])
if isinstance(obj.get('data'), list) and obj['data']:
    item = obj['data'][0]
    print(item.get('url',''))
else:
    print(obj.get('url',''))
PY
)

if [[ -z "$IMAGE_URL" ]]; then
  echo "Seedream request failed:" >&2
  echo "$RESP" >&2
  exit 1
fi

curl -sS "$IMAGE_URL" -o "$OUTFILE"
echo "$OUTFILE"
