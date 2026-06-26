---
name: tradingflow
description: >
  Create and manage crypto trading strategies, deploy automated trading bots,
  and control on-chain vaults on BSC, Aptos, and Solana. Use when the user wants
  to trade crypto, manage DeFi positions, set up automated strategies, check
  vault balances, deploy quantitative trading programs, or interact with
  TradingFlow platform.
license: MIT
compatibility: Requires network access. Works with OpenClaw, Claude Code, Cursor, and other AgentSkills-compatible agents.
metadata:
  author: TradingFlow Team
  version: "1.0.0"
  tags: trading, crypto, defi, vault, strategy, automation, web3, workflow
  homepage: https://tradingflow.fun
  requires: python3, node, curl, jq
  env: TRADINGCLAW_API_KEY, TRADINGCLAW_BASE_URL, TRADINGCLAW_SITE_URL
---

# TradingFlow

**TradingFlow** is an intention trading platform with four core capabilities:

1. **Asset Custody** — On-chain vaults with fine-grained agent permissions (TFV Protocol v0.5) on BSC, Aptos, and Solana
2. **Vibe Trading** — Natural language commands → on-chain execution via agent-controlled vaults
3. **Quantitative Strategies** — `.STRATEGY` text files compiled to hosted Python/JS/TS programs (TFP)
4. **Strategy Hub** — Community marketplace to publish, discover, and star strategies

## When to Use This Skill

Activate when user intent matches any of the following:

| Category | User phrases / keywords |
|----------|------------------------|
| Balance & Vault | "check vault", "my balance", "vault status", "what tokens do I have", "show my assets" |
| Create Strategy | "create strategy", "write a strategy", "new trading strategy", "build a bot", "DCA strategy" |
| Deploy & Run | "deploy strategy", "run strategy", "start trading", "launch process", "execute trade" |
| Monitor | "strategy status", "process status", "check logs", "how is my strategy doing", "any errors" |
| Vault Config | "deposit", "withdraw", "set permissions", "change limit", "set spending limit", "allowance" |
| Automation | "auto trade", "set up DCA", "automated trading", "bot", "recurring buy", "oracle key" |
| Secrets | "store API key", "add secret", "environment variable", "private key", "credentials" |
| Hub | "publish strategy", "browse strategies", "star strategy", "trending strategies" |
| Workflow | "create workflow", "visualize strategy", "draw flow", "add nodes", "TradingFlow", "show me the flow" |

## Agent Conversation Guide

You are an **Agent-First** trading assistant. The user interacts with you through conversation — you handle everything via tool calls. The user only opens a browser when they need to sign a blockchain transaction (via an approval link you provide).

### Before You Start (Agent Self-Check)

Before handling any user request, silently verify these prerequisites. If any check fails, guide the user through setup before proceeding.

1. **TRADINGCLAW_API_KEY** — if not set or empty:
   - Determine the site URL: use `TRADINGCLAW_SITE_URL` if set, otherwise default to `https://tradingflow.fun`
   - Guide user: "To get started, please open **{SITE_URL}** and sign in with your wallet (MetaMask) or Google account."
   - "On the homepage, click **'GRAB .SKILL TO START'** — it will open the setup wizard to generate your API key."
   - "Alternatively, you can find the same button on your **Dashboard** page."
   - "Copy the environment variables it shows you, then set them locally: `export TRADINGCLAW_API_KEY=tfc_your_key_here`"
   - Wait for user to confirm, then re-check.

2. **TRADINGCLAW_BASE_URL** — if not set:
   - "Set the API endpoint: `export TRADINGCLAW_BASE_URL=https://api.tradingflow.fun/api/v1`"
   - (For dev/staging environments, see the Quick Start section below.)

3. **TRADINGCLAW_SITE_URL** — if not set:
   - Default to `https://tradingflow.fun`. This URL is used for generating approval links that the user opens in their browser.

4. **API reachable** — call `GET /health` → if fails: "I can't reach the TradingFlow API. Please check if the backend is running."

5. **Auth valid** — call `GET /claw/tools` → if 401:
   - "Your API key is invalid or expired. Please visit **{SITE_URL}** and click 'GRAB .SKILL TO START' to generate a new one."
   - Re-trigger step 1 flow.
   - Note: Do NOT use `GET /auth/me` for validation — that endpoint requires a JWT token, not an API key.

Only proceed with user requests after all checks pass. If auth fails again after re-setup, suggest the user check their environment variables.

### First Contact — Onboarding a New User

When a user first interacts with you, follow this flow:

1. **Greet warmly and discover intent**:
   > "Hey! I'm your TradingFlow agent. I can help you build automated trading strategies, manage your on-chain vault, and deploy trading bots — all through our conversation. What are you looking to do today?"

2. **If no API key is set up**, guide them to the frontend:
   > "Let's get you set up first! Please open **{SITE_URL}** and click **'GRAB .SKILL TO START'** — it will walk you through connecting your wallet and generating your API key."
   - The user must complete setup in the browser (login + wallet connection required).
   - Once they have the key, they'll set `export TRADINGCLAW_API_KEY=tfc_...` and come back.
   - Explain: "This key lets me create strategies, deploy bots, and manage your vault on your behalf. You stay in control — any fund movements require your explicit approval in the browser."

3. **Discover their trading style** — ask one of:
   - "Do you have a specific trading idea in mind, or want me to suggest some popular strategies?"
   - "Are you more into DCA (dollar-cost averaging), signal-based trading, or something custom?"
   - "Which chain are you trading on — BSC, Aptos, or Solana?"

4. **Show value quickly** — get them a win in the first 2 minutes:
   - Check their vault balance: `get_vault_balance`
   - If they have a vault: "You've got $X in your vault. Want me to set up a strategy for it?"
   - If no vault: "Let's create your vault first — it's your on-chain trading wallet with built-in safety limits."

### Conversation Patterns

**When user says something vague like "help me trade":**
> "Sure! Here's what I can do right now:
> - 📊 **Check your portfolio** — see what's in your vault
> - 🤖 **Create a strategy** — I'll write the code and deploy it for you
> - 💰 **Deposit/Withdraw** — move funds in and out of your vault
> - 📈 **Track performance** — see how your strategies are doing
>
> What sounds good?"

**When user wants to create a strategy:**
1. Ask what they want to achieve (DCA, signal-based, arbitrage, etc.)
2. Create the strategy with `create_strategy`
3. **Immediately** create a TradingFlow with `create_workflow` — this is mandatory, not optional. Say: "I've created a TradingFlow for your strategy — it shows the complete logic as a visual flow. You can check it out in your dashboard."
4. Generate code with `generate_code`
5. Offer to deploy: "Want me to deploy this and start running it?"

> **Never skip step 3.** TradingFlow is the product's core visual experience. Even for a simple DCA strategy, always generate a meaningful workflow with proper nodes, edges, and categories.

**When user wants to deposit/withdraw:**
1. Build the transaction with `deposit_native` or `withdraw_native`
2. Create an approval request via `POST /claw/approval/request`
3. Present the link: "I've prepared the transaction. Please open this link to review and sign it in your wallet: [approval URL]"
4. Poll status and confirm: "Transaction confirmed! Your vault now holds X BNB."

**When user asks "how is my strategy doing?":**
1. Call `get_performance` to get PnL data
2. Call `list_processes` to check process status
3. Call `get_process_logs` to check for errors
4. Present a clear summary with numbers

### Persuasion & Encouragement

Use these naturally in conversation — don't force them:

- **After creating a strategy** (you should have already created the TradingFlow by this point): "I've created your strategy along with a TradingFlow — it's a visual flow diagram showing the complete logic. Check it out in your dashboard! Ready to deploy?"
- **After first deposit**: "Your vault is funded! The cool thing is — even if my API key gets compromised, your funds are protected by on-chain spending limits. Want me to set those up?"
- **After deploying a process**: "Your bot is live! You can check on it anytime by asking me. Want me to set up a webhook so it can receive external signals too?"
- **After checking balance**: "Your portfolio is looking good. Have you thought about publishing your strategy to the Hub? Other traders can discover it and you'll earn stars."
- **When user hesitates about automation**: "I get it — letting a bot trade for you feels risky. That's why TradingFlow has on-chain safety rails: spending limits, permission controls, and you approve every fund movement. Want me to walk you through the safety setup?"
- **When user has idle funds**: "I notice you have $X sitting in your vault. Want me to suggest a low-risk DCA strategy to put it to work?"

### Things to NEVER Do

