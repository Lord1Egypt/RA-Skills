#!/bin/bash
# Onboarding script for Thetanuts OpenClaw Skill
# Creates WDK MCP runtime at ~/.openclaw/wdk-mcp and installs dependencies
#
# Usage: bash scripts/onboard.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🥜 Thetanuts OpenClaw - Onboarding"
echo "=================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}❌ $1 is not installed${NC}"
        echo "   Please install $1 and try again."
        echo "   $2"
        exit 1
    else
        echo -e "${GREEN}✓ $1 found${NC}"
    fi
}

check_command "node" "Install from https://nodejs.org/ or use nvm"
check_command "npm" "Comes with Node.js installation"

# Check node version (need >= 18)
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo -e "${RED}❌ Node.js version must be >= 18 (found v$NODE_VERSION)${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js version $NODE_VERSION OK${NC}"

# openclaw is optional - warn if not found
if command -v openclaw &> /dev/null; then
    echo -e "${GREEN}✓ openclaw found${NC}"
else
    echo -e "${YELLOW}⚠ openclaw not found (optional - install from https://docs.openclaw.ai/)${NC}"
fi

echo ""

# Create WDK MCP directory
WDK_MCP_DIR="$HOME/.openclaw/wdk-mcp"
echo "Setting up WDK MCP runtime at $WDK_MCP_DIR..."

mkdir -p "$WDK_MCP_DIR"
echo -e "${GREEN}✓ Created $WDK_MCP_DIR${NC}"

# Check if .env exists and preserve it
ENV_FILE="$WDK_MCP_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    echo -e "${GREEN}✓ Existing .env file preserved${NC}"
else
    # Create template .env
    cat > "$ENV_FILE" << 'ENVEOF'
# WDK Wallet Configuration
# WARNING: This file contains sensitive wallet data. Never share or commit this file.

# Wallet seed phrase (set by wallet-create.js or wallet-import.js)
# WDK_SEED=

# Active wallet context
WDK_ACTIVE_FAMILY=evm
WDK_ACTIVE_CHAIN=base-mainnet
WDK_ACTIVE_INDEX=0

# RPC URLs (optional overrides)
# EVM_RPC_URL=https://mainnet.base.org
# SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
ENVEOF
    echo -e "${GREEN}✓ Created .env template${NC}"
fi

# Create package.json
PACKAGE_JSON="$WDK_MCP_DIR/package.json"
cat > "$PACKAGE_JSON" << 'PKGEOF'
{
  "name": "wdk-mcp-runtime",
  "version": "1.0.0",
  "description": "WDK MCP Runtime for Thetanuts OpenClaw",
  "type": "module",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "@tetherto/wdk": "^1.0.0-beta.6",
    "@tetherto/wdk-wallet-evm": "^1.0.0-beta.10",
    "@tetherto/wdk-wallet-solana": "^1.0.0-beta.5",
    "@modelcontextprotocol/sdk": "^1.0.0",
    "@thetanuts-finance/thetanuts-client": "^0.2.4",
    "@scure/bip39": "^1.5.4",
    "dotenv": "^16.4.5"
  }
}
PKGEOF
echo -e "${GREEN}✓ Created package.json${NC}"

# Create MCP server scaffold
SERVER_JS="$WDK_MCP_DIR/server.js"
cat > "$SERVER_JS" << 'SERVEREOF'
#!/usr/bin/env node
/**
 * WDK MCP Server - Wallet tools for OpenClaw
 * This is a minimal scaffold. Extend with additional tools as needed.
 */

import { config } from 'dotenv';
import { resolve } from 'path';

// Load .env from this directory
config({ path: resolve(import.meta.dirname, '.env') });

console.log('WDK MCP Server scaffold loaded');
console.log('Active family:', process.env.WDK_ACTIVE_FAMILY || 'evm');
console.log('Active chain:', process.env.WDK_ACTIVE_CHAIN || 'base-mainnet');

// TODO: Implement MCP server with wallet tools
// See @modelcontextprotocol/sdk for implementation details
SERVEREOF
echo -e "${GREEN}✓ Created server.js scaffold${NC}"

# Install project-level dependencies (for wallet scripts)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
echo ""
echo "Installing project dependencies..."
cd "$PROJECT_DIR"
npm install --silent 2>&1 | tail -5
echo -e "${GREEN}✓ Project dependencies installed${NC}"

# Install WDK MCP runtime dependencies
echo ""
echo "Installing WDK MCP runtime dependencies..."
cd "$WDK_MCP_DIR"
npm install --silent 2>&1 | tail -5
echo -e "${GREEN}✓ WDK MCP dependencies installed${NC}"

# Verify installation
echo ""
echo "Verifying installation..."

# Check that key packages are installed
if [ -d "$WDK_MCP_DIR/node_modules/@tetherto/wdk-wallet-evm" ]; then
    echo -e "${GREEN}✓ @tetherto/wdk-wallet-evm installed${NC}"
else
    echo -e "${RED}❌ @tetherto/wdk-wallet-evm not found${NC}"
    exit 2
fi

if [ -d "$WDK_MCP_DIR/node_modules/@tetherto/wdk-wallet-solana" ]; then
    echo -e "${GREEN}✓ @tetherto/wdk-wallet-solana installed${NC}"
else
    echo -e "${RED}❌ @tetherto/wdk-wallet-solana not found${NC}"
    exit 2
fi

if [ -d "$WDK_MCP_DIR/node_modules/@thetanuts-finance/thetanuts-client" ]; then
    echo -e "${GREEN}✓ @thetanuts-finance/thetanuts-client installed${NC}"
else
    echo -e "${RED}❌ @thetanuts-finance/thetanuts-client not found${NC}"
    exit 2
fi

echo ""
echo "=================================="
echo -e "${GREEN}✅ Onboarding complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Create a wallet:    node scripts/wallet-create.js"
echo "  2. Or import existing: node scripts/wallet-import.js --seed-file /path/to/seed.txt"
echo "  3. Check your wallet:  node scripts/wallet-discover.js"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT: Use a DEDICATED wallet seed for this integration.${NC}"
echo -e "${YELLOW}   Do NOT reuse your primary or personal wallet seed phrase.${NC}"
echo ""
