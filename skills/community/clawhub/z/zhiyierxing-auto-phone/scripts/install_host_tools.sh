#!/usr/bin/env bash
set -euo pipefail

DEVICE_TYPE="${1:-android}"
OS_NAME="$(uname -s 2>/dev/null || echo unknown)"

install_adb() {
  if command -v adb >/dev/null 2>&1; then
    echo "[ok] adb is already installed"
    return 0
  fi

  case "$OS_NAME" in
    Darwin)
      if command -v brew >/dev/null 2>&1; then
        echo "[step] installing Android platform tools via Homebrew"
        brew install android-platform-tools
      else
        echo "[error] Homebrew is not installed or not on PATH"
        echo "[next] install Homebrew first, or install Android platform-tools manually"
        return 1
      fi
      ;;
    Linux)
      echo "[error] automatic adb installation for Linux is not implemented yet"
      echo "[next] install adb using your distro package manager, then continue"
      return 1
      ;;
    MINGW*|MSYS*|CYGWIN*)
      if command -v winget >/dev/null 2>&1; then
        echo "[step] installing Android platform tools via winget"
        winget install --id Google.PlatformTools --accept-package-agreements --accept-source-agreements
      else
        echo "[error] winget is not available"
        echo "[next] install Android SDK Platform-Tools manually or install winget, then continue"
        return 1
      fi
      ;;
    *)
      echo "[error] unsupported or unknown host OS: $OS_NAME"
      echo "[next] install Android platform-tools manually, then continue"
      return 1
      ;;
  esac
}

case "$DEVICE_TYPE" in
  android)
    install_adb
    ;;
  harmonyos)
    if command -v hdc >/dev/null 2>&1; then
      echo "[ok] hdc is already installed"
    else
      echo "[error] automatic hdc installation is not implemented yet"
      echo "[next] install HarmonyOS SDK tools manually, then continue"
      exit 1
    fi
    ;;
  iphone)
    echo "[info] iPhone path does not use adb/hdc auto-install here"
    ;;
  *)
    echo "[error] unknown device type: $DEVICE_TYPE"
    exit 1
    ;;
esac

echo "[done] host tool install step finished"
