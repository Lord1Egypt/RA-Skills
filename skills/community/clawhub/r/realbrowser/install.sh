#!/bin/sh
# RealBrowser by Ceki — installation script
# Installs the ceki-sdk CLI. Does NOT transmit any credentials.

set -e

echo "→ Installing ceki-sdk (Python CLI)..."
if command -v pip3 >/dev/null 2>&1; then
    pip3 install --upgrade ceki-sdk --break-system-packages 2>/dev/null \
        || pip3 install --upgrade --user ceki-sdk
elif command -v pip >/dev/null 2>&1; then
    pip install --upgrade ceki-sdk --break-system-packages 2>/dev/null \
        || pip install --upgrade --user ceki-sdk
else
    echo "❌ pip not found. Install Python 3.10+ first."
    exit 1
fi

if ! command -v ceki >/dev/null 2>&1; then
    echo "⚠️  'ceki' command not found in PATH. Try adding ~/.local/bin to PATH:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    exit 1
fi

echo "→ ceki CLI installed: $(ceki --version 2>/dev/null || echo unknown)"
echo ""
echo "✓ Done. Next steps (manual, opt-in):"
echo ""
echo "  1. Sign up at https://ceki.me (email only)"
echo "  2. Generate an API key in the dashboard"
echo "  3. Export when ready to use the CLI:"
echo "       export CEKI_API_KEY=\"<your_key>\""
echo ""
echo "  4. Use only on sites you own or have authorization to operate on."
echo "     See SKILL.md for appropriate use cases and limitations."
echo ""
echo "  Self mode (your own Chrome, free): install the Ceki extension separately"
echo "  from https://browser.ceki.me/install."
