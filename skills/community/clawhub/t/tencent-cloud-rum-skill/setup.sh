#!/bin/bash
# Setup script for Tencent Cloud RUM MCP Skill
# Authentication via SecretId + SecretKey

set -e

echo "🚀 Setting up Tencent Cloud RUM MCP Skill..."
echo ""

# 1. Check mcporter
MCPORTER_VERSION="0.9.0"
if ! command -v mcporter &> /dev/null; then
    echo "⚠️  mcporter not found, installing v${MCPORTER_VERSION}..."
    npm install -g "mcporter@${MCPORTER_VERSION}"
    echo "✅ mcporter v${MCPORTER_VERSION} installed"
fi

# 2. Check environment variable
if [ -z "$RUM_TOKEN" ]; then
    echo "⚠️  RUM_TOKEN environment variable not detected"
    echo ""
    echo "📋 Please configure the environment variable first:"
    echo "   export RUM_TOKEN=\"YourSecretId:YourSecretKey\""
    echo ""
    echo "   Format: SecretId and SecretKey separated by a colon (:)"
    echo ""
    echo "🔗 Get credentials: Visit https://console.tencentcloud.com/cam/capi to obtain your SecretId and SecretKey"
    echo ""
    echo "   If using in OpenClaw, enter SecretId:SecretKey in the API key input field"
    exit 1
fi

# 3. Parse RUM_TOKEN (format: SecretId:SecretKey)
RUM_SECRET_ID="${RUM_TOKEN%%:*}"
RUM_SECRET_KEY="${RUM_TOKEN#*:}"

if [ -z "$RUM_SECRET_ID" ] || [ -z "$RUM_SECRET_KEY" ] || [ "$RUM_SECRET_ID" = "$RUM_TOKEN" ]; then
    echo "❌ RUM_TOKEN format error. Please use SecretId:SecretKey format (colon-separated)"
    exit 1
fi

echo "✅ SecretId and SecretKey parsed successfully"

# 4. Add MCP configuration
echo "🔧 Configuring mcporter..."

# Remove old config if exists
mcporter config remove rum --scope home 2>/dev/null || true

# Write mcporter config file, ensuring both headers are correctly passed
MCPORTER_CONFIG="$HOME/.mcporter/mcporter.json"
mkdir -p "$HOME/.mcporter"

# Use node to safely write/merge config (pass SecretId/SecretKey via env vars)
RUM_SID="$RUM_SECRET_ID" RUM_SKEY="$RUM_SECRET_KEY" MCPORTER_CFG="$MCPORTER_CONFIG" node -e "
const fs = require('fs');
const cfgPath = process.env.MCPORTER_CFG;
let config = {};
try { config = JSON.parse(fs.readFileSync(cfgPath, 'utf8')); } catch(e) {}
if (!config.mcpServers) config.mcpServers = {};
config.mcpServers.rum = {
  url: 'https://app.rumt-zh.com/sse',
  transportType: 'sse',
  headers: {
    SecretId: process.env.RUM_SID,
    SecretKey: process.env.RUM_SKEY
  }
};
fs.writeFileSync(cfgPath, JSON.stringify(config, null, 2));
"

echo "✅ Configuration written to $MCPORTER_CONFIG"

echo ""
echo "✅ Setup complete!"
echo ""

# 5. Verify configuration
echo "🧪 Verifying configuration..."
if mcporter list 2>&1 | grep -q "rum"; then
    echo "✅ Configuration verified successfully!"
    echo ""
    mcporter list | grep -A 1 "rum" || true
else
    echo "⚠️  Configuration verification failed. Please check your network or RUM_TOKEN (format: SecretId:SecretKey)"
    echo ""
    echo "🔗 Get SecretId/SecretKey: https://console.tencentcloud.com/cam/capi"
fi

echo ""
echo "─────────────────────────────────────"
echo "🎉 Setup complete!"
echo ""
echo "📖 Usage:"
echo "   mcporter call \"rum.QueryRumWebProjects()\""
echo "   mcporter call \"rum.QueryRumWebMetric(ProjectId:'123456', Metric:'exception', GroupBy:['level'], Limit:100)\""
echo ""
echo "📖 For more information, see SKILL.md"
echo ""
echo "📚 New to Tencent Cloud RUM?"
echo "   Console:   https://console.tencentcloud.com/rum"
echo "   Demo:      https://console.tencentcloud.com/rum/web/demo"
echo "   Docs:      https://www.tencentcloud.com/zh/document/product/1131/44496"
echo ""
