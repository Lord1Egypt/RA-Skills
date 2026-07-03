#!/usr/bin/env bash
set -euo pipefail

SELF_EXTRACTING=false
if [[ "${1:-}" == "--self-extracting" ]]; then
  SELF_EXTRACTING=true
  shift
fi

OUT_FILE="${1:-}"
CORE_DIR="${PLATFORMIO_CORE_DIR:-$HOME/.platformio}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
PIO_BIN="${PIO_BIN:-pio}"

usage() {
  echo "Usage: $0 [--self-extracting] <output.tgz|output.command>"
  echo "Optional: PLATFORMIO_CORE_DIR=/path/to/.platformio PYTHON_BIN=python3 PIO_BIN=pio $0 <output.tgz>"
  exit 1
}

if [[ -z "$OUT_FILE" ]]; then
  usage
fi

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "[ERROR] macOS installer bundles must be prepared on macOS." >&2
  exit 1
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "[ERROR] Python not found: $PYTHON_BIN" >&2
  exit 1
fi

if ! command -v "$PIO_BIN" >/dev/null 2>&1; then
  echo "[ERROR] PlatformIO not found: $PIO_BIN" >&2
  echo "Install PlatformIO Core on the teacher machine, build the K10 probe project once, then rerun." >&2
  exit 1
fi

ARCH="$(uname -m)"
if [[ "$ARCH" != "arm64" ]]; then
  echo "[ERROR] This installer only supports Apple Silicon Macs (arm64)." >&2
  echo "[ERROR] Current machine architecture: $ARCH" >&2
  exit 1
fi

PKG_NAME="K10P-macos-arm64"
STAGE="$(mktemp -d)"
ROOT="$STAGE/$PKG_NAME"
ARCHIVE_FILE="$STAGE/$PKG_NAME.tgz"

cleanup() {
  rm -rf "$STAGE"
}
trap cleanup EXIT

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
  echo "Build a K10 PlatformIO project once on this Mac, then rerun this script." >&2
  exit 1
fi

mkdir -p "$ROOT/.platformio" "$ROOT/wheelhouse" "$ROOT/examples/Blink/src"

copy_path() {
  local src="$1"
  local dest="$2"
  mkdir -p "$(dirname "$dest")"
  if command -v ditto >/dev/null 2>&1; then
    ditto "$src" "$dest"
  else
    cp -R "$src" "$dest"
  fi
}

for path in "${REQUIRED[@]}"; do
  copy_path "$CORE_DIR/$path" "$ROOT/.platformio/$path"
done

echo "[INFO] Downloading PlatformIO Python wheels for offline target setup..."
"$PYTHON_BIN" -m pip download --dest "$ROOT/wheelhouse" platformio
"$PYTHON_BIN" -m pip download --dest "$ROOT/wheelhouse" "typing-extensions>=4.10.0"

if ! find "$ROOT/wheelhouse" -maxdepth 1 -type f -iname 'typing_extensions-*.whl' | grep -q .; then
  echo "[ERROR] Failed to add typing-extensions to the offline wheelhouse." >&2
  echo "This wheel is required when student Macs use Python older than 3.13." >&2
  exit 1
fi

cat > "$ROOT/examples/Blink/platformio.ini" <<'EOF'
[env:unihiker]
platform = https://github.com/DFRobot/platform-unihiker.git
board = unihiker_k10
framework = arduino
build_flags =
    -DARDUINO_USB_CDC_ON_BOOT=1
    -DARDUINO_USB_MODE=1
    -DModel=None
monitor_speed = 115200
EOF

cat > "$ROOT/examples/Blink/src/main.cpp" <<'EOF'
#include <Arduino.h>
#include "unihiker_k10.h"

UNIHIKER_K10 k10;

void setup() {
  Serial.begin(115200);
  k10.begin();
  k10.initScreen(2);
  k10.creatCanvas();
  k10.setScreenBackground(0xFFFFFF);
  k10.canvas->canvasText("UNIHIKER", 1, 0x0000FF);
  k10.canvas->updateCanvas();
}

void loop() {
  delay(1000);
}
EOF

cat > "$ROOT/setup-platformio.command" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-}"

if [[ -z "$PYTHON_BIN" ]]; then
  if [[ -x /usr/bin/python3 ]]; then
    PYTHON_BIN=/usr/bin/python3
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
  else
    echo "[ERROR] python3 not found on this Mac." >&2
    echo "Install Apple's Command Line Tools or Python 3, then rerun this setup." >&2
    exit 1
  fi
fi

echo "[INFO] K10P root: $ROOT"
echo "[INFO] Python: $PYTHON_BIN"

if [[ ! -d "$ROOT/penv" ]]; then
  "$PYTHON_BIN" -m venv "$ROOT/penv"
fi

"$ROOT/penv/bin/python" -m pip install --no-index --find-links "$ROOT/wheelhouse" platformio

export PLATFORMIO_CORE_DIR="$ROOT/.platformio"
"$ROOT/penv/bin/python" -m platformio --version

echo "[OK] K10 PlatformIO is ready."
echo "[INFO] Test build:"
echo "  \"$ROOT/pio\" run -d \"$ROOT/examples/Blink\""
EOF

cat > "$ROOT/pio" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$ROOT/penv/bin/python"

if [[ ! -x "$PY" ]]; then
  echo "[ERROR] PlatformIO environment is not set up yet." >&2
  echo "Run: \"$ROOT/setup-platformio.command\"" >&2
  exit 1
fi

export PLATFORMIO_CORE_DIR="$ROOT/.platformio"
exec "$PY" -m platformio "$@"
EOF

cat > "$ROOT/platformio" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$ROOT/pio" "$@"
EOF