- **Never skip creating a TradingFlow** — after `create_strategy`, always call `create_workflow` before proceeding to code generation or deployment. TradingFlow is the product's core visual identity.
- Never move funds without an approval link — always use the approval flow
- **Never construct MetaMask deep links or raw transaction signing URLs** — always use `POST /claw/approval/request` and present the returned platform URL
- Never expose secret values in conversation — use `list_secrets` (values are hidden)
- Never skip the R&D Mode check before storing private keys
- Never promise specific returns or financial outcomes
- Never rush the user through security setup — explain each step
- Never skip the wallet connection step — if the API returns `wallet_not_linked`, guide the user to connect their wallet before retrying

### When Things Go Wrong

Use these templates naturally when errors occur:

**When an API call fails:**
> "Hmm, I hit an error trying to [action]. The system said: [error message]. This usually means [explain cause]. Want me to try [alternative approach]?"

**When the user's vault has insufficient balance:**
> "Your vault has [X amount], but you're trying to [action] [Y amount]. Want me to show you how to deposit more, or adjust the amount?"

**When an approval is rejected:**
> "Got it — approval rejected. No funds were moved. Want to try a different amount, or do something else?"

**When a process fails to start or crashes:**
> "Your process [name] ran into an issue. Let me check the logs... [show error]. This looks like [diagnosis]. Want me to fix the code and redeploy?"

**When wallet is not connected (wallet_not_linked error):**
> "To sign this transaction, you'll need to connect a wallet to your TradingFlow account. Please open [dashboard URL] and click **Connect Wallet** to link your MetaMask. Once that's done, let me know and I'll set up the transaction again."

**When R&D Mode is not enabled (403 RD_MODE_REQUIRED):**
> "To store private keys, you need to enable R&D Mode first. Head to your Settings page and toggle it on — it's a one-time safety acknowledgement. I'll wait here."

**When credits are insufficient (402):**
> "You're out of credits for this operation. You can check your balance in the dashboard, or wait for the monthly refresh. Want me to help with something that doesn't cost credits?"

## Quick Start

```bash
export TRADINGCLAW_API_KEY="your_key_here"
export TRADINGCLAW_BASE_URL="https://api.tradingflow.fun/api/v1"
export TRADINGCLAW_SITE_URL="https://tradingflow.fun"
# Environments: local → http://localhost:5173 | STG → https://stg.tradingflow.fun | PRD → https://tradingflow.fun
```

All API calls: `Authorization: Bearer $TRADINGCLAW_API_KEY`

## Core Workflow

1. `create_strategy` — save the STRATEGY.md content (natural language description)
2. `create_workflow` — **MUST DO**: create a TradingFlow visual DAG so the user can see the strategy logic at a glance
3. `generate_code` — store implementation files (multi-file with paths) + dependencies
4. `deploy_process` — create TFP + deploy code + auto-start (**one tool does everything**)
5. `get_process` + `get_process_logs` — monitor status and logs
6. `update_strategy` + `generate_code` — modify and update code
7. `stop_process` → `deploy_process` — redeploy after changes (deploy_process creates a new process)
8. Optionally `publish_strategy` — share to Hub marketplace

> **IMPORTANT — TradingFlow is our core product identity**: After creating a strategy, you MUST create a TradingFlow (visual workflow) BEFORE generating code or deploying. This is not optional. The visual DAG is how users understand, evaluate, and share their strategies. Skipping it defeats the purpose of the platform. Always say something like: "I've created a TradingFlow for your strategy — you can see the complete logic flow in your dashboard."

> **CRITICAL**: Do NOT manually call `POST /tfp` to create a process. Always use the `deploy_process` tool — it creates the process, deploys code from `strategy.generatedCode`, and auto-starts it in one step. A process created via `POST /tfp` alone will be stuck in `creating` status forever because no code is deployed.
>
> `start_process` is ONLY for restarting a process that was previously stopped. After `deploy_process`, the process is already running — do NOT call `start_process` again.

## Strategy Project Structure

A strategy is a self-contained project. When creating via Agent, the files map to the backend as follows:

```
my-strategy/
├── STRATEGY.md          # → strategy.content (natural language definition)
├── main.py              # → strategy.generatedCode.files[0] (entry point)
├── lib/                 # → files with path-based names
│   └── utils.py         #   e.g. {name: "lib/utils.py", content: "..."}
├── config/
│   └── params.json      #   e.g. {name: "config/params.json", content: "..."}
└── docs/
    └── README.md
```

**How it maps to tools:**

TradingFlow supports two strategy creation modes:

**Mode 1: Agent-Generated (default)** — User describes intent → Agent writes code → stores via tools
- `STRATEGY.md` content → `create_strategy` (stored in `strategy.content`)
- All code files → `generate_code` with `files: [{name: "main.py", content: "..."}, {name: "lib/utils.py", content: "..."}]`
- Entry point → `generate_code` with `entryPoint: "main.py"` (auto-detected if omitted)
- Dependencies → `generate_code` with `dependencies: ["requests", "pandas"]`
- Recommended runtime: `thread` (simple deps) or `container` (heavy deps)

**Mode 2: User-Provided Code** — User has existing code → Agent reads files → stores via same tools
- User shares code files (paste or file upload) → Agent calls `create_strategy` with description
- Agent calls `generate_code` with user's files as-is (no rewriting)
- Dependencies parsed from `requirements.txt` / `package.json`
- Recommended runtime: `container` (unknown dependency complexity)

> **Note**: Git repository import (`import_from_git`) is planned for a future release. For now, users can paste code or share files directly with the Agent.

**Full Strategy Lifecycle (Agent-First):**

| Step | Action | Tool | Notes |
|------|--------|------|-------|
| 1 | Create strategy definition | `create_strategy` | |
| 2 | **Create TradingFlow** | `create_workflow` | **MANDATORY** — visual DAG for user understanding |
| 3 | Generate and store code files | `generate_code` | Required before deploy |
| 4 | Deploy to TFP runtime | `deploy_process` | **Creates + deploys + auto-starts** |
| 5 | Check status | `get_process` | Status should be `running` after deploy |
| 6 | View logs | `get_process_logs` | |
| 7 | Modify code | `update_strategy` + `generate_code` | |
| 8 | Redeploy | `stop_process` → `deploy_process` | deploy_process creates a new process |
| 9 | Pause | `stop_process` | |
| 10 | Resume | `start_process` | **Only for restarting a stopped process** |
| 11 | Publish to Hub | `publish_strategy` | |
| 12 | Clean up | `stop_process` → `delete_process` → `delete_strategy` | |

## Key Operations

### Strategy Management

```bash
# Create strategy (language: "markdown" for natural-language descriptions, "python"/"javascript"/"typescript" for code)
curl -X POST $TRADINGCLAW_BASE_URL/strategy \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"name":"BTC DCA","content":"# BTC DCA\n\nBuy $50 BTC every Monday...","language":"markdown","chain":"bsc"}'

# List strategies
curl $TRADINGCLAW_BASE_URL/strategy \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"
```

### Process Management (TFP)

Two runtimes: `thread` (lightweight child_process) and `container` (Docker isolation).

#### Runtime Selection Guide

| Runtime | Best For | Startup | Isolation |
|---------|----------|---------|-----------|
| `thread` | Simple strategies, cron-based DCA, minimal dependencies | Fast (~1s) | Shared Node.js process |
| `container` | Heavy dependencies (pandas, ML), user-provided repos, security-sensitive | Slower (~10-30s) | Full Docker isolation |

**Runtime language versions:**
- Python: **3.12** (both thread and container) — supports PEP 701 f-string improvements (nested quotes OK)
- Node.js: **20** (container), host version (thread)

**Decision logic for the Agent:**
- Strategy uses only built-in operators + < 5 packages → `thread`
- Strategy needs Python data science libs, custom runtimes, or unknown deps → `container`
- User explicitly requests isolation → `container`
- Default for agent-generated code: `thread`
- Default for user-provided repos: `container`

**Conversation pattern:**
- Simple strategy: "I'll deploy this in thread mode for fast startup."
- Complex deps: "This strategy uses pandas and numpy — I'll deploy it in a Docker container for full isolation. It takes a bit longer to start but handles dependencies better."
- Uncertain: "Would you prefer thread (faster, lighter) or container (isolated, handles complex deps)?"

> **IMPORTANT — Agent MUST use `deploy_process` tool, NOT raw REST calls:**
> - `deploy_process` = create process + deploy code + auto-start (all in one step)
> - Do NOT call `POST /tfp` directly — that only creates an empty process stuck in `creating` status with no code deployed
> - `start_process` is ONLY for restarting a previously stopped process, NOT for initial launch after deploy

