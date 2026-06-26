#!/bin/bash
# wsl-windows-bridge installation script
set -e

echo "=== wsl-windows-bridge setup ==="
echo ""

# Auto-detect Windows root
DETECTED_WIN_ROOT=""
for candidate in /mnt/d /mnt/c /mnt/e; do
    if [ -d "$candidate" ] && [ -f "$candidate/app/anaconda/python.exe" ]; then
        DETECTED_WIN_ROOT="$candidate"
        break
    fi
done

if [ -z "$DETECTED_WIN_ROOT" ]; then
    echo "WARNING: Could not auto-detect Windows Python. Please enter path manually."
    echo ""
    read -p "Windows root (e.g. D:\ or /mnt/d): " WIN_ROOT_INPUT
    WIN_ROOT="$WIN_ROOT_INPUT"
else
    echo "Detected Windows root: $DETECTED_WIN_ROOT"
    WIN_ROOT="$DETECTED_WIN_ROOT"
    read -p "Python path [default: $WIN_ROOT/app/anaconda/python.exe]: " PYTHON_INPUT
    PYTHON_INPUT="${PYTHON_INPUT:-$WIN_ROOT/app/anaconda/python.exe}"
fi

if [[ "$PYTHON_INPUT" == /mnt/* ]]; then
    PYTHON_PATH="$PYTHON_INPUT"
elif [[ "$PYTHON_INPUT" == /* ]]; then
    PYTHON_PATH=$(wslpath -w "$PYTHON_INPUT" 2>/dev/null || echo "$PYTHON_INPUT")
else
    PYTHON_PATH="$PYTHON_INPUT"
fi

echo ""
echo "Installing..."

ACTUAL_HOME=$(eval echo ~)
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_BIN="$ACTUAL_HOME/.openclaw/bin"
OPENCLAW_ENV="$ACTUAL_HOME/.openclaw/env.windows.sh"

# 1. Create directories
mkdir -p "$OPENCLAW_BIN"

# 2. Copy wrappers and replace path placeholder
for script in "$SCRIPTS_DIR"/win-*; do
    [ -f "$script" ] || continue
    fname=$(basename "$script")
    sed "s|/home/traceback|$ACTUAL_HOME|g" "$script" > "$OPENCLAW_BIN/$fname"
    chmod +x "$OPENCLAW_BIN/$fname"
done

# 3. Generate env.windows.sh
cat > "$OPENCLAW_ENV" << ENVEOF
#!/bin/bash
# === wsl-windows-bridge environment ===
# Auto-generated at $(date -u +%Y-%m-%dT%H:%M:%SZ)

export WIN_BIN="\$HOME/.openclaw/bin"
export PATH="\$WIN_BIN:\$PATH"

export WIN_ROOT="$WIN_ROOT"
export WIN_ANACONDA="$WIN_ROOT/app/anaconda"
export WIN_SCRIPTS="$WIN_ROOT/app/scripts"
export WIN_PROJECT="$WIN_ROOT/app/project"

export WIN_PYTHON="$PYTHON_PATH"
export WIN_PS="/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
export WIN_CMD="/mnt/c/Windows/System32/cmd.exe"

winpath() { wslpath -w "\$1" 2>/dev/null; }
wslpath_win() { wslpath -u "\$1" 2>/dev/null; }

win-python-check() {
    if [ -f "$PYTHON_PATH" ]; then
        echo "OK: $PYTHON_PATH"
        "$PYTHON_PATH" --version
    else
        echo "ERROR: Python not found at $PYTHON_PATH"
        return 1
    fi
}

win-ps-check() {
    if [ -f "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe" ]; then
        echo "OK: PowerShell available"
    else
        echo "ERROR: PowerShell not found"
        return 1
    fi
}

win-check-all() {
    echo "=== Windows Environment Check ==="
    echo "WIN_ROOT: $WIN_ROOT"
    echo "WIN_ANACONDA: $WIN_ANACONDA"
    echo "WIN_PYTHON: $PYTHON_PATH"
    echo "WIN_PS: /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
    echo ""
    echo "=== Tool Check ==="
    win-python-check
    win-ps-check
    echo ""
    echo "win-* commands in PATH:"
    which win-python win-ps win-cmd win-copy win-run-py win-path 2>/dev/null || echo "  (not found)"
}
ENVEOF

chmod +x "$OPENCLAW_ENV"

# 4. Verify
echo ""
echo "Setup complete. Verifying..."
echo ""
source "$OPENCLAW_ENV" 2>/dev/null

echo "=== Quick Test ==="
"$OPENCLAW_BIN/win-python" -c "import sys; print('Python:', sys.version.split()[0])" 2>/dev/null && echo "OK win-python" || echo "FAIL win-python"
"$OPENCLAW_BIN/win-ps" "Write-Host 'PowerShell OK'" 2>/dev/null && echo "OK win-ps" || echo "FAIL win-ps"
"$OPENCLAW_BIN/win-path" /mnt/d 2>/dev/null && echo "OK win-path" || echo "FAIL win-path"

echo ""
echo "=== Install Info ==="
echo "Wrappers: $OPENCLAW_BIN/"
echo "Config: $OPENCLAW_ENV"
echo "Python: $PYTHON_PATH"
echo ""
echo "Before use, run: source $OPENCLAW_ENV"
