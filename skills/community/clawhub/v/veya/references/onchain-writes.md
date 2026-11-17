# On-chain writes

Write tools send transactions to `Veya.sol` on the selected network (Mainnet by default).
Each write needs:

1. **`apiKey`**: a product key (`veya_dev_…` / `veya_live_…`).
2. **The funded wallet bound to that key**: `payerPrivateKey`, or `VEYA_PAYER_PRIVATE_KEY` on a
   self-hosted server.

Before sending, the server checks the key with the product API, checks that the wallet matches
the key's wallet, and checks the ETH balance. The SDK then confirms `eth_chainId` matches the
profile. The result's `from` is the user's address.

## Contract methods

| Tool | Veya.sol method | Main args |
|---|---|---|
| `veya_store_commitment` | `storeCommitment` | `environmentUuidHex` (16 B), `commitmentHex` (32 B) |
| `veya_attest_execution` | `attestExecution` | `environmentUuidHex`, `blake3HashHex` (32 B), `mldsaSigHex` |
| `veya_register_environment` | `registerEnvironment` | `environmentId` or `environmentUuidHex`; `pqPubkeyHashHex` (32 B, default zeros); `envType` 0–10 (default 0) |
| `veya_register_pq_onchain` | `registerEnvironment` + commitment | `envType` 0–10 (default 1) |
| `veya_anchor_pq_attestation` | `anchorPqAttestation` | `environmentUuidHex`, `identityHashHex`, `executionHashHex` |
| `veya_anchor_proof` | `storeCommitment` | `label`, `content`, optional `environmentId` |
| `veya_prove` (`anchor: true`) | `storeCommitment` | see [proofs.md](proofs.md) |

## Pre-flight checklist

1. `veya_describe`: tell the user the network (Mainnet unless Testnet was selected).
2. `veya_writes_status`: show who pays gas.
3. `veya_account` with `apiKey`: confirm the wallet.
4. Get explicit user confirmation for the write.

## Workflow: register an environment and store a commitment

**1. Register** (product environment from [workspaces.md](workspaces.md))

```json
{ "tool": "veya_register_environment", "arguments": { "apiKey": "veya_live_…", "payerPrivateKey": "0x…", "environmentId": "…" } }
```

```json
{
  "txHash": "0x…",
  "explorer": "https://robinhoodchain.blockscout.com/tx/0x…",
  "from": "0x<user wallet>",
  "environmentUuidHex": "…",
  "consoleSynced": true
}
```

If the result has a `warning`, the chain write succeeded and only the console sync failed.
Do not send it again; share the explorer link.

**2. Hash and store**

```json
{ "tool": "veya_hash_blake3", "arguments": { "data": "Q3 report final" } }
{ "tool": "veya_store_commitment", "arguments": { "apiKey": "veya_live_…", "payerPrivateKey": "0x…", "environmentUuidHex": "<from step 1>", "commitmentHex": "<hash>" } }
```

→ `{ "txHash": "0x…", "explorer": "…", "from": "0x…" }`

**3. Verify**: `veya_verify_commitment_onchain` with the `txHash`.

## Workflow: attest a consensus result

1. `veya_run_consensus` → `agreed_blake3_hash` ([execution.md](execution.md)).
2. `veya_pq_sign` the hash with the operator identity → `signatureHex`.
3. `veya_attest_execution` with `environmentUuidHex`, `blake3HashHex` = agreed hash, `mldsaSigHex` = signature.
4. `veya_verify_transaction` on the returned `txHash`.

## Funding

| Network | Empty-wallet message | Get ETH |
|---|---|---|
| Mainnet | `Your wallet has no ETH on Robinhood Chain. Add funds and try again.` | Bridge or transfer ETH to the wallet on Robinhood Chain |
| Testnet (optional) | `You don't have testnet tokens. Please get them for the transaction.` | https://faucet.testnet.chain.robinhood.com/ |

## Tools

### `veya_store_commitment`

Write a 32-byte commitment to Veya.sol from YOUR wallet (apiKey + payerPrivateKey)

- **Access:** API key + wallet
- **Returns:** `{ txHash, explorer, from }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | yes (or server env) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `environmentUuidHex` | string | yes | 16 bytes (32 hex) |
| `commitmentHex` | string | yes | 32 bytes (64 hex) |

### `veya_attest_execution`

attestExecution on Veya.sol from YOUR wallet with ML-DSA bytes

- **Access:** API key + wallet
- **Returns:** `{ txHash, explorer, from }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | yes (or server env) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `environmentUuidHex` | string | yes | 16 bytes (32 hex) |
| `blake3HashHex` | string | yes | 32 bytes (64 hex) |
| `mldsaSigHex` | string | yes |  |

### `veya_register_environment`

registerEnvironment on Veya.sol from YOUR wallet. Pass product environmentId to confirm the tx on the product API.

- **Access:** API key + wallet
- **Returns:** `txHash`, `explorer`, `from`, `environmentUuidHex`, `consoleSynced`, `confirmed`, optional `warning`
- **Notes:** Pass `environmentId` (product id) or `environmentUuidHex`. `envType` 0–10, default 0. `pqPubkeyHashHex` defaults to 32 zero bytes. If `warning` is set the chain write succeeded; do not resend.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | yes (or server env) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `environmentUuidHex` | string | one of the two | 16 bytes (32 hex) |
| `environmentId` | string | one of the two |  |
| `pqPubkeyHashHex` | string | no | 32 bytes (64 hex) |
| `envType` | number | no |  |

### `veya_register_pq_onchain`

Generate ML-DSA identity and register environment + commitment on Veya.sol from YOUR wallet

- **Access:** API key + wallet
- **Returns:** Public key hex/hash, `environmentTx`, `memoTx`, `explorer`, `from`
- **Notes:** `envType` 0–10, default 1.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | yes (or server env) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `envType` | number | no |  |

### `veya_anchor_pq_attestation`

Link PQ identity hash to execution hash on Veya.sol from YOUR wallet

- **Access:** API key + wallet
- **Returns:** `{ txHash, explorer, from }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | yes (or server env) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `environmentUuidHex` | string | yes | 16 bytes (32 hex) |
| `identityHashHex` | string | yes | 32 bytes (64 hex) |
| `executionHashHex` | string | yes | 32 bytes (64 hex) |