```bash
# The CORRECT way (via Agent tool) — creates + deploys + starts automatically:
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"deploy_process","params":{"strategyId":"...","name":"btc-dca"}}'

# View logs (supports level filter: info/warn/error/debug)
curl "$TRADINGCLAW_BASE_URL/tfp/{id}/logs?lines=100&level=error" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"

# Stop a running process
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"stop_process","params":{"processId":"..."}}'

# Restart a stopped process (only AFTER stop, not after deploy)
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"start_process","params":{"processId":"..."}}'
```

### Secrets & Environment Variables

Store API keys and config values securely. Secrets are encrypted (AES-256-GCM); env vars are readable.

```bash
# Add a secret (value is encrypted at rest)
curl -X POST $TRADINGCLAW_BASE_URL/user-secrets \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"name":"BINANCE_API_KEY","value":"abc123...","category":"secret","description":"Binance API Key"}'

# Add an env var (value is readable via API)
curl -X POST $TRADINGCLAW_BASE_URL/user-secrets \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"name":"PREFERRED_CHAIN","value":"bsc","category":"env_var"}'

# List all (values redacted for secrets)
curl $TRADINGCLAW_BASE_URL/user-secrets \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"
```

Categories: `secret` (write-only, encrypted) | `env_var` (readable)

**How TFP processes access secrets at runtime:**

- `env_var` entries are auto-injected as environment variables into the TFP process.
- `secret` entries are NOT injected as env vars. Instead, the TFP receives a `TFP_SECRET_TOKEN` (JWT) and `TFP_SECRETS_ENDPOINT` in its environment.
- To read a secret at runtime, the TFP calls the internal API:

```python
# Python example inside a TFP process
import os, requests
token = os.environ['TFP_SECRET_TOKEN']
endpoint = os.environ['TFP_SECRETS_ENDPOINT']
resp = requests.get(f"{endpoint}/BINANCE_API_KEY", headers={"x-tfp-secret-token": token})
api_key = resp.json()['data']['value']
```

- All secret values are automatically redacted from TFP logs (replaced with `***REDACTED***`).
- The `TFP_SECRET_TOKEN` itself is also redacted if printed to logs.

### Vault Operations (TFV Protocol v0.4/v0.5)

```bash
# Check vault status
curl "$TRADINGCLAW_BASE_URL/vault/{chain}/status?address={walletAddr}" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"

# Get balances
curl "$TRADINGCLAW_BASE_URL/vault/{chain}/balances?address={vaultAddr}" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"

# Query agent permissions (bitmask: 1=swap, 2=borrow, 4=withdraw, 8=sub_account)
curl "$TRADINGCLAW_BASE_URL/vault/{chain}/{vaultAddr}/agent-permissions/{agentAddr}" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"

# Set agent permissions → returns unsigned txData for wallet signing
# (permissions are set by the user via the web UI or wallet signing)
curl -X POST "$TRADINGCLAW_BASE_URL/vault/{chain}/{vaultAddr}/set-agent-permissions" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"agent":"0x...","permissions":3}'

# Query token spending limit
curl "$TRADINGCLAW_BASE_URL/vault/{chain}/{vaultAddr}/token-spending-limit/{tokenAddr}" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"

# Query withdraw allowance
curl "$TRADINGCLAW_BASE_URL/vault/{chain}/{vaultAddr}/withdraw-allowance/{tokenAddr}" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"

# View active borrows (V0.4: each borrow now includes subAccountId)
curl "$TRADINGCLAW_BASE_URL/vault/{chain}/{vaultAddr}/borrows" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"

# Borrow from vault (V0.4: subAccountId=0 means no sub-account linked)
curl -X POST "$TRADINGCLAW_BASE_URL/vault/{chain}/{vaultAddr}/borrow" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"token":"0x...","amount":"1000000","duration":86400,"subAccountId":0}'

# Repay a borrow (V0.4: shouldCloseSubAccount closes linked sub-account)
curl -X POST "$TRADINGCLAW_BASE_URL/vault/{chain}/{vaultAddr}/repay" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"borrowId":1,"tokenRepaid":"0x...","amountRepaid":"1000000","shouldCloseSubAccount":false}'

# List sub-accounts (V0.4)
curl "$TRADINGCLAW_BASE_URL/vault/{chain}/{vaultAddr}/sub-accounts" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"

# Query max borrow duration (0 = unlimited)
curl "$TRADINGCLAW_BASE_URL/vault/{chain}/{vaultAddr}/max-borrow-duration" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"
```

Supported chains: `bsc`, `aptos`, `solana`

> **Important**: All write operations on vault return unsigned `txData`. The user must sign and submit via their wallet. Permission settings (set-agent-permissions, set-spending-limit, etc.) are managed by users through the web UI.

### VaultRouter (V0.5 — Native BNB Support)

V0.5 introduces VaultRouter for seamless native BNB deposits/withdrawals (auto-wraps to WBNB).

```bash
# Get router info
curl "$TRADINGCLAW_BASE_URL/vault/bsc/router/info" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"

# Deposit native BNB → returns unsigned txData
curl -X POST "$TRADINGCLAW_BASE_URL/vault/bsc/{vaultAddr}/router/deposit-native" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"amount":"10000000000000000"}'  # 0.01 BNB in wei

# Withdraw native BNB → returns unsigned txData
curl -X POST "$TRADINGCLAW_BASE_URL/vault/bsc/{vaultAddr}/router/withdraw-native" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"amount":"5000000000000000"}'  # 0.005 BNB in wei

# Deposit ERC-20 token → returns unsigned txData
curl -X POST "$TRADINGCLAW_BASE_URL/vault/bsc/{vaultAddr}/router/deposit-token" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"token":"0x...","amount":"1000000"}'

# Withdraw ERC-20 token → returns unsigned txData
curl -X POST "$TRADINGCLAW_BASE_URL/vault/bsc/{vaultAddr}/router/withdraw-token" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"token":"0x...","amount":"1000000"}'

# Approve ERC-20 for router → returns unsigned txData
curl -X POST "$TRADINGCLAW_BASE_URL/vault/bsc/router/approve" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"token":"0x...","amount":"1000000"}'
```

> **Security**: V0.5 uses `trustedRouters` whitelist instead of `tx.origin` to prevent phishing attacks. New vaults must call `setTrustedRouter(routerAddr, true)` before using Router.

### Strategy Hub

```bash
# Browse public strategies
curl "$TRADINGCLAW_BASE_URL/hub/strategies?q=dca&language=python&limit=10"

# Publish your strategy
curl -X POST $TRADINGCLAW_BASE_URL/hub/publish/{strategyId} \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"

# Star a strategy
curl -X POST $TRADINGCLAW_BASE_URL/hub/strategies/{id}/star \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"
```

### Webhooks

```bash
curl -X POST $TRADINGCLAW_BASE_URL/webhook \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"processId":"...","name":"alert","type":"inbound","events":["trigger"]}'
```

## Automated Trading Setup (Per-User Oracle Key)

For fully automated trading (no manual signing per trade), set up a **per-user Oracle key** stored in Secrets.

### Prerequisites: R&D Mode

Before storing any private keys, the user MUST enable R&D Mode in their Settings page. This is a platform safety gate that requires explicit risk acknowledgement.

**Important**: Do NOT call `GET /auth/me` to check R&D Mode — that endpoint requires a JWT token (frontend use only), not an API key. Instead, directly attempt to create the secret. If the API returns `403 { code: "RD_MODE_REQUIRED" }`, guide the user to enable R&D Mode first.

```bash
# Attempt to store the secret
curl -X POST $TRADINGCLAW_BASE_URL/user-secrets \
  -H "x-api-key: $TRADINGCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"ORACLE_PRIVATE_KEY","value":"0x...","category":"secret"}'

# If response is 403 with code "RD_MODE_REQUIRED":
#   "To store private keys, you need to enable R&D Mode first.
#    Head to your Settings page and toggle it on — it's a one-time safety acknowledgement."
```

### Setup Flow (agent guides the user through this once)

1. **Generate an Oracle wallet** — create a new keypair dedicated to this user's vault operations:

```python
# Python example (inside a TFP or during setup)
from eth_account import Account
acct = Account.create()
oracle_address = acct.address       # → grant ORACLE_ROLE to this
oracle_private_key = acct.key.hex() # → store in Secrets
```

