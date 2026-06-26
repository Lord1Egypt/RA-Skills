# @sona/openclaw

OpenClaw plugin adapter for **SONA** — The Next-Gen Wallet.

Installs SONA's autonomous wallet capabilities as an OpenClaw skill,
making it discoverable and installable from the ClaWHub marketplace.

```bash
clawhub install sona
```

---

## What this package does

This package exports a single `register(api)` function that wires 10 tools
into any OpenClaw-compatible agent framework. The tools call SONA's HTTP API
(running locally on port 3000) — no changes to the SONA core are required.

```
OpenClaw Agent
     │
     │  natural language
     ▼
 plugin.ts (this package)
     │
     │  HTTP  →  localhost:3000
     ▼
 SONA Dashboard API
     │
     ├─ /api/status         (balance, mode, cycles)
     ├─ /api/policy         (YAML rules)
     ├─ /api/mode           (switch modes)
     ├─ /api/chat           (AI agent command)
     └─ /api/actions/*      (pending + approve)
```

---

## Quick start

### 1. Start SONA

```bash
bun run sona init   # first-time setup
bun run sona start  # dashboard on :3000, agent on :3001
```

### 2. Get a session token

```bash
TOKEN=$(curl -s -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"you","password":"yourpass"}' | jq -r '.token')
```

### 3. Configure environment

```bash
export SONA_API_URL=http://localhost:3000
export SONA_TOKEN=$TOKEN
```

### 4. Install via ClaWHub

```bash
clawhub install sona
```

Or load directly in your agent:

```typescript
import register from "@sona/openclaw/plugin.ts"

register({
  registerTool(tool) {
    // your OpenClaw agent framework handles tool dispatch
    console.log("registered:", tool.name)
  },
})
```

---

## Tools

| Tool | Auth required | Description |
|------|:---:|-------------|
| `get_wallet_status` | No | SOL balance, mode, cycle stats |
| `get_sol_price` | No | Live SOL/USD from Pyth Hermes |
| `get_agent_status` | No | Full agent status |
| `set_mode` | Yes | Switch standard/assisted/god |
| `get_policy` | No | Current YAML policy |
| `transfer_sol` | Yes | Transfer SOL via chat command |
| `chat` | Yes | Natural language command |
| `get_activity` | No | Recent activity summary |
| `get_pending_actions` | Yes | Assisted mode queue |
| `approve_action` | Yes | Approve a queued action |

Auth required for all state-changing operations (transfers, chat commands, mode switching, approvals). `SONA_TOKEN` is passed as `Cookie: sona_session=<token>`. Read-only tools work without a token.

**Security**: The plugin only connects to localhost URLs (`localhost`, `127.0.0.1`, `::1`). If `SONA_API_URL` points to a remote host, the plugin refuses to send credentials and falls back to `http://localhost:3000`.

---

## Smoke test

```bash
SONA_API_URL=http://localhost:3000 \
SONA_TOKEN=<token> \
bun -e "
  import register from './plugin.ts'
  const tools = {}
  register({ registerTool(t) { tools[t.name] = t } })
  const r = await tools.get_wallet_status.execute('test', {})
  console.log(r.content[0].text)
"
```

Expected output:
```
SONA Wallet Status
  Agent:       SONA Agent
  Mode:        god
  Balance:     4.8200 SOL
  Cycles run:  142
  Executions:  7
  SOL price:   $142.30
```

---

## Constitutional Laws

All tool calls pass through SONA's four immutable laws:

1. **Owner Supremacy** — your YAML policy overrides AI reasoning
2. **Bounded Expenditure** — 50M lamports/action (Rust-enforced, non-bypassable)
3. **Radical Transparency** — on-chain Memo on every executed transaction
4. **Fail-Safe Halting** — simulation failure = halt

No OpenClaw tool can bypass these. They are enforced at the Rust signing layer.

---

## Publishing to ClaWHub

1. Push the repo to GitHub (public)
2. Go to [clawhub.ai](https://clawhub.ai) → Publish Skill
3. Point to `packages/openclaw/` as the skill root
4. Skill ID: `sona`, version `0.1.0`
5. Users install with: `clawhub install sona`
