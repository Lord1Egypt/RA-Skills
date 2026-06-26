#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
REQ_FILE="$SCRIPT_DIR/requirements.txt"
SRC_FILE="$SCRIPT_DIR/subtitle_overlay.swift"
BIN_FILE="$SCRIPT_DIR/subtitle_overlay_app"
MIC_SRC_FILE="$SCRIPT_DIR/mic_pcm_stream.swift"
MIC_BIN_FILE="$SCRIPT_DIR/mic_pcm_stream"
APP_DIR="$SCRIPT_DIR/AudioClawOverlay.app"
APP_CONTENTS_DIR="$APP_DIR/Contents"
APP_MACOS_DIR="$APP_CONTENTS_DIR/MacOS"
APP_BIN_FILE="$APP_MACOS_DIR/subtitle_overlay_app"
APP_MIC_BIN_FILE="$APP_MACOS_DIR/mic_pcm_stream"
APP_RESOURCES_DIR="$APP_CONTENTS_DIR/Resources"
PLIST_FILE="$APP_CONTENTS_DIR/Info.plist"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
REQ_HASH="$(shasum -a 256 "$REQ_FILE" | awk '{print $1}')"
STAMP_FILE="$VENV_DIR/.requirements.sha256"
INSTALLED_HASH="$(cat "$STAMP_FILE" 2>/dev/null || true)"
if [ "$REQ_HASH" != "$INSTALLED_HASH" ]; then
  python -m pip install --upgrade pip >/dev/null
  python -m pip install -r "$REQ_FILE" >/dev/null
  printf '%s\n' "$REQ_HASH" >"$STAMP_FILE"
fi

unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy

pkill -f "$BIN_FILE" >/dev/null 2>&1 || true
pkill -f "$APP_BIN_FILE" >/dev/null 2>&1 || true
pkill -f "$SCRIPT_DIR/runner.py" >/dev/null 2>&1 || true
pkill -f "$SCRIPT_DIR/organize_senseaudio_transcript.py" >/dev/null 2>&1 || true
pkill -f "$SCRIPT_DIR/organize_clipboard_text.py" >/dev/null 2>&1 || true
pkill -f "audioclaw-darwin-.* agent --session realtime_interpreter_" >/dev/null 2>&1 || true
pkill -f "$SCRIPT_DIR/mic_pcm_stream" >/dev/null 2>&1 || true
pkill -f "$APP_MIC_BIN_FILE" >/dev/null 2>&1 || true
sleep 1
pkill -9 -f "$BIN_FILE" >/dev/null 2>&1 || true
pkill -9 -f "$APP_BIN_FILE" >/dev/null 2>&1 || true
pkill -9 -f "$SCRIPT_DIR/runner.py" >/dev/null 2>&1 || true
pkill -9 -f "$SCRIPT_DIR/organize_senseaudio_transcript.py" >/dev/null 2>&1 || true
pkill -9 -f "$SCRIPT_DIR/organize_clipboard_text.py" >/dev/null 2>&1 || true
pkill -9 -f "audioclaw-darwin-.* agent --session realtime_interpreter_" >/dev/null 2>&1 || true
pkill -9 -f "$SCRIPT_DIR/mic_pcm_stream" >/dev/null 2>&1 || true
pkill -9 -f "$APP_MIC_BIN_FILE" >/dev/null 2>&1 || true

bash "$SCRIPT_DIR/enter_subtitle_mode.sh" >/dev/null

if [ ! -x "$BIN_FILE" ] || [ "$SRC_FILE" -nt "$BIN_FILE" ]; then
  swiftc -O "$SRC_FILE" -o "$BIN_FILE" -framework AppKit -framework Foundation -framework QuartzCore -framework AVFoundation -framework CoreAudio
fi

if [ ! -x "$MIC_BIN_FILE" ] || [ "$MIC_SRC_FILE" -nt "$MIC_BIN_FILE" ]; then
  swiftc -O "$MIC_SRC_FILE" -o "$MIC_BIN_FILE" -framework AVFoundation
fi

mkdir -p "$APP_MACOS_DIR" "$APP_RESOURCES_DIR"
cat >"$PLIST_FILE" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key>
  <string>subtitle_overlay_app</string>
  <key>CFBundleIdentifier</key>
  <string>local.audioclaw.subtitle-overlay</string>
  <key>CFBundleName</key>
  <string>AudioClaw Overlay</string>
  <key>CFBundleDisplayName</key>
  <string>AudioClaw Overlay</string>
  <key>CFBundlePackageType</key>
  <string>APPL</string>
  <key>CFBundleVersion</key>
  <string>1</string>
  <key>CFBundleShortVersionString</key>
  <string>1.0</string>
  <key>LSMinimumSystemVersion</key>
  <string>13.0</string>
  <key>NSMicrophoneUsageDescription</key>
  <string>AudioClaw 需要访问音频输入以采集系统回环和实时语音字幕。</string>
</dict>
</plist>
PLIST

cp "$BIN_FILE" "$APP_BIN_FILE"
cp "$MIC_BIN_FILE" "$APP_MIC_BIN_FILE"
chmod +x "$APP_BIN_FILE"
chmod +x "$APP_MIC_BIN_FILE"
if command -v xattr >/dev/null 2>&1; then
  xattr -cr "$APP_DIR" >/dev/null 2>&1 || true
fi

open "$APP_DIR" --args "$@"