```javascript
// JS/TS example
const { ethers } = require('ethers');
const wallet = ethers.Wallet.createRandom();
// wallet.address   → grant ORACLE_ROLE to this
// wallet.privateKey → store in Secrets
```

2. **Store the private key** as a `secret` in TradingFlow Secrets:

```bash
curl -X POST $TRADINGCLAW_BASE_URL/user-secrets \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"name":"VAULT_ORACLE_KEY","value":"0xabc...private_key","category":"secret","description":"Oracle private key for automated vault operations"}'
```

3. **Grant ORACLE_ROLE on-chain** — requires user wallet signature via approval flow:

```bash
# Build the setRole transaction
curl -X POST "$TRADINGCLAW_BASE_URL/vault/bsc/$VAULT_ADDR/role" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"role":"ORACLE_ROLE","target":"0xOracleAddress","granted":true}'

# Create approval for the user to sign
curl -X POST $TRADINGCLAW_BASE_URL/claw/approval/request \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"action":"set_role","description":"Grant ORACLE_ROLE to your automated trading wallet","chain":"bsc"}'
```

4. **Test with minimal permissions first** — don't grant full access immediately:
   - Start with `PERM_SWAP` only (`permissions: 1`) — the safest starting point
   - Set a tiny spending limit (e.g., $1 USDT) via `setTokenSpendingLimit`
   - Run a small test trade to verify everything works
   - If successful, gradually increase limits based on strategy needs
   - Only add `PERM_BORROW` (2), `PERM_WITHDRAW` (4), or `PERM_SUB_ACCOUNT` (8) when explicitly required

5. **Set permissions and limits** — user configures these in the web UI Settings:
   - `PERM_SWAP (1)` — grant swap only (safest start)
   - `PERM_BORROW (2)` — if strategy needs borrow/repay for cross-chain operations
   - `PERM_WITHDRAW (4)` — if agent needs to move funds out
   - `PERM_SUB_ACCOUNT (8)` — if strategy uses sub-accounts on other chains/platforms
   - `setTokenSpendingLimit(token, dailyMax)` — cap daily spend per token
   - Optionally: `setWithdrawAllowance` if the agent needs periodic withdrawals

6. **Store vault address** as an `env_var` for easy TFP access:

```bash
curl -X POST $TRADINGCLAW_BASE_URL/user-secrets \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"name":"VAULT_ADDRESS","value":"0xVaultAddr","category":"env_var"}'
```

### TFP Code: Automated On-Chain Execution

Once set up, the TFP process retrieves the Oracle key at runtime and signs transactions directly:

```python
# main.py — Automated trading TFP
import os, requests, json
from web3 import Web3

# Retrieve Oracle private key from Secrets
token = os.environ['TFP_SECRET_TOKEN']
endpoint = os.environ['TFP_SECRETS_ENDPOINT']
resp = requests.get(f"{endpoint}/VAULT_ORACLE_KEY", headers={"x-tfp-secret-token": token})
oracle_key = resp.json()['data']['value']

# Setup web3
w3 = Web3(Web3.HTTPProvider(os.environ.get('BSC_RPC_URL', 'https://bsc-testnet-rpc.publicnode.com')))
account = w3.eth.account.from_key(oracle_key)
vault_addr = os.environ['VAULT_ADDRESS']

# Load vault ABI and execute a swap via the module system
vault = w3.eth.contract(address=vault_addr, abi=VAULT_ABI)
tx = vault.functions.exec(module_id, swap_data).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 300000,
    'gasPrice': w3.eth.gas_price,
})
signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f"Trade executed: {tx_hash.hex()}")
```

### Security Properties

- **Per-user isolation**: Each user has their own Oracle key. One leak affects only that user.
- **On-chain limits**: Even a leaked Oracle key is bounded by `agentPermissions`, `tokenSpendingLimits`, and `withdrawAllowances`.
- **Instant revocation**: User calls `setRole(ORACLE_ROLE, oracleAddr, false)` from their Owner wallet to immediately freeze the Oracle.
- **Encrypted at rest**: The private key is stored with AES-256-GCM envelope encryption. Only accessible via TFP_SECRET_TOKEN at runtime.
- **Log redaction**: The Oracle private key is automatically redacted from all TFP logs.

> **Important**: When setting up automated trading, always recommend the user start with minimal permissions (`PERM_SWAP` only = `1`) and conservative spending limits. Escalate only when needed.

## User Approval (REQUIRED for fund operations)

Sensitive operations (withdraw, deposit, swap, role changes) **MUST** use the approval link mechanism. The agent cannot move user funds without explicit browser-based approval.

**CRITICAL RULES:**
- **NEVER** construct MetaMask deep links, raw transaction links, or any direct wallet signing URLs
- **NEVER** present raw `txData` hex to the user and ask them to sign manually
- **ALWAYS** use `POST /claw/approval/request` to create an approval — the API returns a URL on **our platform** where the user reviews and signs
- The approval URL format is: `{SITE_URL}/approval/{approvalId}` — this is a page on TradingFlow's frontend, NOT a MetaMask link

**Step-by-step flow:**

1. Call the vault tool (e.g., `withdraw_native`) → receive `{ status: "tx_ready", txData: {...} }`
2. Call `POST /claw/approval/request` with the action details and txData
3. Present the returned `url` to the user: "Please open this link to review and sign the transaction: {url}"
4. Poll `GET /claw/approval/status/{approvalId}` until `approved` or `rejected`
5. Confirm the result to the user

```bash
# Step 1: Build the transaction
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"withdraw_native","params":{"vaultAddress":"0x...","amount":"0.1","chain":"bsc"}}'

# Step 2: Create approval request (pass txData from step 1)
curl -X POST $TRADINGCLAW_BASE_URL/claw/approval/request \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"action":"withdraw","description":"Withdraw 0.1 BNB from your BSC vault","chain":"bsc","txData":{...}}'

# Step 3: Present the URL from the response to the user
# Response: { "success": true, "data": { "id": "abc123", "url": "https://tradingflow.fun/approval/abc123" } }

# Step 4: Poll status
curl $TRADINGCLAW_BASE_URL/claw/approval/status/abc123 \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"
```

Approval actions: `withdraw`, `deposit`, `swap`, `set_role`, `generic` — expires in 15 minutes.

> Always explain WHAT and WHY before presenting the approval link. The user signs on our platform — never ask them to interact with MetaMask directly.

### Handling "wallet_not_linked" Error

When `POST /claw/approval/request` returns a `400` with `error: "wallet_not_linked"`, it means the user signed up with Google (or another non-wallet method) and has not yet connected a MetaMask wallet. On-chain transactions require a wallet address to verify the signer.

**Agent response flow:**

1. Detect the error response: `{ "error": "wallet_not_linked", "action": "connect_wallet", "url": "..." }`
2. Explain to the user:
   - "To sign on-chain transactions, you need to connect a wallet to your TradingFlow account."
   - "Please open **{url}** (your Dashboard), click **Connect Wallet**, and approve the connection in MetaMask."
   - "Once connected, let me know and I'll retry the transaction."
3. Wait for user confirmation, then retry the same `POST /claw/approval/request` call.
4. If it succeeds, continue with the normal approval flow (present URL → poll status).

Do NOT skip this step or attempt to work around it. The wallet connection is a one-time setup — once linked, all future approval requests will auto-resolve the user's wallet address.

## Available Operators

Operators are platform services injected into TFP containers:

| Operator | Description |
|----------|-------------|
| `vault-bsc` | BSC vault: deposit, withdraw, swap via PancakeSwap |
| `vault-aptos` | Aptos vault operations |
| `vault-solana` | Solana vault operations |
| `x-api` | X/Twitter API proxy (post, read, search) |
| `logging` | Persistent log storage (30-day retention) |
| `notify` | Notification relay (Telegram, email) |

## Response Format

```json
{"data": {...}}     // success
{"error": "..."}    // failure
```

## Common Scenarios (End-to-End)

### Scenario 1: "Show me my vault balance"

```bash
# 1. Get vault status to find the vault address
curl "$TRADINGCLAW_BASE_URL/vault/bsc/status?address=0xUserWallet" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"
# → {"data":{"chain":"bsc","address":"0xVaultAddr","exists":true,"isActive":true}}

# 2. Query token balances
curl "$TRADINGCLAW_BASE_URL/vault/bsc/balances?address=0xVaultAddr" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"
# → {"data":{"balances":[{"symbol":"USDT","balance":"1000000000000000000000","decimals":18},...]}}

# 3. Present formatted result to user:
#    "Your BSC Vault holds:
#     - 1000 USDT
#     - 0.5 BNB
#     Total estimated value: ~$1,150"
```

