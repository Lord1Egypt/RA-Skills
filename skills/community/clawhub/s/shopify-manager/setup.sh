#!/bin/bash
# Setup script for Shopify Manager skill

set -e

echo "🛍️  Setting up Shopify Manager skill..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

# Install dependencies
echo "   Installing dependencies..."
pip install -q -r requirements.txt

# Check for config
echo ""
if [ ! -f "shopify-config.yaml" ]; then
    echo "⚠️  Configuration file not found!"
    echo "   Copy shopify-config-example.yaml to shopify-config.yaml"
    echo "   and fill in your store details."
else
    echo "✅ Configuration file found"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "   1. Edit shopify-config.yaml with your store details"
echo "   2. Test connection: python src/cli.py config"
echo "   3. Try a dry-run: python src/cli.py products list"
echo ""
