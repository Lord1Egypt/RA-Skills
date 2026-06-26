# Why sponsored mode is the only cross-compatible path

## The constraint

Both `@stellar/mpp` charge mode and x402 Stellar exact support paying for SAC transfers. But only **one** code path produces a transaction XDR that works for both:

> **Source account = `ALL_ZEROS`, envelope unsigned, only Soroban auth entries signed.**

This is called **"sponsored mode"** (MPP) or **"fees sponsored"** (x402). It is the only way a facilitator / server can:

1. Rebuild the transaction with its own source account
2. Apply its own fee bump
3. Submit without the client paying gas

## Why unsponsored breaks x402

If the client signs the full transaction envelope with its own source:

- The envelope commits to that source account. Changing it invalidates all signatures.
- The x402 facilitator cannot rebuild or fee-bump the transaction.
- x402 spec §4 forbids the facilitator from replacing a non-zero source account (signature safety rule).
- `extra.areFeesSponsored: true` is **required** by the current x402 Stellar exact spec.

## Why unsponsored works in MPP alone

The local MPP SDK `charge/client/Charge.ts` has two code paths:

- **Lines 122-199: sponsored** (`feePayer === true`) — signs only auth entries, source is `ALL_ZEROS`. ✅ x402 compatible.
- **Lines 201-268: unsponsored** (`feePayer === false`) — signs the full envelope, source is the client. ❌ not x402 compatible.

If a user says "I don't want sponsored mode":

1. Warn them: "This will break x402 compatibility. The scaffolded client will only work against MPP servers, not x402 facilitators."
2. Ask: "Proceed anyway?"
3. If yes, generate only the MPP adapter, skip the x402 adapter, and note this clearly in the output summary.

## Signing recipe (the right way)

```typescript
import {
  Address,
  Contract,
  Networks,
  Operation,
  rpc,
  TransactionBuilder,
  authorizeEntry,
  nativeToScVal,
  xdr,
} from "@stellar/stellar-sdk";

// 1. Placeholder source — ALL_ZEROS (56-char Stellar strkey for 32 zero bytes)
const ALL_ZEROS = "GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWHF";
const sourceAccount = new Account(ALL_ZEROS, "0");

// 2. Build SAC transfer invocation
const contract = new Contract(assetSacAddress);
const op = contract.call(
  "transfer",
  nativeToScVal(Address.fromString(signerPubkey), { type: "address" }),
  nativeToScVal(Address.fromString(payTo), { type: "address" }),
  nativeToScVal(amountBaseUnits, { type: "i128" }),
);

// 3. Simulate to populate auth + Soroban data
const tx = new TransactionBuilder(sourceAccount, { fee: "0", networkPassphrase })
  .addOperation(op)
  .setTimeout(180)
  .build();
const sim = await rpc.simulateTransaction(tx);

// 4. Compute expiration ledger
const latestLedger = sim.latestLedger;
const ledgerCloseSeconds = 5; // or query getEstimatedLedgerCloseTimeSeconds
const validUntilLedger = latestLedger + Math.ceil(maxTimeoutSeconds / ledgerCloseSeconds);

// 5. Sign EACH auth entry with authorizeEntry — NOT the envelope
const signedAuthEntries = await Promise.all(
  sim.result.auth.map((entry) =>
    authorizeEntry(entry, signerKeypair, validUntilLedger, networkPassphrase),
  ),
);

// 6. Replace auth entries in the operation and rebuild
// (see stellar-mpp-sdk/sdk/src/charge/client/Charge.ts:160-190 for exact reconstruction)
// Export: tx.toXDR() — this is the base64 string that goes into BOTH envelopes.
```

## Never do this in sponsored mode

```typescript
// ❌ WRONG — signs the envelope
tx.sign(signerKeypair);

// ❌ WRONG — uses a real source account
const sourceAccount = await rpc.getAccount(signerPubkey);
```
