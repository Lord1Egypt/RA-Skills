---
name: veya
description: Operate VEYA, the post-quantum execution and proof layer for AI agents on Robinhood Chain, through the hosted VEYA MCP server (51 veya_* tools). Prove and anchor content as BLAKE3 commitments on Veya.sol, verify transactions and commitments, create ML-DSA-44 identities and signatures, manage environments, agents, tool policy and Kyber-768 secure routing, run 2-of-3 consensus and AES-256-GCM sealed execution, store agent memory, browse the public registry, and send on-chain writes from your own wallet. Use when the user mentions VEYA, veyanet, Veya.sol, Robinhood Chain, on-chain proof or attestation of agent work, BLAKE3 commitments, ML-DSA, Kyber, post-quantum signatures, sealed or protected execution, agent consensus, or any veya_ tool.
compatibility: Requires the VEYA MCP server at https://mcp.veyanet.tech/mcp (Streamable HTTP) and network access. Scoped and write tools need a VEYA product API key.
metadata:
  author: veyanet
  homepage: https://veyanet.tech
  mcp-url: https://mcp.veyanet.tech/mcp
  tools: "51"
  version: "1.2.8"
---

# VEYA

VEYA makes agent work verifiable. An agent runs inside a scoped **environment** with an
explicit tool allowlist. Its work is checked by **2-of-3 consensus** or run in **AES-256-GCM
sealed execution**, hashed with **BLAKE3-256**, signed with **ML-DSA-44**, and anchored on the
**Veya.sol** protocol contract on Robinhood Chain. Anyone can verify the record from a tx hash.

```
environment → agent (+ allowedTools) → consensus / sealed execution
  → BLAKE3 digest + ML-DSA signature → Veya.sol (Robinhood Chain) → verify
```

| Network | Veya.sol | Explorer |
|---|---|---|
| **Mainnet (default)** | `0x87dC582eEA544A434a5C1e30Ca3d12c1e548a674` | robinhoodchain.blockscout.com |
| Testnet (optional) | `0x1a1Dc3c55550FCE9F70ef6cDEeF967c0b72a5d84` | explorer.testnet.chain.robinhood.com |

## Before anything

1. If no `veya_*` tools are available, tell the user to add the MCP server
   `https://mcp.veyanet.tech/mcp` (configs in [references/setup.md](references/setup.md)) and stop.
2. Call `veya_describe`. Read `settlement.network`, `settlement.contract`, `settlement.explorer`.
   Use that network and explorer in every answer.

## Access

- **Public** (no key): describe, ping, health, hashing, `veya_prove` without anchor, all verify and on-chain reads, `veya_pq_*`, public registry.
- **API key**: pass the user's product key (`veya_dev_…` / `veya_live_…`) as the `apiKey` argument. Get one at https://app.veyanet.tech (connect wallet → System → API Keys). Needed for environments, agents, policy, routing, memory, consensus, sealed execution, `veya_seal_decision`.
- **API key + wallet**: on-chain writes also need the funded wallet bound to that key (`payerPrivateKey`). Gas is ETH on the selected network.
- **Limits**: consensus, sealed execution and `veya_seal_decision` allow 30 calls/min per key. host-sent seals: 20 per key and 100 per host per UTC day. `/mcp`: 120 requests/min per IP.

Details: [references/auth-and-limits.md](references/auth-and-limits.md).

## Decision flow

| User wants to… | Do this | Guide |
|---|---|---|
| Check status / network | `veya_describe` → `veya_ping_chain` → `veya_api_health` | [service-and-chain](references/service-and-chain.md) |
| Hash or prove text/JSON | `veya_prove { text \| json }` | [proofs](references/proofs.md) |
| Anchor a proof on-chain | `veya_prove { text, anchor: true, environmentId, apiKey, payerPrivateKey }` or `veya_anchor_proof` | [proofs](references/proofs.md) |
| Check a tx or commitment | `veya_verify_transaction` → `veya_verify_commitment_onchain` | [verification](references/verification.md) |
| Check a digest | `veya_commitment_exists { digestHex }` | [verification](references/verification.md) |
| Seal a decision | `veya_seal_decision { evidenceId, decision, apiKey, environmentId }` (mainnet: a registered environment) | [proofs](references/proofs.md) |
| PQ keys, sign, verify | `veya_pq_keygen` → `veya_pq_sign` → `veya_pq_verify` | [identity](references/identity.md) |
| Create a workspace and agent | `veya_create_environment` → `veya_deploy_agent` | [workspaces](references/workspaces.md) |
| Allow/deny tools, route messages | `veya_set_tool_policy`, `veya_route_message`, `veya_route_secure_message` | [policy-and-routing](references/policy-and-routing.md) |
| Quorum or sealed run | `veya_run_consensus`, `veya_sealed_execute`, `veya_run_protected_execution` | [execution](references/execution.md) |
| Agent memory | `veya_store_memory`, `veya_read_memory`, `veya_invalidate_memory` | [memory](references/memory.md) |
| Browse public agents/certificates | `veya_public_*` | [registry](references/registry.md) |
| Write commitments / attestations | `veya_store_commitment`, `veya_attest_execution`, `veya_register_environment` | [onchain-writes](references/onchain-writes.md) |
| Exact args of any tool | – | [tools](references/tools.md) |

