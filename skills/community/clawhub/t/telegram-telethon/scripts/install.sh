#!/bin/bash
set -e

echo "=== tgctl-telethon installer ==="

# Check Python 3
PYTHON=""
for py in /opt/homebrew/bin/python3 python3 python3.12 python3.11 python3.10; do
    if command -v "$py" &>/dev/null; then
        ver=$("$py" -c "import sys; print(sys.version_info[:2] >= (3,9))" 2>/dev/null)
        if [ "$ver" = "True" ]; then
            PYTHON="$py"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "error: Python 3.9+ not found."
    exit 1
fi

echo "Using Python: $PYTHON ($($PYTHON --version))"

# Create venv
VENV_DIR="$HOME/.tgctl-telethon-venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv "$VENV_DIR"
fi

# Install telethon in venv
echo "Installing telethon..."
"$VENV_DIR/bin/pip" install --quiet --upgrade telethon

# Install tgctl script
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TGCTL_SRC="$SCRIPT_DIR/tgctl"

if [ ! -f "$TGCTL_SRC" ]; then
    echo "error: tgctl script not found at $TGCTL_SRC"
    exit 1
fi

# Create wrapper that uses venv python
TGCTL_DST="$INSTALL_DIR/tgctl-telethon"
cat > "$TGCTL_DST" << WRAPPER
#!/bin/bash
exec "$VENV_DIR/bin/python3" "$TGCTL_SRC" "\$@"
WRAPPER

chmod +x "$TGCTL_DST"

echo ""
echo "✅ Installed: $TGCTL_DST"
echo "   venv: $VENV_DIR"
echo "   script: $TGCTL_SRC"
echo ""
echo "Make sure $INSTALL_DIR is in your PATH:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "Usage:"
echo "  export TELEGRAM_API_ID=your_id"
echo "  export TELEGRAM_API_HASH=your_hash"
echo "  tgctl-telethon login"
echo "  tgctl-telethon me"
