# Zonein Command Reference

Detailed parameter tables for all commands. Prefix: `python3 skills/zonein/scripts/zonein.py`

---

## Polymarket (PM)

### `signals` — PM smart money trading signals

| Param | Type | Default | Values | Description |
|-------|------|---------|--------|-------------|
| `--limit` | int | 20 | 1–100 | Max signals to return |
| `--categories` | str | all | `POLITICS,CRYPTO,SPORTS,CULTURE,ECONOMICS,TECH,FINANCE` | Comma-separated filter |
| `--period` | str | WEEK | `DAY`, `WEEK`, `MONTH`, `ALL` | Lookback period |
| `--min-wallets` | int | 3 | ≥1 | Minimum smart wallets for consensus |

### `leaderboard` — PM top traders by PnL

| Param | Type | Default | Values | Description |
|-------|------|---------|--------|-------------|
| `--period` | str | WEEK | `DAY`, `WEEK`, `MONTH`, `ALL` | Ranking period |
| `--category` | str | OVERALL | `OVERALL`, `POLITICS`, `SPORTS`, `CRYPTO`, `CULTURE`, `ECONOMICS`, `TECH`, `FINANCE` | Category filter |
| `--limit` | int | 20 | 1–500 | Max traders to return |

### `consensus` — PM positions where smart bettors agree

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `--min-bettors` | int | 3 | Minimum bettors agreeing on a position |

### `trader` — PM trader profile by wallet

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `wallet` | str | yes | Polymarket wallet address (0x...) |

### `pm-top` — PM top traders by smart score

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `--limit` | int | 50 | Max traders to return |
| `--min-score` | float | 0 | Minimum smart score |

### `smart-bettors` — PM smart money bettors (high ROI, high trade count)

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `--limit` | int | 50 | Max bettors to return |

### `trader-positions` — PM trader current positions

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `wallet` | str | yes | Polymarket wallet address (0x...) |

### `trader-trades` — PM trader trade history

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `wallet` | str | yes | Polymarket wallet address (0x...) |
| `--limit` | int | no | Max trades to return (default 100) |

---

## Perpetuals (HyperLiquid)

### `perp-signals` — Perp trading signals

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `--limit` | int | 20 | Max signals to return |
| `--min-wallets` | int | 3 | Minimum wallets for consensus |
| `--min-score` | float | 0 | Minimum trader credibility score (0–100) |

### `perp-traders` — Perp smart money traders

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `--limit` | int | 20 | Max traders to return |
| `--min-score` | float | 0 | Minimum trader score (0–100) |
| `--categories` | str | all | Comma-separated: `swing_trading`, `large_cap_trader`, `high_win_rate`, `scalper`, etc. |

### `perp-top` — Perp top performers by PnL

| Param | Type | Default | Values | Description |
|-------|------|---------|--------|-------------|
| `--limit` | int | 10 | 1–100 | Max traders |
| `--period` | str | month | `day`, `week`, `month` | PnL ranking period |

### `perp-coins` — Coin distribution (long vs short sentiment)

No parameters. Returns all coins with smart money positions.

### `perp-categories` — Perp trader category list

No parameters.

### `perp-category-stats` — Perp category statistics

No parameters. Returns statistics (trader count, avg score, avg PnL) for each trader category.

### `perp-trader` — Perp trader details by address

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `address` | str | yes | HyperLiquid wallet address (0x...) |

---

## AI Dashboard

The AI Dashboard covers **4 asset types**: `perp` (perpetual futures), `spot` (token holdings), `hip3` (HIP-3 DEX positions), `pm` (prediction markets).

### `dashboard` — AI Dashboard overview

No parameters. Returns stats + top signals across all 4 asset types.

### `dashboard-latest` — Latest AI signal snapshots

| Param | Type | Required | Values | Description |
|-------|------|----------|--------|-------------|
| `type` | str | yes | `perp`, `spot`, `pm`, `hip3` | Asset type |
| `--limit` | int | no | 1–100 | Max snapshots to return |

### `dashboard-asset` — Full detail for a single asset

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | str | yes | Asset type: `perp`, `spot`, `pm`, `hip3` |
| `symbol` | str | yes | Asset symbol (e.g. BTC, ETH, SOL) |

### `agent-signal` — Raw composite data for trading agents

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | str | yes | Coin symbol: BTC, ETH, SOL, or HIP-3 format `dex:COIN` (e.g. `xyz:TSLA`) |
| `--categories` | str | no | Comma-separated SM wallet categories to filter |

Returns raw SM (per-timeframe), TA (multi-timeframe indicators), and Market (derivatives) data in one call.

---

