# Post-quantum identity

VEYA identities use **ML-DSA-44** (FIPS 204) signatures. The identity hash stored on-chain is
the **BLAKE3** fingerprint of the public key. Secure agent messages add a **Kyber-768**
session (see [policy-and-routing.md](policy-and-routing.md)).

These four tools run in the MCP process and do not touch the chain. They are public.

## Workflow: create, sign, verify

**1. Generate**

```json
{ "tool": "veya_pq_keygen", "arguments": {} }
```

```json
{ "publicKeyHex": "…", "privateKeyHex": "…", "publicKeyHash": "…" }
```

Hand `privateKeyHex` to the user to store; do not repeat it in summaries.

**2. Sign**

```json
{ "tool": "veya_pq_sign", "arguments": { "message": "approve task-8819", "privateKeyHex": "…" } }
```

→ `{ "signatureHex": "…" }`

**3. Verify**

```json
{ "tool": "veya_pq_verify", "arguments": { "message": "approve task-8819", "signatureHex": "…", "publicKeyHex": "…" } }
```

→ `{ "valid": true }`

**4. Fingerprint** (when you only have the public key)

```json
{ "tool": "veya_pq_fingerprint", "arguments": { "publicKeyHex": "…" } }
```

→ `{ "publicKeyHash": "…" }`

## Put an identity on-chain

| Goal | Tool |
|---|---|
| New identity + environment + commitment in one step | `veya_register_pq_onchain` |
| Register an environment with an identity hash | `veya_register_environment` with `pqPubkeyHashHex` |
| Link an identity hash to an execution hash | `veya_anchor_pq_attestation` |
| Attest an execution with ML-DSA signature bytes | `veya_attest_execution` |

Details: [onchain-writes.md](onchain-writes.md).

## Tools

### `veya_pq_keygen`

Generate an ML-DSA-44 post-quantum identity keypair (local, no chain write)

- **Access:** Public
- **Returns:** `publicKeyHex`, `privateKeyHex`, `publicKeyHash`

_No arguments._

### `veya_pq_sign`

Sign UTF-8 text with ML-DSA-44

- **Access:** Public
- **Returns:** `{ signatureHex }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `message` | string | yes |  |
| `privateKeyHex` | string | yes |  |

### `veya_pq_verify`

Verify an ML-DSA-44 signature over UTF-8 text

- **Access:** Public
- **Returns:** `{ valid }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `message` | string | yes |  |
| `signatureHex` | string | yes |  |
| `publicKeyHex` | string | yes |  |

### `veya_pq_fingerprint`

BLAKE3 fingerprint of an ML-DSA public key hex

- **Access:** Public
- **Returns:** `{ publicKeyHash }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `publicKeyHex` | string | yes |  |

