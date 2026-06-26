#!/bin/bash
set -e

echo "📦 Installing skill-dependency-resolver..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 required"
    exit 1
fi

# Symlink CLI
CLI_NAME="skill-dependency-resolver"
CLI_PATH="${HOME}/.local/bin/${CLI_NAME}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_SCRIPT="${SKILL_DIR}/source/cli.py"

mkdir -p "${HOME}/.local/bin"

if [ -f "${CLI_PATH}" ]; then
    echo "⚠️  Backing up existing CLI..."
    mv "${CLI_PATH}" "${CLI_PATH}.bak"
fi

ln -s "${CLI_SCRIPT}" "${CLI_PATH}"
chmod +x "${CLI_SCRIPT}"

echo "✅ Installation complete!"
echo "   CLI: ${CLI_PATH}"
echo ""
echo "📝 Usage:"
echo "   skill-dependency-resolver --help"
echo "   skill-dependency-resolver --verbose"
echo ""
echo "🔧 Uninstall:"
echo "   rm ${CLI_PATH}"