## Derivatives (CoinGlass)

### `derivatives` — All derivatives indicators for a coin

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | str | yes | Coin symbol: BTC, ETH, SOL, etc. |

Returns: open interest, funding rate, long/short ratio, liquidation summary, taker buy/sell ratio, market overview. Cached 60s.

### `fear-greed` — Crypto Fear & Greed Index

No parameters.

### `derivatives-pairs` — Per-exchange pair data

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | str | yes | Coin symbol: BTC, ETH, SOL, etc. |

Returns per-exchange breakdown: OI, volume, funding rate, liquidation, price.

---

## Technical Analysis (TAAPI.io)

### `ta` — Multi-timeframe TA indicators

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `symbol` | str | required | Coin symbol: BTC, ETH, SOL, etc. |
| `--timeframes` | str | 15m,1h,4h,1d | Comma-separated timeframes |
| `--indicators` | str | default set | Comma-separated: rsi,macd,bbands,sma,ema,stoch,adx,atr,cci,willr |
| `--exchange` | str | binancefutures | Exchange name |

### `ta-single` — Single TA indicator value

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `symbol` | str | required | Coin symbol |
| `indicator` | str | required | Indicator: rsi, macd, bbands, sma, ema, stoch, adx, atr, cci, willr |
| `--interval` | str | 4h | Timeframe: 15m, 1h, 4h, 1d |
| `--exchange` | str | binancefutures | Exchange name |
| `--period` | int | default | Period parameter (e.g. 14 for RSI) |

---

## Liquidation

### `liquidation-map` — Liquidation price distribution

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `coin` | str | required | Coin symbol: BTC, ETH, SOL, etc. |
| `--buckets` | int | 40 | Number of price buckets (10–100) |

---

## Agent Management

### `agents` — List your trading agents

No parameters.

### `agent-get` — Get full agent config and state

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID (e.g. `agent_abc12345`) |

### `agent-create` — Create a new trading agent

See the **Agent Creation Flow** in SKILL.md for the full conversational workflow.

**Core params:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `--name` | str | required | Agent display name |
| `--type` | str | composite | Preset: `composite`, `momentum_hunter`, `stable_grower`, `precision_master`, `whale_follower`, `scalping_pro`, `swing_trader` + HIP-3: `hip3_whale_follower`, `hip3_diversified`, `hip3_conviction`. Auto-fills SM categories, thresholds, timeframe weights |
| `--execution-mode` | str | auto | `auto` = fully automated. `hitl` = human-in-the-loop (trade plans for approval) |
| `--description` | str | auto | Agent description |

**Agent params:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `--assets` | str | BTC,ETH | Coins: `BTC,ETH,SOL,HYPE` or HIP-3 `dex:COIN` (e.g. `xyz:TSLA`) |
| `--categories` | str | auto | SM wallet categories to follow |
| `--signal-weights` | json | SM=40,TA=35,Market=25 | `{"sm":40,"ta":35,"market":25}` (sum=100) |
| `--trading-risk` | json | from preset | `{max_positions, max_position_size_pct, default_stop_loss_pct, default_take_profit_pct, max_leverage}` |
| `--strength-thresholds` | json | from preset | Entry/exit thresholds per asset |
| `--timeframe-weights` | json | from preset | SM signal timeframe weights (sum=1.0) |
| `--trigger-conditions` | json | auto from preset | Entry/exit triggers. See [Trigger Conditions](TRIGGER_CONDITIONS.md) |
| `--prompt-config` | json | auto-generated | `{trading_strategy, custom_rules, risk_management}` |
| `--leverage` | int | 5 | Max leverage (1–20) |
| `--risk-per-trade` | float | 1 | Risk per trade % |
| `--max-daily-loss` | float | 3 | Max daily loss % |
| `--risk-reward` | str | 1:2 | Risk:reward ratio |
| `--min-confidence` | float | 0.8 | Min LLM confidence (0–1) |
| `--min-consensus` | float | 0.7 | Min SM consensus (0–1) |
| `--max-trades-per-day` | int | 3 | Max trades per day |
| `--withdrawal-addresses` | str | none | Whitelisted 0x addresses (comma-separated) |

### `agent-update` — Update agent configuration

