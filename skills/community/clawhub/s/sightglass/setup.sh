#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Sightglass — Setup"
echo "====================="

# 1. Check/install CLI
if command -v sightglass &>/dev/null; then
  echo "✅ sightglass CLI installed ($(sightglass --version 2>/dev/null || echo 'unknown version'))"
else
  echo "📦 Installing @sightglass/cli..."
  npm i -g @sightglass/cli
  echo "✅ Installed"
fi

# 2. Setup if not configured
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/sightglass"
if [[ -f "$CONFIG_DIR/config.json" ]]; then
  echo "✅ Already configured"
else
  echo "⚙️  Running initial setup..."
  sightglass setup
fi

# 3. Verify watcher
if pgrep -f "sightglass watch" &>/dev/null; then
  echo "✅ Watcher daemon running"
else
  echo "⚠️  Watcher not running. Start it with: sightglass watch"
fi

# 4. Summary
echo ""
echo "--- Status ---"
sightglass --version 2>/dev/null && echo "Config: $CONFIG_DIR"
echo "API: https://sightglass.dev"
echo ""
echo "Next steps:"
echo "  sightglass login    # authenticate with sightglass.dev"
echo "  sightglass watch    # start the watcher daemon"
echo "  sightglass analyze  # analyze agent sessions"
