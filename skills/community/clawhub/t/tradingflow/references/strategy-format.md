# Strategy Format Reference

A strategy is a self-contained project that describes a trading strategy in natural language and contains its implementation code.

## Strategy as a Project

A strategy maps to a folder structure:

```
my-strategy/
├── STRATEGY.md          # Natural language definition (stored in strategy.content)
├── main.py              # Entry point (stored in strategy.generatedCode.files[])
├── lib/                 # Helper modules
│   └── utils.py         #   {name: "lib/utils.py", content: "..."}
├── config/
│   └── params.json      #   {name: "config/params.json", content: "..."}
└── docs/
    └── README.md
```

**How it maps to the API:**

| Local File | API Field | Tool |
|------------|-----------|------|
| `STRATEGY.md` | `strategy.content` | `create_strategy` / `update_strategy` |
| All code files | `strategy.generatedCode.files[]` | `generate_code` |
| Entry point | `strategy.generatedCode.entryPoint` | `generate_code` (auto-detected if omitted) |
| Dependencies | `strategy.generatedCode.dependencies[]` | `generate_code` |

File names support paths (e.g. `lib/utils.py`, `config/params.json`). The TFP runtime creates directories automatically.

## STRATEGY.md Format

```
STRATEGY: <name>
VERSION: <number>
LANGUAGE: <python|javascript|typescript>
CHAIN: <bsc|aptos|solana>

DESCRIPTION:
<free-form description of what the strategy does>

TRIGGERS:
- type: <cron|webhook|price_alert|manual>
  config:
    <key>: <value>

OPERATORS:
- vault-bsc
- logging
- notify

TAGS:
- dca
- btc
- low-risk

LOGIC:
<natural language description of the trading logic>

RISK:
- max_position_size: <value>
- stop_loss: <percentage>
- max_daily_trades: <number>
```

## Example: BTC DCA Strategy

```
STRATEGY: BTC Weekly DCA
VERSION: 1
LANGUAGE: python
CHAIN: bsc

DESCRIPTION:
Dollar-cost average into BTC every Monday at 9:00 UTC.
Uses vault funds to swap USDT → BTC via PancakeSwap.

TRIGGERS:
- type: cron
  config:
    schedule: "0 9 * * 1"

OPERATORS:
- vault-bsc
- logging
- notify

TAGS:
- dca
- btc
- low-risk
- weekly

LOGIC:
1. Check USDT balance in vault
2. If balance >= $50, swap $50 USDT for BTC
3. Log the trade details
4. Send Telegram notification with execution result

RISK:
- max_position_size: 50 USDT
- stop_loss: none (DCA strategy)
- max_daily_trades: 1
```

### Multi-File Implementation

After writing the STRATEGY.md, generate code via `generate_code`:

```json
{
  "tool": "generate_code",
  "params": {
    "strategyId": "...",
    "files": [
      { "name": "main.py", "content": "from lib.swap import execute_dca\n\ndef main():\n    execute_dca(50)\n\nif __name__ == '__main__':\n    main()" },
      { "name": "lib/swap.py", "content": "from web3 import Web3\n\ndef execute_dca(amount_usd):\n    # swap logic here\n    pass" },
      { "name": "config/params.json", "content": "{\"amount_usd\": 50, \"token\": \"BTC\", \"schedule\": \"weekly\"}" }
    ],
    "dependencies": ["web3", "requests"],
    "entryPoint": "main.py"
  }
}
```

## Fields Reference

| Field | Required | Description |
|-------|----------|-------------|
| STRATEGY | yes | Strategy name |
| VERSION | yes | Integer version (auto-incremented on update) |
| LANGUAGE | yes | `python`, `javascript`, or `typescript` |
| CHAIN | no | Target blockchain |
| DESCRIPTION | yes | What the strategy does |
| TRIGGERS | no | When to execute (cron, webhook, price alert) |
| OPERATORS | no | Platform services needed (vault-bsc, logging, etc.) |
| TAGS | no | Searchable labels |
| LOGIC | yes | Step-by-step trading logic |
| RISK | no | Risk management parameters |

## Trigger Types

| Type | Config | Description |
|------|--------|-------------|
| `cron` | `schedule`: cron expression | Periodic execution |
| `webhook` | `events`: string[] | Triggered by external webhook |
| `price_alert` | `token`, `condition`, `threshold` | Triggered when price condition met |
| `manual` | — | User-initiated only |

## Agent Workflow

1. `create_strategy` — save STRATEGY.md content
2. `create_workflow` — **MANDATORY**: create TradingFlow visual DAG (do this BEFORE code generation)
3. `generate_code` — store implementation files + dependencies + entryPoint
4. `deploy_process` — create TFP + deploy code + auto-start (**one tool does everything**)
5. `get_process` / `get_process_logs` — monitor status and logs

> **Note**: `deploy_process` automatically creates the process, deploys code from `strategy.generatedCode`, links the process to the strategy, and starts it. No need to call `link_process` or `start_process` separately after deploy.
>
> **Never skip step 2.** TradingFlow is the product's core visual experience — every strategy MUST have a workflow so users can understand the logic at a glance.
