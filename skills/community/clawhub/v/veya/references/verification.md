# Verification

All verification tools are **public** and read Robinhood Chain directly through
`@veyanet/sdk`. Use them to check any VEYA claim without trusting a screenshot.

## Choose the check

| You have | Call | Proves |
|---|---|---|
| A tx hash | `veya_verify_transaction` | The receipt has Veya.sol events (`CommitmentStored`, `ExecutionAttested`, …) |
| A tx hash, need the strongest check | `veya_verify_commitment_onchain` | Events in the receipt **and** `commitments(digest)` is still true |
| A 32-byte digest | `veya_commitment_exists` | The digest is stored on Veya.sol |
| An environment UUID | `veya_read_environment_onchain` | The environment record on-chain |
| An agent UUID | `veya_read_agent_onchain` | The agent record on-chain |
| A commitment/anchor tx hash | `veya_verify_proof_api` | Product API verify path (`valid`). Registration txs return `NOT_VEYA_TX`; use `veya_verify_transaction` for those |

## Workflow: audit a transaction

1. `veya_describe` → note `settlement.network`, `settlement.contract`, `settlement.explorer`.
2. `veya_verify_transaction` with `txHash` → parsed events and digest.
3. `veya_verify_commitment_onchain` with the same `txHash` → mapping check per stored commitment (empty `commitmentChecks` for attestations).
4. Open `{explorer}/tx/{txHash}` and confirm the `to` address equals `settlement.contract`.
5. Report: network, block, event, digest, explorer link.

```json
{ "tool": "veya_verify_commitment_onchain", "arguments": { "txHash": "0x…" } }
```

## Workflow: check a digest you computed

```json
{ "tool": "veya_hash_blake3", "arguments": { "data": "hello" } }
{ "tool": "veya_commitment_exists", "arguments": { "digestHex": "ea8f163db38682925e4491c5e58d4bb3506ef8c14eb78a86e908c5624a67200f" } }
```

Returns `{ "digestHex": "…", "onChain": true | false }`.

## Input rules

- `txHash`: `0x` + 64 hex (min 66 chars).
- `digestHex`: 32 bytes. UUID args: 16 bytes (32 hex chars, hyphens removed).
- A wrong length returns `Expected <n> bytes, got <m>`.

## Network pins

| Profile | Contract | Explorer |
|---|---|---|
| Mainnet (default) | `0x87dC582eEA544A434a5C1e30Ca3d12c1e548a674` | https://robinhoodchain.blockscout.com |
| Testnet (optional) | `0x1a1Dc3c55550FCE9F70ef6cDEeF967c0b72a5d84` | https://explorer.testnet.chain.robinhood.com |

Example Mainnet receipt (execution attestation, block 91791965):
`0x91550fdd7a60616e3157364d3624d423403c4add2590c36d3ba290fa07cb95cc`.

## Tools

### `veya_verify_transaction`

Verify a Veya.sol commitment from a Robinhood Chain tx hash

- **Access:** Public
- **Returns:** Parsed proofs/events, digests, whether the receipt is a VEYA write

| Arg | Type | Required | Notes |
|---|---|---|---|
| `txHash` | string | yes | `0x` + 64 hex |

### `veya_verify_commitment_onchain`

Parse Veya.sol events from a tx and eth_call commitments(digest) for each CommitmentStored

- **Access:** Public
- **Returns:** Parsed events plus on-chain mapping result per digest

| Arg | Type | Required | Notes |
|---|---|---|---|
| `txHash` | string | yes | `0x` + 64 hex |

### `veya_commitment_exists`

eth_call Veya.sol commitments(bytes32) for a digest

- **Access:** Public
- **Returns:** `{ digestHex, onChain }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `digestHex` | string | yes | 32 bytes (64 hex) |

### `veya_read_environment_onchain`

Read environment record from Veya.sol by 16-byte UUID hex

- **Access:** Public
- **Returns:** Environment record from Veya.sol

| Arg | Type | Required | Notes |
|---|---|---|---|
| `environmentUuidHex` | string | yes | 16 bytes (32 hex) |

### `veya_read_agent_onchain`

Read agent record from Veya.sol by 16-byte UUID hex

- **Access:** Public
- **Returns:** Agent record from Veya.sol

| Arg | Type | Required | Notes |
|---|---|---|---|
| `agentUuidHex` | string | yes | 16 bytes (32 hex) |

