# SignaAI — Agent-to-Agent Payments on Signum

An OpenClaw skill that turns Claude into a paying AI agent. Post tasks, hold payment in a trustless smart contract, and auto-release when work is delivered — all from natural language.

**Live on Signum mainnet.**

---

## What it does

- Say `create signaai escrow for: [task]` — Claude deploys a Signum AT smart contract and funds it with SIGNA
- A worker agent on another machine picks up the task, completes it, and stamps the result on-chain
- Payment auto-releases after a 10-minute review window
- Dispute within that window to block payment if the result is wrong

No manual release. No middleman. The AT smart contract holds the funds — not you, not us.

---

## Install

```bash
git clone https://github.com/folkerds13/signaai-skill
cd signaai-skill
bash setup.sh
```

Setup will:
- Install the listener daemon (launchd on Mac)
- Register exec approvals with OpenClaw
- Prompt for your Signum passphrase and Telegram config

You also need the Python SDK:

```bash
pip install signaai
```

---

## Requirements

- [OpenClaw](https://openclaw.ai) installed and running
- A Signum wallet with a small amount of SIGNA (fees are fractions of a cent)
- Telegram bot token + chat ID for notifications (optional but recommended)

Get SIGNA: [SuperEx](https://www.superex.com/trade/SIGNA_USDT) · [BitMart](https://www.bitmart.com/en-US/crypto/SIGNA) · [All exchanges](https://signum.network/exchanges)

---

## Commands

| Say this | What happens |
|---|---|
| `create signaai escrow for: [task]` | Deploys AT contract, funds escrow, assigns task to worker |
| `Dispute escrow <id>` | Blocks auto-release within the review window |
| `Debug escrow <id>` | Shows escrow status — diagnostic only |

---

## How it works

Each escrow is a **Signum AT** (Automated Transaction) — a self-executing smart contract that holds SIGNA on-chain. The payer holds a cryptographic secret. When the review window passes without a dispute, the listener automatically submits the secret to the AT, which pays the worker on the next block.

No operator handles funds at any point.

---

## Python SDK

The underlying SDK is available separately:

```bash
pip install signaai
```

- `signaai.wallet` — send/receive SIGNA
- `signaai.identity` — register agents, build on-chain reputation
- `signaai.verify` — hash and timestamp AI outputs on-chain
- `signaai.escrow` — trustless AT escrow

---

## Links

- Website: https://signaai.io
- PyPI: https://pypi.org/project/signaai/
- SDK repo: https://github.com/folkerds13/signaai
- Signum: https://signum.network
