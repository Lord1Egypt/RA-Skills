#!/usr/bin/env bash
set -euo pipefail

# SafeFlow Solana — Execute Payment / Query Session
# Uses the SDK via ts-node to execute a payment or query session status.

CONFIG_DIR=".safeflow"
RECIPIENT=""
AMOUNT=""
EVIDENCE_ID=""
QUERY_MODE=false
WALLET_OWNER_OVERRIDE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --recipient) RECIPIENT="$2"; shift 2 ;;
    --amount) AMOUNT="$2"; shift 2 ;;
    --evidence-id) EVIDENCE_ID="$2"; shift 2 ;;
    --query) QUERY_MODE=true; shift ;;
    --wallet-owner) WALLET_OWNER_OVERRIDE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ ! -f "$CONFIG_DIR/config.json" ]; then
  echo "Error: $CONFIG_DIR/config.json not found. Run bootstrap.sh and save_config.sh first."
  exit 1
fi

# Run inline ts-node script
npx ts-node -e "
const fs = require('fs');
const { Connection, Keypair, PublicKey, LAMPORTS_PER_SOL } = require('@solana/web3.js');
const { BN } = require('@coral-xyz/anchor');

(async () => {
  const config = JSON.parse(fs.readFileSync('$CONFIG_DIR/config.json', 'utf8'));
  const idl = JSON.parse(fs.readFileSync('target/idl/safeflow_solana.json', 'utf8'));
  const keypairData = JSON.parse(fs.readFileSync(config.keypairPath, 'utf8'));
  const keypair = Keypair.fromSecretKey(Uint8Array.from(keypairData));

  const walletOwner = new PublicKey('${WALLET_OWNER_OVERRIDE}' || config.walletOwner);
  const clusterUrl = config.cluster === 'devnet'
    ? 'https://api.devnet.solana.com'
    : config.cluster === 'mainnet'
      ? 'https://api.mainnet-beta.solana.com'
      : 'http://localhost:8899';

  const { SafeFlowAgent } = require('./sdk/src/agent');
  const agent = new SafeFlowAgent({
    connection: new Connection(clusterUrl, 'confirmed'),
    programId: new PublicKey(config.programId),
    keypair,
    idl,
  });

  if (${QUERY_MODE}) {
    const session = await agent.getSessionInfo(walletOwner);
    const vault = await agent.getVaultBalance(walletOwner);
    console.log('Session Status:');
    console.log('  Active        :', session.isActive);
    console.log('  Remaining     :', session.remainingBudget.toString(), 'lamports');
    console.log('  Total Spent   :', session.totalSpent.toString(), 'lamports');
    console.log('  Max Total     :', session.maxSpendTotal.toString(), 'lamports');
    console.log('  Rate Limit    :', session.maxSpendPerSecond.toString(), 'lamports/s');
    console.log('  Expires At    :', new Date(session.expiresAt.toNumber() * 1000).toISOString());
    console.log('  Vault Balance :', vault / LAMPORTS_PER_SOL, 'SOL');
    return;
  }

  const recipient = '${RECIPIENT}';
  const amount = '${AMOUNT}';
  if (!recipient || !amount) {
    console.error('Usage: ./execute_payment.sh --recipient <ADDR> --amount <LAMPORTS>');
    process.exit(1);
  }

  const result = await agent.executePayment({
    walletOwner,
    recipient: new PublicKey(recipient),
    amount: new BN(amount),
    evidenceId: '${EVIDENCE_ID}' || '',
  });

  console.log('Payment executed successfully!');
  console.log('  TX Signature:', result.txSignature);
})().catch(err => {
  console.error('Payment failed:', err.message || err);
  process.exit(1);
});
"
