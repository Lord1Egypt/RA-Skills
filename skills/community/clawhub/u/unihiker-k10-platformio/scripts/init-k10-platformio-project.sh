#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-}"

usage() {
  echo "Usage: $0 <project_dir>"
  exit 1
}

if [[ -z "$PROJECT_DIR" ]]; then
  usage
fi

mkdir -p "$PROJECT_DIR/src" "$PROJECT_DIR/lib" "$PROJECT_DIR/data"

if [[ ! -f "$PROJECT_DIR/platformio.ini" ]]; then
  cat > "$PROJECT_DIR/platformio.ini" <<'EOF'
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
fi

if [[ ! -f "$PROJECT_DIR/src/main.cpp" ]]; then
  cat > "$PROJECT_DIR/src/main.cpp" <<'EOF'
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
fi

echo "[OK] K10 PlatformIO project ready: $PROJECT_DIR"
echo "Next: pio run -d \"$PROJECT_DIR\""
