#!/usr/bin/env bash
# Deprecated alias: use install.sh (CUDA/CPU/macOS auto-detect, venv check).
exec "$(cd "$(dirname "$0")" && pwd)/install.sh" "$@"
