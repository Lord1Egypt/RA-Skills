#!/bin/bash
# Web3 Investor MCP Client Wrapper
# Usage:
#   ./run.sh discover --chain ethereum --min-apy 5
#   ./run.sh analyze --product-id <uuid> --depth detailed
#   ./run.sh compare --ids <uuid1> <uuid2>
#   ./run.sh feedback --product-id <uuid> --feedback helpful
#   ./run.sh confirm-intent --session-id xxx --type stablecoin --risk moderate
#   ./run.sh get-intent --session-id xxx

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

exec python3 scripts/mcp_client.py "$@"
