#!/usr/bin/env bash
set -euo pipefail

# Example only. Review the target repo before use.
REPO_DIR="${1:-$HOME/.openclaw/mcp/st-ent-mcp}"
BASE_URL="${SERVICE_API_BASE_URL:-https://co-api.699pic.com}"
API_KEY="${SERVICE_API_KEY:-}"
REVIEWED="${ST_ENT_MCP_REVIEWED:-}"

if ! command -v git >/dev/null 2>&1; then
  echo "git is required but was not found in PATH" >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "node is required but was not found in PATH" >&2
  exit 1
fi

if ! command -v mcporter >/dev/null 2>&1; then
  echo "mcporter is required but was not found in PATH" >&2
  exit 1
fi

if [ "$REVIEWED" != "1" ]; then
  echo "Refusing to run before repo audit. Review the source, then set ST_ENT_MCP_REVIEWED=1." >&2
  exit 1
fi

if [ -z "$API_KEY" ]; then
  echo "SERVICE_API_KEY is required" >&2
  exit 1
fi

if [ ! -d "$REPO_DIR/.git" ]; then
  git clone https://github.com/st699pic/st-ent-mcp "$REPO_DIR"
else
  git -C "$REPO_DIR" pull --ff-only
fi

# Starts the server briefly for a local smoke check after audit.
node "$REPO_DIR/mcp/server.js" </dev/null >/tmp/st-ent-mcp-smoke.out 2>/tmp/st-ent-mcp-smoke.err &
PID=$!
sleep 1
kill "$PID" >/dev/null 2>&1 || true

mcporter config add st-ent-mcp \
  --command node \
  --arg "$REPO_DIR/mcp/server.js" \
  --env "SERVICE_API_BASE_URL=$BASE_URL" \
  --env "SERVICE_API_KEY=$API_KEY" \
  --scope project

echo "Installed/registered st-ent-mcp from: $REPO_DIR"
echo "Next: mcporter list st-ent-mcp --schema"
