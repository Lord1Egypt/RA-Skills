#!/bin/bash
# Visual-Explainer: Serve Report On Different Port
# Usage: ./scripts/serve-report-alt-port.sh [port]
# Default port: 8081 (to avoid conflicts)

PORT=${1:-8081}

echo "🚀 Serving visual-explainer reports on port $PORT..."
echo ""
echo "📖 Main report:"
echo "   http://localhost:$PORT/visual-explainer-skill-report.html"
echo "   http://192.168.50.60:$PORT/visual-explainer-skill-report.html"
echo ""
echo "🔄 Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")/.." && python3 -m http.server $PORT --directory templates