## Workflow 1: prove content (no key)

```json
{ "tool": "veya_prove", "arguments": { "text": "hello" } }
```

Pass **exactly one** of `text`, `json` (a JSON string), `txHash`. Expect `ok: true`, `mode: "digest"`,
`digestHex`, `anchored: false`. `hello` → `ea8f163db38682925e4491c5e58d4bb3506ef8c14eb78a86e908c5624a67200f`.
To anchor: add `anchor: true`, `environmentId` (an environment already on Veya.sol), `apiKey`,
`payerPrivateKey`. Expect `mode: "anchored"`, `txHash`, `explorerUrl`.

## Workflow 2: verify a transaction

Example Mainnet receipt (execution attestation): `0x91550fdd7a60616e3157364d3624d423403c4add2590c36d3ba290fa07cb95cc`.

1. `veya_verify_transaction { txHash }` → Veya.sol events and digest.
2. `veya_verify_commitment_onchain { txHash }` → for commitment txs, confirms `commitments(digest)` is still true (`commitmentChecks` is empty for attestations and registrations).
3. Report network, event, digest, and `{explorer}/tx/{txHash}`. If `to` is not Veya.sol, say it is not a VEYA proof.

## Workflow 3: workspace → agent → policy

1. `veya_account { apiKey }` → confirm the wallet.
2. `veya_create_environment { apiKey, name, type? }` → `environmentId` (`type`: research default, governance, treasury, contributor, protocol, desci).
3. `veya_deploy_agent { apiKey, environmentId, permissionConfig: { allowedTools: [...] } }` → `agentId`. List every tool the agent needs.
4. `veya_set_tool_policy { apiKey, environmentId, agentId, tool, allowed }` to adjust.
5. Optional: `veya_register_environment { apiKey, payerPrivateKey, environmentId }` puts it on-chain.

## Workflow 4: consensus → attestation

1. `veya_api_health` → validators reachable.
2. `veya_run_consensus { apiKey, taskId, payload }` → require `consensus_reached: true`; take `agreed_blake3_hash`.
3. `veya_pq_sign { message: <hash>, privateKeyHex }` → `signatureHex`.
4. `veya_attest_execution { apiKey, payerPrivateKey, environmentUuidHex, blake3HashHex, mldsaSigHex }` → `txHash`, `from`.
5. `veya_verify_transaction { txHash }`.

## Rules

1. Start read-only; write only when the user asks for an on-chain result.
2. Before a write: state the network (Robinhood Chain Mainnet unless Testnet was selected), run `veya_writes_status`, and get the user's confirmation.
3. Use keys only inside tool arguments; never repeat them in replies or store them in memory.
4. Hex: UUIDs are 16 bytes (32 hex), digests 32 bytes (64 hex); `0x` optional.
5. Use `veya_run_consensus` (`veya_client_run_consensus` is a deprecated alias).
6. Never attest when `consensus_reached` is `false`.
7. If a write returns `warning`, the chain write succeeded; do not resend.
8. After every write, return `txHash`, the explorer link and `from`.
9. Describe VEYA only as what it does: it checks, limits, records and proves agent actions. It does not trade, connect to exchanges, hold or move user funds, or read price or market data.

## Errors

| Message | Action |
|---|---|
| `apiKey required` / `Create a product API key…` | Ask for a `veya_dev_`/`veya_live_` key from https://app.veyanet.tech (connect wallet → System → API Keys) |
| `Your wallet has no ETH on Robinhood Chain. Add funds and try again.` | User funds the wallet bound to the key |
| `payerPrivateKey does not match the wallet on this API key…` | Use the wallet shown by `veya_account` |
| `API key limit: 30 requests per minute` | Wait one minute, retry once |
| `Daily seal limit: …` | Pass the user's wallet or wait until 00:00 UTC |
| `SEAL_ENVIRONMENT_REQUIRED` | On mainnet pass `environmentId` of a registered environment (`veya_create_environment` → `veya_register_environment`) |
| `CONFLICT` on `veya_create_environment` | Pick a product-style name without test/demo/tmp/sandbox |
| `NOT_VEYA_TX` | `veya_verify_proof_api` takes commitment/anchor txs; use `veya_verify_transaction` for registrations |
| `consensus_reached: false` / `SEALED_UNREACHABLE` | Check `veya_api_health`; nothing was written |
| `Pass exactly one of text, json, or txHash.` | Fix the `veya_prove` input |

Full list: [references/troubleshooting.md](references/troubleshooting.md).

## Custom logic

For custom pipelines or local signing, use `@veyanet/sdk` (same capabilities as code):
[references/sdk.md](references/sdk.md).

## Links

- App and API keys: https://app.veyanet.tech
- Docs: https://veyanet.tech/docs
- SDK: https://github.com/veyanet/veya-sdk
- MCP server: https://github.com/veyanet/veya-mcp
