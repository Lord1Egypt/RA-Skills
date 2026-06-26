---
name: snap-private-payments
description: Private agent-to-agent payments on Solana using zero-knowledge proofs. Deposit, withdraw, list pools, and estimate fees.
version: 0.1.1
tags:
  - solana
  - privacy
  - zk-proofs
  - payments
  - agents
metadata:
  openclaw:
    env:
      - SNAP_POOL_ADDRESS
      - SNAP_RPC_URL
    optional_env:
      - SNAP_RELAYER_URL
    install: npm install snap-solana-sdk
---

# SNAP Private Payment Skill

Make private payments on Solana using zero-knowledge proofs.
Other agents and on-chain observers cannot see who you paid.

## Commands

### List SNAP pools
"List SNAP pools"
"Show private payment pools"

### Deposit into shielded pool
"Deposit [amount] into the SNAP privacy pool"
"Shield [amount] SOL privately"

### Withdraw from shielded pool
"Withdraw from SNAP pool to [address]"
"Claim my private payment"

### Estimate withdrawal fee
"Estimate SNAP withdrawal fee"
"What will this SNAP withdrawal cost?"

### Check shielded balance
"What's in my SNAP pool?"
"Show my private balance"

## Setup
npm install snap-solana-sdk

## Configuration
SNAP_POOL_ADDRESS=B8SyffZKt8LABKogWjH9rZcjY5PV2hyYRCbTxxbcrpFf
SNAP_RPC_URL=https://api.mainnet-beta.solana.com
SNAP_RELAYER_URL=<optional_relayer_url>

## Links
- GitHub: https://github.com/agentzeny/snap-public
- SDK: https://www.npmjs.com/package/snap-solana-sdk
- Website: https://agentzeny.ai