| Param | Type | Description |
|-------|------|-------------|
| `agent_id` | str | Agent ID (positional) |
| `--name` | str | New name |
| `--description` | str | New description |
| `--assets` | str | Comma-separated assets |
| `--categories` | str | Comma-separated categories |
| `--leverage` | int | Max leverage |
| `--execution-mode` | str | `auto` or `hitl` |
| `--prompt-config` | json | `{trading_strategy, custom_rules, risk_management}` |
| `--trading-strategy` | str | Overall trading approach for LLM (shorthand for prompt_config.trading_strategy) |
| `--custom-rules` | str | Specific entry/exit rules for LLM (shorthand for prompt_config.custom_rules) |
| `--risk-management` | str | Risk management rules for LLM (shorthand for prompt_config.risk_management) |
| `--trigger-conditions` | json | Entry/exit triggers |
| `--trading-risk` | json | Risk parameters |
| `--signal-weights` | json | `{sm, ta, market}` summing to 100 |
| `--strength-thresholds` | json | Entry/exit thresholds per asset |
| `--timeframe-weights` | json | Timeframe weight distribution |
| `--withdrawal-addresses` | str | Withdrawal whitelist |

### `agent-deploy` — Validate config and enable trading

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent to deploy |
| `--confirm` | flag | yes | **Financial gate** — required to execute |

### `agent-enable` — Enable agent for live trading

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |
| `--confirm` | flag | yes | **Financial gate** — required to execute |

### `agent-disable` / `agent-pause` — Stop trading

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

No `--confirm` needed — these are safety actions that stop trading.

### `agent-delete` — Delete agent (soft delete)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

**No `--confirm` flag.** Executes directly — ask user verbally before running.

### `agent-overview` — Agent overview (via AgentsArena)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

Returns: `name`, `status`, `total_pnl`, `roi`, `win_rate`, `profit_factor`, `configuration`, `market_type`.

### `agent-stats` — Performance statistics (via AgentsArena)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

Returns `performance_metrics` + `advanced_metrics` (win_rate, sharpe, drawdown, etc).

### `agent-performance` — Advanced performance metrics (via AgentsArena)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

Returns detailed performance breakdown with advanced metrics (Sharpe, Sortino, drawdown curves, etc).

### `agent-trades` — Trade history (via AgentsArena)

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `agent_id` | str | required | Agent ID |
| `--limit` | int | 50 | Max trades (1–100) |
| `--offset` | int | 0 | Pagination offset |
| `--filter` | str | all | `all`, `wins`, `losses` |

### `agent-vault` — Vault (trading wallet) info

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

### `agent-balance` — Live vault balance from Hyperliquid

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

Returns: `account_value`, `withdrawable`, `has_positions`, `vault_address`.

### `agent-positions` — Open positions (live from Hyperliquid)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

### `agent-deposit` — Get deposit address + safe payment links

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

Returns:
| Field | Description |
|-------|-------------|
| `deposit_address` | Vault address on Arbitrum One |
| `chain` | "Arbitrum One (Chain ID: 42161)" |
| `token` | "USDC" |
| `token_contract` | USDC contract address on Arbitrum |
| `payment_link` | EIP-681 URI — opens wallet app with address + chain + token pre-filled (SAFEST) |
| `qr_code_url` | QR code image URL containing the payment link — scan with mobile wallet |
| `verify_address_url` | Arbiscan link to verify the deposit address on-chain |
| `safety_warnings` | List of critical warnings (wrong chain, wrong token, etc.) |

**Always present `payment_link` and `qr_code_url` to user** — these auto-fill the wallet with correct chain/token/address, eliminating manual copy errors.

### `agent-fund` — Bridge USDC from Arbitrum to Hyperliquid

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |
| `--confirm` | flag | yes | **Financial gate** — required to execute |

**Gas fees sponsored by Zonein** — no ETH needed. Returns `tx_hash` and `amount` bridged.

### `agent-open` — Open a position (executes immediately)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |
| `--coin` | str | yes | BTC, ETH, SOL, HYPE, or `dex:COIN` |
| `--direction` | str | no (LONG) | LONG or SHORT |
| `--size` | float | yes | Position size in USD |
| `--leverage` | int | no | Leverage (1–20) |
| `--stop-loss` | float | no | Stop loss price |
| `--take-profit` | float | no | Take profit price |
| `--order-type` | str | no (market) | `market` or `limit` |
| `--limit-price` | float | no | Required for limit orders |
| `--confirm` | flag | yes | **Financial gate** — required to execute |

### `agent-close` — Close a position (executes immediately)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |
| `--coin` | str | yes | Coin to close |
| `--confirm` | flag | yes | **Financial gate** — required to execute |

### `agent-update-sl-tp` — Update stop-loss / take-profit

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |
| `--coin` | str | yes | Token symbol |
| `--stop-loss` | float | no | New stop loss price |
| `--take-profit` | float | no | New take profit price |
| `--confirm` | flag | yes | **Financial gate** — required to execute |