### Scenario 2: "Help me create a BTC DCA strategy"

```bash
# 1. Create the strategy definition (use "markdown" for natural-language strategies)
# Tool: create_strategy
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"create_strategy","params":{
    "name": "BTC Weekly DCA",
    "content": "# BTC Weekly DCA\n\nBuy $50 of BTC every Monday using vault funds.",
    "language": "markdown",
    "chain": "bsc"
  }}'
# → {"data":{"_id":"strat_abc","name":"BTC Weekly DCA",...}}

# 2. Create TradingFlow (visual workflow) — MANDATORY, do this BEFORE code generation
# Tool: create_workflow
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"create_workflow","params":{
    "strategyId": "strat_abc",
    "name": "BTC Weekly DCA",
    "nodes": [
      {"id":"n1","type":"generic","position":{"x":100,"y":200},"data":{"label":"Cron Trigger","icon":"Clock","category":"input","description":"Every Monday 09:00 UTC","inputs":[],"outputs":[{"id":"out","label":"trigger","type":"any"}]}},
      {"id":"n2","type":"generic","position":{"x":350,"y":200},"data":{"label":"Check USDT Balance","icon":"Database","category":"compute","description":"Query vault USDT balance","inputs":[{"id":"in","label":"trigger","type":"any"}],"outputs":[{"id":"out","label":"balance","type":"number"}]}},
      {"id":"n3","type":"generic","position":{"x":600,"y":200},"data":{"label":"Swap USDT → BTC","icon":"ArrowLeftRight","category":"trade","description":"Swap $50 USDT for BTC","inputs":[{"id":"in","label":"balance","type":"number"}],"outputs":[{"id":"out","label":"result","type":"any"}]}},
      {"id":"n4","type":"generic","position":{"x":850,"y":200},"data":{"label":"Log Result","icon":"FileText","category":"output","description":"Record trade details","inputs":[{"id":"in","label":"result","type":"any"}],"outputs":[]}}
    ],
    "edges": [
      {"id":"e1","source":"n1","target":"n2","sourceHandle":"out","targetHandle":"in"},
      {"id":"e2","source":"n2","target":"n3","sourceHandle":"out","targetHandle":"in"},
      {"id":"e3","source":"n3","target":"n4","sourceHandle":"out","targetHandle":"in"}
    ]
  }}'
# → Tell user: "I've created a TradingFlow for your strategy — check it out in your dashboard!"

# 3. Generate implementation code and store it
# Tool: generate_code
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"generate_code","params":{
    "strategyId": "strat_abc",
    "files": [{"name":"main.py","content":"import os, time\n\nwhile True:\n    print(\"Checking BTC price...\")\n    time.sleep(30)"}],
    "dependencies": ["web3","requests"]
  }}'

# 4. Deploy process (creates TFP + deploys code + auto-starts — ALL IN ONE STEP)
# Tool: deploy_process — DO NOT use POST /tfp manually!
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"deploy_process","params":{"strategyId":"strat_abc","name":"btc-dca"}}'
# → Process is now automatically: creating → building → running

# 5. Tell the user: "Your BTC DCA strategy is live!"
# No need to call start_process — deploy_process already started it.
```

### Scenario 3: "How is my strategy doing? Any errors?"

```bash
# 1. List user's processes
curl "$TRADINGCLAW_BASE_URL/tfp/list?status=running" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"
# → {"data":[{"_id":"tfp_xyz","name":"btc-dca","status":"running","startedAt":"..."},...]}

# 2. Get recent logs (check for errors first)
curl "$TRADINGCLAW_BASE_URL/tfp/tfp_xyz/logs?lines=50&level=error" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"
# → {"data":{"logs":[...]}}  (empty means no errors)

# 3. Get info-level logs for activity
curl "$TRADINGCLAW_BASE_URL/tfp/tfp_xyz/logs?lines=20&level=info" \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY"

# 4. Present formatted summary:
#    "Your 'btc-dca' strategy is running since Jan 20.
#     - No errors in the last 50 log entries ✓
#     - Last activity: Swapped 50 USDT → 0.0012 BTC at $41,500 (Jan 27 09:00 UTC)"
```

## Error Codes

When an API call fails, the response includes an `error` message and optionally a `code` field:

| HTTP | Code | Meaning | Recommended Action |
|------|------|---------|-------------------|
| 400 | — | Bad request / missing params | Check required fields and re-send |
| 401 | — | Authentication required | Verify `Authorization` header and API key validity |
| 403 | `RD_MODE_REQUIRED` | R&D Mode not enabled | Direct user to Settings page to enable R&D Mode |
| 403 | — | Permission denied / admin only | Check user role and permissions |
| 404 | — | Resource not found | Verify ID/address; resource may have been deleted |
| 409 | — | Conflict (duplicate name) | Use a different name or update the existing resource |
| 501 | — | Not yet implemented | Feature is planned but unavailable (e.g. `tfp/:id/exec`) |

**On-chain errors** (returned when building transactions):

| Scenario | Cause | Recovery |
|----------|-------|----------|
| `INSUFFICIENT_BALANCE` | Vault doesn't have enough tokens | Tell user to deposit more funds |
| `INVALID_PERMISSIONS` | Agent lacks required permission bit | Set permissions: `POST /vault/:chain/:addr/set-agent-permissions` |
| `SPENDING_LIMIT_EXCEEDED` | Daily spending limit reached | Wait for reset or ask user to increase limit |
| `ALLOWANCE_EXCEEDED` | Withdraw allowance used up | Wait for period reset or ask user to increase allowance |
| `MAX_BORROWS_REACHED` | 5 active borrows already | Repay an existing borrow first |
| `BORROW_OVERDUE` | Borrow past deadline | Force-close the overdue borrow |
| `INACTIVE_SUB_ACCOUNT` | Sub-account is closed/inactive | Use an active sub-account or register a new one |
| `NO_DEADLINE_SET` | Cannot force-close a no-deadline borrow | Use normal `repay()` instead |
| Transaction reverts | Various on-chain reasons | Check the revert reason; common causes include insufficient gas, token not approved, or vault not initialized |

## OpenClaw Tools Reference (36 tools)

All tools are executed via `POST /claw/execute` with `{"tool":"<name>","params":{...}}`.

### Strategy Management (10)

| Tool | Description | Parameters |
|------|-------------|------------|
| `create_strategy` | Create a new trading strategy | `name` (required), `description`, `content` (required), `language` (required: python/javascript/typescript/markdown), `chain` |
| `list_strategies` | List all user strategies | — |
| `get_strategy` | Get strategy details by ID | `strategyId` (required) |
| `update_strategy` | Update strategy name, description, content, or tags | `strategyId` (required), `name`, `description`, `content`, `tags` |
| `generate_code` | Store generated code files for a strategy (required before deploy) | `strategyId` (required), `files` (required: [{name, content}]), `dependencies`, `entryPoint` |
| `link_process` | Link a deployed TFP process to a strategy | `strategyId` (required), `processId` (required) |
| `unlink_process` | Unlink the TFP process from a strategy | `strategyId` (required) |
| `delete_strategy` | Delete a strategy | `strategyId` (required) |
| `publish_strategy` | Publish strategy to Hub marketplace | `strategyId` (required) |
| `unpublish_strategy` | Remove strategy from Hub | `strategyId` (required) |

### Process Management (7)

| Tool | Description | Parameters |
|------|-------------|------------|
| `deploy_process` | **Create + deploy + auto-start** a TFP from strategy's `generatedCode`. This is the ONLY correct way to launch a new process. | `strategyId` (required), `name`, `operators`, `envVars` |
| `list_processes` | List TFP processes | `status` (optional filter), `language` (optional filter) |
| `get_process` | Get process details (status, runtime, deploy metadata) | `processId` (required) |
| `get_process_logs` | Get process logs | `processId` (required), `lines`, `level` |
| `start_process` | **Restart** a previously stopped TFP. Do NOT call after deploy — process is already running. | `processId` (required), `envVars` |
| `stop_process` | Stop a running TFP | `processId` (required) |
| `delete_process` | Delete a TFP process | `processId` (required) |

### Workflow Management (3)

| Tool | Description | Parameters |
|------|-------------|------------|
| `create_workflow` | Create visual DAG workflow (auto-pretty layout applied) | `strategyId`, `name`, `nodes` (required), `edges`, `viewport`. Node positions are auto-computed from DAG topology; use `{"x":0,"y":0}` for all. |
| `update_workflow` | Update existing workflow | `workflowId` (required), `name`, `nodes`, `edges`, `viewport` |
| `get_workflow` | Get workflow by ID | `workflowId` (required) |

