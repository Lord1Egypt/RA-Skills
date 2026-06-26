#!/usr/bin/env bash
# ═══ Deploy to Vercel ═══
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLATFORM_DIR="$(dirname "$SCRIPT_DIR")/platform"

echo "🚀 Deploying Write My Blog to Vercel..."
cd "$PLATFORM_DIR"

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
  echo "❌ Vercel CLI not found. Install with: npm i -g vercel"
  exit 1
fi

# Build first
echo "📦 Building..."
npm run build

# Deploy
echo "🌐 Deploying..."
vercel --prod

echo "✅ Deployed to Vercel!"
