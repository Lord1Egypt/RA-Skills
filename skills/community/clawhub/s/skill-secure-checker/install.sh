#!/bin/bash
set -e

# Skill Security Scanner - Installation Script
# Installs the skill-security-scanner CLI tool

echo "🔒 Installing skill-security-scanner..."

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment (optional, use system Python if venv not desired)
# python3 -m venv ~/.skill-security-scanner-venv
# source ~/.skill-security-scanner-venv/bin/activate

# Install dependencies (none needed - pure stdlib)
# If future dependencies are added, install them here:
# pip install -r requirements.txt

# Create symlink to CLI
CLI_NAME="skill-secure-checker"
CLI_PATH="${HOME}/.local/bin/${CLI_NAME}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_SCRIPT="${SKILL_DIR}/source/cli.py"

mkdir -p "${HOME}/.local/bin"

if [ -f "${CLI_PATH}" ]; then
    echo "⚠️  Existing CLI found at ${CLI_PATH}, backing up to ${CLI_PATH}.bak"
    mv "${CLI_PATH}" "${CLI_PATH}.bak"
fi

ln -s "${CLI_SCRIPT}" "${CLI_PATH}"
chmod +x "${CLI_SCRIPT}"

echo "✅ Installation complete!"
echo "   CLI: ${CLI_PATH}"
echo ""
echo "📝 Usage:"
echo "   skill-security-scanner skill_path=\"./skills/your-skill\""
echo ""
echo "🧪 Test:"
echo "   skill-security-scanner --help"
echo ""
echo "🔧 Uninstall:"
echo "   rm ${CLI_PATH}"