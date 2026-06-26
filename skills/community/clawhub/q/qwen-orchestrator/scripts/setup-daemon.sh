#!/usr/bin/env bash
# setup-daemon.sh — One-command setup for qwen-orchestrator daemon
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

cd "$SKILL_DIR"

echo "🧩 Running isolation check..."
node "$SCRIPT_DIR/isolation-check.js"

echo "📦 Installing dependencies..."
npm install --silent

echo "🚀 Starting daemon..."
pm2 start qwen-daemon.js --name qwen-daemon --no-autorestart 2>/dev/null || pm2 restart qwen-daemon

echo "💾 Saving PM2 state..."
pm2 save

echo "🔧 Setting up startup..."
pm2 startup 2>/dev/null || echo "  (run 'pm2 startup' manually if needed)"

echo ""
echo "✅ qwen-orchestrator daemon is running!"
echo "   Test: ask-qwen.sh --daemon 'Say OK'"