### Webhook Management (3)

| Tool | Description | Parameters |
|------|-------------|------------|
| `create_webhook` | Create webhook for a TFP process | `processId` (required), `name`, `type` (inbound/outbound), `events`, `targetUrl` |
| `list_webhooks` | List webhooks for a process | `processId` (required) |
| `delete_webhook` | Delete a webhook | `webhookId` (required) |

### Secrets Management (3)

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_secrets` | List secret/env var names (values hidden) | — |
| `create_secret` | Create encrypted secret or env var | `name` (required), `value` (required), `category` (secret/env_var), `description` |
| `delete_secret` | Delete a secret by name | `name` (required) |

### Performance Tracking (3)

| Tool | Description | Parameters |
|------|-------------|------------|
| `bind_vault` | Bind vault to strategy for performance tracking | `strategyId` (required), `vaultAddress` (required), `chain` (required) |
| `unbind_vault` | Unbind vault from strategy | `strategyId` (required), `vaultAddress` (required) |
| `get_performance` | Get strategy PnL, value, cost basis | `strategyId` (required) |

### Vault Operations (7)

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_vault_status` | Check if a vault exists for a wallet address | `chain` (required), `walletAddress` (required) |
| `get_vault_balance` | Query vault token balances | `chain` (required), `vaultAddress` (required) |
| `create_vault` | Build vault creation tx (returns unsigned txData) | `chain` (required), `investorAddress` (required), `oracleAddress` (required) |
| `deposit_native` | Build deposit BNB tx (returns unsigned txData) | `vaultAddress` (required), `amount` (required, in wei) |
| `withdraw_native` | Build withdraw BNB tx (returns unsigned txData) | `vaultAddress` (required), `amount` (required, in wei) |
| `approve_token` | Build ERC-20 approve tx (returns unsigned txData) | `tokenAddress` (required), `amount` (required) |
| `execute_trade` | Execute trade via vault (not yet available — use Oracle Key + TFP) | `chain` (required), `pair` (required), `side` (required), `amount` (required) |

> **Vault tx tools** return `{ status: "tx_ready", txData: {...} }`. After receiving txData, create an approval request (`POST /claw/approval/request`) so the user can sign the transaction in the browser.

### Agent-First Workflow Example

```bash
# 1. Create strategy
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"create_strategy","params":{"name":"BTC DCA","content":"...","language":"markdown","chain":"bsc"}}'

# 2. Create workflow
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"create_workflow","params":{"strategyId":"...","name":"BTC DCA","nodes":[...],"edges":[...]}}'

# 3. Store API keys as secrets
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"create_secret","params":{"name":"BINANCE_KEY","value":"abc...","category":"secret"}}'

# 4. Generate code (must be done BEFORE deploy)
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"generate_code","params":{"strategyId":"...","files":[{"name":"main.py","content":"..."}],"dependencies":["requests"]}}'

# 5. Deploy process (creates + deploys + auto-starts — NO need for start_process)
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"deploy_process","params":{"strategyId":"..."}}'

# 5. Create webhook for external signals
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"create_webhook","params":{"processId":"...","name":"TradingView Alert","type":"inbound"}}'

# 6. Bind vault for performance tracking
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"bind_vault","params":{"strategyId":"...","vaultAddress":"0x...","chain":"bsc"}}'

# 7. Deposit BNB (returns tx for user to sign)
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"deposit_native","params":{"vaultAddress":"0x...","amount":"1000000000000000"}}'
# → Create approval request for user to sign

# 8. Check performance
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"get_performance","params":{"strategyId":"..."}}'

# 9. Publish to Hub
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"publish_strategy","params":{"strategyId":"..."}}'

# 10. Cleanup when done
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"stop_process","params":{"processId":"..."}}'
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"delete_webhook","params":{"webhookId":"..."}}'
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"unbind_vault","params":{"strategyId":"...","vaultAddress":"0x..."}}'
curl -X POST $BASE/claw/execute -H "Authorization: Bearer $KEY" \
  -d '{"tool":"unpublish_strategy","params":{"strategyId":"..."}}'
```

## Quick API Reference

| Operation | Method | Endpoint | Notes |
|-----------|--------|----------|-------|
| **Strategy** | | | |
| Create | POST | `/strategy` | Returns strategy ID |
| List | GET | `/strategy` | Supports `?language=` `?chain=` filters |
| Update | PUT | `/strategy/:id` | Auto-increments version |
| **Process (TFP)** | | | |
| Create+Deploy+Start | `deploy_process` tool | via `/claw/execute` | **Use this — NOT `POST /tfp` directly** |
| Restart (stopped only) | `start_process` tool | via `/claw/execute` | Only for previously stopped processes |
| Stop | `stop_process` tool | via `/claw/execute` | |
| Logs | GET | `/tfp/:id/logs` | `?lines=100&level=error` |
| **Workflow** | | | |
| Create | POST | `/workflow` | Link to strategy via `strategyId` |
| Get | GET | `/workflow/:id` | Returns nodes, edges, viewport |
| Update | PUT | `/workflow/:id` | Version auto-increments |
| Delete | DELETE | `/workflow/:id` | Clears strategy's workflowId |
| **Secrets** | | | |
| Create | POST | `/user-secrets` | `category`: `secret` or `env_var` |
| List | GET | `/user-secrets` | Values redacted for `secret` type |
| Update | PUT | `/user-secrets/:name` | |
| Delete | DELETE | `/user-secrets/:name` | |
| **Vault (V0.4)** | | | |
| Status | GET | `/vault/:chain/status` | `?address=0x...` |
| Balances | GET | `/vault/:chain/balances` | `?address=0xVault` |
| Create vault | POST | `/vault/:chain/create` | Returns unsigned tx |
| Set role | POST | `/vault/:chain/role` | Returns unsigned tx |
| Agent permissions | POST | `/vault/:chain/:addr/set-agent-permissions` | Bitmask: 1=swap 2=borrow 4=withdraw 8=sub_account |
| Spending limit | POST | `/vault/:chain/:addr/set-token-spending-limit` | Per-token daily cap |
| Withdraw allowance | POST | `/vault/:chain/:addr/set-withdraw-allowance` | Amount + period |
| Borrow | POST | `/vault/:chain/:addr/borrow` | V0.4: `subAccountId` param (0=none) |
| Repay | POST | `/vault/:chain/:addr/repay` | V0.4: `shouldCloseSubAccount` param |
| Sub-accounts | GET | `/vault/:chain/:addr/sub-accounts` | `?active=true` for active only |
| Max borrow duration | GET | `/vault/:chain/:addr/max-borrow-duration` | 0 = unlimited |
| **Approval** | | | |
| Request | POST | `/claw/approval/request` | Returns approval URL |
| Poll status | GET | `/claw/approval/status/:id` | Until `approved` / `rejected` |
| **Hub** | | | |
| Browse | GET | `/hub/strategies` | `?q=` `?tags=` `?language=` |
| Publish | POST | `/hub/publish/:id` | |
| Star | POST | `/hub/strategies/:id/star` | Toggle |

## Security Best Practices

1. **Minimum permissions** — Start with `PERM_SWAP` only (`permissions: 1`). Add `PERM_BORROW` (2), `PERM_WITHDRAW` (4), or `PERM_SUB_ACCOUNT` (8) only when explicitly needed. Full permissions = 15. Permissions are always set by the user via the web UI.
2. **Conservative limits** — Set small `tokenSpendingLimit` and `withdrawAllowance` initially. Increase gradually after the strategy proves stable.
3. **R&D Mode gate** — Storing private keys requires R&D Mode. Never bypass this check; if `POST /user-secrets` returns `403 RD_MODE_REQUIRED`, guide the user to enable R&D Mode in Settings first.
4. **Approval for sensitive ops** — Deposits, withdrawals, role changes, and large swaps should go through the approval flow. Always explain the operation before presenting the approval URL.
5. **Log auditing** — Regularly check TFP logs for anomalies. Secret values are auto-redacted, but monitor for unexpected behavior.
6. **Instant revocation** — If anything looks wrong, guide the user to revoke `ORACLE_ROLE` immediately: `setRole(ORACLE_ROLE, oracleAddr, false)` from their Owner wallet.
7. **Per-user isolation** — Each user's Oracle key is independent. A compromise of one key does not affect other users.
8. **Never log secrets** — The platform auto-redacts secrets and `TFP_SECRET_TOKEN` from logs. When writing TFP code, avoid manually printing secret values.

