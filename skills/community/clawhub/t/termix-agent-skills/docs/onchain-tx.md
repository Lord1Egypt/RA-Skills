# On-chain transactions (tx-intents)

Some Provider actions require a real on-chain transaction. The backend never
broadcasts for you — its `*/prepare`, `*/deposit-intent`, `*/submit` endpoints
return an **unsigned tx-intent** that the wallet must sign and broadcast. The
backend already ABI-encodes the call, so you only sign + send.

## tx-intent shape

```json
{ "action": "submitDelivery", "chainId": 56,
  "contract": "0x…",  "callData": "0x…",  "value": "0",
  "id": "…", "status": "PREPARED", "nonceKey": "…" }
```

Agent-mint returns the same idea with slightly different keys
(`{ contract, callData, to, tokenUri, metadataHash, roles }`). The executor
accepts both `contract`/`to` and `callData`/`data`.

## Execute with `scripts/aacp-tx.mjs`

```bash
# single intent
WALLET_KEY=0x… node scripts/aacp-tx.mjs --intent '<intent-json>'

# several intents in order (e.g. approve then deposit) — nonce auto-increments
WALLET_KEY=0x… node scripts/aacp-tx.mjs --intents '[<intent1>,<intent2>]'

# preview only, no broadcast (show the user before signing)
node scripts/aacp-tx.mjs --intent '<intent-json>' --dry-run
```

Output: `{ from, chainId, results:[{ action, txHash, status:"success", blockNumber, nonce }] }`.
The script estimates gas (+20%), fetches EIP-1559 fees (floored to the network
`eth_gasPrice` so BSC does not underprice), waits for the receipt, and **fails
loudly if the tx reverts**.

## After broadcast — let the indexer confirm

DB state is updated by the indexer from the on-chain event, NOT by broadcasting.
Poll the matching read endpoint until it flips:

| Action | Confirm / poll |
|---|---|
| Agent mint (`registerAgent`) | `GET /api/v1/agents/by-tx/:txHash` → `status: "CONFIRMED"` |
| Any tx-intent | `GET /api/v1/onchain/tx/:txHash` (generic indexer status) |
| Checkout `createOrder` | `POST /api/v1/checkout/:id/confirm { txHash }` |
| Campaign fund | `POST /api/v1/campaigns/:id/confirm-funded { txHash }` |
| Delivery / dispute settle | re-read `GET /api/v1/orders/:id` / `GET /api/v1/disputes/:id` until status changes |

## Rules

1. **Confirm with the user before broadcasting** any value-bearing tx (mint gas,
   USDC approve/deposit/escrow). Use `--dry-run` to show the plan first.
2. Never print `WALLET_KEY` or full tokens.
3. Do **not** re-broadcast the same intent on timeout — poll
   `GET /api/v1/onchain/tx/:txHash` and trust the receipt. tx-intents are
   idempotent server-side (`nonceKey`); re-calling the prepare endpoint reuses
   the same intent.
4. **Funding**: the wallet needs BNB for gas and USDC for
   staking / escrow. A bare wallet with no BNB cannot broadcast anything.
5. USDC amounts in API bodies are decimal display units (`"15"`); the backend
   encodes the 6-decimal raw units into `callData`.
