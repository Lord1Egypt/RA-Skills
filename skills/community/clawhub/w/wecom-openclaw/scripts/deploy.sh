#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="${1:-$HOME/wecom-adapter}"

echo "🚀 Deploying WeChat Work adapter to $TARGET_DIR..."

mkdir -p "$TARGET_DIR/logs"

# Copy adapter code
cp "$SKILL_DIR/scripts/index.js" "$TARGET_DIR/index.js"

# Create package.json if not exists
if [ ! -f "$TARGET_DIR/package.json" ]; then
  cat > "$TARGET_DIR/package.json" << 'EOF'
{
  "name": "wecom-adapter",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node --tls-min-v1.2 index.js"
  },
  "dependencies": {
    "express": "^4.21.2",
    "axios": "^1.8.4",
    "xml2js": "^0.6.2",
    "dotenv": "^16.4.7"
  }
}
EOF
fi

# Create .env template if not exists
if [ ! -f "$TARGET_DIR/.env" ]; then
  cat > "$TARGET_DIR/.env" << 'EOF'
# === WeChat Work Credentials ===
CORP_ID=your_corp_id
AGENT_ID=your_agent_id
AGENT_SECRET=your_encoding_aes_key_43chars
APP_SECRET=your_app_secret_for_access_token
WEBHOOK_TOKEN=your_webhook_token

# === OpenClaw ===
OPENCLAW_TOKEN=your_openclaw_bearer_token
OPENCLAW_BASE_URL=http://localhost:18789
CLAUDE_MODEL=claude-haiku-4-5
EOF
  echo "📝 Created .env template at $TARGET_DIR/.env — edit with your credentials"
fi

# Install dependencies
cd "$TARGET_DIR"
npm install

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "  1. Edit $TARGET_DIR/.env with your WeChat Work credentials"
echo "  2. cd $TARGET_DIR && npm start"
echo "  3. In another terminal: cloudflared tunnel --url http://localhost:8090"
echo "  4. Copy tunnel URL to WeChat Work admin → webhook URL"
echo ""
echo "⚠️  IMPORTANT: Add your public IP to WeChat Work's trusted IP list!"
echo "⚠️  IMPORTANT: Complete enterprise verification before production use!"
