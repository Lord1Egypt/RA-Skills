# @stellar/mpp charge mode — wire format

Source: local SDK at `/Users/happyfish/workspace/stellar/stellar-mpp-sdk`.
- Schema: `sdk/src/charge/Methods.ts`
- Client: `sdk/src/charge/client/Charge.ts`
- Server: `sdk/src/charge/server/Charge.ts`

Package: `@stellar/mpp`. Peers: `@stellar/stellar-sdk ^14.6.1`, `mppx ^0.4.11`.

## Request shape (server → client, 402 body)

Wrapped by `mppx` framework. The relevant `stellar.charge` method fields:

```ts
{
  recipient: "G...",         // destination pubkey
  currency: "USDC",          // or SAC contract address
  amount: "1.00",            // human decimal OR base-unit string
  network: "stellar:testnet",
  feePayer: true,            // sponsored mode (REQUIRED for x402 cross-compat)
  challenge: { nonce, expires }
}
```

## Credential shape (client → server)

Discriminated union:

```ts
type ChargeCredential =
  | { type: "transaction"; transaction: string /* base64 XDR */ }
  | { type: "hash"; hash: string /* tx hash after client-side broadcast */ }
```

- `transaction` mode — client builds and partially signs, server broadcasts (pull).
- `hash` mode — client broadcasts itself, sends only the hash (push).

**For cross-compat with x402, use `transaction` mode + `feePayer: true`.** This is the only flow where:
- Source account is `ALL_ZEROS`
- Only auth entries are signed (via `authorizeEntry`)
- The envelope is left for the server to fee-bump / rebuild

See `Charge.ts:122-199` for the exact branch.

## Outer envelope (`mppx.Credential`)

The `@stellar/mpp/charge/client` output is wrapped in an `mppx` Credential envelope before being sent. That envelope includes:

- `type: 'transaction'`
- `transaction: <base64 XDR>`
- Source DID (`did:pkh:stellar:<network>:<pubkey>`)
- Challenge binding (nonce + expiry echo)

## Key difference vs x402

| Aspect | x402 exact | mpp charge |
|---|---|---|
| Outer envelope | `{ x402Version, payload: { transaction } }` | `mppx.Credential` with DID + challenge |
| Field names | `payTo`, `asset`, `amount` | `recipient`, `currency`, `amount` |
| Transport | `X-Payment` header (base64) | `mppx` protocol (stream/body) |
| Sponsored flag | `extra.areFeesSponsored` | `feePayer` |
| Inner XDR | **IDENTICAL** — same SAC transfer + auth-entry signing | **IDENTICAL** |

**The inner XDR is the same.** A single signer can produce both envelopes.

## Imports

```typescript
import { stellar } from "@stellar/mpp/charge/client";
import { Mppx } from "mppx/client";
import { resolveKeypair } from "@stellar/mpp";
```
