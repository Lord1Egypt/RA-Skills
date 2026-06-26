#!/usr/bin/env bash
# Smoke-check the rustok-wallet image: an MCP `initialize` round-trip over stdio.
# Requires Docker, the image present, a created wallet volume, and the password.
#
#   RUSTOK_KEYRING_PASSWORD=... ./health-check.sh
set -euo pipefail

IMAGE="${RUSTOK_WALLET_IMAGE:-ghcr.io/rustok-org/rustok-wallet:latest}"

echo "Checking ${IMAGE} responds to MCP initialize over stdio..."
resp=$(printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"capabilities":["read_wallet"]}}' \
  | docker run -i --rm --init \
      -v rustok-wallet:/data \
      -e RUSTOK_KEYRING_PASSWORD \
      -e RUSTOK_MCP_API_KEY \
      "${IMAGE}" 2>/dev/null | head -n 1)

if echo "${resp}" | grep -q '"serverInfo"'; then
    echo "OK — wallet MCP responded: ${resp}"
else
    echo "FAILED — no MCP response." >&2
    echo "  Run onboarding first (create-wallet) and set RUSTOK_KEYRING_PASSWORD." >&2
    exit 1
fi
