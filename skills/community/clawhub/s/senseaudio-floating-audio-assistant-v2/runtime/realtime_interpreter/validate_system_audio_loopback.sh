#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CAPTURE_SCRIPT="$SCRIPT_DIR/capture_blackhole_probe.sh"
OUT_PATH="${1:-/tmp/blackhole_validation.pcm}"
TEST_AIFF="/tmp/realtime_interpreter_loopback_test.aiff"
DURATION="${DURATION_SECONDS:-4}"

rm -f "$OUT_PATH" "$TEST_AIFF"

echo "Starting BlackHole capture probe for ${DURATION}s..."
DURATION_SECONDS="$DURATION" bash "$CAPTURE_SCRIPT" "$OUT_PATH" >/tmp/blackhole_validation_capture.log 2>&1 &
CAPTURE_PID=$!

cleanup() {
  if kill -0 "$CAPTURE_PID" >/dev/null 2>&1; then
    kill "$CAPTURE_PID" >/dev/null 2>&1 || true
    wait "$CAPTURE_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

sleep 1

echo "Playing test phrase through the current macOS output..."
say -o "$TEST_AIFF" "System audio capture validation for AudioClaw."
afplay "$TEST_AIFF"

wait "$CAPTURE_PID"
trap - EXIT

cat /tmp/blackhole_validation_capture.log

python3 - <<'PY' "$OUT_PATH"
from pathlib import Path
import struct
import sys

path = Path(sys.argv[1])
if not path.exists():
    print("Validation failed: capture file was not created.")
    raise SystemExit(1)

data = path.read_bytes()
if not data:
    print("Validation failed: capture file is empty.")
    raise SystemExit(1)

sample_count = len(data) // 2
samples = struct.unpack("<" + "h" * sample_count, data[: sample_count * 2])
peak = max(abs(v) for v in samples)
avg_abs = sum(abs(v) for v in samples) / len(samples)
nonzero_ratio = sum(1 for v in samples if v) / len(samples)

print(f"samples={len(samples)} peak={peak} avg_abs={avg_abs:.2f} nonzero_ratio={nonzero_ratio:.4f}")

if peak <= 0:
    print("Validation failed: BlackHole captured silence. Route macOS output into a Multi-Output Device that includes BlackHole 2ch, then retry.")
    raise SystemExit(2)

print("Validation succeeded: BlackHole is receiving real system audio.")
PY
