#!/usr/bin/env bash
#
# setup.sh - QR Bridge setup script
# Compiles Swift QR decoder and checks Python dependencies.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== QR Bridge Setup ==="
echo "Skill directory: $SKILL_DIR"
echo ""

# --- 1. Compile Swift QR decoder ---
echo "[1/3] Compiling Swift QR decoder..."
SWIFT_SRC="$SCRIPT_DIR/qr-decode.swift"
SWIFT_BIN="$SCRIPT_DIR/qr-decode"

if [ ! -f "$SWIFT_SRC" ]; then
    echo "ERROR: $SWIFT_SRC not found"
    exit 1
fi

swiftc "$SWIFT_SRC" -o "$SWIFT_BIN" -O 2>&1
if [ $? -eq 0 ] && [ -f "$SWIFT_BIN" ]; then
    chmod +x "$SWIFT_BIN"
    echo "  OK: Compiled to $SWIFT_BIN"
else
    echo "  WARN: Swift compilation failed. Will use interpreted mode (slower)."
fi

# --- 2. Check Python qrcode library for QR generation ---
echo ""
echo "[2/3] Checking Python qrcode library..."
if python3 -c "import qrcode" 2>/dev/null; then
    echo "  OK: qrcode library available"
else
    echo "  Installing qrcode[pil]..."
    pip3 install "qrcode[pil]" 2>&1 | sed 's/^/  /'
fi

# --- 3. Check optional pyzbar fallback ---
echo ""
echo "[3/3] Checking pyzbar fallback decoder..."
if python3 -c "import pyzbar" 2>/dev/null; then
    echo "  OK: pyzbar available as fallback decoder"
else
    echo "  INFO: pyzbar not installed (optional fallback). Install with:"
    echo "        brew install zbar && pip3 install pyzbar"
fi

echo ""
echo "=== Setup Complete ==="
echo "Primary decoder: CoreImage (macOS native, zero dependencies)"
echo "QR generator:    Python qrcode library"
echo ""
echo "Test with: $SWIFT_BIN /path/to/qr-image.png"
