#!/usr/bin/env bash
set -euo pipefail

# SatGate CLI Health Check
# Validates that the CLI is installed and can reach the gateway.

echo "⚡ SatGate CLI Health Check"
echo "───────────────────────────"

# Check binary
if ! command -v satgate-cli &>/dev/null; then
  echo "❌ satgate-cli binary not found in PATH"
  echo "   Run: scripts/install.sh"
  echo "   Or build from source: cd satgate && go build -o satgate-cli ./cmd/satgate-cli/"
  exit 1
fi
echo "✓ Binary: $(which satgate-cli)"
satgate-cli version

# Check config
CONFIG="${HOME}/.satgate/config.json"
if [ -f "$CONFIG" ]; then
  echo "✓ Config: ${CONFIG}"
else
  echo "⚠️  No config file at ${CONFIG}"
  echo "   Run: satgate-cli init"
fi

# Check connection
echo ""
echo "Testing gateway connection..."
if satgate-cli status 2>/dev/null; then
  echo ""
  echo "✓ Connected to SatGate"
else
  echo ""
  echo "❌ Cannot reach gateway"
  echo "   Run: satgate-cli init"
  exit 1
fi
