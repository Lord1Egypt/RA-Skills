---
name: sona
description: Autonomous Solana wallet agent — AI reasons, Rust signs. Transfers, swaps, staking, chat, and mode switching under constitutional spend limits.
license: MIT-0
metadata:
  openclaw:
    requires:
      env:
        - SONA_TOKEN
      bins: []
      config: []
    primaryEnv: SONA_TOKEN
    homepage: https://www.sonawallet.xyz
    repository: https://github.com/Ubuntu-Technologies/sona
    emoji: "\U0001F4B0"
    os:
      - darwin
      - linux
      - win32
---

# SONA — Agentic Wallet Skill

**Category**: Blockchain / AI Wallet
**Networks**: Solana (Devnet)
**Install**: `clawhub install sona`
**Version**: 1.0.1

---

## What is SONA?

SONA is an autonomous Solana wallet agent. It watches your on-chain wallet, reasons
against your YAML policy rules, and executes trades and transfers — governed by four
Constitutional Laws that no AI decision can ever override.

```
Observe → Reason → Decide → Execute
```

Every action is bounded by Constitutional Law: 50M lamports max per action (Rust-enforced),
with an on-chain Memo receipt attached to every transaction.

---

## Plugin Tools (10)

| Tool | Parameters | Description |
|------|------------|-------------|
| `get_wallet_status` | — | SOL balance, address, mode, cycle stats |
| `get_sol_price` | — | Live SOL/USD from Pyth Hermes oracle |
| `get_agent_status` | — | Mode, brain, cycles run, last cycle time |
| `set_mode` | `mode`, `acknowledgment?` | Switch standard / assisted / god mode (auth required) |
| `get_policy` | — | Current YAML policy rules + spend limits |
| `transfer_sol` | `to`, `amount_sol` | Transfer SOL — all Constitutional Laws enforced (auth required) |
| `get_pending_actions` | — | Approval queue in assisted mode (auth required) |
| `approve_action` | `cycle_id` | Approve a queued action to execute (auth required) |
| `chat` | `message` | Natural language command to the SONA AI (auth required) |
| `get_activity` | `limit?` | Recent agent activity summary |

---

## Setup

### 1. Start SONA

```bash
git clone <repo>
cd <repo>
bun install
bun run sona init   # set passphrase, create wallet
bun run sona start  # agent starts on port 3000
```

### 2. Get a session token

```bash
curl -s -c cookies.txt -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"your_user","password":"your_pass"}' | jq -r '.token'
```

### 3. Set environment variables

```bash
export SONA_API_URL=http://localhost:3000
export SONA_TOKEN=<token-from-step-2>
```

### 4. Install the skill

```bash
clawhub install sona
```

---

## Constitutional Laws

All actions are governed by four immutable laws. No tool call can bypass them:

| Law | Name | Enforcement |
|-----|------|-------------|
| I | Owner Supremacy | Your YAML policy overrides all AI reasoning |
| II | Bounded Expenditure | 50M lamports/action hard cap (enforced in Rust) |
| III | Radical Transparency | On-chain Memo receipt on every executed transaction |
| IV | Fail-Safe Halting | Simulation failure → agent halts, funds stay put |

---

## Example Agent Flow

```
Agent: "Check SONA's wallet balance"
→ calls get_wallet_status
→ returns: 4.82 SOL, god mode, 142 cycles run

Agent: "Transfer 0.1 SOL to vault"
→ calls transfer_sol { to: "vault", amount_sol: 0.1 }
→ SONA reasons, simulates, executes within Law II limit
→ returns: tx confirmed, Memo logged on-chain

Agent: "What is the current SOL price?"
→ calls get_sol_price
→ returns: $142.30 USD (Pyth Hermes)
```

---

## Required Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SONA_API_URL` | No | `http://localhost:3000` | SONA dashboard base URL |
| `SONA_TOKEN` | Yes | — | JWT session token (required for all state-changing operations: transfers, chat, mode switching, approvals) |

Read-only tools (`get_wallet_status`, `get_sol_price`, `get_agent_status`, `get_policy`, `get_activity`) work without a token. All state-changing tools require `SONA_TOKEN`.
