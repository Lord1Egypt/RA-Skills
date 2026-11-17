#!/bin/bash
# Start the BlueColumn Voice Agent Memory Bridge
# Usage: ./scripts/start.sh [port]

PORT=${1:-8013}
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Check for .env
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "⚠️  No .env file found. Copy from .env.example:"
    echo "   cp $SCRIPT_DIR/.env.example $SCRIPT_DIR/.env"
    echo "   Then edit with your API keys."
    exit 1
fi

echo "🚀 Starting BlueColumn Voice Agent Memory Bridge on port $PORT..."
cd "$SCRIPT_DIR"
python3 bridge/server.py
