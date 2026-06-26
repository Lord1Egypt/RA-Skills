#!/usr/bin/env bash
# Zero Token Setup — Install Free-Way gateway + configure OpenClaw fallback
# ⚠️ This installs third-party software (Free-Way by GoDiao).
#    Review: https://github.com/GoDiao/Free-Way
#    Pinned to bf5c60f (2026-05-03). Review before changing.
set -euo pipefail

FREE_WAY_REPO="https://github.com/GoDiao/Free-Way.git"
FREE_WAY_TAG="bf5c60f6aac6f6f2eca80f98c1a5a81a023cb165"  # Pinned commit
FREE_WAY_DIR="$HOME/free-way"
FREE_WAY_PORT=8787

echo "🦾 Zero Token Setup"
echo "===================="
echo ""

# Check Node.js
if ! command -v node &>/dev/null; then
    echo "❌ Node.js required. Install: https://nodejs.org"
    exit 1
fi

# Check if Free-Way already installed
if [ ! -d "$FREE_WAY_DIR" ]; then
    echo "📦 Installing Free-Way gateway (pinned)..."
    echo "   Source: $FREE_WAY_REPO"
    echo ""
    git clone --depth 1 "$FREE_WAY_REPO" "$FREE_WAY_DIR"
    cd "$FREE_WAY_DIR"
    git fetch --depth 1 origin "$FREE_WAY_TAG"
    git checkout FETCH_HEAD
    npm install --omit=dev 2>/dev/null || npm install
    npm run build 2>/dev/null || true
    echo "✅ Free-Way installed at $FREE_WAY_DIR (commit: $FREE_WAY_TAG)"
else
    echo "🔍 Found existing $FREE_WAY_DIR — verifying..."
    cd "$FREE_WAY_DIR"
    EXISTING_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
    EXISTING_COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "")
    if [ "$EXISTING_REMOTE" = "$FREE_WAY_REPO" ] && [ "$EXISTING_COMMIT" = "$FREE_WAY_TAG" ]; then
        echo "✅ Verified: $FREE_WAY_DIR matches pinned commit $FREE_WAY_TAG"
    else
        echo "⚠️  EXISTING DIRECTORY DOES NOT MATCH PINNED SOURCE"
        echo "   Expected: $FREE_WAY_REPO @ $FREE_WAY_TAG"
        echo "   Found:    ${EXISTING_REMOTE:-NOT_A_GIT_REPO} @ ${EXISTING_COMMIT:-UNKNOWN}"
        echo ""
        echo "   Refusing to run untrusted code."
        echo "   To fix: rm -rf $FREE_WAY_DIR && re-run this script"
        exit 1
    fi
fi

# Start Free-Way in background if not running
if ! curl -s http://localhost:$FREE_WAY_PORT/health &>/dev/null; then
    echo "🚀 Starting Free-Way on localhost:$FREE_WAY_PORT..."
    nohup npm start > "$FREE_WAY_DIR/free-way.log" 2>&1 &
    sleep 3
    if curl -s http://localhost:$FREE_WAY_PORT/health &>/dev/null; then
        echo "✅ Free-Way running at http://localhost:$FREE_WAY_PORT"
    else
        echo "⚠️  Free-Way may need manual start: cd $FREE_WAY_DIR && npm start"
    fi
else
    echo "✅ Free-Way already running at http://localhost:$FREE_WAY_PORT"
fi

echo ""
echo "📋 Next steps:"
echo ""
echo "1. Open http://localhost:$FREE_WAY_PORT in your browser"
echo "2. Click 'API Keys' tab"
echo "3. Add free API keys (use free-tier or disposable keys only):"
echo ""
echo "   🔑 Gemini Flash   → https://aistudio.google.com/apikey    (1500 req/day)"
echo "   🔑 Groq           → https://console.groq.com/keys          (1000 req/day)"
echo "   🔑 Cerebras       → https://cloud.cerebras.ai              (1700 req/day)"
echo ""
echo "   ⚠️  Use free-tier keys. Do NOT use production API keys."
echo ""
echo "4. Add this model as fallback in OpenClaw:"
echo ""
echo "   openclaw config add-model zero-token \\"
echo "     --provider openai \\"
echo "     --base-url http://localhost:$FREE_WAY_PORT/v1 \\"
echo "     --model llama-3.3-70b"
echo ""
echo "🎉 Done. Your agent uses free models when the main one is down."
echo ""
echo "---"
echo "🛑 To STOP the gateway:"
echo "   pkill -f 'node.*free-way' || lsof -ti:$FREE_WAY_PORT | xargs kill"
echo ""
echo "🗑️  To UNINSTALL:"
echo "   pkill -f 'node.*free-way'; rm -rf $FREE_WAY_DIR"
echo ""
echo "🔍 To CHECK status:"
echo "   curl http://localhost:$FREE_WAY_PORT/health"
