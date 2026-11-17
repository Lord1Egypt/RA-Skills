# Inspect, authorize, and submit

Read [custody-and-settlement.md](custody-and-settlement.md) first. The plan is public and contains exactly eight fields; it never contains a key, recipient, memo, calldata, slippage, or blockhash.

```json
{
  "stock": "AAPL",
  "side": "BUY",
  "order_type": "MARKET",
  "token_pair_name": "USDC-AAPLs",
  "offer_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "stock_mint": "<TRUSTED_AAPL_MINT>",
  "offer_amount_raw": "25000000",
  "request_amount_raw": "0"
}
```

MARKET request `0` means execution-determined with no on-chain minimum receive. A positive quoted request remains only an estimate. LIMIT requires a positive exact request and never calls an API.

Pipe the plan over standard input so the signer does not gain a general plan-file read capability:

```bash
printf '%s' '<PUBLIC_PLAN_JSON>' | \
  "$HOME/.local/share/swimmer-stock-trading/venv/bin/python" \
  "<SKILL_DIR>/scripts/solana_sign_send.py" inspect
```

Present the complete JSON summary. It includes the fixed destination, mint, raw amount, configured cap, settlement model, whether receipt is unknown, explicit warning, authorization text, and `confirmation_id`. Ask the user to authorize that exact irreversible custodial transfer and digest.

After explicit confirmation, send the identical plan:

```bash
printf '%s' '<IDENTICAL_PUBLIC_PLAN_JSON>' | \
  "$HOME/.local/share/swimmer-stock-trading/venv/bin/python" \
  "<SKILL_DIR>/scripts/solana_sign_send.py" send \
  --confirm '<CONFIRMED_CONFIRMATION_ID>'
```

The signer gets a fresh mainnet blockhash after confirmation, constructs the transaction locally, simulates with signature verification, and broadcasts with preflight. Plans never contain stale blockhashes or API calldata. Treat the returned signature as submitted, not settled. Before retrying, inspect the original signature and custodial order status.
