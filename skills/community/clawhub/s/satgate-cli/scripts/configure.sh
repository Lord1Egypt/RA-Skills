#!/usr/bin/env bash
set -euo pipefail

# SatGate CLI Configuration
# Interactive setup for ~/.satgate/config.json

CONFIG_DIR="${HOME}/.satgate"
CONFIG_FILE="${CONFIG_DIR}/config.json"

echo "⚡ SatGate CLI Configuration"
echo "───────────────────────────"
echo ""

# Check if config already exists
if [ -f "$CONFIG_FILE" ]; then
  echo "  Existing config found at ${CONFIG_FILE}"
  read -p "  Overwrite? [y/N]: " OVERWRITE
  if [ "${OVERWRITE,,}" != "y" ]; then
    echo "  Keeping existing config."
    exit 0
  fi
fi

# Cloud URL
echo ""
DEFAULT_URL="https://cloud.satgate.io"
read -p "  Cloud URL [${DEFAULT_URL}]: " CLOUD_URL
CLOUD_URL="${CLOUD_URL:-$DEFAULT_URL}"

# API Key
echo ""
echo "  Get your API key from: ${CLOUD_URL}/cloud/api-keys"
echo ""
read -p "  API Key: " API_KEY
if [ -z "$API_KEY" ]; then
  echo ""
  echo "  ⚠️  No API key provided."
  echo "     Sign up free at: ${CLOUD_URL}/cloud/login"
  echo "     Then get your key at: ${CLOUD_URL}/cloud/api-keys"
  exit 1
fi

# Write config as JSON (matches satgate-cli format)
mkdir -p "$CONFIG_DIR"
cat > "$CONFIG_FILE" <<EOF
{
  "cloud_url": "${CLOUD_URL}",
  "api_key": "${API_KEY}",
  "tenant_id": ""
}
EOF

chmod 600 "$CONFIG_FILE"

echo ""
echo "✓ Config written to ${CONFIG_FILE}"
echo ""
echo "  Next steps:"
echo "    satgate-cli init       # Validate key and set tenant"
echo "    satgate-cli status     # Check your gateway"
