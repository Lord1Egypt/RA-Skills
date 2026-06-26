#!/usr/bin/env bash
# TradeMemory Protocol — Install Script
# Installs tradememory-protocol and all dependencies.

set -euo pipefail

echo "=================================="
echo "  TradeMemory Protocol Installer"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] python3 not found. Install Python 3.10+ first."
    echo "        https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "[OK] Python ${PYTHON_VERSION} found"

# Check pip
if ! python3 -m pip --version &>/dev/null; then
    echo "[ERROR] pip not found. Install pip first."
    exit 1
fi
echo "[OK] pip available"

# Install tradememory-protocol from PyPI
echo ""
echo "Installing tradememory-protocol..."
python3 -m pip install --upgrade tradememory-protocol

# Verify installation
echo ""
python3 -c "import tradememory; print('[OK] tradememory-protocol installed successfully')"

echo ""
echo "=================================="
echo "  Installation Complete"
echo "=================================="
echo ""
echo "Next steps:"
echo "  1. Run the demo:  python3 demo.py"
echo "  2. For MT5 sync:  bash .skills/tradememory/scripts/setup_mt5.sh"
echo "  3. Start server:  python3 -m src.tradememory.server"
echo ""
