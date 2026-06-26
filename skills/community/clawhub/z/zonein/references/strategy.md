# Zonein Trading Strategy Reference

## Signal Scoring Formula

### Prediction Market Signals

Signals are scored 0-100 based on weighted components:

| Component | Weight | Description |
|-----------|--------|-------------|
| Consensus Ratio | 25% | % of wallets agreeing on direction (YES/NO) |
| User Count | 30% | Number of smart wallets holding the market |
| Leaderboard Rank | 20% | Best rank among holders (lower = better) |
| Price Deviation | 10% | Penalty if entry price deviates from current |
| Reward Ratio | 15% | Potential payout relative to cost |

**Threshold:** Signals with score >= 60 are considered actionable.

### Perp Signals

Perp signals are consensus-based:
- **Consensus** = dominant_side_count / total_count
- Higher consensus + more wallets = stronger signal
- Best trader score adds credibility
- Long/Short value ratio shows conviction

## Risk Management Rules

### Position Sizing
- **Max per trade:** 5% of portfolio
- **Max total exposure:** 50% of portfolio
- **Max per category:** 20% of portfolio

### Safety Rails
- **Min edge:** 3-5% (signal price vs market price)
- **Daily loss limit:** 10% of portfolio
- **Cooldown:** 24h per market after analysis without trade
- **Kill switch:** Disable agent immediately if daily loss exceeded

### Agent Types

#### Prediction Market Agent
- Follows smart bettor consensus on Polymarket
- Trades YES/NO shares based on signal strength
- Domain filter: categories like POLITICS, CRYPTO, SPORTS
- Uses LLM to validate signal direction before execution

#### Perp Trading Agent (V2)
- Follows HyperLiquid whale positions via composite signals (SM + TA + Market)
- Opens LONG/SHORT based on `trigger_conditions` evaluation
- Agent types: `scalping_pro`, `momentum_hunter`, `swing_trader`, `stable_grower`, `precision_master`, `whale_follower`, `composite`
- Configurable `signal_weights` for SM/TA/Market importance
- LLM validates signals with `prompt_config` (trading_strategy, custom_rules, risk_management)
- Execution modes: `auto` (fully automated) or `hitl` (human-in-the-loop approval)

## Trading Flow (V2)

```
1. Signal Fetch
   └─ MCPSignalSource fetches composite data per symbol
   └─ SM (per-timeframe: 1h, 4h, 24h) + TA (RSI, MACD, SuperTrend, ADX) + Market (funding, OI, L/S ratio, taker ratio)

2. Trigger Evaluation (hard filter)
   └─ evaluate_trigger_conditions(entry.long / entry.short)
   └─ All conditions in AND group must pass
   └─ If not met → skip signal entirely (no LLM call)

3. Signal Scoring
   └─ Composite confidence = weighted sum (signal_weights: sm/ta/market)
   └─ SM strength from long_ratio/short_ratio per timeframe
   └─ TA alignment from RSI/MACD/SuperTrend votes
   └─ Market bias from funding/OI/taker ratio

4. LLM Decision
   └─ Entry prompt with full SM + TA + Market context
   └─ Style-specific system prompt (momentum, scalping, swing, etc.)
   └─ Returns: action, stop_loss_pct, take_profit_pct, reasoning

5. Execution
   └─ auto mode: execute immediately on Hyperliquid
   └─ hitl mode: create trade plan → Telegram notification → user approves/rejects

6. Position Monitoring
   └─ Exit trigger_conditions evaluated each cycle
   └─ LLM monitor prompt with position + current signals
   └─ SM flip detection (warning, not auto-close)
   └─ Stop-loss / Take-profit enforcement
```

## Recommended Cron Schedules

| Schedule | Job | Description |
|----------|-----|-------------|
| `*/5 * * * *` | Signal scan | Check for new signals every 5 min |
| `0 * * * *` | Risk check | Hourly portfolio risk assessment |
| `0 */6 * * *` | Performance | 6-hourly PnL and win rate report |
| `0 23 * * *` | Daily summary | End-of-day report with full breakdown |
| `0 8 * * 1` | Weekly review | Monday morning weekly performance review |
