#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$SCRIPT_DIR/mic_pcm_stream"
SRC="$SCRIPT_DIR/mic_pcm_stream.swift"
OUT_PATH="${1:-/tmp/blackhole_probe.pcm}"
DURATION="${DURATION_SECONDS:-3}"

if [ ! -x "$BIN" ] || [ "$SRC" -nt "$BIN" ]; then
  swiftc -O "$SRC" -o "$BIN" -framework AVFoundation
fi

echo "Capturing from BlackHole 2ch for ${DURATION}s -> $OUT_PATH"
"$BIN" --device-name "BlackHole 2ch" --sample-rate 16000 --duration-seconds "$DURATION" > "$OUT_PATH"

BYTES=$(wc -c < "$OUT_PATH" | tr -d ' ')
echo "Captured bytes: $BYTES"
if [ "$BYTES" -gt 0 ]; then
  echo "Probe capture succeeded."
else
  echo "Probe capture produced no audio bytes."
fi
