# Solana Token Monitor — Agent Instructions

You have access to the Solana Token Monitor skill. Use it when the user mentions:
- Monitoring a token, watching a price, getting alerts
- A Solana contract address
- "Watch my token", "alert me if...", "how is my token doing"

## Commands

### Set up monitoring
```bash
python3 ~/.openclaw/workspace/skills/solana-token-monitor/monitor.py setup <CONTRACT_ADDRESS> <SYMBOL>
```

With optional Telegram bot delivery:
```bash
python3 ~/.openclaw/workspace/skills/solana-token-monitor/monitor.py setup <CONTRACT_ADDRESS> <SYMBOL> --telegram-token <BOT_TOKEN> --chat-id <CHAT_ID>
```

### Get a status report
```bash
python3 ~/.openclaw/workspace/skills/solana-token-monitor/monitor.py report <SYMBOL>
```

### Check for alerts (run during heartbeat)
```bash
python3 ~/.openclaw/workspace/skills/solana-token-monitor/monitor.py check <SYMBOL>
```

### List all monitored tokens
```bash
python3 ~/.openclaw/workspace/skills/solana-token-monitor/monitor.py list
```

## Heartbeat Behavior

During each heartbeat, run `check` for all monitored tokens:

```bash
python3 ~/.openclaw/workspace/skills/solana-token-monitor/monitor.py list
# then for each symbol:
python3 ~/.openclaw/workspace/skills/solana-token-monitor/monitor.py check <SYMBOL>
```

If alerts are returned:
- 🔴 URGENT — notify the user immediately, any time of day
- 🟡 NOTABLE — notify during waking hours (8am–11pm user timezone)
- ⚪ FYI — batch into a daily summary

If Telegram bot credentials are stored in the config, the script delivers alerts directly. Otherwise, send alerts yourself via the message tool.

## Example Setup Flow

User: "Monitor my SHEP token at GtLwWPQZEfSB1hSNbvdy68xjanbNx19rNbUHdgAw2s4M"

Run:
```bash
python3 ~/.openclaw/workspace/skills/solana-token-monitor/monitor.py setup GtLwWPQZEfSB1hSNbvdy68xjanbNx19rNbUHdgAw2s4M SHEP
```

If the token has no active liquidity pool, inform the user: "No active pool found for this contract. The token may not be listed on a DEX yet, or the pool was removed."

Otherwise confirm: "✅ Now monitoring $SHEP. I'll alert you on price moves >5%, volume spikes, liquidity changes, and market cap milestones."
