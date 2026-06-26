#!/bin/bash
# Vision Tagger Setup Script
# Compiles the Swift binary and installs Python dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔧 Vision Tagger Setup"
echo "======================"

# Check macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "❌ Error: This skill requires macOS (uses Apple Vision framework)"
    exit 1
fi

# Check Xcode CLI tools
if ! command -v swiftc &> /dev/null; then
    echo "📦 Installing Xcode Command Line Tools..."
    xcode-select --install
    echo "⏳ Please complete the Xcode installation and run this script again."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required"
    exit 1
fi

# Install Pillow if needed
if ! python3 -c "import PIL" 2>/dev/null; then
    echo "📦 Installing Pillow..."
    pip3 install Pillow
fi

# Compile Swift binary
echo "🔨 Compiling image_tagger..."
cd "$SCRIPT_DIR"
swiftc -O -o image_tagger image_tagger.swift

# Verify
if [[ -x "$SCRIPT_DIR/image_tagger" ]]; then
    echo "✅ Setup complete!"
    echo ""
    echo "Usage:"
    echo "  $SCRIPT_DIR/image_tagger /path/to/image.jpg"
    echo "  python3 $SCRIPT_DIR/annotate_image.py /path/to/image.jpg"
else
    echo "❌ Compilation failed"
    exit 1
fi
