#!/usr/bin/env bash
set -euo pipefail

BUNDLE="${1:-}"
ARDUINO_DATA_DIR="${ARDUINO_DATA_DIR:-}"

usage() {
  cat <<'EOF'
Usage: install-offline-bundle.sh <k10-arduino-bundle.tgz>

Environment:
  ARDUINO_DATA_DIR=/path/to/Arduino15  Override Arduino data directory.
EOF
  exit 1
}

detect_arduino_data_dir() {
  if [[ -n "$ARDUINO_DATA_DIR" ]]; then
    echo "$ARDUINO_DATA_DIR"
    return
  fi

  case "$(uname -s)" in
    Darwin*) echo "$HOME/Library/Arduino15" ;;
    Linux*) echo "$HOME/.arduino15" ;;
    CYGWIN*|MINGW*|MSYS*) echo "${LOCALAPPDATA:-$HOME/AppData/Local}/Arduino15" ;;
    *) echo "$HOME/.arduino15" ;;
  esac
}

if [[ -z "$BUNDLE" || ! -f "$BUNDLE" ]]; then
  usage
fi

DATA_DIR="$(detect_arduino_data_dir)"
mkdir -p "$DATA_DIR"
tar -xzf "$BUNDLE" -C "$DATA_DIR"

echo "[OK] Installed K10 Arduino support files into: $DATA_DIR"
echo "[INFO] Verify with: doctor-offline.sh"
echo "[INFO] If arduino-cli cannot list K10, add the K10 and ESP32 board manager URLs from SKILL.md."
