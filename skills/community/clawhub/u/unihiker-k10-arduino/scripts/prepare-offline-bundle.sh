#!/usr/bin/env bash
set -euo pipefail

OUT_FILE=""
ARDUINO_DATA_DIR="${ARDUINO_DATA_DIR:-}"
INCLUDE_STAGING=false

usage() {
  cat <<'EOF'
Usage: prepare-offline-bundle.sh <output.tgz> [--include-staging]

Environment:
  ARDUINO_DATA_DIR=/path/to/Arduino15  Override Arduino data directory.

The bundle includes installed K10/ESP32 board packages and package index files.
Use --include-staging only when you also want raw download caches; it can add many GB.
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --include-staging) INCLUDE_STAGING=true; shift ;;
    -h|--help) usage ;;
    *)
      if [[ -z "$OUT_FILE" ]]; then
        OUT_FILE="$1"
        shift
      else
        usage
      fi
      ;;
  esac
done

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

if [[ -z "$OUT_FILE" ]]; then
  usage
fi

DATA_DIR="$(detect_arduino_data_dir)"
REQUIRED=(
  "packages/UNIHIKER"
  "packages/esp32"
)

missing=()
for path in "${REQUIRED[@]}"; do
  if [[ ! -e "$DATA_DIR/$path" ]]; then
    missing+=("$path")
  fi
done

if (( ${#missing[@]} > 0 )); then
  echo "[ERROR] Missing Arduino support files in $DATA_DIR:" >&2
  printf '  - %s\n' "${missing[@]}" >&2
  echo "Install the K10 BSP and ESP32 core on the teacher machine, then rerun." >&2
  exit 1
fi

entries=("${REQUIRED[@]}")
while IFS= read -r file; do
  rel="${file#$DATA_DIR/}"
  entries+=("$rel")
done < <(find "$DATA_DIR" -maxdepth 1 -type f \( -name 'package*.json' -o -name 'library_index.json' \) | sort)

if [[ "$INCLUDE_STAGING" == true && -d "$DATA_DIR/staging" ]]; then
  entries+=("staging")
fi

mkdir -p "$(dirname "$OUT_FILE")"
tar -czf "$OUT_FILE" -C "$DATA_DIR" "${entries[@]}"

echo "[OK] Arduino offline bundle written: $OUT_FILE"
du -h "$OUT_FILE" | awk '{print "[INFO] Bundle size: " $1}'
echo "[INFO] Source data dir: $DATA_DIR"
echo "[INFO] Install with: install-offline-bundle.sh \"$OUT_FILE\""
