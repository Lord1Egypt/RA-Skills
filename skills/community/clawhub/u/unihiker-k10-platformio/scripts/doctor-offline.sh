#!/usr/bin/env bash
set -euo pipefail

CORE_DIR="${PLATFORMIO_CORE_DIR:-$HOME/.platformio}"

REQUIRED=(
  "platforms/unihiker"
  "packages/framework-arduinounihiker"
  "packages/toolchain-riscv32-esp"
  "packages/toolchain-xtensa-esp32s3"
  "packages/tool-esptoolpy"
  "packages/tool-scons"
)

OPTIONAL=(
  "packages/toolchain-xtensa-esp32"
  "packages/tool-mkfatfs"
  "packages/tool-mklittlefs"
  "packages/tool-mkspiffs"
)

echo "[INFO] PlatformIO core dir: $CORE_DIR"

ok=true
for path in "${REQUIRED[@]}"; do
  if [[ -e "$CORE_DIR/$path" ]]; then
    size=$(du -sh "$CORE_DIR/$path" 2>/dev/null | awk '{print $1}')
    echo "[OK] $path present ($size)"
  else
    echo "[MISSING] $path"
    ok=false
  fi
done

for path in "${OPTIONAL[@]}"; do
  if [[ -e "$CORE_DIR/$path" ]]; then
    size=$(du -sh "$CORE_DIR/$path" 2>/dev/null | awk '{print $1}')
    echo "[OK] optional $path present ($size)"
  else
    echo "[WARN] optional $path missing"
  fi
done

if command -v pio >/dev/null 2>&1; then
  echo "[INFO] pio: $(pio --version)"
  if pio pkg list -g 2>/dev/null | grep -q 'framework-arduinounihiker'; then
    echo "[OK] pio can list framework-arduinounihiker"
  else
    echo "[WARN] pio did not list framework-arduinounihiker"
    echo "[WARN] Directory checks are authoritative for offline bundle installation."
  fi
else
  echo "[WARN] pio not found in PATH; package files can still be installed."
fi

if [[ "$ok" == true ]]; then
  echo "[OK] PlatformIO K10 offline support looks ready."
else
  exit 1
fi
