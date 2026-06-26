#!/bin/bash
# ============================================================
# Singularity EvoMap Heartbeat - Linux/macOS Shell Wrapper
# ============================================================
# Just runs evomap-heartbeat.js with Node.js
# Requirements: Node.js 18+
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js not found. Please install Node.js 18+"
    exit 1
fi

cd "$SCRIPT_DIR"
exec node evomap-heartbeat.js
