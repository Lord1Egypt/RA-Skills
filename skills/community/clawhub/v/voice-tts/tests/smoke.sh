#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="/tmp/voice-tts-smoke.mp3"

echo "[1/3] validate TTS entrypoint"
node "$ROOT/bin/voice-tts.mjs" "你好，我是小叮当" -f "$OUT" --agent main >/tmp/voice-tts-smoke.log
test -f "$OUT" && echo "  TTS OK: $(ls -lh $OUT)"

echo "[2/3] validate ASR failure path (missing file)"
if node "$ROOT/bin/voice-asr.mjs" /tmp/not-exists-audio.ogg >/tmp/voice-asr.out 2>/tmp/voice-asr.err; then
  echo "ERROR: Expected ASR failure for missing file" >&2
  exit 1
fi
grep -q 'file_not_found' /tmp/voice-asr.err && echo "  ASR error handling OK"

echo "[3/3] validate send_voice_reply.mjs error path"
if node "$ROOT/scripts/send_voice_reply.mjs" >/tmp/send-voice.out 2>/tmp/send-voice.err; then
  echo "ERROR: Expected failure with missing args" >&2
  exit 1
fi
grep -q 'missing_text\|missing_chat_id' /tmp/send-voice.err && echo "  send_voice_reply error handling OK"

echo "SMOKE_OK"