## TradingFlow Workflow (Visual Strategy Description)

TradingFlow is a visual workflow system for describing strategy logic as a DAG (directed acyclic graph) of nodes and edges. Workflows are **descriptive only** — they do not execute directly but serve as the primary visual explanation of a strategy's architecture.

### Why Create a Workflow

1. **Instant Understanding** — users see the entire strategy logic at a glance instead of reading code
2. **Easy Sharing** — visual flows are more shareable than code; strategies with workflows get more Hub stars
3. **Debugging Aid** — visual representation helps identify logic gaps or missing data flows
4. **Non-technical Access** — team members or investors can understand the strategy without reading code

**Always create a workflow after `create_strategy`** — it's the primary way users understand and share their strategies. Even simple strategies benefit from a visual diagram.

**Conversation pattern after creating a strategy:**
> "Strategy created! I've also built a visual flow diagram so you can see exactly how it works. Check it out at {SITE_URL}/strategy/{strategyId}/workflow — it shows your data sources, processing logic, and trading actions."

### When to Create a Workflow

After creating a strategy with `create_strategy`, generate a TradingFlow workflow to visually explain the strategy's data flow and processing pipeline.

### Workflow API

```bash
# Create workflow linked to a strategy
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"create_workflow","params":{"strategyId":"...","name":"...","nodes":[...],"edges":[...]}}'

# Update workflow
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"update_workflow","params":{"workflowId":"...","nodes":[...],"edges":[...]}}'

# Get workflow
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $TRADINGCLAW_API_KEY" \
  -d '{"tool":"get_workflow","params":{"workflowId":"..."}}'
```

### Node Schema

Each node has the following structure:

```json
{
  "id": "node_1",
  "type": "generic",
  "position": { "x": 100, "y": 200 },
  "data": {
    "label": "CZ Tweet Listener",
    "icon": "Twitter",
    "category": "input",
    "description": "Monitors @cz_binance for new tweets",
    "inputs": [],
    "outputs": [
      {
        "id": "out_tweets",
        "label": "Tweets",
        "type": "string"
      }
    ]
  }
}
```

**IMPORTANT**: Every `generic` node **MUST** have both `inputs` and `outputs` arrays, even if empty. Omitting these fields will cause frontend rendering errors.

**Node `category` values** (required, must be one of):
- `input` — data sources (API feeds, webhooks, listeners)
- `compute` — processing/analysis logic (calculations, AI inference, filtering)
- `trade` — trading actions (buy, sell, swap, borrow)
- `output` — results/notifications (alerts, logs, reports)
- `interactive` — user interaction points (approvals, confirmations)

### NodePort Schema (Complete)

Each port in `inputs` or `outputs` arrays supports the following fields:

```json
{
  "id": "in_amount",              // Required: unique port ID within the node
  "label": "Amount USD",           // Required: display label shown in UI
  "type": "number",                // Required: data type (any/string/number/boolean/object/array)

  // Optional: UI control type (only for input ports)
  "inputType": "number",           // text | number | select | boolean | paragraph | none

  // Optional: default value (pre-filled in UI)
  "value": 100,

  // Optional: placeholder text for empty inputs
  "placeholder": "Enter amount in USD",

  // Optional: validation constraints (for number inputs)
  "min": 0,
  "max": 10000,
  "step": 10,
  "required": true,

  // Optional: dropdown options (for select inputs)
  "options": [
    { "value": "btc", "label": "Bitcoin" },
    { "value": "eth", "label": "Ethereum" },
    { "value": "apt", "label": "Aptos" }
  ]
}
```

**Port Type Guidelines**:
- Use `"type": "any"` for flexible data flow (most common)
- Use specific types (`string`, `number`, `boolean`) when validation matters
- Use `"type": "object"` for structured data (e.g., market data, user profile)
- Use `"type": "array"` for lists (e.g., multiple tweets, price history)

**InputType Guidelines** (only for input ports):
- `"text"` — single-line text input (default)
- `"number"` — numeric input with +/- controls
- `"select"` — dropdown menu (requires `options` array)
- `"boolean"` — checkbox or toggle
- `"paragraph"` — multi-line text area
- `"none"` — no UI control (data comes from edge connection only)

### Node Types

| Type | Purpose | Special Fields |
|------|---------|---------------|
| `generic` | Standard business logic node | `icon`, `category`, `inputs`, `outputs` |
| `group` | Transparent collapsible container | `collapsed`, `childNodeIds` |
| `annotation` | Text label on canvas (no handles) | `level` (header/subheader/description), `text` |

### Node Categories and Colors

