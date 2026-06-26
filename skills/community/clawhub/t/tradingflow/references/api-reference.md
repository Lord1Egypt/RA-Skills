# TradingFlow API Reference

Base URL: `$TRADINGCLAW_BASE_URL` (default: `https://api.tradingflow.fun/api/v1`)

Auth header: `Authorization: Bearer $TRADINGCLAW_API_KEY`

Response format: `{"data":{...}}` on success, `{"error":"message"}` on failure.

---

## Strategy Endpoints

Prefix: `/strategy`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/strategy` | Yes | Create strategy |
| GET | `/strategy/list` | Yes | List user strategies |
| GET | `/strategy/:id` | Yes | Get strategy details |
| PUT | `/strategy/:id` | Yes | Update strategy (auto-increments version) |
| POST | `/strategy/:id/generate` | Yes | Store generated code |
| POST | `/strategy/:id/link-process` | Yes | Link strategy to TFP |
| DELETE | `/strategy/:id/link-process` | Yes | Unlink TFP |
| DELETE | `/strategy/:id` | Yes | Soft delete |

### POST /strategy

```json
{
  "name": "BTC DCA",
  "description": "Dollar cost average BTC weekly",
  "content": "STRATEGY: BTC DCA\nVERSION: 1\n...",
  "language": "python",
  "chain": "bsc",
  "triggers": [],
  "operators": [],
  "tags": ["dca", "btc"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | yes | Strategy name |
| content | string | yes | Strategy definition text |
| language | `python` / `javascript` / `typescript` / `markdown` | yes | Language (`markdown` for natural-language strategy descriptions) |
| description | string | no | Human-readable description |
| chain | string | no | Target chain (bsc, aptos, solana) |
| triggers | array | no | Trigger configuration |
| operators | array | no | Operator dependencies |
| tags | string[] | no | Searchable tags |

### PUT /strategy/:id

```json
{
  "name": "Updated Name",
  "content": "updated strategy text...",
  "description": "Updated with risk controls",
  "triggers": [],
  "operators": [],
  "tags": ["updated"]
}
```

All fields optional. Updating `content` auto-increments the version.

### POST /strategy/:id/generate

```json
{
  "files": [
    {"name": "main.py", "content": "import ccxt\n..."},
    {"name": "utils.py", "content": "def helper(): ..."}
  ],
  "dependencies": ["ccxt", "requests"]
}
```

### GET /strategy/list

Query params: `?language=python&chain=bsc&isPublic=true`

---

## TFP (Process) Endpoints

Prefix: `/tfp`

> **⚠️ IMPORTANT FOR AGENTS**: Do NOT call `POST /tfp` directly to create processes. Always use the `deploy_process` tool via `POST /claw/execute` — it creates the process, deploys code from `strategy.generatedCode`, and auto-starts it in one step. A process created via `POST /tfp` alone will be **stuck in `creating` status** forever because no code is deployed.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/tfp` | Yes | Create process (low-level — prefer `deploy_process` tool) |
| GET | `/tfp/list` | Yes | List user processes |
| GET | `/tfp/:id` | Yes | Get process details |
| POST | `/tfp/:id/deploy` | Yes | Deploy code (low-level — prefer `deploy_process` tool) |
| POST | `/tfp/:id/start` | Yes | Restart a stopped process (NOT for initial launch) |
| POST | `/tfp/:id/stop` | Yes | Stop a running process |
| POST | `/tfp/:id/restart` | Yes | Restart a process |
| GET | `/tfp/:id/logs` | Yes | Get stdout/stderr logs |
| POST | `/tfp/:id/exec` | Yes | Execute command in container (501 — not yet implemented) |
| DELETE | `/tfp/:id` | Yes | Soft delete |

### Recommended: Use `deploy_process` tool

```bash
# This is the CORRECT way for agents to create+deploy+start a process:
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"deploy_process","params":{"strategyId":"...","name":"btc-dca-bot"}}'
# → Automatically: creates TFP → deploys code from strategy.generatedCode → starts process
```

### POST /tfp (low-level, internal use only)

```json
{
  "name": "btc-dca-bot",
  "language": "python",
  "runtime": "thread",
  "strategyId": "optional_strategy_id",
  "resources": {"cpu": 0.25, "memory": 256, "disk": 500},
  "triggers": [],
  "operators": ["vault-bsc"],
  "envVars": {"NODE_ENV": "production"}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | yes | Process display name |
| language | `python` / `javascript` / `typescript` | yes | Programming language |
| runtime | `thread` / `container` | no | Default: `thread`. `thread` = child_process (fast start), `container` = Docker (full isolation) |
| strategyId | string | no | Link to an existing strategy |
| resources | object | no | CPU/memory/disk limits |
| triggers | array | no | Event triggers |
| operators | string[] | no | Operator dependencies |
| envVars | object | no | Environment variables injected at runtime |

### POST /tfp/:id/deploy (low-level, internal use only)

```json
{
  "files": [
    {"name": "main.py", "content": "import requests\n..."},
    {"name": "utils.py", "content": "def helper(): ..."}
  ],
  "dependencies": ["requests", "ccxt"]
}
```

### GET /tfp/:id/logs

Query params: `?lines=100&level=error`

| Param | Type | Description |
|-------|------|-------------|
| lines | number | Number of log lines to return (default varies) |
| level | `info` / `warn` / `error` / `debug` | Filter by log level. Omit for all levels |

### GET /tfp/list

Query params: `?status=running&language=python`

---

## User Secrets Endpoints

Prefix: `/user-secrets`

Manages encrypted secrets and environment variables for TFP processes.
Secrets use AES-256-GCM envelope encryption; env vars are stored and readable.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/user-secrets` | Yes | Create secret or env var |
| GET | `/user-secrets` | Yes | List all (values redacted for secrets) |
| PUT | `/user-secrets/:name` | Yes | Update value |
| DELETE | `/user-secrets/:name` | Yes | Delete |
| GET | `/user-secrets/:name/value` | Yes | Get plaintext value (env_var only) |
| GET | `/user-secrets/internal/:name` | TFP SDK | Internal: TFP reads secret at runtime via `x-tfp-secret-token` header |

### POST /user-secrets

```json
{
  "name": "BINANCE_API_KEY",
  "value": "abc123...",
  "category": "secret",
  "description": "Main Binance account API key"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | yes | Unique name (uppercase, A-Z_0-9 recommended) |
| value | string | yes | The secret or env var value |
| category | `secret` / `env_var` | yes | `secret` = encrypted, write-only; `env_var` = readable |
| description | string | no | Human-readable description |

### PUT /user-secrets/:name

```json
{
  "value": "new_value_here"
}
```

### GET /user-secrets/:name/value

Returns plaintext value. **Only works for `env_var` category.** Secrets cannot be read back.

---

## Vault Endpoints (TFV Protocol v0.3)

Prefix: `/vault`

All write operations return unsigned `txData` for the user to sign via their wallet.
Supported chains: `bsc`, `aptos`, `solana`.

### Core Operations (v0.2)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vault/chains` | No | List supported chains |
| GET | `/vault/:chain/status` | Yes | Vault address and deployment status |
| GET | `/vault/:chain/balances` | Yes | Token balances in vault |
| POST | `/vault/:chain/create` | Yes | Build create-vault tx |
| POST | `/vault/:chain/role` | Yes | Build set-role tx |
| POST | `/vault/:chain/spending-limit` | Yes | Build spending-limit tx (v0.2 legacy) |

#### GET /vault/:chain/status

Query: `?address={walletAddress}`

Response:
```json
{
  "data": {
    "chain": "bsc",
    "address": "0x1234...vault",
    "exists": true,
    "isActive": true
  }
}
```

#### GET /vault/:chain/balances

Query: `?address={vaultAddress}`

Response:
```json
{
  "data": {
    "balances": [
      {"symbol": "USDT", "balance": "1250500000000000000000", "address": "0x...", "decimals": 18},
      {"symbol": "BNB", "balance": "2350000000000000000", "address": "native", "decimals": 18}
    ]
  }
}
```

#### POST /vault/:chain/create

```json
{
  "investor": "0x...",
  "oracle": "0x..."
}
```

#### POST /vault/:chain/role

```json
{
  "vaultAddress": "0x...",
  "role": "agent",
  "target": "0x..."
}
```

### Agent Permissions (v0.3)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vault/:chain/:address/agent-permissions/:agent` | Yes | Query agent permission bitmask |
| POST | `/vault/:chain/:address/set-agent-permissions` | Yes | Build set-permissions tx |

Permission bitmask: `1` = SWAP, `2` = BORROW, `4` = WITHDRAW. Combine with OR (e.g. `3` = SWAP + BORROW).

#### POST /vault/:chain/:address/set-agent-permissions

```json
{
  "agent": "0x...",
  "permissions": 7
}
```

### Per-Token Spending Limits (v0.3)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vault/:chain/:address/token-spending-limit/:token` | Yes | Query daily spending limit for a token |
| POST | `/vault/:chain/:address/set-token-spending-limit` | Yes | Build set-limit tx |

#### GET response

```json
{
  "data": {
    "limit": "1000000000000000000000",
    "spentToday": "250000000000000000000",
    "resetsAt": "1706745600"
  }
}
```

#### POST /vault/:chain/:address/set-token-spending-limit

```json
{
  "token": "0x...",
  "dailyLimit": "1000000000000000000000"
}
```

### Withdraw Allowance (v0.3)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vault/:chain/:address/withdraw-allowance/:token` | Yes | Query withdraw allowance |
| POST | `/vault/:chain/:address/set-withdraw-allowance` | Yes | Build set-allowance tx |
| POST | `/vault/:chain/:address/agent-withdraw` | Yes | Build agent-withdraw tx |

#### GET response

```json
{
  "data": {
    "total": "5000000000000000000000",
    "used": "1000000000000000000000",
    "remaining": "4000000000000000000000",
    "resetsAt": "1706745600"
  }
}
```

#### POST /vault/:chain/:address/set-withdraw-allowance

```json
{
  "token": "0x...",
  "amount": "5000000000000000000000",
  "period": 86400
}
```

`period` is in seconds. Common values: 3600 (1h), 86400 (24h), 604800 (7d).

#### POST /vault/:chain/:address/agent-withdraw

```json
{
  "token": "0x...",
  "amount": "500000000000000000000",
  "to": "0x..."
}
```

### Borrow / Repay (v0.3)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vault/:chain/:address/borrows` | Yes | List active borrow records |
| POST | `/vault/:chain/:address/borrow` | Yes | Build borrow tx |
| POST | `/vault/:chain/:address/repay` | Yes | Build repay tx |
| POST | `/vault/:chain/:address/force-close-borrow` | Yes | Build force-close tx (for overdue borrows) |

#### GET /vault/:chain/:address/borrows response

```json
{
  "data": {
    "borrows": [
      {
        "borrowId": 0,
        "agent": "0x...",
        "tokenBorrowed": "0x...",
        "amountBorrowed": "1000000000000000000",
        "borrowedAt": "1706659200",
        "deadline": "1706745600",
        "isRepaid": false
      }
    ]
  }
}
```

#### POST /vault/:chain/:address/borrow

```json
{
  "token": "0x...",
  "amount": "1000000000000000000",
  "duration": 86400
}
```

#### POST /vault/:chain/:address/repay

```json
{
  "borrowId": 0,
  "tokenRepaid": "0x...",
  "amountRepaid": "1000000000000000000"
}
```

#### POST /vault/:chain/:address/force-close-borrow

```json
{
  "borrowId": 0
}
```

---

## Webhook Endpoints

Prefix: `/webhook`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/webhook` | Yes | Create webhook |
| GET | `/webhook/list/:processId` | Yes | List webhooks for process |
| GET | `/webhook/:id` | Yes | Get webhook details |
| DELETE | `/webhook/:id` | Yes | Soft delete |
| POST | `/webhook/inbound/:token` | No | Trigger webhook (public, no auth) |

### POST /webhook

```json
{
  "processId": "...",
  "name": "price-alert",
  "type": "inbound",
  "events": ["trigger"],
  "targetUrl": "https://...",
  "headers": {},
  "secret": "optional_hmac_secret"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| processId | string | yes | Target TFP process |
| name | string | yes | Webhook display name |
| type | string | yes | Webhook type (e.g. `inbound`) |
| events | string[] | yes | Events to listen for |
| targetUrl | string | no | Outbound webhook URL |
| headers | object | no | Custom headers for outbound |
| secret | string | no | HMAC signing secret |

Response includes `inboundUrl` for external services to call.

---

## Claw (Agent) Endpoints

Prefix: `/claw`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/claw/skill` | No | Get SKILL.md content (public) |
| GET | `/claw/skill/download` | Yes | Download personalized SKILL.md with API key hints |
| POST | `/claw/setup` | Yes | One-click setup: generate API key + SKILL instructions |
| POST | `/claw/api-key` | Yes | Generate new API key |
| GET | `/claw/api-keys` | Yes | List API keys |
| DELETE | `/claw/api-key/:keyId` | Yes | Revoke API key |
| GET | `/claw/tools` | No | List available tools (public) |
| POST | `/claw/execute` | Yes* | Execute tool call |

*`/claw/execute` accepts both JWT and `tfc_` API key auth.

### POST /claw/setup

```json
{
  "name": "My Trading Agent"
}
```

Returns API key, SKILL content, and setup instructions.

### POST /claw/execute

```json
{
  "tool": "create_strategy",
  "params": {
    "name": "ETH Momentum",
    "content": "...",
    "language": "python",
    "chain": "bsc"
  }
}
```

Available tools: `create_strategy`, `list_strategies`, `deploy_process`, `list_processes`, `get_process_logs`, `stop_process`, `start_process`, `get_vault_balance`, `execute_trade`

---

## Agent Approval Endpoints

Prefix: `/claw/approval`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/claw/approval/request` | Yes* | Request user approval (returns URL) |
| GET | `/claw/approval/:token` | No | Get approval details (public) |
| POST | `/claw/approval/:token/respond` | Yes | User approves/rejects (requires JWT) |
| GET | `/claw/approval/status/:approvalId` | Yes* | Poll approval status |

*Accepts both JWT and API key.

### POST /claw/approval/request

```json
{
  "action": "withdraw",
  "description": "Withdraw 50 USDT from BSC vault to external wallet",
  "chain": "bsc",
  "params": {"amount": "50", "token": "USDT", "to": "0x..."},
  "txData": {"to": "0xVault", "data": "0x...", "value": "0", "chainId": 97},
  "requiredAddress": "0xInvestorWallet"
}
```

> `requiredAddress` is optional — if omitted and `txData` is present, the backend auto-resolves from the user's linked wallet. Returns `wallet_not_linked` error if no wallet is bound.

Actions: `withdraw`, `deposit`, `swap`, `set_role`, `generic` — expires in 15 minutes.

### POST /claw/approval/:token/respond

```json
{
  "decision": "approve",
  "txHash": "0x..."
}
```

---

## Strategy Hub Endpoints

Prefix: `/hub`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/hub/strategies` | Optional | Browse published strategies (paginated) |
| GET | `/hub/strategies/:id` | Optional | View strategy details (increments view count) |
| POST | `/hub/strategies/:id/star` | Yes | Toggle star/unstar on a strategy |
| GET | `/hub/starred` | Yes | List user's starred strategies |
| POST | `/hub/publish/:id` | Yes | Publish your strategy to Hub |
| POST | `/hub/unpublish/:id` | Yes | Unpublish strategy from Hub |

### GET /hub/strategies

Query params:

| Param | Type | Description |
|-------|------|-------------|
| q / search | string | Search by name/description |
| tags | string | Filter by tag |
| language | string | Filter by language |
| chain | string | Filter by chain |
| sort | string | Sort order |
| page | number | Page number |
| limit | number | Items per page |

---

## Operator Endpoints

Prefix: `/operator`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/operator/list` | Yes | List available operators |
| GET | `/operator/:id` | Yes | Get operator details |

---

## Credits Endpoints

Prefix: `/credits`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/credits/costs` | No | Current pricing table |
| GET | `/credits/balance` | Yes | Current credit balance |
| GET | `/credits/stats` | Yes | Credit usage statistics |
| GET | `/credits/history` | Yes | Transaction history (paginated) |
| POST | `/credits/add` | Admin | Admin: adjust user credits |
| POST | `/credits/refresh` | Yes | Check and execute monthly credit refresh |

### GET /credits/history

Query params: `?page=1&limit=20&type=deduction`

### POST /credits/add (admin only)

```json
{
  "userId": "...",
  "amount": 1000,
  "type": "bonus",
  "metadata": {"reason": "Beta reward"}
}
```

---

## Subscription Endpoints

Prefix: `/subscriptions`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/subscriptions/current` | Yes | Get current subscription info |
| POST | `/subscriptions/purchase` | Yes | Purchase Pro subscription |
| POST | `/subscriptions/confirm` | Admin | Admin: confirm payment |

### POST /subscriptions/purchase

```json
{
  "transactionId": "0x...",
  "amount": 29.99
}
```

---

## Auth Endpoints

Prefix: `/auth`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/auth/google` | No | Initiate Google OAuth |
| GET | `/auth/google/callback` | No | Google OAuth callback |
| GET | `/auth/wallet/nonce` | No | Get nonce for wallet signing |
| POST | `/auth/wallet/verify` | Optional | Verify wallet signature and login/bind |
| GET | `/auth/me` | Yes | Current user profile |
| PUT | `/auth/me` | Yes | Update profile |
| GET | `/auth/identities` | Yes | List user identities |
| GET | `/auth/identities/check` | Optional | Check if identity is bound |
| DELETE | `/auth/identities/:identityId` | Yes | Unbind identity |
| POST | `/auth/invitation/bind` | Yes | Bind invitation code |
| GET | `/auth/invitation/info` | Yes | Get invitation code and stats |
| POST | `/auth/redeem` | Yes | Redeem activation code |

### GET /auth/wallet/nonce

Query: `?address=0x...&chain=ethereum`

Supported chains: `ethereum`, `aptos`, `solana`

### POST /auth/wallet/verify

```json
{
  "address": "0x...",
  "signature": "0x...",
  "walletType": "metamask",
  "chain": "ethereum",
  "pubKey": "optional_for_solana"
}
```

Returns `{ token, user }` on success.

### PUT /auth/me

```json
{
  "name": "Cleopatra",
  "username": "cleo",
  "bio": "DeFi enthusiast",
  "avatar": "https://...",
  "location": "Singapore",
  "website": "https://tradingflow.fun"
}
```

All fields optional.

---

## Cluster Endpoints

Prefix: `/cluster`

Internal endpoints for multi-node deployment. Generally not used by end users.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/cluster/status` | No | Cluster health status |
| GET | `/cluster/surges` | No | Active Surge worker nodes |
| GET | `/cluster/flow/:flowId/assignment` | No | Flow assignment info |
| POST | `/cluster/recover` | No | Trigger stale flow recovery |
