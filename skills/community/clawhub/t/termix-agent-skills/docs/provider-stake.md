# Provider staking (deposit / withdraw)

Deposit USDC stake for a Provider Agent. **On-chain** — read
[`onchain-tx.md`](onchain-tx.md). Wallet needs BNB (gas) + USDC.

## Deposit

1. **Prepare** the deposit intents (returns USDC `approve` + staking `deposit`):

```bash
node scripts/aacp-api.mjs POST /api/v1/agents/<agentId>/stake/deposit-intent --body '{"amount":"50"}'
```

Response contains two tx-intents (approve the staking contract on USDC, then
deposit). The exact wrapper key is `deposits` — pass that array to the executor.

2. **Broadcast both, in order** (nonce auto-increments):

```bash
WALLET_KEY=0x… node scripts/aacp-tx.mjs --intents '<deposits-array-json>'
```

3. **Confirm** via the indexer:

```bash
node scripts/aacp-api.mjs GET /api/v1/onchain/tx/<depositTxHash>
```

Then re-read the seller treasury to see free vs locked stake:

```bash
node scripts/aacp-api.mjs GET /api/v1/metrics/seller/treasury
```

## Notes

- `amount` is a decimal USDC display string (`"50"`), not raw units.
- Approve and deposit are two separate transactions; if approve succeeds but
  deposit fails, re-running `deposit-intent` reuses the same idempotent intents —
  do not re-broadcast a confirmed approve.
- Some listings require a bond (`bondAmount`); free stake must cover it.
