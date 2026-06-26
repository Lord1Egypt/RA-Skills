# x402 Stellar "exact" scheme — wire format

Source: `x402-foundation/x402` — `typescript/packages/mechanisms/stellar/src/exact/client/scheme.ts` and `specs/schemes/exact/scheme_exact_stellar.md`.

Package: `@x402/stellar` v2.9.0. Peer: `@stellar/stellar-sdk ^14.6.1`.

## PaymentRequirements (server → client, in 402 body)

```json
{
  "scheme": "exact",
  "network": "stellar:testnet",
  "amount": "10000000",
  "asset": "C...",
  "payTo": "G...",
  "maxTimeoutSeconds": 60,
  "extra": { "areFeesSponsored": true }
}
```

- `network` — CAIP-2 (`stellar:testnet` | `stellar:pubnet`)
- `amount` — base units as `i128` decimal string (USDC has 7 decimals)
- `asset` — SEP-41 Soroban token contract (SAC) address
- `payTo` — destination `G...` pubkey
- `maxTimeoutSeconds` — used to derive auth-entry `expiration` ledger
- `extra.areFeesSponsored` — **MUST be `true`**. Current spec only supports sponsored mode.

## PaymentPayload (client → server, in `X-Payment` header)

```json
{
  "x402Version": 1,
  "scheme": "exact",
  "network": "stellar:testnet",
  "payload": { "transaction": "<base64 XDR>" }
}
```

The whole object is base64-encoded and placed in the `X-Payment` HTTP header.

## Inner transaction (the XDR)

1. Build a Soroban `invokeHostFunction` op calling `transfer(from=signer.address, to=payTo, amount=i128)` on the SAC contract.
2. Source account: `ALL_ZEROS` placeholder (facilitator rebuilds).
3. Sign **auth entries only** via `tx.signAuthEntries(...)` where `expiration = currentLedger + ceil(maxTimeoutSeconds / estimatedLedgerSeconds)`.
4. Do **not** sign the transaction envelope.
5. Export with `tx.built!.toXDR()`.

## Client entry point

```typescript
import { x402Client } from "@x402/core/client";
import { createEd25519Signer } from "@x402/stellar";
import { ExactStellarScheme } from "@x402/stellar/exact/client";

const signer = createEd25519Signer(privateKey, "stellar:testnet");
const client = new x402Client().register("stellar:*", new ExactStellarScheme(signer));
```

Scheme method:

```typescript
async createPaymentPayload(
  x402Version: number,
  paymentRequirements: PaymentRequirements,
): Promise<Pick<PaymentPayload, "x402Version" | "payload">>
// returns { x402Version, payload: { transaction: tx.built!.toXDR() } }
```

## Ledger close time

Spec: query `getEstimatedLedgerCloseTimeSeconds(network)` live. Fallback to **5 seconds** if RPC unreachable. Both testnet and pubnet are ~5s in practice.
