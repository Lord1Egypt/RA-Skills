---
name: skill-catalyst-calendar
description: Track upcoming market-moving events (macro, crypto protocol, exchange listings, regulatory decisions, conference keynotes, ETF approvals) and pre-flag relevant assets 7-14 days before the event. Use when building a forward-looking trading calendar, identifying pre-event positioning opportunities, or reviewing upcoming catalysts for any asset class.
---

# Catalyst Calendar

Forward-looking event tracker. Identifies upcoming catalysts and surfaces pre-positioning opportunities before the market prices them in.

## What Counts as a Catalyst

- **Macro:** Fed decisions, CPI prints, GDP data, regulatory announcements
- **Crypto-specific:** Protocol upgrades, halving events, token unlocks, mainnet launches
- **Exchange:** Binance/Coinbase/Kraken new listings, futures launches
- **Regulatory:** ETF approvals/rejections, SEC/CFTC rulings, country-level bans or legalization
- **Conferences:** Major industry events (ETHDenver, Consensus, Binance Blockchain Week, NVIDIA GTC, etc.)
- **Earnings/Partnerships:** Public company earnings with crypto exposure (Coinbase, MicroStrategy, Marathon)

## Calendar Storage

Stored at: `~/.openclaw/workspace/trading/catalyst-calendar.json`

```json
{
  "events": [
    {
      "id": "evt-001",
      "date": "2026-03-19",
      "event": "FOMC Rate Decision",
      "category": "macro",
      "impact": "high",
      "affected_assets": ["BTC", "ETH", "all"],
      "pre_position_days": 3,
      "notes": "Rate hold expected — risk-on if confirmed",
      "source": "federalreserve.gov"
    },
    {
      "id": "evt-002",
      "date": "2026-04-10",
      "event": "Ethereum Pectra Upgrade",
      "category": "protocol",
      "impact": "high",
      "affected_assets": ["ETH", "staking tokens"],
      "pre_position_days": 14,
      "notes": "EIP-7251 — raises validator limit, reduces sell pressure",
      "source": "ethereum.org"
    }
  ]
}
```

## Usage

### View upcoming catalysts (next 14 days)
```
List upcoming catalysts from trading/catalyst-calendar.json for the next 14 days. Flag any where pre_position_days window is now open.
```

### Add new event
```
Add to catalyst-calendar.json: [event details]
```

### Weekly scan (find new catalysts)
```
Search for upcoming crypto and macro events this week. Update catalyst-calendar.json with any new high-impact events in the next 30 days.
```

## Alert Logic

When today's date is within `pre_position_days` of an event:
```
📅 CATALYST ALERT — 7 days to Ethereum Pectra Upgrade
  Date: 2026-04-10
  Impact: HIGH
  Affected: ETH, staking tokens
  Pre-position window: OPEN NOW
  Notes: EIP-7251 — raises validator limit, reduces sell pressure
  Action: Review ETH position vs threshold-watcher signal
```

## Cron Integration

- **Weekly scan** (Monday 07:00 UTC): scrape upcoming events, update calendar
- **Daily check** (07:00 UTC): flag events where pre-position window opens today

## Integration with Trading Pipeline

- Outputs feed `skill-crypto-threshold-watcher` (set tighter thresholds near high-impact events)
- Logged to `skill-trading-journal` as context for trade decisions
- Informs `backtest-expert` on regime conditions (pre/post catalyst)
