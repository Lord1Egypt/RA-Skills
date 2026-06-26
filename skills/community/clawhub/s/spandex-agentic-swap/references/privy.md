# Privy Interop Notes

Technical requirements for executing spanDEX swap steps via Privy's wallet RPC.

## Transaction payload

When passing `steps[].params` to Privy's `eth_sendTransaction`:

- **`value` must be a hex string** — e.g. `"0x0"`, not `0` or `"0"`. Privy will reject non-hex values.
- All other fields (`from`, `to`, `data`) pass through as-is from the spanDEX response.

## Receipt polling

Privy's wallet RPC does not support `eth_getTransactionReceipt`. After submitting a transaction, poll a public Base RPC endpoint directly:

```bash
curl -sS https://mainnet.base.org \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params":["0x<txhash>"],"id":1}'
```

| `result` value | Meaning |
| --- | --- |
| `null` | Transaction is still pending — keep polling |
| `{ "status": "0x1", ... }` | Confirmed successfully |
| `{ "status": "0x0", ... }` | Transaction reverted — do not proceed |

One confirmation is sufficient on Base.

## Partial failure

If the approval transaction confirms but the swap transaction reverts:

- Tell the user clearly: the approval is onchain, but no tokens were swapped
- Do not retry the approval — it is already approved
- Offer to fetch a fresh quote and retry the swap step only
