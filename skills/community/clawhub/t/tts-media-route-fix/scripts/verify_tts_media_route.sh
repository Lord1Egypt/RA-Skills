#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "Usage: $0 <base_url> <bearer_token> <tts_id> <output_headers_file>" >&2
  echo "Example: $0 http://127.0.0.1:15443 abc123 9f2c... /tmp/tts_headers.txt" >&2
  exit 2
fi

BASE_URL="$1"
TOKEN="$2"
TTS_ID="$3"
HEADERS_OUT="$4"
URL="${BASE_URL%/}/media/tts/${TTS_ID}.mp3"

curl -sS -D "$HEADERS_OUT" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Range: bytes=0-127" \
  "$URL" \
  -o /tmp/tts-sample.bin

status=$(head -n1 "$HEADERS_OUT" | awk '{print $2}')
ctype=$(grep -i '^Content-Type:' "$HEADERS_OUT" | tail -n1 | cut -d' ' -f2- | tr -d '\r')

if [[ "$status" != "200" && "$status" != "206" ]]; then
  echo "FAIL: expected 200/206, got $status" >&2
  exit 3
fi

if [[ "$ctype" != "audio/mpeg"* ]]; then
  echo "FAIL: expected Content-Type audio/mpeg, got '$ctype'" >&2
  exit 4
fi

if file /tmp/tts-sample.bin | grep -qiE 'HTML|text'; then
  echo "FAIL: sample looks like text/html, not mp3 binary" >&2
  exit 5
fi

echo "OK: status=$status content-type=$ctype"
