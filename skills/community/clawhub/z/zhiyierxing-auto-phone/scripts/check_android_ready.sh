#!/usr/bin/env bash
set -euo pipefail

if ! command -v adb >/dev/null 2>&1; then
  echo "[error] adb not found. Install Android platform-tools first."
  exit 1
fi

echo "[step] checking adb devices"
adb devices || true

DEVICES=$(adb devices | awk 'NR>1 && $2=="device" {print $1}')
if [ -z "$DEVICES" ]; then
  echo "[error] no authorized Android device found"
  echo "Fixes:"
  echo "  1. Use a data-capable USB cable"
  echo "  2. Enable Developer Options and USB debugging"
  echo "  3. Accept the USB debugging authorization popup on the phone"
  echo "  4. Retry: adb kill-server && adb start-server && adb devices"
  exit 1
fi

echo "[ok] device(s):"
echo "$DEVICES"

echo "[step] checking ADB Keyboard availability"
IME_LIST=$(adb shell ime list -a 2>/dev/null || true)
if echo "$IME_LIST" | grep -q 'com.android.adbkeyboard/.AdbIME'; then
  echo "[ok] ADB Keyboard is installed or discoverable"
else
  echo "[warn] ADB Keyboard not found in ime list"
  echo "Install ADB Keyboard APK, then run:"
  echo "  adb shell ime enable com.android.adbkeyboard/.AdbIME"
  echo "  adb shell ime set com.android.adbkeyboard/.AdbIME"
fi

echo "[done] android readiness check finished"
