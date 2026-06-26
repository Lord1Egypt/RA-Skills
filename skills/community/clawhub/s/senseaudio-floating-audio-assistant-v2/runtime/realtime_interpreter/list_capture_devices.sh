#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$SCRIPT_DIR/mic_pcm_stream"
SRC="$SCRIPT_DIR/mic_pcm_stream.swift"

if [ ! -x "$BIN" ] || [ "$SRC" -nt "$BIN" ]; then
  swiftc -O "$SRC" -o "$BIN" -framework AVFoundation
fi

exec "$BIN" --list-devices
