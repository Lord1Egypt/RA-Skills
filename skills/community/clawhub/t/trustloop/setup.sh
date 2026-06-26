#!/usr/bin/env bash
# TrustLoop setup — verifies TRUSTLOOP_API_KEY is configured

set -e

if [ -z "$TRUSTLOOP_API_KEY" ]; then
  echo ""
  echo "⚠️  TRUSTLOOP_API_KEY is not set."
  echo ""
  echo "1. Sign up free at: https://app.trustloop.live"
  echo "2. Copy your API key from the dashboard"
  echo "3. Run: export TRUSTLOOP_API_KEY=tl_your_key_here"
  echo ""
  exit 1
fi

echo ""
echo "✅ TrustLoop is configured."
echo "   Dashboard: https://app.trustloop.live"
echo ""
echo "To verify your connection:"
echo "   node trustloop-check.js web_search '{\"query\":\"test\"}'"
echo ""