cat > "$ROOT/compile-project" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${1:-}"

if [[ -z "$PROJECT_DIR" ]]; then
  echo "Usage: $0 <PlatformIOProject>" >&2
  exit 1
fi

exec "$ROOT/pio" run -d "$PROJECT_DIR"
EOF

cat > "$ROOT/upload-project" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${1:-}"
PORT="${2:-}"

if [[ -z "$PROJECT_DIR" ]]; then
  echo "Usage: $0 <PlatformIOProject> [serial-port]" >&2
  exit 1
fi

if [[ -n "$PORT" ]]; then
  exec "$ROOT/pio" run -d "$PROJECT_DIR" -t upload --upload-port "$PORT"
else
  exec "$ROOT/pio" run -d "$PROJECT_DIR" -t upload
fi
EOF

cat > "$ROOT/monitor-project" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${1:-}"
PORT="${2:-}"

if [[ -z "$PROJECT_DIR" ]]; then
  echo "Usage: $0 <PlatformIOProject> [serial-port]" >&2
  exit 1
fi

if [[ -n "$PORT" ]]; then
  exec "$ROOT/pio" device monitor -d "$PROJECT_DIR" --port "$PORT"
else
  exec "$ROOT/pio" device monitor -d "$PROJECT_DIR"
fi
EOF

cat > "$ROOT/README-macOS.txt" <<EOF
K10 PlatformIO macOS offline installer
======================================

Prepared for: Apple Silicon macOS (arm64)

1. Copy this $PKG_NAME folder from the USB drive to the Mac, for example:
   ~/K10P

2. Open Terminal and run:
   cd ~/K10P
   ./setup-platformio.command

3. Verify:
   ./pio --version
   ./pio run -d ./examples/Blink

4. Build or upload a student project:
   ./compile-project "/path/to/PlatformIOProject"
   ./upload-project "/path/to/PlatformIOProject" /dev/cu.usbmodemXXXX

Notes:
- Intel Macs are not supported by this installer.
- The scripts use this folder's private .platformio and penv directories.
- If macOS blocks scripts copied from the internet, run:
  xattr -dr com.apple.quarantine ~/K10P
EOF

cat > "$ROOT/metadata.txt" <<EOF
name=$PKG_NAME
created_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
macos_arch=arm64
platformio_core_dir=$CORE_DIR
platformio_version=$("$PIO_BIN" --version)
python=$("$PYTHON_BIN" --version 2>&1)
EOF

chmod +x \
  "$ROOT/setup-platformio.command" \
  "$ROOT/pio" \
  "$ROOT/platformio" \
  "$ROOT/compile-project" \
  "$ROOT/upload-project" \
  "$ROOT/monitor-project"

mkdir -p "$(dirname "$OUT_FILE")"
tar -czf "$ARCHIVE_FILE" -C "$STAGE" "$PKG_NAME"

if [[ "$OUT_FILE" == *.command ]]; then
  SELF_EXTRACTING=true
fi

if [[ "$SELF_EXTRACTING" == true ]]; then
  cat > "$OUT_FILE" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

PKG_NAME="K10P-macos-arm64"
INSTALL_DIR="${K10P_INSTALL_DIR:-$HOME/K10P}"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "[ERROR] This installer must run on macOS." >&2
  exit 1
fi

if [[ "$(uname -m)" != "arm64" ]]; then
  echo "[ERROR] This installer only supports Apple Silicon Macs (arm64)." >&2
  echo "[ERROR] Current machine architecture: $(uname -m)" >&2
  exit 1
fi

ARCHIVE_LINE="$(awk '/^__K10P_ARCHIVE_BELOW__$/ { print NR + 1; exit 0; }' "$0")"
if [[ -z "$ARCHIVE_LINE" ]]; then
  echo "[ERROR] Embedded archive marker not found." >&2
  exit 1
fi

if [[ ! -d "$INSTALL_DIR" ]]; then
  TMP_DIR="$(mktemp -d)"
  cleanup() {
    rm -rf "$TMP_DIR"
  }
  trap cleanup EXIT

  echo "[INFO] Extracting K10 PlatformIO to: $INSTALL_DIR"
  tail -n +"$ARCHIVE_LINE" "$0" | tar -xzf - -C "$TMP_DIR"
  mkdir -p "$(dirname "$INSTALL_DIR")"
  mv "$TMP_DIR/$PKG_NAME" "$INSTALL_DIR"
else
  echo "[INFO] Existing K10 PlatformIO folder found: $INSTALL_DIR"
  echo "[INFO] Reusing it and running setup."
fi

echo "[INFO] Running setup..."
"$INSTALL_DIR/setup-platformio.command"

echo
echo "[OK] K10 PlatformIO is installed at: $INSTALL_DIR"
echo "[INFO] Build test:"
echo "  \"$INSTALL_DIR/pio\" run -d \"$INSTALL_DIR/examples/Blink\""
exit 0

__K10P_ARCHIVE_BELOW__
EOF
  cat "$ARCHIVE_FILE" >> "$OUT_FILE"
  chmod +x "$OUT_FILE"
  echo "[OK] macOS self-extracting installer written: $OUT_FILE"
  du -h "$OUT_FILE" | awk '{print "[INFO] Installer size: " $1}'
  echo "[INFO] Copy this .command file to a USB drive, run it on Apple Silicon Macs, and it will install into ~/K10P."
else
  cp "$ARCHIVE_FILE" "$OUT_FILE"
  echo "[OK] macOS offline installer written: $OUT_FILE"
  du -h "$OUT_FILE" | awk '{print "[INFO] Installer size: " $1}'
  echo "[INFO] Copy this .tgz to a USB drive, extract it on Apple Silicon Macs, then run setup-platformio.command."
fi
