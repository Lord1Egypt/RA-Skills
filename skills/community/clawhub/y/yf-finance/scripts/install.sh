#!/usr/bin/env bash
# Verify yf-cli is installed; install via uv if missing.
set -euo pipefail

if ! command -v yf &>/dev/null; then
  echo "yf-cli not found — installing via uv..."
  uv tool install yf-cli
else
  echo "yf-cli $(yf --version) is ready."
fi
