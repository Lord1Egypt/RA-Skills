#!/usr/bin/env bash
set -euo pipefail

# SafeFlow Solana — Agent Bootstrap Script
# Generates an agent keypair and prints owner handoff instructions.

PROGRAM_ID="DwYEDn6xRpSbnNA7mkszQgDAUoHGfgdBNSi6pwy4qJKy"
CLUSTER="devnet"
CONFIG_DIR=".safeflow"

while [[ $# -gt 0 ]]; do
  case $1 in
    --program-id) PROGRAM_ID="$2"; shift 2 ;;
    --cluster) CLUSTER="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

mkdir -p "$CONFIG_DIR"

KEYPAIR_FILE="$CONFIG_DIR/agent-keypair.json"

if [ -f "$KEYPAIR_FILE" ]; then
  echo "[bootstrap] Agent keypair already exists at $KEYPAIR_FILE"
else
  solana-keygen new --no-bip39-passphrase -o "$KEYPAIR_FILE" --force
  echo "[bootstrap] Generated new agent keypair at $KEYPAIR_FILE"
fi

AGENT_ADDRESS=$(solana-keygen pubkey "$KEYPAIR_FILE")

cat > "$CONFIG_DIR/config.json" <<EOF
{
  "programId": "$PROGRAM_ID",
  "cluster": "$CLUSTER",
  "agentAddress": "$AGENT_ADDRESS",
  "keypairPath": "$KEYPAIR_FILE"
}
EOF

echo ""
echo "============================================"
echo "  SafeFlow Solana — Agent Bootstrap Complete"
echo "============================================"
echo ""
echo "Agent Address : $AGENT_ADDRESS"
echo "Program ID    : $PROGRAM_ID"
echo "Cluster       : $CLUSTER"
echo "Keypair       : $KEYPAIR_FILE"
echo ""
echo "--- Owner Handoff Instructions ---"
echo ""
echo "1. Fund the agent with ~0.01 SOL for gas:"
echo "   solana transfer $AGENT_ADDRESS 0.01 --url $CLUSTER"
echo ""
echo "2. Open the SafeFlow dashboard and:"
echo "   - Connect your wallet"
echo "   - Enter agent address: $AGENT_ADDRESS"
echo "   - Set rate limit, total cap, and deposit amount"
echo "   - Click 'Create Wallet & Session'"
echo ""
echo "3. After setup, run:"
echo "   ./save_config.sh --wallet-owner <YOUR_PUBKEY>"
echo ""
