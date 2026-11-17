# Tool reference — all 51 VEYA MCP tools

Generated from the tool registrations in `veya-mcp/src/tools/*.ts`. Names, argument names, types and required flags match the server code.

**Reply shape.** Every tool returns one MCP text item containing JSON. Errors set `isError: true` with `{ "error": "…" }` (or a `refusal` field for `veya_prove` / `veya_seal_decision`). Product API and registry tools wrap the response as `{ "httpStatus": 200, "body": { … } }`. API timeout is 20 s (`veya_api_health`: 8 s).

**apiKey.** The MCP schema marks `apiKey` and `payerPrivateKey` optional so clients can pass them per call; the server still refuses scoped calls without them (`apiKey required`). "yes" in the tables below means the server needs it. Never put keys in `mcp.json`.

**Hex.** A `0x` prefix is optional. UUIDs are 16 bytes (32 hex). Digests are 32 bytes (64 hex).

## Index

| # | Tool | Group | Access |
|---|---|---|---|
| 1 | [`veya_describe`](#veya_describe) | [Service and chain](service-and-chain.md) | Public |
| 2 | [`veya_ping_chain`](#veya_ping_chain) | [Service and chain](service-and-chain.md) | Public |
| 3 | [`veya_api_health`](#veya_api_health) | [Service and chain](service-and-chain.md) | Public |
| 4 | [`veya_writes_status`](#veya_writes_status) | [Service and chain](service-and-chain.md) | Public |
| 5 | [`veya_prove`](#veya_prove) | [Proofs](proofs.md) | Public · anchor: API key + wallet |
| 6 | [`veya_hash_blake3`](#veya_hash_blake3) | [Proofs](proofs.md) | Public |
| 7 | [`veya_seal_decision`](#veya_seal_decision) | [Proofs](proofs.md) | API key · wallet or host relayer |
| 8 | [`veya_anchor_proof`](#veya_anchor_proof) | [Proofs](proofs.md) | API key + wallet |
| 9 | [`veya_list_proofs`](#veya_list_proofs) | [Proofs](proofs.md) | API key (guest: listing) |
| 10 | [`veya_verify_proof_api`](#veya_verify_proof_api) | [Proofs](proofs.md) | Public |
| 11 | [`veya_verify_transaction`](#veya_verify_transaction) | [Verification](verification.md) | Public |
| 12 | [`veya_verify_commitment_onchain`](#veya_verify_commitment_onchain) | [Verification](verification.md) | Public |
| 13 | [`veya_commitment_exists`](#veya_commitment_exists) | [Verification](verification.md) | Public |
| 14 | [`veya_read_environment_onchain`](#veya_read_environment_onchain) | [Verification](verification.md) | Public |
| 15 | [`veya_read_agent_onchain`](#veya_read_agent_onchain) | [Verification](verification.md) | Public |
| 16 | [`veya_pq_keygen`](#veya_pq_keygen) | [Post-quantum identity](identity.md) | Public |
| 17 | [`veya_pq_sign`](#veya_pq_sign) | [Post-quantum identity](identity.md) | Public |
| 18 | [`veya_pq_verify`](#veya_pq_verify) | [Post-quantum identity](identity.md) | Public |
| 19 | [`veya_pq_fingerprint`](#veya_pq_fingerprint) | [Post-quantum identity](identity.md) | Public |
| 20 | [`veya_guest_login`](#veya_guest_login) | [Accounts, environments, agents](workspaces.md) | Public |
| 21 | [`veya_account`](#veya_account) | [Accounts, environments, agents](workspaces.md) | API key |
| 22 | [`veya_list_environments`](#veya_list_environments) | [Accounts, environments, agents](workspaces.md) | API key (guest: listing) |
| 23 | [`veya_get_environment`](#veya_get_environment) | [Accounts, environments, agents](workspaces.md) | API key (guest: listing) |
| 24 | [`veya_create_environment`](#veya_create_environment) | [Accounts, environments, agents](workspaces.md) | API key |
| 25 | [`veya_list_agents`](#veya_list_agents) | [Accounts, environments, agents](workspaces.md) | API key (guest: listing) |
| 26 | [`veya_deploy_agent`](#veya_deploy_agent) | [Accounts, environments, agents](workspaces.md) | API key |
| 27 | [`veya_set_tool_policy`](#veya_set_tool_policy) | [Policy and routing](policy-and-routing.md) | API key (owner) |
| 28 | [`veya_route_message`](#veya_route_message) | [Policy and routing](policy-and-routing.md) | API key (owner) |
| 29 | [`veya_route_secure_message`](#veya_route_secure_message) | [Policy and routing](policy-and-routing.md) | API key (owner) |
| 30 | [`veya_verify_secure_message`](#veya_verify_secure_message) | [Policy and routing](policy-and-routing.md) | Public |
| 31 | [`veya_boundnet_invoke`](#veya_boundnet_invoke) | [Policy and routing](policy-and-routing.md) | API key |
| 32 | [`veya_run_consensus`](#veya_run_consensus) | [Execution](execution.md) | API key · 30/min per key |
| 33 | [`veya_client_run_consensus`](#veya_client_run_consensus) | [Execution](execution.md) | API key · 30/min per key |
| 34 | [`veya_sealed_execute`](#veya_sealed_execute) | [Execution](execution.md) | API key · 30/min per key |
| 35 | [`veya_run_protected_execution`](#veya_run_protected_execution) | [Execution](execution.md) | API key |
| 36 | [`veya_list_executions`](#veya_list_executions) | [Execution](execution.md) | API key (guest: listing) |
| 37 | [`veya_store_memory`](#veya_store_memory) | [Memory](memory.md) | API key (owner) |
| 38 | [`veya_read_memory`](#veya_read_memory) | [Memory](memory.md) | API key (owner) |
| 39 | [`veya_invalidate_memory`](#veya_invalidate_memory) | [Memory](memory.md) | API key (owner) |
| 40 | [`veya_list_api_memory`](#veya_list_api_memory) | [Memory](memory.md) | API key (guest: listing) |
| 41 | [`veya_public_stats`](#veya_public_stats) | [Public registry](registry.md) | Public |
| 42 | [`veya_public_list_agents`](#veya_public_list_agents) | [Public registry](registry.md) | Public |
| 43 | [`veya_public_get_agent`](#veya_public_get_agent) | [Public registry](registry.md) | Public |
| 44 | [`veya_public_list_certificates`](#veya_public_list_certificates) | [Public registry](registry.md) | Public |
| 45 | [`veya_public_get_certificate`](#veya_public_get_certificate) | [Public registry](registry.md) | Public |
| 46 | [`veya_public_get_execution`](#veya_public_get_execution) | [Public registry](registry.md) | Public |
| 47 | [`veya_store_commitment`](#veya_store_commitment) | [On-chain writes](onchain-writes.md) | API key + wallet |
| 48 | [`veya_attest_execution`](#veya_attest_execution) | [On-chain writes](onchain-writes.md) | API key + wallet |
| 49 | [`veya_register_environment`](#veya_register_environment) | [On-chain writes](onchain-writes.md) | API key + wallet |
| 50 | [`veya_register_pq_onchain`](#veya_register_pq_onchain) | [On-chain writes](onchain-writes.md) | API key + wallet |
| 51 | [`veya_anchor_pq_attestation`](#veya_anchor_pq_attestation) | [On-chain writes](onchain-writes.md) | API key + wallet |

## Service and chain

Workflow guide: [service-and-chain.md](service-and-chain.md)

### `veya_describe`

Service info: AES-256-GCM sealed execution and the selected settlement profile

- **Access:** Public
- **Use when:** First call after connecting; confirms network, contract and write policy.
- **Returns:** `name`, `version`, `publicUrl`, `settlement` {`network`,`chainId`,`contract`,`explorer`,`rpc`}, `productApi`, `sealed`, `mainnet`, `writes`, `toolSurface`, `fleet`, `publicPasteUrl`

_No arguments._

```json
{"tool": "veya_describe", "arguments": {}}
```

### `veya_ping_chain`

Ping Robinhood Chain RPC — chain id, block, contract

- **Access:** Public
- **Use when:** Live RPC check before any verify or write.
- **Returns:** Ping fields from `VeyaClient.pingChain()`, `chainId` (string), `expectedChainId`, `config`

_No arguments._

```json
{"tool": "veya_ping_chain", "arguments": {}}
```

### `veya_api_health`

Check the VEYA API /health status (api.veyanet.tech), including fleet status

- **Access:** Public
- **Use when:** Before consensus, sealed or product calls; shows fleet status.
- **Returns:** `{ httpStatus, body }`; body has `status` (`ok`/`degraded`), `validators.reachable`, `sealed.reachable`

_No arguments._

```json
{"tool": "veya_api_health", "arguments": {}}
```

### `veya_writes_status`

Reports how on-chain writes work on this server: your own wallet sends them, the host relayer does not

- **Access:** Public
- **Use when:** Before a write, to show the user which wallet sends the write.
- **Returns:** `userPaidWrites`, `operatorRelayerWrites`, `requires` {`apiKey`,`payerPrivateKey`}, `gasPayer`, `emptyWallet`, `faucetUrl` (Testnet)

_No arguments._

```json
{"tool": "veya_writes_status", "arguments": {}}
```

## Proofs

Workflow guide: [proofs.md](proofs.md)

### `veya_prove`

Prove text, canonical JSON, or a receipt hash. Anchor writes only when a product API key and a payer key are passed.

- **Access:** Public · anchor: API key + wallet
- **Use when:** One proof object from text, JSON, or a receipt hash.
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

```json
{"tool": "veya_prove", "arguments": {"text": "hello"}}
```

### `veya_hash_blake3`

Compute BLAKE3 hex digest (commitment helper)

- **Access:** Public
- **Use when:** Preview a BLAKE3-256 digest before storing a commitment.
- **Returns:** `{ hash }` (64 hex chars)

| Arg | Type | Required | Notes |
|---|---|---|---|
| `data` | string | yes |  |

```json
{"tool": "veya_hash_blake3", "arguments": {"data": "hello"}}
```

### `veya_seal_decision`

Seal an evidence id and a decision. attestExecution is sent only when a payer key is passed, or when this host's seal-decision relayer switch is on. On Mainnet pass environmentId or set VEYA_SEAL_DECISION_ENVIRONMENT_ID. Without either, the result is SEAL_ENVIRONMENT_REQUIRED and nothing is sent.

- **Access:** API key · wallet or host relayer
- **Use when:** Seal an evidence id + decision object with a sealed fingerprint, 2-of-3 ML-DSA quorum, and an `attestExecution` receipt.
- **Returns:** `ok`, `evidenceId`, `sealed`, `attestation`, `chain` (receipt or null). Sealed node offline: `code` `SEALED_UNREACHABLE`, `transaction` null
- **Notes:** `decision` is a string that parses to a JSON object. The receipt is written when `payerPrivateKey` is passed, or when the host enables `VEYA_SEAL_DECISION_RELAYER` (then 20 per key and 100 per host per UTC day). Otherwise `chain` is null. **Mainnet:** pass `environmentId` of an environment registered on Robinhood Chain (`veya_create_environment` → `veya_register_environment`), unless the host sets `VEYA_SEAL_DECISION_ENVIRONMENT_ID`. Without one the call returns `SEAL_ENVIRONMENT_REQUIRED` and nothing is sent.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `evidenceId` | string | yes |  |
| `decision` | string | yes |  |
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | no (writes the receipt when passed) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `environmentId` | string (UUID) | mainnet: yes, unless the host sets `VEYA_SEAL_DECISION_ENVIRONMENT_ID` | environment registered on the active network |

```json
{"tool": "veya_seal_decision", "arguments": {"evidenceId": "ticket-1042", "decision": "{\"action\":\"approve\"}", "apiKey": "veya_live_…", "environmentId": "…"}}
```

### `veya_anchor_proof`

Anchor a content proof on Veya.sol from YOUR wallet (apiKey + payerPrivateKey). Does not use the hosted relayer.

- **Access:** API key + wallet
- **Use when:** Stamp labeled content on Veya.sol; hashes `label\ncontent` with BLAKE3 and calls `storeCommitment`.
- **Returns:** `{ txHash, explorer, from, hash, label, recorded }` (plus `recordError` if the proof list could not save it)

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `payerPrivateKey` | string | yes (or server env) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `label` | string | yes |  |
| `content` | string | yes |  |
| `environmentId` | string | no | omit to use the shared proof environment; pass an environment registered on the active network to anchor under it |

```json
{"tool": "veya_anchor_proof", "arguments": {"apiKey": "veya_live_…", "label": "contract-v2", "content": "…"}}
```

### `veya_list_proofs`

List Use-mode proof anchors for the account

- **Access:** API key (guest: listing)
- **Use when:** List Use-mode proof anchors for the account.
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |

```json
{"tool": "veya_list_proofs", "arguments": {"apiKey": "veya_live_…"}}
```

### `veya_verify_proof_api`

Check a commitment or anchor transaction through the product API. A registration transaction is not a proof and returns NOT_VEYA_TX.

- **Access:** Public
- **Use when:** Verify an anchored proof through the product API (`GET /api/verify/:signature`).
- **Returns:** `{ httpStatus, body }` with `valid`
- **Notes:** `signature` is the tx hash of a commitment write (`veya_prove` with `anchor`, `veya_store_commitment`, `veya_anchor_proof`, `veya_seal_decision`). A registration tx (`veya_register_environment` / `veya_deploy_agent`) returns `NOT_VEYA_TX` (HTTP 404); check those with `veya_verify_transaction`.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `signature` | string | yes |  |

```json
{"tool": "veya_verify_proof_api", "arguments": {"signature": "0x…"}}
```

## Verification

Workflow guide: [verification.md](verification.md)

### `veya_verify_transaction`

Verify a Veya.sol commitment from a Robinhood Chain tx hash

- **Access:** Public
- **Use when:** Someone sent a tx hash; parse its Veya.sol events.
- **Returns:** Parsed proofs/events, digests, whether the receipt is a VEYA write

| Arg | Type | Required | Notes |
|---|---|---|---|
| `txHash` | string | yes | `0x` + 64 hex |

```json
{"tool": "veya_verify_transaction", "arguments": {"txHash": "0x…"}}
```

### `veya_verify_commitment_onchain`

Parse Veya.sol events from a tx and eth_call commitments(digest) for each CommitmentStored

- **Access:** Public
- **Use when:** Strongest check: events in the receipt and `commitments(digest)` still true.
- **Returns:** Parsed events plus on-chain mapping result per digest

| Arg | Type | Required | Notes |
|---|---|---|---|
| `txHash` | string | yes | `0x` + 64 hex |

```json
{"tool": "veya_verify_commitment_onchain", "arguments": {"txHash": "0x…"}}
```

### `veya_commitment_exists`

eth_call Veya.sol commitments(bytes32) for a digest

- **Access:** Public
- **Use when:** You have a 32-byte digest and want a yes/no.
- **Returns:** `{ digestHex, onChain }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `digestHex` | string | yes | 32 bytes (64 hex) |

```json
{"tool": "veya_commitment_exists", "arguments": {"digestHex": "ea8f…200f"}}
```

### `veya_read_environment_onchain`

Read environment record from Veya.sol by 16-byte UUID hex

- **Access:** Public
- **Use when:** Read an environment record by 16-byte UUID.
- **Returns:** Environment record from Veya.sol

| Arg | Type | Required | Notes |
|---|---|---|---|
| `environmentUuidHex` | string | yes | 16 bytes (32 hex) |

```json
{"tool": "veya_read_environment_onchain", "arguments": {"environmentUuidHex": "7d0af0ba2ae34d0ebc750bbaccb3dd71"}}
```

### `veya_read_agent_onchain`

Read agent record from Veya.sol by 16-byte UUID hex

- **Access:** Public
- **Use when:** Read an agent record by 16-byte UUID.
- **Returns:** Agent record from Veya.sol

| Arg | Type | Required | Notes |
|---|---|---|---|
| `agentUuidHex` | string | yes | 16 bytes (32 hex) |

```json
{"tool": "veya_read_agent_onchain", "arguments": {"agentUuidHex": "55c7a27d64a3420589ab9fa0ab13a9af"}}
```

## Post-quantum identity

Workflow guide: [identity.md](identity.md)

### `veya_pq_keygen`

Generate an ML-DSA-44 post-quantum identity keypair (local, no chain write)

- **Access:** Public
- **Use when:** New ML-DSA-44 identity for an agent or operator.
- **Returns:** `publicKeyHex`, `privateKeyHex`, `publicKeyHash`

_No arguments._

```json
{"tool": "veya_pq_keygen", "arguments": {}}
```

### `veya_pq_sign`

Sign UTF-8 text with ML-DSA-44

- **Access:** Public
- **Use when:** Sign UTF-8 text with ML-DSA-44.
- **Returns:** `{ signatureHex }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `message` | string | yes |  |
| `privateKeyHex` | string | yes |  |

```json
{"tool": "veya_pq_sign", "arguments": {"message": "hello", "privateKeyHex": "…"}}
```

### `veya_pq_verify`

Verify an ML-DSA-44 signature over UTF-8 text

- **Access:** Public
- **Use when:** Check an ML-DSA-44 signature.
- **Returns:** `{ valid }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `message` | string | yes |  |
| `signatureHex` | string | yes |  |
| `publicKeyHex` | string | yes |  |

```json
{"tool": "veya_pq_verify", "arguments": {"message": "hello", "signatureHex": "…", "publicKeyHex": "…"}}
```

### `veya_pq_fingerprint`

BLAKE3 fingerprint of an ML-DSA public key hex

- **Access:** Public
- **Use when:** BLAKE3 fingerprint of a public key (the identity hash used on-chain).
- **Returns:** `{ publicKeyHash }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `publicKeyHex` | string | yes |  |

```json
{"tool": "veya_pq_fingerprint", "arguments": {"publicKeyHex": "…"}}
```

## Accounts, environments, agents

Workflow guide: [workspaces.md](workspaces.md)

### `veya_guest_login`

Create a guest session on the product API (Use listing only). Guest cannot mint API keys or write from MCP.

- **Access:** Public
- **Use when:** Browse showcase rooms without a key.
- **Returns:** Guest JWT, `mode: guest` (listing only)

_No arguments._

```json
{"tool": "veya_guest_login", "arguments": {}}
```

### `veya_account`

Return the wallet bound to a product API key

- **Access:** API key
- **Use when:** Confirm which wallet a key belongs to.
- **Returns:** `{ httpStatus, body }` with `wallet`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |

```json
{"tool": "veya_account", "arguments": {"apiKey": "veya_live_…"}}
```

### `veya_list_environments`

List environments for a product API key (guest JWT sees showcase / Use scope only)

- **Access:** API key (guest: listing)
- **Use when:** List environments for the key.
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |

```json
{"tool": "veya_list_environments", "arguments": {"apiKey": "veya_live_…"}}
```

### `veya_get_environment`

Get one environment by id

- **Access:** API key (guest: listing)
- **Use when:** Fetch one environment.
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |

```json
{"tool": "veya_get_environment", "arguments": {"apiKey": "veya_live_…", "environmentId": "…"}}
```

### `veya_create_environment`

Create a workspace in the product API. This does not spend gas and sends no transaction. Guests and non-keys are refused. type is stored for the API and defaults to research when omitted. Names that start with test, demo, tmp, sandbox, or e2e are refused. Use a real workspace name of at least 6 characters, or a name that starts with VEYA.

- **Access:** API key
- **Use when:** Create a workspace (API row, no gas).
- **Returns:** `{ httpStatus, body }` with the new environment
- **Notes:** `type` defaults to `research`. Register it on-chain later with `veya_register_environment`. Use a product-style name such as `VEYA Treasury Ops`: names with the words `test`, `demo`, `tmp` or `sandbox` return `CONFLICT` (HTTP 409).

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `name` | string | yes |  |
| `type` | enum: `research`, `governance`, `treasury`, `contributor`, `protocol`, `desci` | no |  |

```json
{"tool": "veya_create_environment", "arguments": {"apiKey": "veya_live_…", "name": "VEYA Treasury Ops", "type": "treasury"}}
```

### `veya_list_agents`

List agents in an environment

- **Access:** API key (guest: listing)
- **Use when:** List agents in an environment.
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |

```json
{"tool": "veya_list_agents", "arguments": {"apiKey": "veya_live_…", "environmentId": "…"}}
```

### `veya_deploy_agent`

Create an agent in a workspace. This does not spend gas and sends no transaction. Limit the agent with permissionConfig.allowedTools. If allowedTools is omitted, the agent cannot call a tool. type is stored for the API and defaults to coordination when omitted.

- **Access:** API key
- **Use when:** Create an agent with an explicit tool allowlist (no gas).
- **Returns:** `{ httpStatus, body }` with the new agent
- **Notes:** `type` defaults to `coordination`. List tools in `permissionConfig.allowedTools`; an agent with an empty list calls no tools.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |
| `type` | string | no |  |
| `agentKind` | string | yes (the API refuses an agent without it) | display name, at least 3 characters, example `Record Agent` |
| `permissionConfig` | object | no |  |

```json
{"tool": "veya_deploy_agent", "arguments": {"apiKey": "veya_live_…", "environmentId": "…", "agentKind": "Record Agent", "permissionConfig": {"allowedTools": ["veya_prove"]}}}
```

## Policy and routing

Workflow guide: [policy-and-routing.md](policy-and-routing.md)

### `veya_set_tool_policy`

Allow or deny a tool for an agent. Requires the API key that owns the environment. Saved on that account.

- **Access:** API key (owner)
- **Use when:** Allow or deny one tool for one agent.
- **Returns:** Saved rule

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `agentId` | string | yes |  |
| `tool` | string | yes |  |
| `allowed` | boolean | yes |  |

```json
{"tool": "veya_set_tool_policy", "arguments": {"apiKey": "veya_live_…", "environmentId": "…", "agentId": "…", "tool": "veya_anchor_proof", "allowed": false}}
```

### `veya_route_message`

Check the saved tool rule for this API key before routing. Deny stays deny.

- **Access:** API key (owner)
- **Use when:** Check the saved rule before passing a message between agents.
- **Returns:** Route result with `policyStatus` (`allowed`/`denied`)
- **Notes:** A denied rule stays denied.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `id` | string | yes |  |
| `fromAgent` | string | yes |  |
| `toAgent` | string | yes |  |
| `tool` | string | yes |  |
| `payload` | any JSON | no |  |

```json
{"tool": "veya_route_message", "arguments": {"apiKey": "veya_live_…", "environmentId": "…", "id": "msg-1", "fromAgent": "…", "toAgent": "…", "tool": "veya_prove"}}
```

### `veya_route_secure_message`

Check the saved tool rule for this API key, then wrap an allowed message in a Kyber-768 session and an ML-DSA-44 signature.

- **Access:** API key (owner)
- **Use when:** Same check, then Kyber-768 session + ML-DSA-44 signature envelope.
- **Returns:** Secure envelope (session id, signature, `policyStatus`)

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `id` | string | yes |  |
| `fromAgent` | string | yes |  |
| `toAgent` | string | yes |  |
| `tool` | string | yes |  |
| `payload` | any JSON | no |  |
| `senderPrivateKeyHex` | string | yes |  |
| `senderPublicKeyHex` | string | yes |  |

```json
{"tool": "veya_route_secure_message", "arguments": {"apiKey": "veya_live_…", "environmentId": "…", "id": "msg-2", "fromAgent": "…", "toAgent": "…", "tool": "veya_prove", "senderPrivateKeyHex": "…", "senderPublicKeyHex": "…"}}
```

### `veya_verify_secure_message`

Verify ML-DSA signature on a secure routed message envelope

- **Access:** Public
- **Use when:** Receiver checks the envelope signature.
- **Returns:** `{ valid }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `message` | object | yes |  |
| `senderPublicKeyHex` | string | yes |  |

```json
{"tool": "veya_verify_secure_message", "arguments": {"message": {}, "senderPublicKeyHex": "…"}}
```

### `veya_boundnet_invoke`

Invoke a Boundnet / coordination tool via product API (policy gated)

- **Access:** API key
- **Use when:** Call a coordination tool as an agent; policy gated.
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |
| `agentId` | string | yes |  |
| `toolName` | string | yes |  |
| `arguments` | object | no |  |

```json
{"tool": "veya_boundnet_invoke", "arguments": {"apiKey": "veya_live_…", "environmentId": "…", "agentId": "…", "toolName": "…", "arguments": {}}}
```

## Execution

Workflow guide: [execution.md](execution.md)

### `veya_run_consensus`

Run 2-of-3 BLAKE3 consensus on this server's validator list. Needs a product API key. Returns consensus_reached: false if validators are unreachable.

- **Access:** API key · 30/min per key
- **Use when:** 2-of-3 BLAKE3 quorum digest before attesting.
- **Returns:** `task_id`, `agreed_blake3_hash`, `node_results`, `consensus_reached`, `threshold`, `reachable`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `taskId` | string | yes |  |
| `payload` | object | no |  |

```json
{"tool": "veya_run_consensus", "arguments": {"apiKey": "veya_live_…", "taskId": "task-8819", "payload": {"amount": 250}}}
```

### `veya_client_run_consensus`

Deprecated: use veya_run_consensus. Same server validator list. Needs a product API key.

- **Access:** API key · 30/min per key
- **Use when:** Deprecated alias. Use `veya_run_consensus`.
- **Returns:** Same as `veya_run_consensus`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `taskId` | string | yes |  |
| `payload` | object | no |  |

```json
{"tool": "veya_client_run_consensus", "arguments": {"apiKey": "veya_live_…", "taskId": "task-8819"}}
```

### `veya_sealed_execute`

AES-256-GCM protected execution on this server's sealed node. Needs a product API key. The call fails closed when that capacity is unreachable.

- **Access:** API key · 30/min per key
- **Use when:** Run a sensitive payload on the AES-256-GCM sealed node.
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

```json
{"tool": "veya_sealed_execute", "arguments": {"apiKey": "veya_live_…", "environmentId": "…", "agentId": "…", "eventType": "decision", "payload": {}, "sessionEntropyHex": "<64 hex>"}}
```

### `veya_run_protected_execution`

Run protected execution via product API (Build). Product API key required.

- **Access:** API key
- **Use when:** Protected execution through the product API (Build).
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

```json
{"tool": "veya_run_protected_execution", "arguments": {"apiKey": "veya_live_…", "environmentId": "…", "agentId": "…", "eventType": "decision", "payload": {}}}
```

### `veya_list_executions`

List executions for an environment via product API

- **Access:** API key (guest: listing)
- **Use when:** List executions for an environment.
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |

```json
{"tool": "veya_list_executions", "arguments": {"apiKey": "veya_live_…", "environmentId": "…"}}
```

## Memory

Workflow guide: [memory.md](memory.md)

### `veya_store_memory`

Store agent memory for the account behind this API key. No key, no write.

- **Access:** API key (owner)
- **Use when:** Save agent memory on the account.
- **Returns:** Stored row with `id`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `agentId` | string | yes |  |
| `data` | string | yes |  |

```json
{"tool": "veya_store_memory", "arguments": {"apiKey": "veya_live_…", "environmentId": "…", "agentId": "…", "data": "…"}}
```

### `veya_read_memory`

Read one memory row owned by this API key.

- **Access:** API key (owner)
- **Use when:** Read one memory row.
- **Returns:** Memory row

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `id` | string | yes |  |

```json
{"tool": "veya_read_memory", "arguments": {"apiKey": "veya_live_…", "environmentId": "…", "id": "…"}}
```

### `veya_invalidate_memory`

Nullify one memory row owned by this API key.

- **Access:** API key (owner)
- **Use when:** Nullify one memory row.
- **Returns:** Nullified row

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `id` | string | yes |  |

```json
{"tool": "veya_invalidate_memory", "arguments": {"apiKey": "veya_live_…", "environmentId": "…", "id": "…"}}
```

### `veya_list_api_memory`

List memory entries via product API for an environment

- **Access:** API key (guest: listing)
- **Use when:** List memory entries for an environment.
- **Returns:** `{ httpStatus, body }`
- **Notes:** `scope`: `environment`, `agent`, or `session`.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |
| `scope` | enum: `environment`, `agent`, `session` | no |  |

```json
{"tool": "veya_list_api_memory", "arguments": {"apiKey": "veya_live_…", "environmentId": "…", "scope": "agent"}}
```

## Public registry

Workflow guide: [registry.md](registry.md)

### `veya_public_stats`

Public registry stats from the product API (verified agents / proofs)

- **Access:** Public
- **Use when:** Public counts (verified agents, proofs).
- **Returns:** `{ httpStatus, body }`

_No arguments._

```json
{"tool": "veya_public_stats", "arguments": {}}
```

### `veya_public_list_agents`

List public agent registry rows

- **Access:** Public
- **Use when:** Browse public agents (limit 1–100).
- **Returns:** `{ httpStatus, body }`
- **Notes:** `limit` 1–100.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `limit` | number | no |  |
| `offset` | number | no |  |

```json
{"tool": "veya_public_list_agents", "arguments": {"limit": 20, "offset": 0}}
```

### `veya_public_get_agent`

Fetch one public agent by id

- **Access:** Public
- **Use when:** One public agent.
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes |  |

```json
{"tool": "veya_public_get_agent", "arguments": {"id": "…"}}
```

### `veya_public_list_certificates`

List public certificate / attestation rows

- **Access:** Public
- **Use when:** Browse public certificates/attestations.
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `limit` | number | no |  |
| `offset` | number | no |  |

```json
{"tool": "veya_public_list_certificates", "arguments": {"limit": 20}}
```

### `veya_public_get_certificate`

Fetch one public certificate by id

- **Access:** Public
- **Use when:** One public certificate.
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes |  |

```json
{"tool": "veya_public_get_certificate", "arguments": {"id": "…"}}
```

### `veya_public_get_execution`

Fetch a public execution proof by id

- **Access:** Public
- **Use when:** One public execution proof.
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes |  |

```json
{"tool": "veya_public_get_execution", "arguments": {"id": "…"}}
```

## On-chain writes

Workflow guide: [onchain-writes.md](onchain-writes.md)

### `veya_store_commitment`

Write a 32-byte commitment to Veya.sol from YOUR wallet (apiKey + payerPrivateKey)

- **Access:** API key + wallet
- **Use when:** Store a 32-byte digest for a 16-byte environment UUID (`storeCommitment`).
- **Returns:** `{ txHash, explorer, from }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | yes (or server env) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `environmentUuidHex` | string | yes | 16 bytes (32 hex) |
| `commitmentHex` | string | yes | 32 bytes (64 hex) |

```json
{"tool": "veya_store_commitment", "arguments": {"apiKey": "veya_live_…", "environmentUuidHex": "…", "commitmentHex": "…"}}
```

### `veya_attest_execution`

attestExecution on Veya.sol from YOUR wallet with ML-DSA bytes

- **Access:** API key + wallet
- **Use when:** Write an execution hash + ML-DSA signature (`attestExecution`).
- **Returns:** `{ txHash, explorer, from }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | yes (or server env) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `environmentUuidHex` | string | yes | 16 bytes (32 hex) |
| `blake3HashHex` | string | yes | 32 bytes (64 hex) |
| `mldsaSigHex` | string | yes |  |

```json
{"tool": "veya_attest_execution", "arguments": {"apiKey": "veya_live_…", "environmentUuidHex": "…", "blake3HashHex": "…", "mldsaSigHex": "…"}}
```

### `veya_register_environment`

registerEnvironment on Veya.sol from YOUR wallet. Pass product environmentId to confirm the tx on the product API.

- **Access:** API key + wallet
- **Use when:** Register an environment on-chain; with `environmentId` the product console is synced.
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

```json
{"tool": "veya_register_environment", "arguments": {"apiKey": "veya_live_…", "environmentId": "…"}}
```

### `veya_register_pq_onchain`

Generate ML-DSA identity and register environment + commitment on Veya.sol from YOUR wallet

- **Access:** API key + wallet
- **Use when:** Generate an ML-DSA identity and register environment + commitment in one step.
- **Returns:** Public key hex/hash, `environmentTx`, `memoTx`, `explorer`, `from`
- **Notes:** `envType` 0–10, default 1.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | yes (or server env) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `envType` | number | no |  |

```json
{"tool": "veya_register_pq_onchain", "arguments": {"apiKey": "veya_live_…", "envType": 1}}
```

### `veya_anchor_pq_attestation`

Link PQ identity hash to execution hash on Veya.sol from YOUR wallet

- **Access:** API key + wallet
- **Use when:** Link a PQ identity hash to an execution hash (`anchorPqAttestation`).
- **Returns:** `{ txHash, explorer, from }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `payerPrivateKey` | string | yes (or server env) | funded wallet bound to the API key (or `VEYA_PAYER_PRIVATE_KEY` on a self-hosted server) |
| `environmentUuidHex` | string | yes | 16 bytes (32 hex) |
| `identityHashHex` | string | yes | 32 bytes (64 hex) |
| `executionHashHex` | string | yes | 32 bytes (64 hex) |

```json
{"tool": "veya_anchor_pq_attestation", "arguments": {"apiKey": "veya_live_…", "environmentUuidHex": "…", "identityHashHex": "…", "executionHashHex": "…"}}
```
