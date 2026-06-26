#!/usr/bin/env bash
set -euo pipefail

# Minimal smoke test for Sure API.
# - Confirms base URL reachable
# - Calls /api/v1/accounts

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQ="$DIR/sure_api_request.sh"

echo "[1/2] GET /api/v1/accounts"
"$REQ" GET /api/v1/accounts | head -c 1200
echo

echo "[2/2] done"
