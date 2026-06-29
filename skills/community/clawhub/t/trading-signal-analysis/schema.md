# Trading Signal Analysis Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `trading-signal-analysis`

x402 availability: not enabled for this product.

## `analyze_signals`

Action slug: `analyze-signals`

Price: `6` credits

Detect trading signals from OHLCV data using SMA/EMA crossovers, RSI, MACD, Bollinger Bands, breakouts, and volume spikes. Returns signal counts, recent events, and latest indicator values.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `atr_period` | `integer` | no | ATR period. |
| `bollinger_period` | `integer` | no | Bollinger Bands period. |
| `bollinger_stddev` | `number` | no | Bollinger Bands standard deviation multiplier. |
| `breakout_lookback` | `integer` | no | Breakout lookback period. |
| `candles` | `array` | yes | OHLCV candle series (minimum 30 rows). Each item needs open, high, low, close (required) and optional timestamp and volume. |
| `ema_fast` | `integer` | no | EMA fast period. |
| `ema_slow` | `integer` | no | EMA slow period. |
| `macd_signal_period` | `integer` | no | MACD signal line period. |
| `return_indicator_series` | `boolean` | no | Return full indicator arrays in response. |
| `rsi_overbought` | `number` | no | RSI overbought threshold. |
| `rsi_oversold` | `number` | no | RSI oversold threshold. |
| `rsi_period` | `integer` | no | RSI period. |
| `sma_fast` | `integer` | no | SMA fast period. |
| `sma_slow` | `integer` | no | SMA slow period. |
| `symbol` | `string` | no | Optional symbol label (e.g., BTC-USD). |
| `timeframe` | `string` | no | Optional timeframe label (e.g., 1H, 1D). |
| `volume_spike_multiplier` | `number` | no | Volume spike detection multiplier. |
| `volume_window` | `integer` | no | Volume SMA window. |

Sample parameters:

```json
{
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
```

Generated JSON parameter schema:

```json
{
  "atr_period": {
    "default": 14,
    "description": "ATR period.",
    "required": false,
    "type": "integer"
  },
  "bollinger_period": {
    "default": 20,
    "description": "Bollinger Bands period.",
    "required": false,
    "type": "integer"
  },
  "bollinger_stddev": {
    "default": 2,
    "description": "Bollinger Bands standard deviation multiplier.",
    "required": false,
    "type": "number"
  },
  "breakout_lookback": {
    "default": 20,
    "description": "Breakout lookback period.",
    "required": false,
    "type": "integer"
  },
  "candles": {
    "description": "OHLCV candle series (minimum 30 rows). Each item needs open, high, low, close (required) and optional timestamp and volume.",
    "items": {
      "properties": {
        "close": {
          "type": "number"
        },
        "high": {
          "type": "number"
        },
        "low": {
          "type": "number"
        },
        "open": {
          "type": "number"
        },
        "timestamp": {
          "type": "string"
        },
        "volume": {
          "type": "number"
        }
      },
      "type": "object"
    },
    "required": true,
    "type": "array"
  },
  "ema_fast": {
    "default": 12,
    "description": "EMA fast period.",
    "required": false,
    "type": "integer"
  },
  "ema_slow": {
    "default": 26,
    "description": "EMA slow period.",
    "required": false,
    "type": "integer"
  },
  "macd_signal_period": {
    "default": 9,
    "description": "MACD signal line period.",
    "required": false,
    "type": "integer"
  },
  "return_indicator_series": {
    "description": "Return full indicator arrays in response.",
    "required": false,
    "type": "boolean"
  },
  "rsi_overbought": {
    "default": 70,
    "description": "RSI overbought threshold.",
    "required": false,
    "type": "number"
  },
  "rsi_oversold": {
    "default": 30,
    "description": "RSI oversold threshold.",
    "required": false,
    "type": "number"
  },
  "rsi_period": {
    "default": 14,
    "description": "RSI period.",
    "required": false,
    "type": "integer"
  },
  "sma_fast": {
    "default": 20,
    "description": "SMA fast period.",
    "required": false,
    "type": "integer"
  },
  "sma_slow": {
    "default": 50,
    "description": "SMA slow period.",
    "required": false,
    "type": "integer"
  },
  "symbol": {
    "description": "Optional symbol label (e.g., BTC-USD).",
    "required": false,
    "type": "string"
  },
  "timeframe": {
    "description": "Optional timeframe label (e.g., 1H, 1D).",
    "required": false,
    "type": "string"
  },
  "volume_spike_multiplier": {
    "default": 1.5,
    "description": "Volume spike detection multiplier.",
    "required": false,
    "type": "number"
  },
  "volume_window": {
    "default": 20,
    "description": "Volume SMA window.",
    "required": false,
    "type": "integer"
  }
}
```

