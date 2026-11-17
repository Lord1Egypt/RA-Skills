# ZK-Bankir Monitor — ClawHub Skill

Monitor your ZK-Bankir sovereign banking treasury from any OpenClaw agent.

## What It Does

This skill lets OpenClaw agents query a ZK-Bankir server:
- **Health checks** — is the server alive?
- **Treasury balances** — BTC (COLDCARD watch-only), PUSD (Payy ZK), Kraken (exchange)
- **Decision ledger** — append-only, hash-chained audit trail
- **Hash-chain verification** — SHA-256 integrity check
- **Operator console** — pending human-approval decisions

## Why ZK-Bankir?

ZK-Bankir is a sovereign personal banking platform built on Rails 8.1.3. It's designed for individuals who want:

- **Full custody** — you hold the keys (COLDCARD Q hardware wallet)
- **Zero-knowledge privacy** — PUSD transfers via Payy Network
- **Append-only audit** — every financial decision is hash-chained, immutable
- **Policy-gated automation** — auto <$1k, human approval $1k-$10k, hard deny >$10k
- **Watch-only default** — no private keys on the server, ever

## Installation

```bash
# Install the skill into your workspace
openclaw skills install @1beekeeper/zk-bankir-monitor

# Or install globally for all agents
openclaw skills install @1beekeeper/zk-bankir-monitor --global
```

## Quick Start

```bash
# Set your ZK-Bankir host (default: localhost:3000)
export ZK_BANKIR_HOST=http://your-server:3000

# Then ask your agent:
# "What's my treasury balance?"
# "Verify the decision ledger hash chain"
# "Show me pending decisions that need approval"
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ZK_BANKIR_HOST` | `http://localhost:3000` | Base URL of ZK-Bankir server |
| `ZK_BANKIR_PATH` | `~/App/domains/finance/zk-bankir` | Project path for hash-chain verification |

## Tiers

### Free
- Health checks
- Treasury balances (all assets)
- Decision ledger (last 10)
- Hash-chain verification

### Premium ($19)
- Historical balance tracking with alerts
- Decision monitoring (approval-needed alerts)
- Automated daily summaries (cron-ready)
- Webhook alerts (Slack/Telegram)

## Requirements

- `curl` and `jq` on PATH
- A running ZK-Bankir Rails server
- ZK-Bankir v1.0+ (Phase 1 complete)

## Security

This skill is **read-only**. It never:
- Stores or transmits private keys
- Initiates trades or withdrawals
- Modifies the decision ledger
- Bypasses the Policy Engine

All queries go through ZK-Bankir's REST API which is watch-only by default (Gebud 5).

## Links

- ZK-Bankir repo: https://gitlab.com/1Beekeeper/zk-bankir
- Documentation: https://gitlab.com/1Beekeeper/zk-bankir/-/tree/main/docs
- De 10 Gebuden: https://gitlab.com/1Beekeeper/zk-bankir/-/blob/main/docs/02-doctrine.md
