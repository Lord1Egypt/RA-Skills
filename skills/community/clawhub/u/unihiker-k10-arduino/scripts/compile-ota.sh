#!/usr/bin/env bash
# Unihiker K10 Arduino Compile & OTA Upload - Bash Version (macOS / Linux)
# Usage: ./compile-ota.sh <sketch_dir> [-i <device_ip>] [-n]
#
# Optimized compilation with:
#   - Incremental builds (--build-path .arduino-build)
#   - Parallel compilation (--jobs 0)
#   - Global build cache
#   - Custom OTA partition table
#
# If -i <ip> is provided, uploads the compiled .bin via HTTP OTA after compilation.
# Without -i, compiles only. Use -n to skip upload even with -i.

set -euo pipefail

FQBN="UNIHIKER:esp32:k10"

# --- helpers ---
info()  { echo -e "\033[36m[INFO]\033[0m $*"; }
ok()    { echo -e "\033[32m[OK]\033[0m $*"; }
warn()  { echo -e "\033[33m[WARN]\033[0m $*"; }
err()   { echo -e "\033[31m[ERROR]\033[0m $*"; }

usage() {
  echo "Usage: $0 <sketch_dir> [-i <device_ip>] [-n]"
  echo ""
  echo "  sketch_dir    Path to the Arduino sketch directory"
  echo "  -i <ip>       Device IP for OTA upload (default: skip upload)"
  echo "  -n            No upload (skip even if -i is set)"
  exit 1
}

# --- parse args ---
SKETCH_DIR=""
IP=""
NO_UPLOAD=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -i) IP="$2"; shift 2 ;;
    -n) NO_UPLOAD=true; shift ;;
    -*) usage ;;
    *)  SKETCH_DIR="$1"; shift ;;
  esac
done

if [[ -z "$SKETCH_DIR" ]]; then
  usage
fi

SKETCH_PATH="$(realpath "$SKETCH_DIR")"
SKETCH_NAME="$(basename "$SKETCH_PATH")"
BUILD_CACHE_DIR="$SKETCH_PATH/.arduino-build"
OUTPUT_DIR="$SKETCH_PATH/build"

if [[ ! -d "$SKETCH_PATH" ]]; then
  err "Sketch directory not found: $SKETCH_DIR"
  exit 1
fi

info "Sketch: $SKETCH_NAME"
info "FQBN: $FQBN"
info "Build cache: $BUILD_CACHE_DIR"
info "Output dir: $OUTPUT_DIR"

# Find arduino-cli
ARDUINO_CLI=""
if command -v arduino-cli &>/dev/null; then
  ARDUINO_CLI="arduino-cli"
elif [[ -x "$(dirname "$0")/arduino-cli" ]]; then
  ARDUINO_CLI="$(dirname "$0")/arduino-cli"
else
  err "arduino-cli not found in PATH or script directory"
  echo "Install: https://arduino.github.io/arduino-cli/latest/installation/"
  exit 1
fi

info "Using arduino-cli: $ARDUINO_CLI"

# Create directories
mkdir -p "$BUILD_CACHE_DIR" "$OUTPUT_DIR"

# Compile with optimizations
info "Compiling (incremental + parallel)..."

START_TIME=$(date +%s)

"$ARDUINO_CLI" compile \
  --fqbn "$FQBN" \
  "$SKETCH_PATH" \
  --build-path "$BUILD_CACHE_DIR" \
  --output-dir "$OUTPUT_DIR" \
  --build-property "build.partitions=custom" \
  --jobs 0

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

if [[ $? -ne 0 ]]; then
  err "Compilation failed"
  exit 1
fi

ok "Compilation successful in ${ELAPSED}s"
info "Output: $OUTPUT_DIR/${SKETCH_NAME}.ino.bin"

# OTA upload
if [[ "$NO_UPLOAD" == false && -n "$IP" ]]; then
  BIN_FILE="$OUTPUT_DIR/${SKETCH_NAME}.ino.bin"

  if [[ ! -f "$BIN_FILE" ]]; then
    err "Binary not found: $BIN_FILE"
    exit 1
  fi

  info "Uploading via OTA to $IP ..."

  RESPONSE=$(curl -s -w "\n%{http_code}" \
    -F "file=@${BIN_FILE}" \
    -H "Connection: close" \
    --connect-timeout 10 \
    --max-time 60 \
    "http://${IP}/ota" 2>&1) || {
    err "OTA upload failed: could not connect to $IP"
    echo "Tips:"
    echo "  - Ensure device is on the same network or connected to K10-pH-Titrator AP"
    echo "  - Verify IP address: $IP"
    echo "  - First upload requires USB (partition table change)"
    exit 1
  }

  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  if [[ "$BODY" == "OK" ]]; then
    ok "OTA upload successful. Device will restart in ~1.2s."
  else
    warn "OTA upload returned: $BODY (HTTP $HTTP_CODE)"
  fi
elif [[ -z "$IP" ]]; then
  info "No -i <ip> specified, skipping OTA upload."
  info "To upload: $0 $SKETCH_DIR -i <device_ip>"
  info "Or run: python3 ota_upload.py $OUTPUT_DIR/${SKETCH_NAME}.ino.bin --ip <device_ip>"
fi
