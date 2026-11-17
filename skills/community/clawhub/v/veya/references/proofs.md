# Proofs

Proofs turn content into a **BLAKE3-256** commitment and, when asked, anchor it on
`Veya.sol`. Anyone can later check the commitment from the transaction hash.

| Need | Tool |
|---|---|
| Digest only, nothing sent | `veya_prove` (no `anchor`) or `veya_hash_blake3` |
| Prove an existing receipt | `veya_prove` with `txHash` |
| Digest + on-chain anchor in one call | `veya_prove` with `anchor: true` |
| Labeled content proof in the product account | `veya_anchor_proof` → `veya_list_proofs` → `veya_verify_proof_api` |
| Sealed decision with quorum + attestation | `veya_seal_decision` |

## Workflow: prove text (no key)

```json
{ "tool": "veya_prove", "arguments": { "text": "hello" } }
```

```json
{
  "ok": true,
  "mode": "digest",
  "inputKind": "text",
  "digestHex": "ea8f163db38682925e4491c5e58d4bb3506ef8c14eb78a86e908c5624a67200f",
  "anchored": false
}
```

For JSON pass a string: `{ "json": "{\"b\":2,\"a\":1}" }`. JSON is canonicalized, so key
order does not change the digest; array order does.

## Workflow: prove an existing receipt

```json
{ "tool": "veya_prove", "arguments": { "txHash": "0x91550fdd7a60616e3157364d3624d423403c4add2590c36d3ba290fa07cb95cc" } }
```

A VEYA receipt returns `mode: "verified"` with `event`, `blockNumber`, `explorerUrl`.
A receipt with no VEYA log, or one sent to another contract, returns `ok: false`,
`mode: "refused"` and a `refusal` such as `No VEYA log was found on that transaction.`
(This example is a Mainnet execution attestation; it returns `mode: "verified"`, event `ExecutionAttested`.)

## Workflow: prove and anchor

Needs a product API key, an environment that already exists on `Veya.sol`, and the funded
wallet bound to the key.

```json
{
  "tool": "veya_prove",
  "arguments": {
    "text": "Board resolution 2026-10-11",
    "anchor": true,
    "environmentId": "7d0af0ba-2ae3-4d0e-bc75-0bbaccb3dd71",
    "apiKey": "veya_live_…",
    "payerPrivateKey": "0x…"
  }
}
```

One `storeCommitment` is sent and read back: `mode: "anchored"`, `anchored: true`, `txHash`,
`explorerUrl`. `environmentId` may be a UUID or 32 hex chars.

## Workflow: labeled content proof

1. `veya_anchor_proof` with `apiKey`, `label`, `content` (+ wallet). The server hashes
   `label + "\n" + content` and returns `{ txHash, explorer, from, hash, label, recorded }` (plus `recordError` if the proof list could not save it). `from` is the user's wallet.
2. `veya_list_proofs` with `apiKey` lists the account's anchors.
3. `veya_verify_proof_api` with `signature` = the tx hash returns `valid`.

## Workflow: seal a decision

```json
{
  "tool": "veya_seal_decision",
  "arguments": {
    "evidenceId": "ticket-1042",
    "decision": "{\"action\":\"approve\",\"amount\":250}",
    "apiKey": "veya_live_…",
    "environmentId": "…"
  }
}
```

On mainnet, `environmentId` is an environment registered on Robinhood Chain: create it with
`veya_create_environment`, register it with `veya_register_environment`, then pass its id here
(or the host sets `VEYA_SEAL_DECISION_ENVIRONMENT_ID`). Verify the receipt with
`veya_verify_transaction` on `chain.txHash`.

The decision runs in the AES-256-GCM sealed runtime and is signed by a 2-of-3 ML-DSA quorum.
Result: `ok`, `evidenceId`, `sealed` (fingerprint, `runtime: "AES-256-GCM"`), `attestation`, `chain`.

- `chain` holds the `attestExecution` receipt when `payerPrivateKey` is passed, or when the
  host turns on the seal-decision relayer (`VEYA_SEAL_DECISION_RELAYER=1`). Otherwise `chain` is `null`.
- Limits: 30 calls per minute per key; host-sent seals 20 per key and 100 per host per UTC day.
- Sealed node offline: `code: "SEALED_UNREACHABLE"`, `transaction: null`; nothing is sent.