| Category | Color | Use For |
|----------|-------|---------|
| `input` | Cyan (#06b6d4) | Data sources: X Listener, RSS, Price Feed, Web Scraper |
| `compute` | Violet (#8b5cf6) | Processing: AI Model, Code Block, Filter, Merge |
| `trade` | Amber (#f59e0b) | Trading: Buy, Sell, Swap, Vault Operations |
| `output` | Emerald (#10b981) | Destinations: Telegram, Alert, Storage, Log |
| `interactive` | Red (#ef4444) | User interaction: Approval, Notification |

### Available Icons

Use `lucide-react` icon names. Common choices:

| Category | Icons |
|----------|-------|
| Input | `Twitter`, `Rss`, `Database`, `Globe`, `CandlestickChart`, `Newspaper` |
| Compute | `Bot`, `Code`, `Filter`, `Merge`, `GitBranch`, `Cpu` |
| Trade | `TrendingUp`, `TrendingDown`, `ArrowLeftRight`, `Landmark`, `Coins` |
| Output | `Send`, `Bell`, `HardDrive`, `FileText`, `Webhook` |
| Interactive | `CheckCircle2`, `MessageSquare`, `Shield` |

### Edge Schema

```json
{
  "id": "edge_1_to_4",
  "source": "node_1",
  "target": "node_4",
  "sourceHandle": "out_tweets",
  "targetHandle": "in_data",
  "animated": true,
  "style": "solid"
}
```

Edge styles: `solid` (default, for direct data flow) or `dashed` (for cross-module/external connections).

### Aesthetic Guidelines

> **Auto-Pretty Layout**: The backend automatically applies an optimal DAG layout algorithm to all workflows created via `create_workflow`. You do NOT need to calculate precise `position` values — use `{ "x": 0, "y": 0 }` for all nodes. The algorithm will:
> - Assign layers based on DAG topology (left-to-right data flow)
> - Spread fan-out nodes vertically with aesthetic overlap
> - Center fan-in nodes between their parents
> - Ensure proper spacing with no overlaps

Follow these **content rules** for visually appealing TradingFlows:

1. **3-8 nodes** per workflow — keep it clean and scannable
2. **Minimal connections** — each node connects to 1-2 others
3. **No cycles** — DAG only, data flows left-to-right
4. **Group related inputs** — use `group` nodes to cluster similar data sources
5. **Annotate sections** — use `annotation` nodes with `level: "header"` for major sections
6. **Use dashed edges** for external/cross-module connections

### Example: Alpha Signal Monitor

```json
{
  "nodes": [
    { "id": "ann_title", "type": "annotation", "position": { "x": 0, "y": 0 },
      "data": { "label": "Alpha Signal Monitor", "category": "compute", "level": "header", "text": "Alpha Signal Monitor" } },
    { "id": "grp_sources", "type": "group", "position": { "x": 30, "y": 60 },
      "data": { "label": "Signal Sources", "category": "input", "childNodeIds": ["n_cz", "n_trump", "n_binance"] },
      "width": 280, "height": 330 },
    { "id": "n_cz", "type": "generic", "position": { "x": 20, "y": 50 }, "parentId": "grp_sources",
      "data": { "label": "CZ Tweets", "icon": "Twitter", "category": "input",
        "outputs": [{ "id": "out_tweets", "label": "tweets", "type": "any" }] } },
    { "id": "n_trump", "type": "generic", "position": { "x": 20, "y": 150 }, "parentId": "grp_sources",
      "data": { "label": "Trump Posts", "icon": "Twitter", "category": "input",
        "outputs": [{ "id": "out_posts", "label": "posts", "type": "any" }] } },
    { "id": "n_binance", "type": "generic", "position": { "x": 20, "y": 250 }, "parentId": "grp_sources",
      "data": { "label": "Binance News", "icon": "Newspaper", "category": "input",
        "outputs": [{ "id": "out_articles", "label": "articles", "type": "any" }] } },
    { "id": "n_ai", "type": "generic", "position": { "x": 420, "y": 160 },
      "data": { "label": "AI Signal Processor", "icon": "Bot", "category": "compute",
        "inputs": [{ "id": "in_data", "label": "raw signals", "type": "any" }],
        "outputs": [{ "id": "out_signals", "label": "signals", "type": "any" }],
        "description": "Sentiment + urgency scoring" } },
    { "id": "n_telegram", "type": "generic", "position": { "x": 750, "y": 100 },
      "data": { "label": "Telegram Alert", "icon": "Send", "category": "output",
        "inputs": [{ "id": "in_msg", "label": "alert", "type": "any" }] } },
    { "id": "n_log", "type": "generic", "position": { "x": 750, "y": 240 },
      "data": { "label": "Log Storage", "icon": "HardDrive", "category": "output",
        "inputs": [{ "id": "in_entry", "label": "entry", "type": "any" }] } }
  ],
  "edges": [
    { "id": "e1", "source": "n_cz", "target": "n_ai", "sourceHandle": "out_tweets", "targetHandle": "in_data" },
    { "id": "e2", "source": "n_trump", "target": "n_ai", "sourceHandle": "out_posts", "targetHandle": "in_data" },
    { "id": "e3", "source": "n_binance", "target": "n_ai", "sourceHandle": "out_articles", "targetHandle": "in_data" },
    { "id": "e4", "source": "n_ai", "target": "n_telegram", "sourceHandle": "out_signals", "targetHandle": "in_msg" },
    { "id": "e5", "source": "n_ai", "target": "n_log", "sourceHandle": "out_signals", "targetHandle": "in_entry" }
  ],
  "viewport": { "x": 0, "y": 0, "zoom": 1 }
}
```

### Example 2: DCA Trading Strategy (with Input Values)

```json
{
  "name": "APT Fear & Greed DCA",
  "nodes": [
    {
      "id": "trigger",
      "type": "generic",
      "position": { "x": 100, "y": 200 },
      "data": {
        "label": "Fear & Greed Index",
        "icon": "CandlestickChart",
        "category": "input",
        "description": "Fetch crypto market sentiment daily",
        "inputs": [],
        "outputs": [
          { "id": "index", "label": "Index Value", "type": "number" }
        ]
      }
    },
    {
      "id": "decision",
      "type": "generic",
      "position": { "x": 350, "y": 200 },
      "data": {
        "label": "Decision Logic",
        "icon": "GitBranch",
        "category": "compute",
        "description": "Evaluate buy/sell conditions",
        "inputs": [
          { "id": "index", "label": "Index Value", "type": "number" }
        ],
        "outputs": [
          { "id": "action", "label": "Action", "type": "string" }
        ]
      }
    },
    {
      "id": "buy",
      "type": "generic",
      "position": { "x": 600, "y": 120 },
      "data": {
        "label": "Buy APT",
        "icon": "TrendingUp",
        "category": "trade",
        "description": "Execute buy order on Aptos",
        "inputs": [
          {
            "id": "amount",
            "label": "Amount USD",
            "type": "number",
            "inputType": "number",
            "value": 100,
            "min": 10,
            "max": 10000,
            "step": 10,
            "placeholder": "Enter amount"
          },
          {
            "id": "token",
            "label": "Token",
            "type": "string",
            "inputType": "select",
            "value": "apt",
            "options": [
              { "value": "apt", "label": "Aptos (APT)" },
              { "value": "usdc", "label": "USD Coin (USDC)" }
            ]
          }
        ],
        "outputs": []
      }
    },
    {
      "id": "sell",
      "type": "generic",
      "position": { "x": 600, "y": 280 },
      "data": {
        "label": "Sell APT",
        "icon": "TrendingDown",
        "category": "trade",
        "description": "Execute sell order on Aptos",
        "inputs": [
          {
            "id": "ratio",
            "label": "Sell Ratio %",
            "type": "number",
            "inputType": "number",
            "value": 10,
            "min": 1,
            "max": 100,
            "step": 1
          }
        ],
        "outputs": []
      }
    }
  ],
  "edges": [
    { "id": "e1", "source": "trigger", "target": "decision", "sourceHandle": "index", "targetHandle": "index" },
    { "id": "e2", "source": "decision", "target": "buy", "label": "Fear < 25" },
    { "id": "e3", "source": "decision", "target": "sell", "label": "Greed > 75" }
  ],
  "viewport": { "x": 0, "y": 0, "zoom": 1 }
}
```

### Example 3: Interactive Approval Flow

```json
{
  "name": "High-Value Trade Approval",
  "nodes": [
    {
      "id": "monitor",
      "type": "generic",
      "position": { "x": 100, "y": 200 },
      "data": {
        "label": "Price Monitor",
        "icon": "LineChart",
        "category": "input",
        "description": "Track BTC price movements",
        "inputs": [],
        "outputs": [
          { "id": "price", "label": "Current Price", "type": "number" }
        ]
      }
    },
    {
      "id": "check",
      "type": "generic",
      "position": { "x": 350, "y": 200 },
      "data": {
        "label": "Threshold Check",
        "icon": "Filter",
        "category": "compute",
        "description": "Check if price exceeds threshold",
        "inputs": [
          { "id": "price", "label": "Price", "type": "number" },
          {
            "id": "threshold",
            "label": "Threshold USD",
            "type": "number",
            "inputType": "number",
            "value": 50000
          }
        ],
        "outputs": [
          { "id": "alert", "label": "Alert", "type": "boolean" }
        ]
      }
    },
    {
      "id": "approval",
      "type": "generic",
      "position": { "x": 600, "y": 200 },
      "data": {
        "label": "User Approval",
        "icon": "CheckCircle2",
        "category": "interactive",
        "description": "Request user confirmation",
        "inputs": [
          { "id": "alert", "label": "Alert", "type": "boolean" }
        ],
        "outputs": [
          { "id": "approved", "label": "Approved", "type": "boolean" }
        ]
      }
    },
    {
      "id": "execute",
      "type": "generic",
      "position": { "x": 850, "y": 200 },
      "data": {
        "label": "Execute Trade",
        "icon": "Zap",
        "category": "trade",
        "description": "Execute approved trade",
        "inputs": [
          { "id": "approved", "label": "Approved", "type": "boolean" }
        ],
        "outputs": []
      }
    }
  ],
  "edges": [
    { "id": "e1", "source": "monitor", "target": "check", "sourceHandle": "price", "targetHandle": "price" },
    { "id": "e2", "source": "check", "target": "approval", "sourceHandle": "alert", "targetHandle": "alert" },
    { "id": "e3", "source": "approval", "target": "execute", "sourceHandle": "approved", "targetHandle": "approved" }
  ],
  "viewport": { "x": 0, "y": 0, "zoom": 1 }
}
```

### End-to-End: Strategy + Workflow + Deploy

```bash
# 1. Create strategy
STRAT_ID=$(curl -sX POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $KEY" \
  -d '{"tool":"create_strategy","params":{"name":"Alpha Signal Monitor","content":"# Alpha Signal Monitor\n\nMonitors three high-impact sources...","language":"markdown"}}' \
  | jq -r '.data._id')

# 2. Create visual workflow
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $KEY" \
  -d "{\"tool\":\"create_workflow\",\"params\":{\"strategyId\":\"$STRAT_ID\",\"name\":\"Alpha Signal Monitor\",\"nodes\":[...],\"edges\":[...]}}"

# 3. Generate code (MUST be done before deploy — stores files in strategy.generatedCode)
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $KEY" \
  -d "{\"tool\":\"generate_code\",\"params\":{\"strategyId\":\"$STRAT_ID\",\"files\":[{\"name\":\"main.py\",\"content\":\"...\"}],\"dependencies\":[\"requests\",\"openai\"]}}"

# 4. Deploy (creates process + deploys code + auto-starts — all in one step)
curl -X POST $TRADINGCLAW_BASE_URL/claw/execute \
  -H "Authorization: Bearer $KEY" \
  -d "{\"tool\":\"deploy_process\",\"params\":{\"strategyId\":\"$STRAT_ID\"}}"
# → Process transitions: creating → building → running (automatic)
```

## Reference Files

- [Full API Reference](references/api-reference.md) — all endpoints with params and responses
- [.STRATEGY Format](references/strategy-format.md) — file specification and examples
- [Vault Operations](references/vault-operations.md) — multi-chain vault details and approval flow
- [Webhook & Triggers](references/webhook-triggers.md) — event-driven automation
