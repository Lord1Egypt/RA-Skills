#!/usr/bin/env bash
# Tavily Search skill installer
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📦 Installing Tavily Search skill..."

# Install Python dependencies
pip install --break-system-packages --quiet tavily-python 2>/dev/null || {
    echo "⚠️  pip install failed, trying without --break-system-packages..."
    pip install --quiet tavily-python 2>/dev/null || {
        echo "❌ Failed to install tavily-python. Install manually: pip install tavily-python"
        exit 1
    }
}

# Verify API key
if [ -z "${TAVILY_API_KEY:-}" ]; then
    echo "⚠️  TAVILY_API_KEY not set. Set it in OpenClaw config before using."
else
    echo "✅ TAVILY_API_KEY found"
fi

# Quick smoke test
if python3 "$SCRIPT_DIR/lib/tavily_search.py" --help >/dev/null 2>&1; then
    echo "✅ Tavily Search skill ready."
else
    echo "⚠️  Smoke test failed - check Python dependencies."
    exit 1
fi