## `backtest_strategy`

Action slug: `backtest-strategy`

Price: `6` credits

Backtest a trading strategy on OHLCV data. Returns trade log, equity curve, and performance metrics (win rate, Sharpe, Sortino, drawdown, MAE/MFE).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `atr_period` | `integer` | no | ATR period. |
| `bollinger_period` | `integer` | no | Bollinger Bands period. |
| `bollinger_stddev` | `number` | no | Bollinger Bands standard deviation. |
| `breakout_lookback` | `integer` | no | Breakout lookback period. |
| `candles` | `array` | yes | OHLCV candle series (minimum 30 rows). |
| `ema_fast` | `integer` | no | EMA fast period. |
| `ema_slow` | `integer` | no | EMA slow period. |
| `include_short` | `boolean` | no | Allow short entries. |
| `initial_capital` | `number` | no | Starting equity. |
| `macd_signal_period` | `integer` | no | MACD signal line period. |
| `max_trades` | `integer` | no | Maximum number of closed trades. |
| `periods_per_year` | `integer` | no | Annualization factor for Sharpe/Sortino (252 for daily, 8760 for hourly). |
| `rsi_overbought` | `number` | no | RSI overbought threshold. |
| `rsi_oversold` | `number` | no | RSI oversold threshold. |
| `rsi_period` | `integer` | no | RSI period. |
| `sma_fast` | `integer` | no | SMA fast period. |
| `sma_slow` | `integer` | no | SMA slow period. |
| `stop_loss_pct` | `number` | no | Stop loss percentage (0.001 to 0.95). |
| `strategy` | `string` | no | Backtest strategy to use. |
| `symbol` | `string` | no | Optional symbol label. |
| `take_profit_pct` | `number` | no | Take profit percentage (0.001 to 5.0). |
| `timeframe` | `string` | no | Optional timeframe label. |
| `trailing_stop_pct` | `number` | no | Trailing stop percentage (0.001 to 0.95). |
| `transaction_cost_bps` | `number` | no | Round-trip transaction cost in basis points per side. |
| `volume_window` | `integer` | no | Volume SMA window. |

Sample parameters:

```json
{
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
  "include_short": true
}
```

Generated JSON parameter schema:

```json
{
  "atr_period": {
    "default": 14,
    "description": "ATR period.",
    "required": false,
    "type": "integer"
  },
  "bollinger_period": {
    "default": 20,
    "description": "Bollinger Bands period.",
    "required": false,
    "type": "integer"
  },
  "bollinger_stddev": {
    "default": 2,
    "description": "Bollinger Bands standard deviation.",
    "required": false,
    "type": "number"
  },
  "breakout_lookback": {
    "default": 20,
    "description": "Breakout lookback period.",
    "required": false,
    "type": "integer"
  },
  "candles": {
    "description": "OHLCV candle series (minimum 30 rows).",
    "items": {
      "properties": {
        "close": {
          "type": "number"
        },
        "high": {
          "type": "number"
        },
        "low": {
          "type": "number"
        },
        "open": {
          "type": "number"
        },
        "timestamp": {
          "type": "string"
        },
        "volume": {
          "type": "number"
        }
      },
      "type": "object"
    },
    "required": true,
    "type": "array"
  },
  "ema_fast": {
    "default": 12,
    "description": "EMA fast period.",
    "required": false,
    "type": "integer"
  },
  "ema_slow": {
    "default": 26,
    "description": "EMA slow period.",
    "required": false,
    "type": "integer"
  },
  "include_short": {
    "description": "Allow short entries.",
    "required": false,
    "type": "boolean"
  },
  "initial_capital": {
    "default": 10000,
    "description": "Starting equity.",
    "required": false,
    "type": "number"
  },
  "macd_signal_period": {
    "default": 9,
    "description": "MACD signal line period.",
    "required": false,
    "type": "integer"
  },
  "max_trades": {
    "default": 1000,
    "description": "Maximum number of closed trades.",
    "required": false,
    "type": "integer"
  },
  "periods_per_year": {
    "default": 252,
    "description": "Annualization factor for Sharpe/Sortino (252 for daily, 8760 for hourly).",
    "required": false,
    "type": "integer"
  },
  "rsi_overbought": {
    "default": 70,
    "description": "RSI overbought threshold.",
    "required": false,
    "type": "number"
  },
  "rsi_oversold": {
    "default": 30,
    "description": "RSI oversold threshold.",
    "required": false,
    "type": "number"
  },
  "rsi_period": {
    "default": 14,
    "description": "RSI period.",
    "required": false,
    "type": "integer"
  },
  "sma_fast": {
    "default": 20,
    "description": "SMA fast period.",
    "required": false,
    "type": "integer"
  },
  "sma_slow": {
    "default": 50,
    "description": "SMA slow period.",
    "required": false,
    "type": "integer"
  },
  "stop_loss_pct": {
    "description": "Stop loss percentage (0.001 to 0.95).",
    "required": false,
    "type": "number"
  },
  "strategy": {
    "default": "composite",
    "description": "Backtest strategy to use.",
    "enum": [
      "sma_cross",
      "ema_cross",
      "macd_cross",
      "rsi_reversion",
      "breakout",
      "composite"
    ],
    "required": false,
    "type": "string"
  },
  "symbol": {
    "description": "Optional symbol label.",
    "required": false,
    "type": "string"
  },
  "take_profit_pct": {
    "description": "Take profit percentage (0.001 to 5.0).",
    "required": false,
    "type": "number"
  },
  "timeframe": {
    "description": "Optional timeframe label.",
    "required": false,
    "type": "string"
  },
  "trailing_stop_pct": {
    "description": "Trailing stop percentage (0.001 to 0.95).",
    "required": false,
    "type": "number"
  },
  "transaction_cost_bps": {
    "default": 5,
    "description": "Round-trip transaction cost in basis points per side.",
    "required": false,
    "type": "number"
  },
  "volume_window": {
    "default": 20,
    "description": "Volume SMA window.",
    "required": false,
    "type": "integer"
  }
}
```

