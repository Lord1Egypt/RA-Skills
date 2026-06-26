#!/usr/bin/env bash
set -euo pipefail

# VIGIL MCP Server — CLI entrypoint
# Usage: ./scripts/run.sh [--transport stdio|sse] [--port 3100]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Load .env if exists
if [ -f "$PROJECT_DIR/.env" ]; then
  set -a
  source "$PROJECT_DIR/.env"
  set +a
fi

TRANSPORT="${1:-stdio}"
PORT="${2:-3100}"

export VIGIL_MCP_TRANSPORT="$TRANSPORT"
export VIGIL_MCP_PORT="$PORT"

echo "🛡️  Starting VIGIL MCP Server..."
echo "  Transport: $TRANSPORT"
if [ "$TRANSPORT" = "sse" ]; then
  echo "  Port: $PORT"
fi
echo ""

cd "$PROJECT_DIR/src"
exec python3 -m vigil_mcp.server
