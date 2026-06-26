# Integration Guide — Payout to External Wallet

## Overview

When your service needs to send USDC to an external wallet address on Base chain (withdrawals, settlements to non-agent wallets, etc.), use the **Payout** function.

## When to Use

- Recipient is a **wallet address** (0x...) → use Payout (this guide)
- Recipient is an **AI agent** (Agent ID) → use [INTEGRATION-GUIDE-PAY-TO-AGENT.md](INTEGRATION-GUIDE-PAY-TO-AGENT.md)

## Usage

```bash
fluxa-wallet payout \
  --to "0x4eb5b229d43c30fc629d92bf7ed415d6d7f0cabe" \
  --amount "1000000" \
  --id "settlement_20260320_001"
```

Each payout requires individual user authorization via an approval URL. There is no mandate-based autonomy for payouts.

For the complete payout flow (create, approve, poll status), see [PAYOUT.md](PAYOUT.md).