### `agent-orders` — Manual order history

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `agent_id` | str | required | Agent ID |
| `--limit` | int | 20 | Max orders |

### `agent-withdraw` — Withdraw funds (FULL SWEEP)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |
| `--to` | str | yes | Destination 0x... wallet on Arbitrum |
| `--confirm` | flag | yes | **Financial gate** — required to execute |

Agent must be **disabled** before withdrawing. **No `--amount` param — withdraws ALL funds from vault.** Partial withdrawal not supported.

### `agent-backtest` — Run backtest simulation

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `agent_id` | str | required | Agent ID |
| `--symbol` | str | BTC | Coin: BTC, ETH, SOL, HYPE |
| `--days` | int | 30 | Period (7–90 days) |
| `--initial-balance` | float | 10000 | Starting balance USD |

**Requires `--confirm`.**

### `agent-backtests` — List past backtests

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `agent_id` | str | required | Agent ID |
| `--limit` | int | 10 | Max results |

### `agent-templates` — Agent types & default config

No parameters.

### `agent-assets` — Available trading assets

No parameters. Returns: BTC, ETH, SOL, HYPE. For HIP-3, use `hip3-dexs` and `hip3-assets`.

### `agent-categories` — Smart money categories with live stats

No parameters.

---

## HIP-3 Trading

HIP-3 = builder-deployed perpetuals on Hyperliquid — stocks (TSLA, NVDA), commodities (GOLD), indices (US500), exotic assets.

**Uses the SAME commands as regular perps** — just use `dex:COIN` format (e.g. `xyz:TSLA`).

| | Regular Perps | HIP-3 Perps |
|-|---------------|-------------|
| **Coin** | `BTC`, `ETH` | `xyz:TSLA`, `hyna:BTC` |
| **Margin** | Cross or Isolated | **Isolated only** |
| **Fees** | Standard | 2x standard |

### `hip3-dexs` / `hip3-assets` — HIP-3 DEX discovery

List all HIP-3 DEXs (xyz, flx, vntl, hyna, km, cash) and their assets with prices, OI, max leverage.

**HIP-3 SM Categories:**
| Category | Description |
|----------|-------------|
| `scalper` | Ultra-short holds < 4h |
| `day_trader` | Intraday 4-48h |
| `swing_trader` | 2-14 days |
| `position_trader` | > 14 days |
| `trend_follower` | Strong long bias >=70% |
| `short_bias` | Predominantly short >=70% |
| `aggressive_leverage` | High leverage >=8x |
| `conservative` | Low leverage <=3x |
| `high_conviction` | Few big bets |
| `multi_asset` | 5+ assets |
| `alpha_generator` | Exceptional risk-adjusted returns |
| `perp_verified` | Also SM in perp trading |

---

## HITL Trade Plans

When an agent has `execution_mode=hitl`, it creates trade plans instead of executing automatically.

### `agent-check` — Check pending trade plans across all agents

No parameters.

### `agent-plans` — List trade plans for a specific agent

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `agent_id` | str | required | Agent ID |
| `--status` | str | pending | `pending`, `approved`, `rejected`, `expired`, `all` |
| `--limit` | int | 20 | Max plans |

### `agent-plan-detail` — Full trade plan with evidence

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |
| `plan_id` | str | yes | Plan ID |

### `agent-plan-action` — Act on a pending trade plan

Unified command for approve/reject/edit/paper actions on trade plans.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |
| `plan_id` | str | yes | Trade plan ID |
| `action` | str | yes | `approve`, `reject`, `edit`, `paper` |
| `--notes` | str | no | User reasoning |
| `--edits` | json | no | For edit: `{entry, stop_loss, take_profit, size_usd, leverage}` |

**`approve` and `edit` require `--confirm`.** `reject` does NOT need `--confirm`. Reject triggers a 30-minute cooldown for the same token.

### `agent-plan-history` — Past trade plans

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `agent_id` | str | required | Agent ID |
| `--limit` | int | 20 | Max results |

---

## Telegram Notifications

### `telegram-setup-init` — Easy setup (recommended)

```
telegram-setup-init --bot-token "<BOT_TOKEN>"
```

1. User creates bot via @BotFather → gets token
2. Run setup-init → server responds "send /start to your bot"
3. User sends /start → webhook auto-detects chat_id → done

### `telegram-setup` — Advanced setup (manual chat_id)

```
telegram-setup --bot-token "<BOT_TOKEN>" --chat-id "<CHAT_ID>"
```

### `telegram-config` — View current config

No parameters.

### `telegram-disable` — Disable notifications + remove webhook

No parameters.

---

## Utility

### `status` — Check API key status

No parameters.
