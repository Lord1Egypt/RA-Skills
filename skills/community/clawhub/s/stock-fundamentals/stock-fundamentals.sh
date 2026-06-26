#!/bin/bash
# Stock Fundamentals - Analyze stock fundamentals from Yahoo Finance

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
uv run "$SCRIPT_DIR/src/main.py" "$@"
