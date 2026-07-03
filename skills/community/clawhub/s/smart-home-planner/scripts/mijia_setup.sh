#!/bin/bash
# Mijia API Setup Script
# Usage: bash mijia_setup.sh

set -e

echo "=== Mijia API Setup ==="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $PYTHON_VERSION"

# Check pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "Error: pip not found. Please install pip first."
    exit 1
fi

# Install mijiaAPI
echo ""
echo "Installing mijiaAPI..."
pip3 install mijiaAPI 2>/dev/null || pip install mijiaAPI

# Verify installation
echo ""
echo "Verifying installation..."
python3 -c "from mijiaAPI import mijiaAPI; print('mijiaAPI installed successfully')" || {
    echo "Error: Installation verification failed"
    exit 1
}

# Create config directory
CONFIG_DIR="$HOME/.config/mijia-api"
mkdir -p "$CONFIG_DIR"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Run: python3 -c \"from mijiaAPI import mijiaAPI; api = mijiaAPI(); api.login()\""
echo "2. Scan the QR code with Mi Home app"
echo "3. Auth token will be saved to: $CONFIG_DIR/auth.json"
echo ""
echo "Or use CLI: mijiaAPI -l (to list devices after login)"
