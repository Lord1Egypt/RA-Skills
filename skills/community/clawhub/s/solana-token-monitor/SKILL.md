---
name: solana-token-monitor
description: >
  Monitor any Solana token 24/7 using DexScreener. Get alerts for price
  moves, whale activity, volume spikes, liquidity changes, and market cap milestones.
  Built by the creator of $SHEP — a real Solana token founder who needed this and built it.
  Use when: (1) you launched a Solana token and want passive monitoring, (2) you
  want alerts on any Solana token, (3) you want instant token status reports.
  Alerts print to stdout (readable by the OpenClaw agent) and optionally deliver
  directly via Telegram Bot API if you configure a bot token and chat ID.
metadata:
  openclaw:
    emoji: "🐕"
    version: "1.1.0"
    author: "ShepDog (https://shepdogcoin.com)"
    tags: ["crypto", "solana", "defi", "token", "monitoring", "alerts"]
    requires:
      bins: ["python3"]
---

# Solana Token Monitor

Monitor any Solana token 24/7. Built by a real Solana token founder.

## Setup (2 minutes)

### Basic setup (alerts delivered by OpenClaw agent)

```bash
python3 ~/.openclaw/workspace/skills/solana-token-monitor/monitor.py setup <CONTRACT_ADDRESS> <SYMBOL>
```

The agent reads alert output during heartbeats and notifies you through whatever channel you use (Telegram, Discord, etc.).

### With direct Telegram bot delivery (optional)

If you have a Telegram bot token and chat ID, the script delivers alerts autonomously without agent involvement:

```bash
python3 ~/.openclaw/workspace/skills/solana-token-monitor/monitor.py setup <CONTRACT_ADDRESS> <SYMBOL> --telegram-token <BOT_TOKEN> --chat-id <CHAT_ID>
```

To get a Telegram bot token: message @BotFather on Telegram → /newbot.
To get your chat ID: message @userinfobot on Telegram.

## What It Monitors

- **Price** — alerts when price moves >5% in 1 hour
- **Volume** — alerts when 24h volume is 2x the previous period
- **Liquidity** — alerts when liquidity drops >20% (rug warning)
- **Market cap milestones** — notifies at $10K, $50K, $100K, $500K, $1M
- **Buy/sell ratio** — included in every status report

All thresholds are configurable in the saved config file.

## Alert Levels

- 🔴 **URGENT** — liquidity drop >20%, price crash >15%
- 🟡 **NOTABLE** — price move >5%, volume spike, milestone hit
- ⚪ **FYI** — no issues, everything normal

## Commands

```bash
# Set up monitoring for a token
python3 monitor.py setup <CONTRACT_ADDRESS> <SYMBOL>

# Get a status report
python3 monitor.py report <SYMBOL>

# Check for alerts (run during heartbeat)
python3 monitor.py check <SYMBOL>

# List all monitored tokens
python3 monitor.py list
```

## How It Works

Uses the free DexScreener public API — no API key required:
`https://api.dexscreener.com/tokens/v1/solana/{CONTRACT_ADDRESS}`

The API returns live price, volume, liquidity, and transaction data for any token with an active liquidity pool on Solana DEXs.

Tokens without an active liquidity pool will return "no data" — this is correct behavior, not a bug.

## Config File

After setup: `~/.openclaw/workspace/data/token-monitors/{SYMBOL}.json`

All thresholds, milestones, and alert history are stored here and editable.

## Daily Report Format

```
🐕 Solana Token Monitor — Status Report
────────────────────────────────────────
Token:      $BONK
Chain:      Solana

Price:      $0.00000590
  1h:       ▲ 0.2%
  24h:      ▲ 7.9%

Market Cap: $524,405,127
Volume 24h: $16,814.00
Liquidity:  $850,822.00

Txns 24h:   201 buys / 188 sells
Telegram:   ✅

Contract:   DezXAZ8z7PnrnRJjz3...
────────────────────────────────────────
Built by ShepDog 🐕 shepdogcoin.com
```

## Built By

This skill was built by the creator of $SHEP — a real Solana meme coin founder
who launched a token on Raydium and needed exactly this tool.

🐕 $SHEP — The Loyal Crypto Companion
Website: https://shepdogcoin.com
X: https://x.com/ShepDogCoin

---

*Free to use. If this helps you, consider checking out $SHEP.*
