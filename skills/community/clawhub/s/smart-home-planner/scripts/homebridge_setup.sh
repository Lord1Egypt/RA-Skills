#!/bin/bash
# Homebridge + MCP Server Setup Script
# Usage: bash homebridge_setup.sh

set -e

echo "=== Homebridge + MCP Server Setup ==="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js not found. Please install Node.js 18+ first."
    echo "  macOS:   brew install node"
    echo "  Linux:   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install -y nodejs"
    exit 1
fi

NODE_VERSION=$(node -v)
echo "Node.js version: $NODE_VERSION"

# Check npm
if ! command -v npm &> /dev/null; then
    echo "Error: npm not found."
    exit 1
fi

# Install homebridge-mcp-server
echo ""
echo "Installing homebridge-mcp-server..."
npm install -g @mp-consulting/homebridge-mcp-server

# Verify installation
echo ""
echo "Verifying installation..."
homebridge-mcp-server --version 2>/dev/null && echo "homebridge-mcp-server installed successfully" || echo "Installed (version check not available)"

# Check if Homebridge is running
echo ""
echo "Checking Homebridge connectivity..."
HB_URL="${HOMEBRIDGE_URL:-http://localhost:8581}"
if curl -s -o /dev/null -w "%{http_code}" "$HB_URL/api/auth/check" 2>/dev/null | grep -q "200\|401"; then
    echo "Homebridge is reachable at $HB_URL"
else
    echo "Warning: Homebridge not reachable at $HB_URL"
    echo ""
    echo "You need to install and start Homebridge first:"
    echo "  Docker:  docker run -d --name homebridge --net=host -e HOMEBRIDGE_CONFIG_UI=1 -v ~/homebridge:/homebridge homebridge/homebridge:latest"
    echo "  npm:     npm install -g homebridge homebridge-config-ui-x && homebridge"
    echo ""
    echo "Then set environment variables:"
    echo "  export HOMEBRIDGE_URL=\"http://<host>:8581\""
    echo "  export HOMEBRIDGE_USERNAME=\"admin\""
    echo "  export HOMEBRIDGE_PASSWORD=\"<password>\""
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Ensure Homebridge is running and accessible"
echo "2. Set environment variables (HOMEBRIDGE_URL, HOMEBRIDGE_USERNAME, HOMEBRIDGE_PASSWORD)"
echo "3. Add MCP server to your agent config:"
echo ""
echo "  Claude Code: claude mcp add homebridge -- homebridge-mcp-server"
echo "  Claude Desktop: Add to claude_desktop_config.json (see knowledge/homekit-guide.md)"
echo "  OpenCode: Add to opencode.json (see knowledge/homekit-guide.md)"
