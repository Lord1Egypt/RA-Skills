# SAR v0.1 Canonicalization and Verification

Concise reference for how SettlementWitness receipts are constructed and
verified locally. This is not a full spec replacement.

Full public spec and live key registry:
- https://defaultverifier.com/verified
- https://defaultverifier.com/.well-known/sar-keys.json

---

## Signed core fields

These fields and only these fields are included in the canonical digest:

| Field | Type | Notes |
|---|---|---|
| `task_id_hash` | string | `sha256:<hex>` prefix required |
| `verdict` | string | `PASS`, `FAIL`, or `INDETERMINATE` |
| `confidence` | number | numeric confidence score |
| `reason_code` | string | e.g. `SPEC_MATCH`, `SPEC_MISMATCH`, `SPEC_AMBIGUOUS` |
| `ts` | string | ISO 8601 UTC timestamp |
| `verifier_kid` | string | key identifier selecting the signing key |
| `counterparty` | string | optional; included only when present and non-empty |

Fields excluded from the signed core (they may appear in a receipt but do not
affect the digest): `receipt_id`, `sig`, `sar_version`, and any other
non-core metadata or notes.

---

## Canonicalization rule (RFC 8785 / JCS)

1. Build the core object from the signed core fields above (and `counterparty`
   if present and non-empty).
2. Serialize to JSON using RFC 8785 (JSON Canonicalization Scheme):
   - Keys sorted lexicographically
   - No insignificant whitespace
   - Numbers in canonical form
   - Unicode escaping per spec
3. The result is a deterministic byte sequence. The same core fields always
   produce the same canonical bytes.

The `jcs` Python package (`pip install jcs`) implements RFC 8785 and is used
by `scripts/verify_receipt.py`.

---

## Digest rule

```
canonical_bytes = JCS(core)
digest_bytes    = SHA-256(canonical_bytes)       # 32 bytes
receipt_id      = "sha256:" + hex(digest_bytes)  # lowercase hex
```

The `receipt_id` prefix `sha256:` is required. Any receipt without it must
fail verification.

---

## Signature rule

```
sig_bytes = Ed25519.sign(digest_bytes, private_key)
sig       = "base64url:" + base64url_nopad(sig_bytes)
```

The signature is over the 32-byte SHA-256 digest — not over the full canonical
JSON. The `base64url:` prefix is required. The verifier selects the public key
from the registry by matching `verifier_kid`.

Verification (`scripts/verify_receipt.py`):
1. Decode `sig` bytes (strip `base64url:` prefix, flexible base64url decode)
2. Load public key by `verifier_kid` from `keys/sar-keys.json`
3. Call `Ed25519PublicKey.verify(sig_bytes, digest_bytes)`

---

## Verdict semantics

| Verdict | Cryptographic validity | Meaning |
|---|---|---|
| `PASS` | Valid signed receipt | Issuer attested spec was met |
| `FAIL` | Valid signed receipt | Issuer attested spec was not met |
| `INDETERMINATE` | Valid signed receipt | Issuer attested honest uncertainty |

All three are valid signed outcomes. `valid: true` in the verifier output
means the cryptography checks out — it does not mean the verdict was `PASS`.

---

## Tamper detection

Any mutation of a signed core field (verdict, confidence, reason_code,
task_id_hash, ts, verifier_kid, or counterparty) will:

1. Change the canonical bytes
2. Change the digest
3. Cause `receipt_id` to not match (detectable without the private key)
4. Cause the signature to fail (the signature was made over the original digest)

Both failures are reported in `errors[]`. A receipt with a tampered core
cannot be made to verify without access to the private signing key.
