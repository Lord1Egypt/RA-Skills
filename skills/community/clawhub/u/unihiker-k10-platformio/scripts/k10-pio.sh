#!/usr/bin/env bash
set -euo pipefail

COMMAND="${1:-}"
PROJECT_DIR="${2:-.}"
PORT="${3:-}"

usage() {
  cat <<'EOF'
Usage:
  k10-pio.sh doctor [project_dir]
  k10-pio.sh ports
  k10-pio.sh build [project_dir]
  k10-pio.sh upload [project_dir] [port]
  k10-pio.sh monitor [project_dir] [port]
EOF
  exit 1
}

need_pio() {
  if ! command -v pio >/dev/null 2>&1; then
    echo "[ERROR] pio not found. Install PlatformIO Core first." >&2
    echo "See: https://docs.platformio.org/en/latest/core/installation/methods/installer-script.html" >&2
    exit 1
  fi
}

case "$COMMAND" in
  doctor)
    need_pio
    echo "[INFO] PlatformIO:"
    pio --version
    echo
    echo "[INFO] esptool Python dependency check:"
    python3 - <<'PY' || true
try:
    import intelhex
    print("[OK] intelhex module available to python3")
except Exception as exc:
    print("[WARN] python3 cannot import intelhex:", exc)
    print("[WARN] If pio build fails inside tool-esptoolpy, repair/reinstall PlatformIO Core.")
PY
    echo
    echo "[INFO] Core directory:"
    pio system info | sed -n '/PlatformIO Core Directory/,+1p' || true
    echo
    echo "[INFO] K10 project config:"
    if [[ -f "$PROJECT_DIR/platformio.ini" ]]; then
      grep -E '^(platform|board|framework|[[:space:]]*-DARDUINO_USB|[[:space:]]*-DModel)' "$PROJECT_DIR/platformio.ini" || true
    else
      echo "[WARN] No platformio.ini found in $PROJECT_DIR"
    fi
    ;;
  ports)
    need_pio
    pio device list
    ;;
  build)
    need_pio
    pio run -d "$PROJECT_DIR"
    ;;
  upload)
    need_pio
    if [[ -n "$PORT" ]]; then
      pio run -d "$PROJECT_DIR" -t upload --upload-port "$PORT"
    else
      pio run -d "$PROJECT_DIR" -t upload
    fi
    ;;
  monitor)
    need_pio
    if [[ -n "$PORT" ]]; then
      pio device monitor -d "$PROJECT_DIR" --port "$PORT"
    else
      pio device monitor -d "$PROJECT_DIR"
    fi
    ;;
  *)
    usage
    ;;
esac
