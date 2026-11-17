# Consensus and protected execution

VEYA checks agent work two ways:

- **2-of-3 consensus**: three validator nodes hash the same payload with BLAKE3 and sign
  with ML-DSA. Agreement means at least two matching hashes.
- **Protected (sealed) execution**: the payload runs on a sealed node with **AES-256-GCM**,
  producing a BLAKE3 hash of the ciphertext and an ML-DSA signature over the execution hash.

Validators and sealed capacity belong to the product API fleet. Check `veya_api_health` first.

## Limits

`veya_run_consensus`, `veya_client_run_consensus` and `veya_sealed_execute` allow
**30 calls per minute per API key** (server default, `VEYA_CAPACITY_PER_MINUTE`).
Over the limit: `API key limit: 30 requests per minute`.

## Workflow: consensus, then attest

**1. Run consensus**

```json
{ "tool": "veya_run_consensus", "arguments": { "apiKey": "veya_live_…", "taskId": "task-8819", "payload": { "amount": 250, "to": "0x…" } } }
```

```json
{
  "task_id": "task-8819",
  "agreed_blake3_hash": "…",
  "consensus_reached": true,
  "threshold": 2,
  "reachable": 3,
  "node_results": [ … ]
}
```

If fewer than two nodes agree or answer, `consensus_reached` is `false` and
`agreed_blake3_hash` is `null`. Do not attest in that case.

**2. Anchor the agreed hash**

Use `agreed_blake3_hash` as `blake3HashHex` in `veya_attest_execution`, or as
`executionHashHex` in `veya_anchor_pq_attestation` ([onchain-writes.md](onchain-writes.md)).

## Workflow: sealed execution

```json
{
  "tool": "veya_sealed_execute",
  "arguments": {
    "apiKey": "veya_live_…",
    "environmentId": "…", "agentId": "…",
    "eventType": "treasury.decision",
    "payload": { "action": "rebalance" },
    "sessionEntropyHex": "<64 hex chars of fresh randomness>"
  }
}
```

The server only returns results whose seal is verified. If sealed capacity is offline the
call returns an error and nothing is stored.

## Workflow: product protected execution

`veya_run_protected_execution` runs the same sealed path through the product API (Build),
with optional `disclose` and `seal` field lists that choose which payload fields stay
visible and which are sealed. List history with `veya_list_executions`.
The sealed result is stored in the product API; this call does not write on-chain. To
put it on Robinhood Chain, commit the result hash with `veya_store_commitment` (or
`veya_prove` with `anchor: true`) and check it with `veya_verify_commitment_onchain`.

## Tools

### `veya_run_consensus`

Run 2-of-3 BLAKE3 consensus on this server's validator list. Needs a product API key. Returns consensus_reached: false if validators are unreachable.

- **Access:** API key · 30/min per key
- **Returns:** `task_id`, `agreed_blake3_hash`, `node_results`, `consensus_reached`, `threshold`, `reachable`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `taskId` | string | yes |  |
| `payload` | object | no |  |

### `veya_client_run_consensus`

Deprecated: use veya_run_consensus. Same server validator list. Needs a product API key.

- **Access:** API key · 30/min per key
- **Returns:** Same as `veya_run_consensus`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `taskId` | string | yes |  |
| `payload` | object | no |  |

### `veya_sealed_execute`

AES-256-GCM protected execution on this server's sealed node. Needs a product API key. The call fails closed when that capacity is unreachable.

- **Access:** API key · 30/min per key
- **Returns:** Sealed result (commitment, `verified`, hashes); unverified seals return an error
- **Notes:** `sessionEntropyHex` minimum 16 hex chars; use 32 random bytes (64 hex).

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `agentId` | string | yes |  |
| `eventType` | string | yes |  |
| `payload` | object | yes |  |
| `sessionEntropyHex` | string | yes |  |

### `veya_run_protected_execution`

Run protected execution via product API (Build). Product API key required.

- **Access:** API key
- **Returns:** `{ httpStatus, body }`
- **Notes:** The sealed result is stored in the product API (`veya_list_executions`). This MCP call does not write on-chain. To put the result on Robinhood Chain, commit its hash with `veya_store_commitment` or `veya_prove` with `anchor: true`.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |
| `agentId` | string | yes |  |
| `eventType` | string | yes |  |
| `payload` | object | yes |  |
| `disclose` | string[] | no |  |
| `seal` | string[] | no |  |

### `veya_list_executions`

List executions for an environment via product API

- **Access:** API key (guest: listing)
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |

