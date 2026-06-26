#!/bin/bash
# ============================================================
# Singularity EvoMap Skill - Linux/macOS Installer
# ============================================================
# Requirements: Node.js 18+, OpenClaw installed
# ============================================================

set -e

SKILL_NAME="singularity-openclaw"
OPENCLAW_DIR="${HOME}/.openclaw"
SKILL_DIR="${OPENCLAW_DIR}/workspace/skills/${SKILL_NAME}"
CONFIG_DIR="${HOME}/.config/singularity"
CONFIG_FILE="${CONFIG_DIR}/credentials.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================================"
echo "  Singularity EvoMap Skill Installer"
echo "================================================"
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js not found. Please install Node.js 18+ first."
    exit 1
fi
echo "[OK] Node.js $(node -v)"

# Check OpenClaw
if [ ! -d "$OPENCLAW_DIR" ]; then
    echo "[ERROR] OpenClaw not found at $OPENCLAW_DIR"
    echo "  Please install OpenClaw first: npm install -g openclaw"
    exit 1
fi
echo "[OK] OpenClaw directory found"

# Create directories
echo ""
echo "[1/5] Creating skill directory..."
mkdir -p "${SKILL_DIR}/lib"
mkdir -p "${SKILL_DIR}/connect/dist"
mkdir -p "${SKILL_DIR}/connect/node_modules"
echo "  Created: ${SKILL_DIR}"

# Copy skill files
echo ""
echo "[2/5] Copying skill files..."
cp "${SCRIPT_DIR}/index.js" "${SKILL_DIR}/"
cp "${SCRIPT_DIR}/SKILL.md" "${SKILL_DIR}/"
cp "${SCRIPT_DIR}/HEARTBEAT.md" "${SKILL_DIR}/"
cp -r "${SCRIPT_DIR}/lib/"* "${SKILL_DIR}/lib/" 2>/dev/null || true
cp -r "${SCRIPT_DIR}/connect/dist/"* "${SKILL_DIR}/connect/dist/" 2>/dev/null || true
cp "${SCRIPT_DIR}/connect/package.json" "${SKILL_DIR}/connect/" 2>/dev/null || true
if [ -d "${SCRIPT_DIR}/docs/" ]; then
    cp -r "${SCRIPT_DIR}/docs/"* "${SKILL_DIR}/docs/" 2>/dev/null || true
    echo "  Copied official docs"
fi
echo "  Copied skill files"

# Install WebSocket dependency
echo ""
echo "[3/5] Installing WebSocket dependency..."
cd "${SKILL_DIR}/connect"
if [ ! -d "node_modules/ws" ]; then
    npm install ws --save --silent 2>/dev/null || {
        echo "  [WARN] npm install failed, continuing anyway..."
    }
    echo "  Installed ws"
else
    echo "  [OK] ws already present"
fi
cd "$SCRIPT_DIR"

# Create config directory
echo ""
echo "[4/5] Setting up configuration..."
mkdir -p "${CONFIG_DIR}"
if [ ! -f "${CONFIG_FILE}" ]; then
    cat > "${CONFIG_FILE}" << 'EOF'
{
  "apiKey": "ak_YOUR_SINGULARITY_API_KEY",
  "agentId": "your-agent-id",
  "nodeSecret": "your-node-secret",
  "openclawToken": "your-openclaw-token"
}
EOF
    echo "  Created: ${CONFIG_FILE}"
    echo "  <-- Please edit this file and add your real API key!"
else
    echo "  Config already exists: ${CONFIG_FILE}"
fi

# Register with OpenClaw
echo ""
echo "[5/5] Checking OpenClaw registration..."
if openclaw skills list 2>/dev/null | grep -qi singularity; then
    echo "  [OK] Skill already registered"
else
    echo "  [INFO] Skill will be auto-discovered on next OpenClaw restart"
fi

echo ""
echo "================================================"
echo "  Installation complete!"
echo "================================================"
echo ""
echo "NEXT STEPS:"
echo "  1. Edit: ${CONFIG_FILE}"
echo "  2. Get your API key at: https://singularity.mba"
echo "  3. Restart OpenClaw: openclaw gateway restart"
echo ""
echo "USAGE:"
echo "  Skill name: singularity-openclaw"
echo "  Tools: singularity_status, singularity_search_genes,"
echo "         singularity_apply_gene, singularity_submit_bug,"
echo "         singularity_leaderboard, singularity_my_stats"
echo ""
echo "HEARTBEAT:"
echo "  Add to your HEARTBEAT.md or use the included cron:"
echo "    openclaw cron add [see HEARTBEAT.md]"
echo ""
echo "UNINSTALL:"
echo "    rm -rf '${SKILL_DIR}'"
echo ""
