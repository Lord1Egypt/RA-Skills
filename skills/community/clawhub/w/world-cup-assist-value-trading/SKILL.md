---
name: world-cup-assist-value-trading
description: "Scans World Cup Most Assists markets on Simmer, compares market price to FBref-based form value, and prints buy signals for 8%+ discounts."
metadata:
  author: "maxhejohansen-boop"
  version: "1.0.3"
  displayName: "World Cup Assist Value Signal Tool"
  difficulty: "intermediate"
tags:
  - world-cup
---

# World Cup Assist Value Signal Tool

Scans all "World Cup: Most Assists" markets on Simmer and compares each player's market-implied probability to a form-based expected value computed from FBref/ESPN stats. Prints signals when the market price sits 8%+ below the model's expected price.

> 🚨 **Framework, not a production trading system.** Read [DISCLAIMER.md](./DISCLAIMER.md) before connecting to a wallet with real funds. Defaults: dry-run, $10 max per trade, 5 trades max per run.

> **This is a template.** The default signal is FBref/ESPN club-form assists data fed through an unbacktested scoring formula — remix it with your own stats source or weighting. The skill handles market discovery and signal ranking; your agent provides the alpha.

This is a **signal tool**, not an automated trade executor — by default it only prints ranked buy signals. Live trading via SimmerClient is gated behind `DRY_RUN = False` and is off by default.

## How it works

1. **Market discovery**: Fetches all outcomes from Simmer's "World Cup: Most Assists" market using `SimmerClient.get_markets(q="assists")`.
2. **Filter**: Ignores any player priced below 2% — these are longshots where the model's signal is mostly noise.
3. **Form-based value**: For each remaining player, searches FBref/ESPN/WhoScored via Tavily for recent club assist numbers and converts them into an expected market price.
4. **Comparison**: If the form-based expected price is at least 8% above the live market price, the player is flagged as a buy signal.
5. **Output**: Signals are printed sorted by discount size, capped at 5 per run. In dry-run (default), nothing is traded — only printed. If `DRY_RUN = False`, trades are placed via `SimmerClient.trade()`, tagged with `source` and `skill_slug`, and include `reasoning`.

## Remixing this skill

- Swap the stats source (FBref/ESPN/WhoScored) for any other data provider.
- Adjust the scoring weights in `get_expected_price()`.
- Change `THRESHOLD`, `MIN_PRICE`, `MAX_TRADE_USD`, or `MAX_TRADES_PER_RUN` to fit your own risk tolerance.

## Notes
- The fair-value formula is a first pass and has not been backtested against historical World Cup results.
- Requires `SIMMER_API_KEY` and `TAVILY_API_KEY` environment variables.
- Designed to be run on a schedule (cron) ahead of matches involving tracked teams.

## Linked Files
- `references/player_baselines.md` - Baseline stats for monitored players
- `references/2024_25_baseline_refresh.md` - Auditable 2024/25 baseline refresh notes
- `references/2025_26_baseline_refresh.md` - Auditable 2025/26 baseline refresh notes
- `references/world_cup_2026_fixtures.md` - World Cup 2026 match schedule
- `references/research_notes.md` - Methodology, limitations, and improvement notes
- `scripts/signal.py` - Executable signal generation script (dry-run mode)
- `DISCLAIMER.md` - Required disclaimer, read before live use
