#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/root/.openclaw/workspace"

echo "🚀 Installing Workspace Heartbeat Integration..."

# 1. Verify Python 3.8+
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED="3.8"
if [ "$(printf '%s\n' "$REQUIRED" "$PY_VERSION" | sort -V | head -n1)" != "$REQUIRED" ]; then
    echo "❌ Python $REQUIRED+ required, found $PY_VERSION"
    exit 1
fi

echo "✅ Python $PY_VERSION detected"

# 2. Install skill to OpenClaw
echo "📦 Publishing skill to ClawHub..."
if command -v clawhub &> /dev/null; then
    cd "$SKILL_DIR"
    clawhub publish . --slug workspace-heartbeat-integration --name "Workspace Heartbeat Integration" --version 1.0.0 --changelog "自动同步 HEARTBEAT 和 self-improving 状态"
    echo "✅ Skill published successfully"
else
    echo "⚠️  clawhub CLI not found, skipping publish"
    echo "   Install with: npm install -g clawhub"
fi

# 3. Create symlink for CLI command (optional)
INSTALL_DIR="${HOME}/.local/bin"
mkdir -p "$INSTALL_DIR"
ln -sf "$SKILL_DIR/source/integration.py" "$INSTALL_DIR/workspace-heartbeat-integration"
chmod +x "$SKILL_DIR/source/integration.py"

if [[ ":$PATH:" == *":$INSTALL_DIR:"* ]]; then
    echo "✅ CLI command installed to $INSTALL_DIR (already in PATH)"
else
    echo "⚠️  CLI installed to $INSTALL_DIR but not in PATH"
    echo "   Add to PATH: export PATH=\"$INSTALL_DIR:\$PATH\""
fi

# 4. Create default config
CONFIG_DIR="${HOME}/.config/workspace-heartbeat-integration"
mkdir -p "$CONFIG_DIR"
cat > "$CONFIG_DIR/config.json" << 'EOF'
{
  "auto_sync": true,
  "log_retention_days": 30,
  "memory_update_threshold": 3,
  "excluded_dirs": [".git", "node_modules", "__pycache__", ".venv"]
}
EOF
echo "✅ Default config created at $CONFIG_DIR/config.json"

# 5. Verify installation
echo ""
echo "🎉 Installation complete!"
echo ""
echo "Usage:"
echo "  workspace-heartbeat-integration --sync               # Sync state"
echo "  workspace-heartbeat-integration --log learning:desc # Log work"
echo "  workspace-heartbeat-integration --report --format markdown  # Generate report"
echo ""
echo "Next step: Add to your HEARTBEAT.md to automate:"
echo "  workspace-heartbeat-integration --sync"
echo ""