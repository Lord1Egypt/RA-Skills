#!/usr/bin/env bash
set -euo pipefail

# x-twitter-browser skill setup
# Installs playwright and Chromium. Safe to run multiple times; skips if already installed.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SKILL_ROOT"

echo "Setting up x-twitter-browser skill..."
echo ""

echo "Installing playwright (Python package)..."
python3 -m pip install --user playwright
echo "✓ Playwright package installed."

echo ""
if [[ "$(uname)" == "Darwin" ]] && [[ -d "/Applications/Google Chrome.app" ]]; then
  echo "Chrome detected. Skipping Chromium install (will use system Chrome)."
else
  echo "Installing Chromium browser (first time may take 2-5 min, ~150MB)..."
  python3 -m playwright install chromium
  echo "✓ Chromium browser installed."
fi

echo ""
echo "Setup complete. If Chromium fails to start later, run:"
echo "  python3 -m playwright install-deps chromium"
echo ""
