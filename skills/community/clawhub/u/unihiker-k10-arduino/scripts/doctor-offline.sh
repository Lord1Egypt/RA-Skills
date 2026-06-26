#!/usr/bin/env bash
set -euo pipefail

ARDUINO_DATA_DIR="${ARDUINO_DATA_DIR:-}"

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

DATA_DIR="$(detect_arduino_data_dir)"
echo "[INFO] Arduino data dir: $DATA_DIR"

ok=true
for path in "packages/UNIHIKER" "packages/esp32"; do
  if [[ -e "$DATA_DIR/$path" ]]; then
    size=$(du -sh "$DATA_DIR/$path" 2>/dev/null | awk '{print $1}')
    echo "[OK] $path present ($size)"
  else
    echo "[MISSING] $path"
    ok=false
  fi
done

if command -v arduino-cli >/dev/null 2>&1; then
  echo "[INFO] arduino-cli: $(arduino-cli version 2>/dev/null | head -1)"
  if arduino-cli board listall 2>/dev/null | grep -qi 'UNIHIKER:esp32:k10'; then
    echo "[OK] arduino-cli can see UNIHIKER:esp32:k10"
  else
    echo "[WARN] arduino-cli did not list UNIHIKER:esp32:k10"
    echo "[WARN] Check board manager URLs and package index files."
    ok=false
  fi
else
  echo "[WARN] arduino-cli not found in PATH; package files can still be installed."
fi

if [[ "$ok" == true ]]; then
  echo "[OK] Arduino K10 offline support looks ready."
else
  exit 1
fi