## `full_analysis`

Action slug: `full-analysis`

Price: `6` credits

Run both signal analysis and strategy backtest, generate downloadable charts and trade log CSV.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `atr_period` | `integer` | no | ATR period. |
| `bollinger_period` | `integer` | no | Bollinger Bands period. |
| `bollinger_stddev` | `number` | no | Bollinger Bands standard deviation. |
| `breakout_lookback` | `integer` | no | Breakout lookback. |
| `candles` | `array` | yes | OHLCV candle series (minimum 30 rows). |
| `chart_height` | `integer` | no | Chart height in pixels. |
| `chart_width` | `integer` | no | Chart width in pixels. |
| `ema_fast` | `integer` | no | EMA fast period. |
| `ema_slow` | `integer` | no | EMA slow period. |
| `expiration_days` | `integer` | no | Cloud file retention in days (1-7). |
| `include_short` | `boolean` | no | Allow short entries. |
| `initial_capital` | `number` | no | Starting equity. |
| `macd_signal_period` | `integer` | no | MACD signal line period. |
| `max_trades` | `integer` | no | Maximum closed trades. |
| `periods_per_year` | `integer` | no | Annualization factor for Sharpe/Sortino. |
| `return_indicator_series` | `boolean` | no | Return full indicator arrays. |
| `rsi_overbought` | `number` | no | RSI overbought threshold. |
| `rsi_oversold` | `number` | no | RSI oversold threshold. |
| `rsi_period` | `integer` | no | RSI period. |
| `sma_fast` | `integer` | no | SMA fast period. |
| `sma_slow` | `integer` | no | SMA slow period. |
| `stop_loss_pct` | `number` | no | Stop loss percentage. |
| `store_charts` | `boolean` | no | Generate and store signal and performance charts. |
| `store_trade_log` | `boolean` | no | Store trade log as downloadable CSV. |
| `strategy` | `string` | no | Backtest strategy to use. |
| `symbol` | `string` | no | Optional symbol label. |
| `take_profit_pct` | `number` | no | Take profit percentage. |
| `timeframe` | `string` | no | Optional timeframe label. |
| `trailing_stop_pct` | `number` | no | Trailing stop percentage. |
| `transaction_cost_bps` | `number` | no | Transaction cost in basis points. |
| `volume_spike_multiplier` | `number` | no | Volume spike multiplier. |
| `volume_window` | `integer` | no | Volume SMA window. |

Sample parameters:

```json
{
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
  "chart_height": 900,
  "chart_width": 1400,
  "ema_fast": 12
}
```

Generated JSON parameter schema:

