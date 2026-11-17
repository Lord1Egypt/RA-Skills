# Access and limits

## Three access levels

| Level | Needs | Tools |
|---|---|---|
| **Public** | Nothing | `veya_describe`, `veya_ping_chain`, `veya_api_health`, `veya_writes_status`, `veya_hash_blake3`, `veya_prove` (no anchor), `veya_verify_*`, `veya_commitment_exists`, `veya_read_*_onchain`, `veya_pq_*`, `veya_verify_secure_message`, `veya_public_*`, `veya_verify_proof_api`, `veya_guest_login` |
| **API key** | `apiKey` argument (`veya_dev_…` / `veya_live_…`) | environments, agents, policy, routing, memory, consensus, sealed and protected execution, Boundnet, proofs list, `veya_seal_decision` |
| **API key + wallet** | `apiKey` + the funded wallet bound to it | `veya_store_commitment`, `veya_attest_execution`, `veya_register_environment`, `veya_register_pq_onchain`, `veya_anchor_pq_attestation`, `veya_anchor_proof`, `veya_prove` with `anchor: true` |

- The product API key is passed **as a tool argument**. The MCP server forwards it to
  `https://api.veyanet.tech` as `X-Api-Key`.
- Keys must start with `veya_dev_`, `veya_live_`, `vya_dev_` or `vya_live_`.
- A guest JWT from `veya_guest_login` (passed as `sessionToken`) lists showcase data only.
- Memory, tool rules and routing are owned by the key's account; another key cannot read them.
- Wallet writes check that the wallet matches the key's wallet before sending.

## Server endpoint auth

The hosted endpoint needs no header. A self-hosted server with `MCP_API_KEY` set requires:

```http
Authorization: Bearer <MCP_API_KEY>
```

Missing or wrong → HTTP 401 `{ "error": "unauthorized" }`.

## Limits (server defaults)

| Scope | Limit | Error |
|---|---|---|
| `/mcp` requests per client IP | 120 per minute | HTTP 429 |
| `veya_run_consensus`, `veya_client_run_consensus`, `veya_sealed_execute`, `veya_seal_decision` per API key | 30 per minute | `API key limit: 30 requests per minute` |
| host-sent `veya_seal_decision` per API key | 20 per UTC day | `Daily seal limit: 20 relayer sends for this API key` |
| host-sent `veya_seal_decision` per host | 100 per UTC day | `Daily seal limit: 100 relayer sends for this host` |
| Optional MCP sessions (`/mcp/session`) | 30 min idle, 1000 open | – |
| Product API call timeout | 20 s (`veya_api_health` 8 s) | `timeout` |

Per-minute windows reset each clock minute. Daily caps reset at 00:00 UTC (05:30 IST).
A relayer seal counts only when it succeeds.

## Agent rules

1. Ask for the API key only when a tool needs it, and use it only in `apiKey`.
2. Do not echo keys or wallet secrets in replies, memory or logs.
3. Confirm the network and get the user's go-ahead before any wallet write.