## Tools

### `veya_prove`

Prove text, canonical JSON, or a receipt hash. Anchor writes only when a product API key and a payer key are passed.

- **Access:** Public · anchor: API key + wallet
- **Returns:** `ok`, `mode` (`digest`/`verified`/`anchored`/`refused`), `inputKind`, `digestHex`, `anchored`, `chainId`, `contractAddress`, `txHash`, `explorerUrl`, `event`, `blockNumber`, `refusal`
- **Notes:** Pass exactly one of `text`, `json`, `txHash`. With `anchor: true` also pass `apiKey`, `environmentId` (an environment already on Veya.sol; UUID or 32-hex) and the funded wallet. Same JSON object with keys in another order hashes the same. Text `hello` → digest `ea8f163db38682925e4491c5e58d4bb3506ef8c14eb78a86e908c5624a67200f`.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `text` | string | one of text/json/txHash |  |
| `json` | string | one of text/json/txHash |  |
| `txHash` | string | one of text/json/txHash | `0x` + 64 hex |
| `anchor` | boolean | no |  |
| `environmentId` | string | when `anchor` is true |  |
| `apiKey` | string | when `anchor` is true | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | when `anchor` is true | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |

### `veya_hash_blake3`

Compute BLAKE3 hex digest (commitment helper)

- **Access:** Public
- **Returns:** `{ hash }` (64 hex chars)

| Arg | Type | Required | Notes |
|---|---|---|---|
| `data` | string | yes |  |

### `veya_seal_decision`

Seal an evidence id and a decision. attestExecution is sent only when a payer key is passed, or when this host's seal-decision relayer switch is on. On Mainnet pass environmentId or set VEYA_SEAL_DECISION_ENVIRONMENT_ID. Without either, the result is SEAL_ENVIRONMENT_REQUIRED and nothing is sent.

- **Access:** API key · wallet or host relayer
- **Returns:** `ok`, `evidenceId`, `sealed`, `attestation`, `chain` (receipt or null). Sealed node offline: `code` `SEALED_UNREACHABLE`, `transaction` null
- **Notes:** `decision` is a string that parses to a JSON object. The receipt is written when `payerPrivateKey` is passed, or when the host enables `VEYA_SEAL_DECISION_RELAYER` (then 20 per key and 100 per host per UTC day). Otherwise `chain` is null. **Mainnet:** pass `environmentId` of an environment registered on Robinhood Chain (`veya_create_environment` → `veya_register_environment`), unless the host sets `VEYA_SEAL_DECISION_ENVIRONMENT_ID`. Without one the call returns `SEAL_ENVIRONMENT_REQUIRED` and nothing is sent.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `evidenceId` | string | yes |  |
| `decision` | string | yes |  |
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | no (writes the receipt when passed) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `environmentId` | string (UUID) | mainnet: yes, unless the host sets `VEYA_SEAL_DECISION_ENVIRONMENT_ID` | environment registered on the active network |

### `veya_anchor_proof`

Anchor a content proof on Veya.sol from YOUR wallet (apiKey + payerPrivateKey). Does not use the hosted relayer.

- **Access:** API key + wallet
- **Returns:** `{ txHash, explorer, from, hash, label, recorded }` (plus `recordError` if the proof list could not save it)

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `payerPrivateKey` | string | yes (or server env) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `label` | string | yes |  |
| `content` | string | yes |  |
| `environmentId` | string | no | omit to use the shared proof environment; pass an environment registered on the active network to anchor under it |

### `veya_list_proofs`

List Use-mode proof anchors for the account

- **Access:** API key (guest: listing)
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |

### `veya_verify_proof_api`

Check a commitment or anchor transaction through the product API. A registration transaction is not a proof and returns NOT_VEYA_TX.

- **Access:** Public
- **Returns:** `{ httpStatus, body }` with `valid`
- **Notes:** `signature` is the tx hash of a commitment write (`veya_prove` with `anchor`, `veya_store_commitment`, `veya_anchor_proof`, `veya_seal_decision`). A registration tx (`veya_register_environment` / `veya_deploy_agent`) returns `NOT_VEYA_TX` (HTTP 404); check those with `veya_verify_transaction`.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `signature` | string | yes |  |

