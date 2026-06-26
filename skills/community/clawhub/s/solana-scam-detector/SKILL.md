---
name: solana-scam-detector
description: Detect scam tokens on Solana before you trade. Checks ticker patterns, token age, and known scam mints. Read-only — no wallet signing required.
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["node"], "modules": ["@solana/web3.js"] },
      "env": { "RPC_URL": "Solana RPC endpoint (optional, default: public RPC)" }
    },
  }
---

# Solana Scam Detector

Read-only scam detection for Solana tokens. No wallet signing required.

## What It Does

- **Token Age Check** — Flags tokens younger than threshold
- **Ticker Pattern Check** — Flags fake stock tokens (META, AAPL, etc.)
- **Mint Blacklist** — Check against known scam mints

## Read-Only

This module **only reads blockchain data**. It does NOT:
- ❌ Require wallet key file
- ❌ Require Telegram ID
- ❌ Store trade history
- ❌ Send any transactions

## Installation

```bash
npm install @solana/web3.js
```

## Configuration

**Required:** None (uses default public RPC)

**Optional (agent can ask user):**
- `RPC_URL` — Custom RPC endpoint (default: public RPC)
- `MIN_TOKEN_AGE_HOURS` — Minimum hours (default: 4)

## Usage

```javascript
const { checkTokenSafety, isValidSolanaAddress } = require('./lib/scam_check.js');

// Validate address first
if (!isValidSolanaAddress(mint)) {
  console.log('Invalid address');
  return;
}

// Check token
const result = await checkTokenSafety(mint, symbol);
console.log(result);
// { safe: true, issues: [], config: {...} }
```

## Agent Instructions

**Keep it simple — this is read-only:**

1. Use default public RPC or ask user for their RPC URL
2. Optionally ask user for MIN_TOKEN_AGE_HOURS preference
3. Optionally allow user to add to BLACKLIST_EXACT / BLACKLIST_MINTS
4. Never ask for wallet key, Telegram ID, or trade history

## Files

- `lib/scam_check.js` — Main detection logic (read-only)
- `lib/config.js` — Minimal config (RPC URL only)
- `SKILL.md` — This file