# Agent memory

Memory rows are stored on the account behind the API key
(`/v1/environments/:id/scoped-memory`). Only that key can read or nullify them.

## Workflow

**Store**

```json
{ "tool": "veya_store_memory", "arguments": { "apiKey": "veya_live_…", "environmentId": "…", "agentId": "…", "data": "Client prefers weekly summaries." } }
```

Save the returned row `id`.

**Read**

```json
{ "tool": "veya_read_memory", "arguments": { "apiKey": "veya_live_…", "environmentId": "…", "id": "…" } }
```

**Nullify** (the row is marked invalid)

```json
{ "tool": "veya_invalidate_memory", "arguments": { "apiKey": "veya_live_…", "environmentId": "…", "id": "…" } }
```

**List**

```json
{ "tool": "veya_list_api_memory", "arguments": { "apiKey": "veya_live_…", "environmentId": "…", "scope": "agent" } }
```

`scope`: `environment`, `agent`, or `session`.

## Good practice

- Store facts the agent needs later; keep secrets and keys out of memory.
- Nullify rows that are outdated instead of storing contradictions.

## Tools

### `veya_store_memory`

Store agent memory for the account behind this API key. No key, no write.

- **Access:** API key (owner)
- **Returns:** Stored row with `id`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `agentId` | string | yes |  |
| `data` | string | yes |  |

### `veya_read_memory`

Read one memory row owned by this API key.

- **Access:** API key (owner)
- **Returns:** Memory row

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `id` | string | yes |  |

### `veya_invalidate_memory`

Nullify one memory row owned by this API key.

- **Access:** API key (owner)
- **Returns:** Nullified row

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `id` | string | yes |  |

### `veya_list_api_memory`

List memory entries via product API for an environment

- **Access:** API key (guest: listing)
- **Returns:** `{ httpStatus, body }`
- **Notes:** `scope`: `environment`, `agent`, or `session`.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |
| `scope` | enum: `environment`, `agent`, `session` | no |  |

