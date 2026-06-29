---
name: trading-signal-analysis
description: "Trading Signal Analysis: Ingest OHLCV datasets for any stock or cryptocurrency and generate. Use when an agent needs trading signal analysis, generate buy and sell trading signals from technical indicators, backtest trading strategies against historical ohlcv price data, analyze maximum adverse excursion and maximum favorable excursion for trade risk, calculate win rate and expectancy for systematic trading strategies, analyze signals, candles, symbol through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/trading-signal-analysis
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/trading-signal-analysis"}}
---
# Trading Signal Analysis

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Analyze any stock or cryptocurrency with professional-grade trading signal diagnostics powered by multi-indicator technical analysis. Feed in OHLCV price data and get back actionable buy and sell signals, strategy backtests with historical performance metrics, and detailed risk analytics including maximum adverse excursion, maximum favorable excursion, win rate, expectancy, and drawdown analysis. Identify trend and momentum regimes, evaluate signal strength across multiple timeframes, and export publication-ready analysis charts and trade logs. Perfect for systematic traders building quantitative strategies, portfolio managers evaluating entry and exit timing, crypto analysts screening for momentum setups, and researchers backtesting technical indicators against real market data.

## Product Instructions
### Trading Signal Analysis

Advanced signal detection, backtesting, and risk analytics engine for stock and crypto OHLCV data. Computes technical indicators, detects trading signals, runs strategy backtests with MAE/MFE analysis, and generates downloadable charts and trade logs.

#### Actions

##### analyze_signals

Detect trading signals from OHLCV candle data. Computes SMA, EMA, RSI, MACD, Bollinger Bands, ATR, breakout levels, and volume analysis. Returns signal counts, recent signal events, and current indicator values.

**Required:** `candles` (array of OHLCV objects, minimum 30 rows)

```json
{
  "candles": [
    {"timestamp": "2024-01-01T00:00:00Z", "open": 42000, "high": 42500, "low": 41800, "close": 42300, "volume": 1500},
    {"timestamp": "2024-01-02T00:00:00Z", "open": 42300, "high": 43000, "low": 42100, "close": 42800, "volume": 1800}
  ],
  "symbol": "BTC-USD",
  "timeframe": "1D"
}
```

##### backtest_strategy

Run a strategy backtest on OHLCV data. Returns trade log, equity curve, and metrics (win rate, Sharpe, Sortino, max drawdown, MAE/MFE, profit factor).

**Required:** `candles`

```json
{
  "candles": [{"open": 100, "high": 105, "low": 98, "close": 103, "volume": 5000}],
  "symbol": "AAPL",
  "strategy": "sma_cross",
  "initial_capital": 10000,
  "stop_loss_pct": 0.02,
  "take_profit_pct": 0.05
}
```

##### full_analysis

Run both signal analysis and backtest, generate downloadable signal chart, performance chart, and trade log CSV.

**Required:** `candles`

```json
{
  "candles": [{"open": 100, "high": 105, "low": 98, "close": 103, "volume": 5000}],
  "symbol": "ETH-USD",
  "timeframe": "1H",
  "strategy": "composite",
  "initial_capital": 50000,
  "store_charts": true,
  "store_trade_log": true
}
```

#### Candle Data Format

Each candle object requires:
- `open` (number) -- Open price (required)
- `high` (number) -- High price (required)
- `low` (number) -- Low price (required)
- `close` (number) -- Close price (required)
- `timestamp` (string) -- Optional timestamp
- `volume` (number) -- Optional volume (defaults to 0)

Minimum 30 candles required; more is better for accurate indicator calculations.

#### Strategy Options

| Strategy | Description |
|---|---|
| sma_cross | SMA fast/slow crossover |
| ema_cross | EMA fast/slow crossover |
| macd_cross | MACD line/signal crossover |
| rsi_reversion | Mean reversion on RSI oversold/overbought |
| breakout | Price breakout above/below rolling high/low |
| composite | Multi-indicator consensus (default, requires 3+ aligned signals) |

#### Indicator Parameters

All have sensible defaults. Key ones:
- `sma_fast` / `sma_slow` -- SMA periods (default: 20/50)
- `ema_fast` / `ema_slow` -- EMA periods (default: 12/26)
- `rsi_period` -- RSI period (default: 14)
- `macd_signal_period` -- MACD signal period (default: 9)
- `bollinger_period` / `bollinger_stddev` -- Bollinger Bands (default: 20/2.0)
- `atr_period` -- ATR period (default: 14)
- `breakout_lookback` -- Rolling high/low window (default: 20)

#### Risk Controls

- `stop_loss_pct` -- Stop loss as decimal (e.g., 0.02 = 2%)
- `take_profit_pct` -- Take profit as decimal (e.g., 0.05 = 5%)
- `trailing_stop_pct` -- Trailing stop as decimal

#### Output Options

