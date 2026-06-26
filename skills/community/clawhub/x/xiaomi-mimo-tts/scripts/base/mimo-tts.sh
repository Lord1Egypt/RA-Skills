#!/usr/bin/env bash
# Shell base implementation wrapper for mimo-tts
# Supports: --voice, --style, --dry-run

set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/_env.sh"

TEXT="$1"
OUTPUT="${2:-$SKILL_OUT/output.mock.ogg}"
shift || true

VOICE="${MIMO_VOICE:-mimo_default}"
STYLE="${MIMO_STYLE:-}"
DRY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --voice) VOICE="$2"; shift 2;;
    --style) STYLE="$2"; shift 2;;
    --dry-run) DRY=1; shift;;
    *) shift;;
  esac
done

if [[ -n "$STYLE" && "$TEXT" != "<style>*" ]]; then
  TEXT="<style>$STYLE</style>$TEXT"
fi

if [[ $DRY -eq 1 ]]; then
  echo "DRY RUN: request payload preview"
  python3 - <<PY
import json
body={
  'model':'mimo-v2-tts',
  'messages':[{'role':'user','content':'请朗读'},{'role':'assistant','content':"""$TEXT"""}],
  'audio':{'format':'wav','voice':'$VOICE'}
}
print(json.dumps(body,ensure_ascii=False,indent=2))
PY
  exit 0
fi

# prefer node -> python -> shell implementations
if command -v node >/dev/null 2>&1 && [ -f "${SKILL_HOME}/scripts/base/mimo_tts.js" ]; then
  node "${SKILL_HOME}/scripts/base/mimo_tts.js" "$TEXT" "$OUTPUT" --voice "$VOICE"
  exit $?
fi

if command -v python3 >/dev/null 2>&1 && [ -f "${SKILL_HOME}/scripts/base/mimo_tts.py" ]; then
  python3 "${SKILL_HOME}/scripts/base/mimo_tts.py" "$TEXT" "$OUTPUT" --voice "$VOICE"
  exit $?
fi

# fallback: simple curl-based request
curl -s -X POST "https://api.xiaomimimo.com/v1/chat/completions" \
  -H "Authorization: Bearer ${XIAOMI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$(printf '%s' "{\"model\":\"mimo-v2-tts\",\"messages\":[{\"role\":\"user\",\"content\":\"请朗读\"},{\"role\":\"assistant\",\"content\":\"$TEXT\"}],\"audio\":{\"format\":\"wav\",\"voice\":\"$VOICE\"}}")" \
  | jq -r '.choices[0].message.audio.data' | base64 -d > "$OUTPUT.wav" || true

if command -v ffmpeg >/dev/null 2>&1; then
  ffmpeg -y -i "$OUTPUT.wav" -acodec libopus -b:a 128k "$OUTPUT" >/dev/null 2>&1 && rm -f "$OUTPUT.wav"
else
  echo "ffmpeg not found; leaving wav at $OUTPUT.wav"
  mv "$OUTPUT.wav" "$OUTPUT"
fi

echo "$OUTPUT"
