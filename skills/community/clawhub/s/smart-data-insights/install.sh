#!/bin/bash
# Data Analyst Skill - Installation Script

set -e

echo "🚀 Installing Data Analyst Skill..."
echo ""

# Check Python version
echo "📋 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✅ Python $PYTHON_VERSION found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip3."
    exit 1
fi
echo "✅ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -q pandas openpyxl matplotlib seaborn

# Verify installation
echo ""
echo "🔍 Verifying installation..."
python3 -c "import pandas, matplotlib, openpyxl, seaborn; print('✅ All dependencies installed successfully')"

# Set permissions
echo ""
echo "🔐 Setting permissions..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
chmod +x "$SCRIPT_DIR/tools/"*.py
chmod +x "$SCRIPT_DIR/test.sh"

# Run tests
echo ""
echo "🧪 Running tests..."
bash "$SCRIPT_DIR/test.sh"

# Success message
echo ""
echo "========================================"
echo "✅ Installation Complete!"
echo "========================================"
echo ""
echo "📊 Data Analyst Skill is ready to use."
echo ""
echo "Quick Start:"
echo "  python3 $SCRIPT_DIR/tools/analyze.py your_data.csv"
echo ""
echo "Full Analysis:"
echo "  python3 $SCRIPT_DIR/tools/analyze.py your_data.csv --clean --visualize --report"
echo ""
echo "For more information, see:"
echo "  - README.md"
echo "  - INSTALL.md"
echo ""
echo "🎉 Happy analyzing!"
