#!/usr/bin/env bash
#
# deploy-cloud.sh — Deploy Memory Crystal Cloud MCP server to Cloudflare.
# Pulls all credentials from 1Password. No keys in env files.
#
# Usage:
#   bash scripts/deploy-cloud.sh          # full setup (first time)
#   bash scripts/deploy-cloud.sh deploy   # just redeploy Worker code
#
# Prerequisites:
#   - wrangler CLI installed (npm install -g wrangler)
#   - 1Password items populated:
#     "Parker - Cloudflare Memory Crystal Keys" (api-token, account-id)
#     "OpenAI API" (api key)

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

# ── Pull credentials from 1Password ──

echo "Pulling credentials from 1Password..."

OP_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token)

CF_API_TOKEN=$(OP_SERVICE_ACCOUNT_TOKEN="$OP_TOKEN" op item get "Parker - Cloudflare Memory Crystal Keys" \
  --vault="Agent Secrets" --fields label=api-token --reveal)

CF_ACCOUNT_ID=$(OP_SERVICE_ACCOUNT_TOKEN="$OP_TOKEN" op item get "Parker - Cloudflare Memory Crystal Keys" \
  --vault="Agent Secrets" --fields label=account-id --reveal)

OPENAI_API_KEY=$(OP_SERVICE_ACCOUNT_TOKEN="$OP_TOKEN" op item get "OpenAI API" \
  --vault="Agent Secrets" --fields label="api key" --reveal)

if [[ "$CF_API_TOKEN" == "REPLACE_WITH_CLOUDFLARE_API_TOKEN" || "$CF_ACCOUNT_ID" == "REPLACE_WITH_CLOUDFLARE_ACCOUNT_ID" ]]; then
  echo "Error: Cloudflare credentials not yet filled in 1Password."
  echo "Update 'Parker - Cloudflare Memory Crystal Keys' in Agent Secrets vault."
  exit 1
fi

export CLOUDFLARE_API_TOKEN="$CF_API_TOKEN"
export CLOUDFLARE_ACCOUNT_ID="$CF_ACCOUNT_ID"

echo "  Cloudflare Account ID: ${CF_ACCOUNT_ID:0:8}..."
echo "  Cloudflare API Token: ${CF_API_TOKEN:0:8}..."
echo "  OpenAI API Key: ${OPENAI_API_KEY:0:8}..."

# ── Deploy only? ──

if [[ "${1:-}" == "deploy" ]]; then
  echo ""
  echo "Building and deploying Worker..."
  npm run build:cloud
  npx wrangler deploy --config wrangler-mcp.toml
  echo "Done. Worker deployed."
  exit 0
fi

# ── Full setup (first time) ──

echo ""
echo "=== Step 1: Create D1 database ==="

# Check if database already exists
DB_ID=$(npx wrangler d1 list --json 2>/dev/null | python3 -c "
import sys, json
dbs = json.load(sys.stdin)
for db in dbs:
    if db['name'] == 'memory-crystal-cloud':
        print(db['uuid'])
        break
" 2>/dev/null || echo "")

if [[ -z "$DB_ID" ]]; then
  echo "Creating D1 database: memory-crystal-cloud"
  DB_OUTPUT=$(npx wrangler d1 create memory-crystal-cloud 2>&1)
  DB_ID=$(echo "$DB_OUTPUT" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1)
  echo "  Created: $DB_ID"
else
  echo "  Already exists: $DB_ID"
fi

if [[ -z "$DB_ID" ]]; then
  echo "Error: Could not get D1 database ID"
  exit 1
fi

# Update wrangler-mcp.toml with database ID
if grep -q 'database_id = ""' wrangler-mcp.toml; then
  sed -i.bak "s/database_id = \"\"/database_id = \"$DB_ID\"/" wrangler-mcp.toml
  rm -f wrangler-mcp.toml.bak
  echo "  Updated wrangler-mcp.toml with database_id"
fi

echo ""
echo "=== Step 2: Create Vectorize index ==="

VEC_EXISTS=$(npx wrangler vectorize list --json 2>/dev/null | python3 -c "
import sys, json
indexes = json.load(sys.stdin)
for idx in indexes:
    if idx['name'] == 'memory-crystal-chunks':
        print('yes')
        break
" 2>/dev/null || echo "")

if [[ "$VEC_EXISTS" != "yes" ]]; then
  echo "Creating Vectorize index: memory-crystal-chunks (1024 dims, cosine)"
  npx wrangler vectorize create memory-crystal-chunks --dimensions 1024 --metric cosine
  echo "  Created."
else
  echo "  Already exists."
fi

echo ""
echo "=== Step 3: Run D1 migrations ==="

npx wrangler d1 migrations apply memory-crystal-cloud --config wrangler-mcp.toml
echo "  Migrations applied."

echo ""
echo "=== Step 4: Set Worker secrets ==="

echo "$OPENAI_API_KEY" | npx wrangler secret put OPENAI_API_KEY --config wrangler-mcp.toml
echo "  OPENAI_API_KEY set."

# Generate signing key for OAuth tokens
MCP_SIGNING_KEY=$(openssl rand -hex 32)
echo "$MCP_SIGNING_KEY" | npx wrangler secret put MCP_SIGNING_KEY --config wrangler-mcp.toml
echo "  MCP_SIGNING_KEY set (generated)."

# Generate relay encryption key (base64, 32 bytes)
RELAY_KEY=$(openssl rand -base64 32)
echo "$RELAY_KEY" | npx wrangler secret put RELAY_ENCRYPTION_KEY --config wrangler-mcp.toml
echo "  RELAY_ENCRYPTION_KEY set (generated)."

echo ""
echo "=== Step 5: Build and deploy ==="

npm run build:cloud
npx wrangler deploy --config wrangler-mcp.toml

echo ""
echo "=== Done ==="
echo ""
echo "Memory Crystal Cloud MCP server deployed."
echo "Worker URL: https://memory-crystal-cloud.<your-subdomain>.workers.dev"
echo ""
echo "Next steps:"
echo "  1. Test: curl https://memory-crystal-cloud.<subdomain>.workers.dev/health"
echo "  2. Test OAuth: GET /.well-known/oauth-authorization-server"
echo "  3. Connect from ChatGPT or Claude"
