#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || -z "${1:-}" ]]; then
  echo "Usage: $0 <x-api-key>"
  exit 1
fi

KEY="$1"
CONF_DIR="$HOME/.config/seedream5.0"
CONF_FILE="$CONF_DIR/.env"

mkdir -p "$CONF_DIR"
cat > "$CONF_FILE" <<EOF
X_API_KEY=$KEY
EOF
chmod 600 "$CONF_FILE"

echo "x-api-key saved to $CONF_FILE"
