#!/bin/bash
# scaffold.sh — Generate an x402 pay-per-call endpoint project
# Usage: bash scaffold.sh <name> <description> <price_usdc>

set -euo pipefail

NAME="${1:?Usage: scaffold.sh <name> <description> <price_usdc>}"
DESC="${2:-My x402 API}"
PRICE="${3:-0.01}"
DIR="./$NAME"

if [ -d "$DIR" ]; then
    echo "❌ Directory $DIR already exists"
    exit 1
fi

echo "🚀 Scaffolding x402 endpoint: $NAME"
mkdir -p "$DIR"

# package.json
cat > "$DIR/package.json" << EOF
{
  "name": "$NAME",
  "version": "1.0.0",
  "description": "$DESC",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.21.0",
    "ethers": "^6.13.0"
  }
}
EOF

# .env
cat > "$DIR/.env" << EOF
# x402 Configuration
WALLET_ADDRESS=0xYOUR_BASE_WALLET_ADDRESS
USDC_CONTRACT=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
CHAIN_ID=8453
PORT=3402
PRICE_USDC=$PRICE
BASE_RPC=https://mainnet.base.org
EOF

# server.js
cat > "$DIR/server.js" << 'SERVEREOF'
require("dotenv").config();
const express = require("express");
const { ethers } = require("ethers");

const app = express();
app.use(express.json());

const {
  WALLET_ADDRESS,
  USDC_CONTRACT,
  CHAIN_ID,
  PORT = 3402,
  PRICE_USDC = "0.01",
  BASE_RPC = "https://mainnet.base.org",
} = process.env;

const provider = new ethers.JsonRpcProvider(BASE_RPC);

// USDC has 6 decimals
const priceWei = ethers.parseUnits(PRICE_USDC, 6);

// ERC-20 Transfer event
const TRANSFER_TOPIC = ethers.id("Transfer(address,address,uint256)");

async function verifyPayment(txHash) {
  try {
    const receipt = await provider.getTransactionReceipt(txHash);
    if (!receipt || receipt.status !== 1) return false;

    for (const log of receipt.logs) {
      if (
        log.address.toLowerCase() === USDC_CONTRACT.toLowerCase() &&
        log.topics[0] === TRANSFER_TOPIC
      ) {
        const to = ethers.getAddress("0x" + log.topics[2].slice(26));
        const amount = BigInt(log.data);
        if (
          to.toLowerCase() === WALLET_ADDRESS.toLowerCase() &&
          amount >= priceWei
        ) {
          return true;
        }
      }
    }
    return false;
  } catch {
    return false;
  }
}

// Track used tx hashes to prevent replay
const usedTxHashes = new Set();

// x402 middleware
function x402Middleware(req, res, next) {
  const txHash = req.headers["x-payment-tx"] || req.query.tx;

  if (!txHash) {
    return res.status(402).json({
      error: "Payment Required",
      price: `${PRICE_USDC} USDC`,
      currency: "USDC",
      network: "base",
      chainId: parseInt(CHAIN_ID),
      payTo: WALLET_ADDRESS,
      token: USDC_CONTRACT,
      instructions:
        "Send USDC to payTo address on Base, then retry with X-Payment-Tx header",
    });
  }

  if (usedTxHashes.has(txHash.toLowerCase())) {
    return res.status(402).json({ error: "Transaction already used" });
  }

  verifyPayment(txHash).then((valid) => {
    if (valid) {
      usedTxHashes.add(txHash.toLowerCase());
      next();
    } else {
      res.status(402).json({
        error: "Payment not verified",
        hint: "Ensure USDC was sent to the correct address on Base",
      });
    }
  });
}

// Health endpoint (free)
app.get("/health", (req, res) => {
  res.json({ status: "ok", service: process.env.npm_package_name || "x402-service" });
});

// Pricing endpoint (free)
app.get("/pricing", (req, res) => {
  res.json({
    price: `${PRICE_USDC} USDC`,
    network: "base",
    chainId: parseInt(CHAIN_ID),
    payTo: WALLET_ADDRESS,
    token: USDC_CONTRACT,
  });
});

// === YOUR ENDPOINTS GO HERE ===
// Add x402Middleware to any route that requires payment

app.get("/api/data", x402Middleware, (req, res) => {
  // Replace this with your actual service logic
  res.json({
    message: "Payment verified! Here's your data.",
    timestamp: new Date().toISOString(),
    // Add your data here
  });
});

// ==============================

app.listen(PORT, () => {
  console.log(`x402 endpoint live on http://localhost:${PORT}`);
  console.log(`Price: ${PRICE_USDC} USDC on Base`);
  console.log(`Wallet: ${WALLET_ADDRESS}`);
});
SERVEREOF

# dotenv dependency
cat > "$DIR/.gitignore" << EOF
node_modules/
.env
EOF

# Install dotenv too
cd "$DIR"
cat package.json | python3 -c "
import sys, json
p = json.load(sys.stdin)
p['dependencies']['dotenv'] = '^16.4.0'
json.dump(p, sys.stdout, indent=2)
" > package.json.tmp && mv package.json.tmp package.json

echo ""
echo "✅ x402 endpoint scaffolded at $DIR/"
echo ""
echo "Next steps:"
echo "  1. Edit $DIR/.env — set your WALLET_ADDRESS"
echo "  2. cd $DIR && npm install"
echo "  3. node server.js"
echo "  4. Test: curl http://localhost:3402/pricing"
echo "  5. Deploy: cloudflared tunnel --url http://localhost:3402"
