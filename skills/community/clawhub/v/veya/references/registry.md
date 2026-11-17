# Public registry

The product API publishes verified agents, certificates (attestations) and execution proofs
at `/public/*`. These tools are public and return `{ httpStatus, body }`.

| Tool | Endpoint |
|---|---|
| `veya_public_stats` | `GET /public/stats` |
| `veya_public_list_agents` | `GET /public/agents?limit&offset` |
| `veya_public_get_agent` | `GET /public/agents/:id` |
| `veya_public_list_certificates` | `GET /public/certificates?limit&offset` |
| `veya_public_get_certificate` | `GET /public/certificates/:id` |
| `veya_public_get_execution` | `GET /public/executions/:id` |

## Workflow: due diligence on an agent

1. `veya_public_stats` → overall counts.
2. `veya_public_list_agents` with `{ "limit": 20 }` → find the agent; `limit` is 1–100.
3. `veya_public_get_agent` with `id` → public fields.
4. `veya_public_list_certificates` / `veya_public_get_certificate` → its attestations.
5. Cross-check a certificate's tx with `veya_verify_commitment_onchain`
   ([verification.md](verification.md)) and an on-chain record with `veya_read_agent_onchain`.

## Tools

### `veya_public_stats`

Public registry stats from the product API (verified agents / proofs)

- **Access:** Public
- **Returns:** `{ httpStatus, body }`

_No arguments._

### `veya_public_list_agents`

List public agent registry rows

- **Access:** Public
- **Returns:** `{ httpStatus, body }`
- **Notes:** `limit` 1–100.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `limit` | number | no |  |
| `offset` | number | no |  |

### `veya_public_get_agent`

Fetch one public agent by id

- **Access:** Public
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes |  |

### `veya_public_list_certificates`

List public certificate / attestation rows

- **Access:** Public
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `limit` | number | no |  |
| `offset` | number | no |  |

### `veya_public_get_certificate`

Fetch one public certificate by id

- **Access:** Public
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes |  |

### `veya_public_get_execution`

Fetch a public execution proof by id

- **Access:** Public
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes |  |