- `return_indicator_series` -- Include full indicator arrays (default: false)
- `store_charts` -- Generate PNG charts (default: true, full_analysis only)
- `store_trade_log` -- Generate CSV trade log (default: true, full_analysis only)
- `expiration_days` -- File retention 1-7 days (default: 7)
- `chart_width` / `chart_height` -- Chart dimensions in pixels

#### Performance Metrics

Backtest results include:
- **total_trades**, **wins**, **losses**, **win_rate_pct**
- **total_return_pct**, **final_equity**
- **max_drawdown_pct**
- **expectancy_pct** -- Average trade return
- **profit_factor** -- Sum of wins / sum of losses
- **sharpe** -- Annualized Sharpe ratio
- **sortino** -- Annualized Sortino ratio
- **average_trade_mae_pct** -- Average Maximum Adverse Excursion
- **average_trade_mfe_pct** -- Average Maximum Favorable Excursion
- **average_bars_held** -- Average trade duration

#### Important Notes

- Candle data must have at least 30 rows; more rows than the largest indicator window + 2.
- `sma_fast` must be less than `sma_slow`; `ema_fast` must be less than `ema_slow`.
- `rsi_oversold` must be less than `rsi_overbought`.
- Transaction costs are applied as basis points per side (default 5 bps = 0.05%).
- Set `periods_per_year` to match your data frequency (252 for daily, 8760 for hourly).
- Charts are stored in cloud storage with signed download URLs.

## When To Use
- Use this skill for `Trading Signal Analysis` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: trading signal analysis, generate buy and sell trading signals from technical indicators, backtest trading strategies against historical ohlcv price data, analyze maximum adverse excursion and maximum favorable excursion for trade risk, calculate win rate and expectancy for systematic trading strategies, analyze signals, candles, symbol.
- Supported action names: `analyze_signals`, `backtest_strategy`, `full_analysis`.

## Use Cases
- Generate buy and sell trading signals from technical indicators
- Backtest trading strategies against historical OHLCV price data
- Analyze maximum adverse excursion and maximum favorable excursion for trade risk
- Calculate win rate and expectancy for systematic trading strategies
- Measure portfolio drawdown and volatility metrics
- Detect momentum and trend regime changes in stock or crypto markets
- Export candlestick signal charts with indicator overlays
- Generate trade logs for strategy performance review
- Screen stocks and cryptocurrencies for technical signal setups
- Evaluate entry and exit timing with multi-indicator analysis

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `3`.
x402 availability: not enabled for this product.

- `analyze_signals` (action slug: `analyze-signals`): Detect trading signals from OHLCV data using SMA/EMA crossovers, RSI, MACD, Bollinger Bands, breakouts, and volume spikes. Returns signal counts, recent events, and latest indicator values. Price: `6` credits. Parameters: `atr_period`, `bollinger_period`, `bollinger_stddev`, `breakout_lookback`, `candles`, `ema_fast`, `ema_slow`, `macd_signal_period`, plus 10 more.
- `backtest_strategy` (action slug: `backtest-strategy`): Backtest a trading strategy on OHLCV data. Returns trade log, equity curve, and performance metrics (win rate, Sharpe, Sortino, drawdown, MAE/MFE). Price: `6` credits. Parameters: `atr_period`, `bollinger_period`, `bollinger_stddev`, `breakout_lookback`, `candles`, `ema_fast`, `ema_slow`, `include_short`, plus 17 more.
- `full_analysis` (action slug: `full-analysis`): Run both signal analysis and strategy backtest, generate downloadable charts and trade log CSV. Price: `6` credits. Parameters: `atr_period`, `bollinger_period`, `bollinger_stddev`, `breakout_lookback`, `candles`, `chart_height`, `chart_width`, `ema_fast`, plus 24 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "trading-signal-analysis"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "trading-signal-analysis"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "trading-signal-analysis"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "trading-signal-analysis"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "trading-signal-analysis"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "trading-signal-analysis"
  }
}
```

## Call This Tool
Product slug: `trading-signal-analysis`

Marketplace page: https://www.agentpmt.com/marketplace/trading-signal-analysis

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Trading-Signal-Analysis",
    "arguments": {
      "action": "analyze_signals",
      "atr_period": 14,
      "bollinger_period": 20,
      "bollinger_stddev": 2,
      "breakout_lookback": 20,
      "candles": [
        {
          "close": 1,
          "high": 1,
          "low": 1,
          "open": 1,
          "timestamp": "example timestamp",
          "volume": 1
        }
      ],
      "ema_fast": 12,
      "ema_slow": 26,
      "macd_signal_period": 9
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "trading-signal-analysis",
  "parameters": {
    "action": "analyze_signals",
    "atr_period": 14,
    "bollinger_period": 20,
    "bollinger_stddev": 2,
    "breakout_lookback": 20,
    "candles": [
      {
        "close": 1,
        "high": 1,
        "low": 1,
        "open": 1,
        "timestamp": "example timestamp",
        "volume": 1
      }
    ],
    "ema_fast": 12,
    "ema_slow": 26,
    "macd_signal_period": 9
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `analyze_signals` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/trading-signal-analysis
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
