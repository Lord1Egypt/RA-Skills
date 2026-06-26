---
name: signing-agent
skill: signing
description: Cryptographic message signing and verification across five standards — SIP-018 structured Clarity data, Stacks plain-text (SIWS), Bitcoin BIP-137/BIP-322 (legacy and native SegWit/Taproot), BIP-340 Schnorr for Taproot multisig, and Nostr event signing via NIP-06 key derivation.
---

# Signing Agent

This agent handles all cryptographic signing and verification for the AIBTC platform. It supports five signing standards: SIP-018 (on-chain verifiable structured data), Stacks plain-text (SIWS wallet authentication), Bitcoin BIP-137/BIP-322 (BIP-137 for legacy 1.../3... addresses, BIP-322 "simple" for native SegWit bc1q and Taproot bc1p addresses), BIP-340 Schnorr (Taproot script-path and multisig), and Nostr event signing using NIP-06 key derivation. Signing operations require an unlocked wallet; hash and verify operations do not.

## Prerequisites

- For signing operations (sip018-sign, stacks-sign, btc-sign, schnorr-sign-digest, nostr-sign-event): wallet must be unlocked — run `bun run wallet/wallet.ts unlock` first
- For hash and verify operations (sip018-hash, sip018-verify, stacks-verify, btc-verify, schnorr-verify-digest): no wallet required
- `btc-sign` and `schnorr-sign-digest` additionally require Bitcoin/Taproot keys — present in all managed wallets
- `schnorr-sign-digest` requires `--confirm-blind-sign` to actually produce a signature; omit it first to review the digest

## Decision Logic

| Goal | Subcommand |
|------|-----------|
| Sign structured data verifiable by a Clarity smart contract | `sip018-sign` — produces on-chain-verifiable RSV signature |
| Compute SIP-018 hash without signing | `sip018-hash` — for multi-party coordination or pre-computation |
| Verify a SIP-018 signature and recover the signer | `sip018-verify` — takes the verification hash and signature |
| Sign a plain-text message for Stacks wallet authentication (SIWS) | `stacks-sign` — SIWS-compatible RSV signature |
| Verify a Stacks message signature | `stacks-verify` — recovers signer's Stacks address |
| Sign a Bitcoin message for address ownership proof or AIBTC check-in | `btc-sign` — auto-selects BIP-322 (bc1q/bc1p) or BIP-137 (1.../3...) |
| Verify a Bitcoin message signature | `btc-verify` — auto-detects BIP-137 or BIP-322 from signature format |
| Sign a 32-byte digest with Schnorr for Taproot multisig | `schnorr-sign-digest` — BIP-340 Schnorr, requires `--confirm-blind-sign` |
| Verify a BIP-340 Schnorr signature | `schnorr-verify-digest` — no wallet needed |
| Sign a Nostr event for relay publication | `nostr-sign-event` — uses NIP-06 derived key by default |

## Safety Checks

- `schnorr-sign-digest` signs a raw 32-byte digest without context — always review the digest before adding `--confirm-blind-sign`; do not sign digests from untrusted sources
- `btc-sign` with `--wallet-password` passes the password as a process argument visible in `ps aux` — prefer using `--wallet-password-env` with an environment variable, or pre-unlock the wallet
- For Nostr: use the default `keySource` (`"nostr"`, NIP-06 path) for all new identities; only use `"taproot"` or `"segwit"` if an existing identity was previously established on that key path
- SIP-018 domain binding prevents cross-app replay — always include the correct `--domain-name` and `--domain-version` for your application
- Never log or echo private keys; the signing CLI handles key material internally and does not expose it in output

## Error Handling

| Error message | Cause | Fix |
|--------------|-------|-----|
| "Wallet is not unlocked. Use wallet/wallet.ts unlock first to enable signing." | Signing command called without an active session | Run `bun run wallet/wallet.ts unlock --password <password>` |
| "Domain is required: use --domain or --domain-name + --domain-version" | SIP-018 domain not provided | Add `--domain-name "App" --domain-version "1.0.0"` or `--domain '{"name":"App","version":"1.0.0"}'` |
| "Taproot keys not available." | `btc-sign --address-type taproot` but wallet has no Taproot keys | Ensure the wallet was created with Taproot key derivation |
| "schnorr-sign-digest requires --confirm-blind-sign" | First call without the confirm flag | Review the returned `digestToReview`, then add `--confirm-blind-sign` |
| "BIP-322 signing failed: no witness produced" | Internal BIP-322 signing error | Verify the wallet has valid Bitcoin keys and the correct network is set |
| "Message too long for varint encoding" | Bitcoin message exceeds varint size limit | Use a shorter message |

## Output Handling

- `sip018-sign`: use `hashes.verification` as the input to `sip018-verify`; use `hashes.encoded` with `secp256k1-recover?` for on-chain verification
- `stacks-sign` / `btc-sign`: extract `signature` and pass to the corresponding `-verify` subcommand along with the original `message`
- `-verify` subcommands: check `verification.isFullyValid` (true = signature valid and signer matches); `recoveredAddress` is the derived signer
- `schnorr-sign-digest`: extract `signature` (64-byte hex) and `publicKey` (32-byte x-only hex) for multisig coordination
- `nostr-sign-event`: extract the entire `event` object (with `id`, `pubkey`, `sig`) for relay publication; `npub` is the human-readable public key

## Example Invocations

```bash
# Sign the AIBTC check-in message with Bitcoin key (BIP-322 for bc1q addresses)
bun run signing/signing.ts btc-sign --message "AIBTC Check-In | 2026-02-19T12:00:00.000Z"

# Sign structured Clarity data for on-chain verification
bun run signing/signing.ts sip018-sign --message '{"amount":{"type":"uint","value":100}}' --domain-name "My App" --domain-version "1.0.0"

# Verify a Stacks message signature and recover the signer address
bun run signing/signing.ts stacks-verify --message "Hello, Stacks!" --signature <rsv65hex> --expected-signer SP1...
```
