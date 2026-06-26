# Agent Configuration Reference

---

## Agent Type Presets

| `agent_type` | SM Categories | Thresholds (buy/sell) | Timeframes (24h/4h/1h) |
|-------------|--------------|----------------------|------------------------|
| `scalping_pro` | scalper, short_term_trading | BTC 65/65, ETH 70/65, SOL+ 78/65 | 20%/40%/40% |
| `swing_trader` | swing_trading, stable, high_win_rate | BTC 75/70, ETH 78/70, SOL+ 82/70 | 50%/35%/15% |
| `momentum_hunter` | high_risk_high_return, momentum_trader, short_term_trading | BTC 65/65, ETH 70/65, SOL+ 78/65 | 20%/40%/40% |
| `whale_follower` | btc_trader, large_cap_trader | BTC 75/70, ETH 78/70, SOL+ 82/70 | 50%/35%/15% |
| `stable_grower` | stable, high_win_rate, swing_trading | BTC 75/70, ETH 78/70, SOL+ 82/70 | 50%/35%/15% |
| `precision_master` | high_win_rate, swing_trading, trend_follower | BTC 75/70, ETH 78/70, SOL+ 82/70 | 50%/35%/15% |
| `composite` | ALL categories | BTC 75/70, ETH 78/70, SOL+ 82/70 | 50%/35%/15% |
| `hip3_whale_follower` | whale_trader, high_pnl_trader, perp_verified | BTC 75/70, ETH 78/70, SOL+ 82/70 | 50%/35%/15% |
| `hip3_diversified` | diversified_trader, risk_manager, balanced_trader | BTC 75/70, ETH 78/70, SOL+ 82/70 | 50%/35%/15% |
| `hip3_conviction` | high_conviction, high_pnl_trader, whale_trader | BTC 65/65, ETH 70/65, SOL+ 78/65 | 20%/40%/40% |

Auto-select HIP-3 types when `allowed_assets` contains `dex:COIN` format.

---

## AI Type Mapping (internal — never show to user)

| User says (intent) | → `agent_type` |
|-------------------|----------------|
| Follow whales / big money / smart money | `whale_follower` (perp) or `hip3_whale_follower` (HIP-3) |
| Quick trades / scalping / fast in-and-out | `scalping_pro` |
| Hold days-weeks / swing / patient setups | `swing_trader` |
| Momentum / trend / ride strong moves | `momentum_hunter` |
| Safe / conservative / low risk | `stable_grower` |
| Precise entries / sniper / high accuracy | `precision_master` |
| Balanced / no strong preference | `composite` |
| Aggressive + conviction / go big | `hip3_conviction` (HIP-3) or `momentum_hunter` (perp) |
| Diversified / spread across many assets | `hip3_diversified` (HIP-3) or `composite` (perp) |
| Unclear / vague | Default: `composite` (perp) or `hip3_diversified` (HIP-3) |

---

## Risk Profile Levels

| Level | Leverage | SL/TP | Max Positions | Position Size | Daily Loss |
|-------|---------|-------|---------------|---------------|------------|
| Conservative | 3x | 3%/9% (1:3 RR) | 3 | 10% | 1% |
| Moderate | 5x | 5%/10% (1:2 RR) | 5 | 15% | 3% |
| Aggressive | 10x | 5%/7.5% (1:1.5 RR) | 8 | 20% | 5% |

**⚠️ Leverage × SL caps enforced:**
- 15x+ leverage: min 5% SL (auto-widened if lower)
- 10x+ leverage: min 4% SL
- 5x+ leverage: min 3% SL
- Precision Master default SL increased to 3% (was 0.5%)

---

## Dynamic Stop Loss (DSL)

Two-phase trailing stop loss that automatically manages SL on Hyperliquid after entry.

**Phase 1 — Let It Breathe:** Wide retrace allowance with absolute floor. Does NOT trail — protects against catastrophic loss.

**Phase 2 — Lock the Bag:** Activates at ROE threshold. Tiered trailing stops that tighten as profit grows.

| Style | Phase 2 Trigger | Tiers (ROE%) | Phase 1 Retrace | Abs Floor |
|-------|----------------|--------------|-----------------|-----------|
| Scalping | 5% ROE | 4 (5/10/15/25) | 1.5% | 1.5% |
| Momentum | 8% ROE | 5 (8/15/25/40/60) | 2.5% | 2% |
| Swing | 15% ROE | 5 (15/25/40/60/80) | 4% | 5% |
| Smart Money | 10% ROE | 6 (10/20/30/50/75/100) | 3% | 3% |
| Mean Reversion | 8% ROE | 3 (8/15/25) | 2% | 2% |
| Position | 20% ROE | 4 (20/40/60/100) | 5% | 5% |

**Config** (`dsl_config` field):
- **Omit / `null`** → Use style defaults (recommended)
- **`{enabled: false}`** → Disable DSL entirely (static SL only)
- **Custom** → `{phase1_retrace: 0.02, phase1_absolute_floor_pct: 0.005, phase2_trigger_roe: 8.0, tiers: [{roe: 8, retrace: 0.05}, ...]}`

**DSL + LLM interaction:**
- LLM's `stop_loss_pct` sets initial SL only
- After entry, DSL manages SL automatically on exchange
- LLM can still recommend "close" for strong multi-factor reversals

---

## Order Types

- **Market** (default): Immediate execution. Best for high-urgency entries.
- **Limit** (GTC): Resting order at specific price. Best for mean reversion, support/resistance. Auto-cancelled if not filled.

---

## Strength Thresholds

> **⚠️ When `trigger_conditions` are configured (recommended), strength thresholds are bypassed.** Only agents WITHOUT trigger_conditions use these.

| Agent Type | BTC buy/sell | ETH buy/sell | SOL+ buy/sell | Timeframes 24h/4h/1h |
|------------|-------------|-------------|---------------|---------------------|
| scalping_pro, momentum_hunter | 65/65 | 70/65 | 78/65 | 0.2/0.4/0.4 |
| All others | 75/70 | 78/70 | 82/70 | 0.5/0.35/0.15 |

Timeframe weights must sum to 1.0.

---

## Must-Have Fields Checklist

Before deploying, ensure ALL exist:

| # | Field | Auto-filled? | Notes |
|---|-------|-------------|-------|
| 1 | `trigger_conditions` | ✅ auto from preset | Entry/exit rules. Can customize. |
| 2 | `trading_risk` | ✅ auto from risk_profile + leverage | SL/TP, sizing, leverage |
| 3 | `llm` | ✅ auto from model_provider + model_name | LLM config |
| 4 | `signal_weights` | ✅ from preset | SM/TA/Market weighting |
| 5 | `strength_thresholds` | ✅ from preset | Min signal strength |
| 6 | `timeframe_weights` | ✅ from preset | 24h/4h/1h weighting |
| 7 | `prompt_config.trading_strategy` | ✅ auto-generated | Overall approach |
| 8 | `prompt_config.custom_rules` | ✅ auto-generated | Entry/exit rules |
| 9 | `prompt_config.risk_management` | ✅ auto-generated | Risk rules |
| 10 | `dsl_config` | ✅ auto from trading_style | Dynamic Stop Loss |
