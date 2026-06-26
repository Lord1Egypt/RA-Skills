#!/usr/bin/env bash
# deploy.sh: Deploy hosted MCP server to wip.computer
#
# Prerequisites:
#   - SSH config has Host wip.computer
#   - pm2 installed on the server
#   - nginx configured on the server
#
# Usage: bash deploy.sh

set -euo pipefail

REMOTE="wip.computer"
REMOTE_DIR="/var/www/wip.computer/app/mcp-server"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Deploying hosted MCP server to ${REMOTE}..."

# 1. Create remote directory structure
echo "Creating remote directories..."
ssh "${REMOTE}" "mkdir -p ${REMOTE_DIR}/inbox"

# 2. Copy server files
echo "Copying files..."
scp "${SCRIPT_DIR}/server.mjs" "${REMOTE}:${REMOTE_DIR}/"
scp "${SCRIPT_DIR}/inbox.mjs" "${REMOTE}:${REMOTE_DIR}/"
scp "${SCRIPT_DIR}/tools.mjs" "${REMOTE}:${REMOTE_DIR}/"
scp "${SCRIPT_DIR}/package.json" "${REMOTE}:${REMOTE_DIR}/"

# 3. Install dependencies
echo "Installing dependencies..."
ssh "${REMOTE}" "cd ${REMOTE_DIR} && npm install --omit=dev"

# 4. Register with pm2 (restart if already running)
echo "Starting with pm2..."
ssh "${REMOTE}" "cd ${REMOTE_DIR} && pm2 delete mcp-server 2>/dev/null || true && pm2 start server.mjs --name mcp-server && pm2 save"

# 5. Configure nginx reverse proxy
echo "Configuring nginx..."
ssh "${REMOTE}" "cat > /tmp/mcp-server.conf << 'NGINX'
# MCP server reverse proxy
# Location block to add inside the wip.computer server block
location /mcp {
    proxy_pass http://127.0.0.1:18800/mcp;
    proxy_http_version 1.1;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;

    # SSE support (for MCP Streamable HTTP GET streams)
    proxy_set_header Connection '';
    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 86400;
    chunked_transfer_encoding on;
}
NGINX
"

echo ""
echo "nginx config written to /tmp/mcp-server.conf on the server."
echo "To activate, add it to your server block and reload:"
echo "  ssh ${REMOTE} 'sudo cp /tmp/mcp-server.conf /etc/nginx/snippets/mcp-server.conf'"
echo "  # Then include it in your server block: include snippets/mcp-server.conf;"
echo "  ssh ${REMOTE} 'sudo nginx -t && sudo systemctl reload nginx'"
echo ""
echo "Deployment complete."
echo "Health check: curl https://wip.computer/health"
echo "MCP endpoint: https://wip.computer/mcp"
