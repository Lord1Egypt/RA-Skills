#!/usr/bin/env bash
# Test script for qr-bridge
# Tests: decode, generate, and round-trip verification
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SWIFT_SRC="$REPO_DIR/scripts/qr-decode.swift"
BINARY="$REPO_DIR/scripts/qr-decode"
PASS=0
FAIL=0

# --- Helpers ---
pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

check_output() {
  local output="$1" expected="$2" label="$3"
  local decoded=$(echo "$output" | sed 's|\\\/|/|g')
  if echo "$decoded" | grep -q "$expected"; then
    pass "$label"
  else
    fail "$label — expected: $expected"
  fi
}

# --- Setup ---
echo "=== qr-bridge test suite ==="
echo ""

# Compile if needed
if [ ! -f "$BINARY" ]; then
  echo "Compiling qr-decode.swift..."
  swiftc "$SWIFT_SRC" -o "$BINARY" -O
  echo "Compiled successfully."
fi

# --- Test 1: Decode pre-existing test QR ---
echo "[Test 1] Decode test-qr.png (https://example.com/hello)"
OUTPUT=$("$BINARY" "$SCRIPT_DIR/test-qr.png" 2>&1) || true
check_output "$OUTPUT" "https://example.com/hello" "URL content match"
check_output "$OUTPUT" '"ok" : true' "ok field is true"
check_output "$OUTPUT" '"count" : 1' "count is 1"

# --- Test 2: Generate + decode round-trip ---
echo "[Test 2] Generate QR → decode round-trip"
ROUND_TRIP_URL="https://mp.weixin.qq.com/s/qr-bridge-test"
ROUND_TRIP_IMG="/tmp/qr-bridge-roundtrip-test.png"

python3 -c "
import qrcode, sys
qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data(sys.argv[1])
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')
img.save(sys.argv[2])
" "$ROUND_TRIP_URL" "$ROUND_TRIP_IMG" 2>/dev/null

if [ -f "$ROUND_TRIP_IMG" ]; then
  pass "QR generation"
  OUTPUT=$("$BINARY" "$ROUND_TRIP_IMG" 2>&1) || true
  check_output "$OUTPUT" "$ROUND_TRIP_URL" "Round-trip decode matches"
  rm -f "$ROUND_TRIP_IMG"
else
  fail "QR generation — file not created"
fi

# --- Test 3: Plain text QR (non-URL) ---
echo "[Test 3] Plain text QR (non-URL content)"
PLAIN_TEXT="Hello, this is plain text - not a URL"
PLAIN_IMG="/tmp/qr-bridge-plain-test.png"

python3 -c "
import qrcode, sys
qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data(sys.argv[1])
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')
img.save(sys.argv[2])
" "$PLAIN_TEXT" "$PLAIN_IMG" 2>/dev/null

if [ -f "$PLAIN_IMG" ]; then
  OUTPUT=$("$BINARY" "$PLAIN_IMG" 2>&1) || true
  check_output "$OUTPUT" "Hello, this is plain text" "Plain text decode"
  rm -f "$PLAIN_IMG"
else
  fail "Plain text QR generation"
fi

# --- Test 4: Non-existent file error handling ---
echo "[Test 4] Error handling — non-existent file"
OUTPUT=$("$BINARY" "/tmp/does-not-exist-qr.png" 2>&1) || true
check_output "$OUTPUT" '"ok" : false' "Returns ok: false for missing file"
check_output "$OUTPUT" "File not found" "Error message present"

# --- Test 5: No QR code in image ---
echo "[Test 5] Error handling — image with no QR code"
NO_QR_IMG="/tmp/qr-bridge-noqr-test.png"
python3 -c "
from PIL import Image
img = Image.new('RGB', (200, 200), color='white')
img.save('$NO_QR_IMG')
" 2>/dev/null

if [ -f "$NO_QR_IMG" ]; then
  OUTPUT=$("$BINARY" "$NO_QR_IMG" 2>&1) || true
  check_output "$OUTPUT" '"ok" : false' "Returns ok: false for no QR"
  check_output "$OUTPUT" '"count" : 0' "Count is 0"
  rm -f "$NO_QR_IMG"
else
  fail "Blank image generation"
fi

# --- Summary ---
echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
  exit 1
else
  exit 0
fi
