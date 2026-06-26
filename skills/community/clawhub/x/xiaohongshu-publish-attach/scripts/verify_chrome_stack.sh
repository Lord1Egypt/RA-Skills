#!/usr/bin/env bash
# Check Chrome + chromedriver versions match (required for Selenium attach).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=load_chromedriver_env.sh
source "$SCRIPT_DIR/load_chromedriver_env.sh"
load_chromedriver_env "$SCRIPT_DIR"

CHROME_BIN=""
for candidate in google-chrome-stable google-chrome chromium-browser chromium; do
  if command -v "$candidate" >/dev/null 2>&1; then
    CHROME_BIN="$candidate"
    break
  fi
done

if [[ -z "$CHROME_BIN" ]]; then
  echo "FAIL: Chrome not found on PATH." >&2
  exit 1
fi

CHROME_VER=$("$CHROME_BIN" --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | head -1)
echo "Chrome ($CHROME_BIN): $CHROME_VER"

CD="${CHROMEDRIVER_PATH:-}"
if [[ -z "$CD" ]]; then
  CD=$(command -v chromedriver 2>/dev/null || true)
fi
if [[ -z "$CD" && -x /usr/local/bin/chromedriver ]]; then
  CD=/usr/local/bin/chromedriver
fi
if [[ -z "$CD" && -x "${HOME}/.local/bin/chromedriver" ]]; then
  CD="${HOME}/.local/bin/chromedriver"
fi

if [[ -z "$CD" ]]; then
  echo "FAIL: chromedriver not found. Set CHROMEDRIVER_PATH or run install_chromedriver.sh" >&2
  exit 1
fi

echo "chromedriver: $CD"
DRV_RAW=$("$CD" --version 2>&1 || true)
echo "  $DRV_RAW"
DRV_VER=$(echo "$DRV_RAW" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | head -1)

if [[ -z "$DRV_VER" ]]; then
  echo "WARN: cannot parse chromedriver version string." >&2
  exit 1
fi

if [[ "$CHROME_VER" == "$DRV_VER" ]]; then
  echo "OK: versions match ($CHROME_VER)."
  exit 0
fi

# Same major.minor.build is often enough for attach mode
CHROME_SHORT=$(echo "$CHROME_VER" | cut -d. -f1-3)
DRV_SHORT=$(echo "$DRV_VER" | cut -d. -f1-3)
if [[ "$CHROME_SHORT" == "$DRV_SHORT" ]]; then
  echo "OK: versions close enough ($CHROME_VER vs $DRV_VER)."
  exit 0
fi

echo "FAIL: version mismatch." >&2
echo "  Chrome:       $CHROME_VER" >&2
echo "  chromedriver: $DRV_VER" >&2
echo "Re-install driver: bash $(dirname "$0")/install_chromedriver.sh" >&2
echo "Or manual (example for 148.0.7778.215):" >&2
echo "  wget https://storage.googleapis.com/chrome-for-testing-public/148.0.7778.215/linux64/chromedriver-linux64.zip" >&2
exit 1
