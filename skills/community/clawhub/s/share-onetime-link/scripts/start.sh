#!/bin/bash
# Start the share-onetime-link server
# Configure these variables before running:

export SHARE_PUBLIC_URL="${SHARE_PUBLIC_URL:-http://localhost:5050}"
export SHARE_PORT="${SHARE_PORT:-5050}"
export SHARE_SECRET="${SHARE_SECRET:-}"   # Recommended: set a strong random secret
# export SHARED_DIR="/custom/path/to/shared"   # Optional

if [ -z "$SHARE_SECRET" ]; then
  echo "[warn] SHARE_SECRET not set — /generate and /status are unprotected!"
fi

echo "Starting share server on port $SHARE_PORT"
echo "Public URL: $SHARE_PUBLIC_URL"

cd "$(dirname "$0")"
node server.js