```json
{
  "atr_period": {
    "default": 14,
    "description": "ATR period.",
    "required": false,
    "type": "integer"
  },
  "bollinger_period": {
    "default": 20,
    "description": "Bollinger Bands period.",
    "required": false,
    "type": "integer"
  },
  "bollinger_stddev": {
    "default": 2,
    "description": "Bollinger Bands standard deviation.",
    "required": false,
    "type": "number"
  },
  "breakout_lookback": {
    "default": 20,
    "description": "Breakout lookback.",
    "required": false,
    "type": "integer"
  },
  "candles": {
    "description": "OHLCV candle series (minimum 30 rows).",
    "items": {
      "properties": {
        "close": {
          "type": "number"
        },
        "high": {
          "type": "number"
        },
        "low": {
          "type": "number"
        },
        "open": {
          "type": "number"
        },
        "timestamp": {
          "type": "string"
        },
        "volume": {
          "type": "number"
        }
      },
      "type": "object"
    },
    "required": true,
    "type": "array"
  },
  "chart_height": {
    "default": 900,
    "description": "Chart height in pixels.",
    "required": false,
    "type": "integer"
  },
  "chart_width": {
    "default": 1400,
    "description": "Chart width in pixels.",
    "required": false,
    "type": "integer"
  },
  "ema_fast": {
    "default": 12,
    "description": "EMA fast period.",
    "required": false,
    "type": "integer"
  },
  "ema_slow": {
    "default": 26,
    "description": "EMA slow period.",
    "required": false,
    "type": "integer"
  },
  "expiration_days": {
    "default": 7,
    "description": "Cloud file retention in days (1-7).",
    "required": false,
    "type": "integer"
  },
  "include_short": {
    "description": "Allow short entries.",
    "required": false,
    "type": "boolean"
  },
  "initial_capital": {
    "default": 10000,
    "description": "Starting equity.",
    "required": false,
    "type": "number"
  },
  "macd_signal_period": {
    "default": 9,
    "description": "MACD signal line period.",
    "required": false,
    "type": "integer"
  },
  "max_trades": {
    "default": 1000,
    "description": "Maximum closed trades.",
    "required": false,
    "type": "integer"
  },
  "periods_per_year": {
    "default": 252,
    "description": "Annualization factor for Sharpe/Sortino.",
    "required": false,
    "type": "integer"
  },
  "return_indicator_series": {
    "description": "Return full indicator arrays.",
    "required": false,
    "type": "boolean"
  },
  "rsi_overbought": {
    "default": 70,
    "description": "RSI overbought threshold.",
    "required": false,
    "type": "number"
  },
  "rsi_oversold": {
    "default": 30,
    "description": "RSI oversold threshold.",
    "required": false,
    "type": "number"
  },
  "rsi_period": {
    "default": 14,
    "description": "RSI period.",
    "required": false,
    "type": "integer"
  },
  "sma_fast": {
    "default": 20,
    "description": "SMA fast period.",
    "required": false,
    "type": "integer"
  },
  "sma_slow": {
    "default": 50,
    "description": "SMA slow period.",
    "required": false,
    "type": "integer"
  },
  "stop_loss_pct": {
    "description": "Stop loss percentage.",
    "required": false,
    "type": "number"
  },
  "store_charts": {
    "default": true,
    "description": "Generate and store signal and performance charts.",
    "required": false,
    "type": "boolean"
  },
  "store_trade_log": {
    "default": true,
    "description": "Store trade log as downloadable CSV.",
    "required": false,
    "type": "boolean"
  },
  "strategy": {
    "default": "composite",
    "description": "Backtest strategy to use.",
    "enum": [
      "sma_cross",
      "ema_cross",
      "macd_cross",
      "rsi_reversion",
      "breakout",
      "composite"
    ],
    "required": false,
    "type": "string"
  },
  "symbol": {
    "description": "Optional symbol label.",
    "required": false,
    "type": "string"
  },
  "take_profit_pct": {
    "description": "Take profit percentage.",
    "required": false,
    "type": "number"
  },
  "timeframe": {
    "description": "Optional timeframe label.",
    "required": false,
    "type": "string"
  },
  "trailing_stop_pct": {
    "description": "Trailing stop percentage.",
    "required": false,
    "type": "number"
  },
  "transaction_cost_bps": {
    "default": 5,
    "description": "Transaction cost in basis points.",
    "required": false,
    "type": "number"
  },
  "volume_spike_multiplier": {
    "default": 1.5,
    "description": "Volume spike multiplier.",
    "required": false,
    "type": "number"
  },
  "volume_window": {
    "default": 20,
    "description": "Volume SMA window.",
    "required": false,
    "type": "integer"
  }
}
```
