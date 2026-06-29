#!/usr/bin/env bash
set -euo pipefail

OUT_FILE="${1:-}"
CORE_DIR="${PLATFORMIO_CORE_DIR:-$HOME/.platformio}"

usage() {
  echo "Usage: $0 <output.tgz>"
  echo "Optional: PLATFORMIO_CORE_DIR=/path/to/.platformio $0 <output.tgz>"
  exit 1
}

if [[ -z "$OUT_FILE" ]]; then
  usage
fi

REQUIRED=(
  "platforms/unihiker"
  "packages/framework-arduinounihiker"
  "packages/toolchain-riscv32-esp"
  "packages/toolchain-xtensa-esp32"
  "packages/toolchain-xtensa-esp32s3"
  "packages/tool-esptoolpy"
  "packages/tool-scons"
  "packages/tool-mkfatfs"
  "packages/tool-mklittlefs"
  "packages/tool-mkspiffs"
)

missing=()
for path in "${REQUIRED[@]}"; do
  if [[ ! -e "$CORE_DIR/$path" ]]; then
    missing+=("$path")
  fi
done

if (( ${#missing[@]} > 0 )); then
  echo "[ERROR] Missing PlatformIO support files in $CORE_DIR:" >&2
  printf '  - %s\n' "${missing[@]}" >&2
  echo "Build a K10 PlatformIO project once, then rerun this script." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT_FILE")"
tar -czf "$OUT_FILE" -C "$CORE_DIR" "${REQUIRED[@]}"

echo "[OK] Offline bundle written: $OUT_FILE"
du -h "$OUT_FILE" | awk '{print "[INFO] Bundle size: " $1}'
echo "[INFO] Install with: install-offline-bundle.sh \"$OUT_FILE\""
