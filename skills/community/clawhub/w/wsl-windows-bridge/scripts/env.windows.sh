#!/bin/bash
# === wsl-windows-bridge environment configuration ===
# Load this file before using any win-* commands

# === Paths ===
export WIN_BIN="/home/traceback/.openclaw/bin"
export PATH="$WIN_BIN:$PATH"

export WIN_ROOT="/mnt/d"
export WIN_ANACONDA="$WIN_ROOT/app/anaconda"
export WIN_SCRIPTS="$WIN_ROOT/app/scripts"
export WIN_PROJECT="$WIN_ROOT/app/project"

export WIN_PYTHON="$WIN_ANACONDA/python.exe"
export WIN_PS="/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
export WIN_CMD="/mnt/c/Windows/System32/cmd.exe"

# === PATH ===
export PATH="$WIN_BIN:$PATH"

# === Path conversion ===
winpath() {
    wslpath -w "$1" 2>/dev/null
}

wslpath_win() {
    wslpath -u "$1" 2>/dev/null
}

# === Verification ===
win-python-check() {
    if [ -f "$WIN_PYTHON" ]; then
        echo "OK: $WIN_PYTHON"
        "$WIN_PYTHON" --version
    else
        echo "ERROR: Windows Python not found at $WIN_PYTHON"
        return 1
    fi
}

win-ps-check() {
    if [ -f "$WIN_PS" ]; then
        echo "OK: PowerShell available"
    else
        echo "ERROR: PowerShell not found at $WIN_PS"
        return 1
    fi
}

win-check-all() {
    echo "=== Windows Environment Check ==="
    echo "WIN_ROOT: $WIN_ROOT"
    echo "WIN_ANACONDA: $WIN_ANACONDA"
    echo "WIN_PYTHON: $WIN_PYTHON"
    echo "WIN_PS: $WIN_PS"
    echo "WIN_CMD: $WIN_CMD"
    echo ""
    echo "=== Tool Check ==="
    win-python-check
    win-ps-check
    echo ""
    echo "win-* commands in PATH:"
    which win-python win-ps win-cmd win-copy win-run-py win-path 2>/dev/null || echo "  (not found)"
}
