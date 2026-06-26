# Threshold Trader - Publishing Guide

## Skill Structure ✅

```
threshold-trader/
├── SKILL.md              # AgentSkills-compliant metadata + docs
├── clawhub.json          # ClawHub + automaton config  
├── threshold_trader.py   # Main trading logic
└── README-PUBLISH.md     # This file
```

## Quick Start

### 1. Test Locally

```bash
cd threshold-trader

# Set your API key
export SIMMER_API_KEY="your-api-key-here"

# Test in dry-run mode (safe, no real trades)
python threshold_trader.py

# Test with custom configuration
export THRESHOLD_PROBABILITY="0.65"
export TRADE_SIDE="YES"
export SIMMER_VENUE="sim"
python threshold_trader.py
```

### 2. Publish to ClawHub

```bash
# From inside the threshold-trader folder
npx clawhub@latest publish . --slug threshold-trader --version 1.0.0

# Or auto-bump version
npx clawhub@latest publish . --slug threshold-trader --bump patch
```

### 3. Verify Installation

```bash
# Test that others can install it
npx clawhub@latest install threshold-trader
```

If you see a "suspicious" warning from VirusTotal Code Insight, it's likely a false positive. The skill is clean — check that all env vars are declared in `clawhub.json`.

## Registry Sync

Within 6 hours of publishing to ClawHub, your skill will automatically appear at:
- https://simmer.markets/skills

No approval process needed — the sync job detects `simmer-sdk` in dependencies.

## Updating

```bash
# Bump version and republish
npx clawhub@latest publish . --slug threshold-trader --bump patch
```

The registry syncs every 6 hours and updates version info automatically.

## Environment Variables

Users configure the skill via these env vars (all optional except `SIMMER_API_KEY`):

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SIMMER_API_KEY` | ✅ Yes | - | Your API key from simmer.markets/dashboard |
| `THRESHOLD_PROBABILITY` | No | 0.70 | Probability threshold (0.0-1.0) |
| `TRADE_SIDE` | No | YES | Which side to trade (YES or NO) |
| `SIMMER_VENUE` | No | sim | Trading venue (sim, polymarket, kalshi) |
| `SIMMER_MIN_EV` | No | 0.03 | Minimum edge required (3%) |
| `SIMMER_KELLY_MULTIPLIER` | No | 0.25 | Kelly fraction for sizing |
| `MAX_POSITION_SIZE` | No | 100.0 | Max position size in USD |

## Automaton Mode

The skill runs automatically every 15 minutes when installed via ClawHub (configured in `clawhub.json`).

Users can disable automation and run manually:
```bash
python threshold_trader.py          # dry-run mode
python threshold_trader.py --live   # live trading
```

## Remixing

This is a **remixable template**. The core signal logic is in the `should_trade()` function — users can replace the fixed threshold with:

- ML model predictions
- External API data (weather, news, social sentiment)
- Multi-market correlations
- Event-driven signals

The skill handles all the infrastructure:
- ✅ Position sizing (Kelly criterion)
- ✅ Safety checks (flip-flop, slippage, edge)
- ✅ Trade execution with proper tagging
- ✅ Auto-redemption of winning positions
- ✅ Venue-specific state management

## Key Features

1. **Safe by Default**: Dry-run mode unless `--live` flag is passed
2. **Position Sizing**: Uses Kelly criterion via `simmer_sdk.sizing`
3. **Safety Checks**: Validates flip-flop warnings, slippage, and edge
4. **Auto-Redeem**: Collects payouts from resolved markets
5. **Venue-Aware**: Properly handles sim/polymarket/kalshi state
6. **Tagged Trades**: All trades include `source` and `skill_slug`
7. **Reasoning**: Every trade includes human-readable reasoning

## Compliance

✅ Uses `SimmerClient` for all trades  
✅ Defaults to dry-run mode  
✅ Tags trades with `source` and `skill_slug`  
✅ Includes reasoning in all trades  
✅ Reads API keys from environment  
✅ Checks context before trading  
✅ Uses recommended position sizing  
✅ Calls `auto_redeem()` for payouts  

## Support

- Documentation: https://docs.simmer.markets/skills/building
- Discord: https://t.me/+m7sN0OLM_780M2Fl
- Issues: Email simmer@agentmail.to

---

**Ready to publish!** 🚀

Just run: `npx clawhub@latest publish . --slug threshold-trader --version 1.0.0`
