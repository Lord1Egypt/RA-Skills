# Accounts, environments and agents

An **environment** is a scoped workspace (a "room"). **Agents** live inside it and carry a
`permissionConfig` that lists the tools they may call. These tools use the product API
(`https://api.veyanet.tech`). They create database rows only: no gas.

## Credentials

| Action | Guest JWT (`veya_guest_login`) | Product API key |
|---|---|---|
| List showcase environments, agents, proofs | yes | yes |
| `veya_account` | – | yes |
| Create environment | – | yes |
| Deploy agent, protected execution, Boundnet | – | yes |
| On-chain writes | – | yes, plus the wallet bound to the key |

Create a key (`veya_dev_…` or `veya_live_…`) at https://app.veyanet.tech: connect your wallet, then open **System → API Keys**.

## Workflow: set up a workspace with one agent

**1. Check the key**

```json
{ "tool": "veya_account", "arguments": { "apiKey": "veya_live_…" } }
```

→ `{ "httpStatus": 200, "body": { "wallet": "0x…", … } }`

**2. Create the environment**

```json
{ "tool": "veya_create_environment", "arguments": { "apiKey": "veya_live_…", "name": "VEYA Treasury Ops", "type": "treasury" } }
```

`type`: `research` (default), `governance`, `treasury`, `contributor`, `protocol`, `desci`.
Save `body.id` as `environmentId`.

**3. Deploy an agent with an allowlist**

```json
{
  "tool": "veya_deploy_agent",
  "arguments": {
    "apiKey": "veya_live_…",
    "environmentId": "…",
    "agentKind": "reviewer",
    "permissionConfig": { "allowedTools": ["veya_prove", "veya_store_memory"] }
  }
}
```

`type` defaults to `coordination`. List every tool the agent needs; an agent with no
`allowedTools` calls no tools. Save `body.id` as `agentId`.

**4. Inspect**

`veya_list_environments`, `veya_get_environment`, `veya_list_agents`.

**5. (Optional) Register on-chain**

`veya_register_environment` with `apiKey` + `environmentId` writes `registerEnvironment`
from the user's wallet and syncs the console (`consoleSynced: true`). See
[onchain-writes.md](onchain-writes.md).

## Tools

### `veya_guest_login`

Create a guest session on the product API (Use listing only). Guest cannot mint API keys or write from MCP.

- **Access:** Public
- **Returns:** Guest JWT, `mode: guest` (listing only)

_No arguments._

### `veya_account`

Return the wallet bound to a product API key

- **Access:** API key
- **Returns:** `{ httpStatus, body }` with `wallet`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |

### `veya_list_environments`

List environments for a product API key (guest JWT sees showcase / Use scope only)

- **Access:** API key (guest: listing)
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |

### `veya_get_environment`

Get one environment by id

- **Access:** API key (guest: listing)
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |

### `veya_create_environment`

Create a workspace in the product API. This does not spend gas and sends no transaction. Guests and non-keys are refused. type is stored for the API and defaults to research when omitted. Names that start with test, demo, tmp, sandbox, or e2e are refused. Use a real workspace name of at least 6 characters, or a name that starts with VEYA.

- **Access:** API key
- **Returns:** `{ httpStatus, body }` with the new environment
- **Notes:** `type` defaults to `research`. Register it on-chain later with `veya_register_environment`. Use a product-style name such as `VEYA Treasury Ops`: names with the words `test`, `demo`, `tmp` or `sandbox` return `CONFLICT` (HTTP 409).

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `name` | string | yes |  |
| `type` | enum: `research`, `governance`, `treasury`, `contributor`, `protocol`, `desci` | no |  |

### `veya_list_agents`

List agents in an environment

- **Access:** API key (guest: listing)
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes (or `sessionToken` for listing) | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |

### `veya_deploy_agent`

Create an agent in a workspace. This does not spend gas and sends no transaction. Limit the agent with permissionConfig.allowedTools. If allowedTools is omitted, the agent cannot call a tool. type is stored for the API and defaults to coordination when omitted.

- **Access:** API key
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

