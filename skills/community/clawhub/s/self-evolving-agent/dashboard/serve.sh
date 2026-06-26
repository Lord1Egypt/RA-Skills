#!/usr/bin/env bash
# ============================================================
# serve.sh — Local dev server for SEA Dashboard
#
# Usage:
#   bash dashboard/serve.sh          # port 8420 (default)
#   bash dashboard/serve.sh 9000     # custom port
# ============================================================

PORT="${1:-8420}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Rebuild index before serving so data is fresh
echo "📦 Building data index..."
bash "$SCRIPT_DIR/build-index.sh" 2>&1 | sed 's/^/   /'

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  🧠 Self-Evolving Agent Dashboard                    ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  URL:  http://localhost:${PORT}/dashboard/           ║"
echo "║  Stop: Ctrl+C                                        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  Served from: $SKILL_DIR"
echo "  Tip: Re-run build-index.sh after new proposals appear"
echo "       to refresh the data without restarting the server."
echo ""

# Serve from skill root so ../data/ paths work from dashboard/
cd "$SKILL_DIR"
python3 -m http.server "$PORT" --directory .
