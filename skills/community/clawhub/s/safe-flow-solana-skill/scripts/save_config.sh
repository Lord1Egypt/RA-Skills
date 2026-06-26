#!/usr/bin/env bash
set -euo pipefail

# SafeFlow Solana — Save Owner Config
# Stores the wallet owner pubkey so the agent knows which wallet to operate on.

CONFIG_DIR=".safeflow"
WALLET_OWNER=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --wallet-owner) WALLET_OWNER="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$WALLET_OWNER" ]; then
  echo "Usage: ./save_config.sh --wallet-owner <OWNER_PUBKEY>"
  exit 1
fi

if [ ! -f "$CONFIG_DIR/config.json" ]; then
  echo "Error: $CONFIG_DIR/config.json not found. Run bootstrap.sh first."
  exit 1
fi

# Update config with wallet owner using a portable approach
TMP_FILE=$(mktemp)
node -e "
  const fs = require('fs');
  const cfg = JSON.parse(fs.readFileSync('$CONFIG_DIR/config.json', 'utf8'));
  cfg.walletOwner = '$WALLET_OWNER';
  fs.writeFileSync('$CONFIG_DIR/config.json', JSON.stringify(cfg, null, 2));
"

echo "[save_config] Wallet owner saved: $WALLET_OWNER"
echo "[save_config] Config file: $CONFIG_DIR/config.json"
cat "$CONFIG_DIR/config.json"
