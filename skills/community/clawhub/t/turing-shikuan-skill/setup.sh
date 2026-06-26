#!/bin/bash

set -euo pipefail

MCP_NAME="turing-shikuan-mcp"
MCP_URL="https://turing-mcp-server-test.turingsenseai.com/mcp"

API_KEY="${TURING_SHIKUAN_API_KEY:-${TURING_API_KEY:-}}"
API_SECRET="${TURING_SHIKUAN_API_SECRET:-${TURING_API_SECRET:-}}"

echo "Setting up ${MCP_NAME}..."
echo

if ! command -v mcporter >/dev/null 2>&1; then
  echo "mcporter not found. Installing mcporter..."
  npm install -g mcporter
  echo "mcporter installed."
fi

echo "Checking API credentials..."
if [ -z "${API_KEY}" ] || [ -z "${API_SECRET}" ]; then
  echo "Missing API credentials."
  echo "Please set one of the following variable pairs before running setup.sh:"
  echo
  echo "  export TURING_SHIKUAN_API_KEY=\"your_turing_api_key_here\""
  echo "  export TURING_SHIKUAN_API_SECRET=\"your_turing_api_secret_here\""
  echo
  echo "Or use the fallback names:"
  echo
  echo "  export TURING_API_KEY=\"your_turing_api_key_here\""
  echo "  export TURING_API_SECRET=\"your_turing_api_secret_here\""
  exit 1
fi
echo "API credentials detected."
echo

echo "Registering ${MCP_NAME} with mcporter..."
mcporter config add "${MCP_NAME}" "${MCP_URL}" \
  --header "x-api-key=${API_KEY}" \
  --header "x-api-secret=${API_SECRET}" \
  --scope project
echo "Registration completed."
echo

echo "Verifying configuration..."
if mcporter list 2>&1 | grep -q "${MCP_NAME}"; then
  echo "Configuration verified."
  echo
  mcporter list | grep -A 1 "${MCP_NAME}" || true
else
  echo "Configuration was added, but verification did not find ${MCP_NAME}."
  echo "Please refresh the MCP list or restart the client and check again."
fi
