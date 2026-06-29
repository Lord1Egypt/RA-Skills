#!/usr/bin/env bash
set -euo pipefail

BUNDLE="${1:-}"
CORE_DIR="${PLATFORMIO_CORE_DIR:-$HOME/.platformio}"

usage() {
  echo "Usage: $0 <k10-platformio-bundle.tgz>"
  echo "Optional: PLATFORMIO_CORE_DIR=/path/to/.platformio $0 <bundle.tgz>"
  exit 1
}

if [[ -z "$BUNDLE" || ! -f "$BUNDLE" ]]; then
  usage
fi

mkdir -p "$CORE_DIR"
tar -xzf "$BUNDLE" -C "$CORE_DIR"

echo "[OK] Installed K10 PlatformIO support files into: $CORE_DIR"
echo "[INFO] Verify with: doctor-offline.sh"
echo "[INFO] Or run: pio pkg list -g | grep -E 'unihiker|framework-arduinounihiker|xtensa-esp32s3|riscv32-esp'"
