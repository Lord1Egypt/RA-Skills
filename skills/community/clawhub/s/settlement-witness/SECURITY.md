# SECURITY.md — SettlementWitness Trust Model

## Trust model

Verification is local-first. `scripts/verify_receipt.py` works entirely
offline using a pinned public key registry bundled with this skill package.

The **private signing key is never bundled** and never leaves the DefaultVerifier
server. This skill can only verify — it cannot issue signed receipts.

## What verification proves

A `valid: true` result means:

- `receipt_id` matches the SHA-256 digest of the RFC 8785 canonical form of
  the signed core fields
- The Ed25519 signature verifies against the public key identified by
  `verifier_kid` in the bundled registry
- The receipt structure satisfies SAR v0.1 field and prefix expectations
- The signed `verdict` (`PASS`, `FAIL`, or `INDETERMINATE`) is preserved
  exactly as issued — it is not reinterpreted

## What verification does not prove

A `valid: true` result does not prove:

- Legal settlement finality
- Payment finality or fund release
- That funds are held, escrowed, or custodied anywhere
- That DefaultVerifier executed a task
- That DefaultVerifier approved an action
- That DefaultVerifier controls funds or enforces outcomes
- Truth of external-world facts beyond what is encoded in the signed receipt

DefaultVerifier issues signed evidence. What you do with that evidence is your
responsibility.

## Key pinning and rotation

The bundled `keys/sar-keys.json` is a pinned trust root. It contains the
public key(s) active at the time this skill package was published. As of
v0.1.1 it pins the full current SAR production registry: `sar-prod-ed25519-01`,
`sar-prod-ed25519-02`, and `sar-prod-ed25519-03`.

Local verification requires the receipt's `verifier_kid` to be present in the
local registry. A receipt signed by a kid that is not bundled will fail offline
with `verifier_kid not found in registry`, even if the signature is otherwise
valid.

A future key rotation on the DefaultVerifier side will cause local verification
to fail for receipts signed by newer keys until the bundled registry is updated
in a new package version.

To use an updated registry without waiting for a package update, set:

```bash
SAR_KEYS_REGISTRY_PATH=/path/to/updated-keys.json
```

Fresh registry: https://defaultverifier.com/.well-known/sar-keys.json

## Sensitive data

Do not send sensitive task outputs for remote receipt emission. Remote
issuance sends the `task_id`, `spec`, and `output` you provide — if any of
these are sensitive, use local verification of an existing receipt instead.

## Tamper detection

The bundled `fixtures/tampered-receipt.json` is derived from a valid PASS
receipt with a single core-field mutation (`verdict` changed from `PASS` to
`FAIL` while the original `receipt_id` and `sig` are kept). The verifier must
reject it with both a digest mismatch and a signature failure.

Run to confirm tamper detection works:

```bash
python3 scripts/verify_receipt.py fixtures/tampered-receipt.json
# expected: valid: false
```

## Reporting issues

Repository: https://github.com/nutstrut/default-settlement-verifier
