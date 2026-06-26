---
name: tvfetch-backtest
version: 1.0.0
description: Backtesting-focused variant — framework-aware data export
triggers:
  - /tvfetch-backtest
  - /backtest
tools:
  - Bash
  - Read
  - Write
---

# tvfetch-backtest

Backtesting-focused data fetching. When saving data, always asks which framework
the user targets and provides framework-specific code snippets.

## Behavior

1. Fetch OHLCV bars via `scripts/lib/fetch.py`
2. When saving or exporting, ask: **Which backtesting framework?**
   - `backtrader`
   - `freqtrade`
   - `vectorbt`
3. Output data in the framework's expected format with a ready-to-run code snippet

## Framework Formats

### backtrader

Save as CSV with columns: `datetime,open,high,low,close,volume,openinterest`

```python
import backtrader as bt

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=20)

    def next(self):
        if self.data.close[0] > self.sma[0] and not self.position:
            self.buy()
        elif self.data.close[0] < self.sma[0] and self.position:
            self.sell()

cerebro = bt.Cerebro()
data = bt.feeds.GenericCSVData(
    dataname='{{FILE_PATH}}',
    dtformat='%Y-%m-%d',
    datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=6
)
cerebro.adddata(data)
cerebro.run()
cerebro.plot()
```

### freqtrade

Save as JSON in freqtrade's OHLCV format:

```python
# Place in user_data/data/{{EXCHANGE}}/{{PAIR}}-{{TIMEFRAME}}.json
# Format: [[timestamp_ms, open, high, low, close, volume], ...]

# freqtrade backtesting command:
# freqtrade backtesting --strategy MyStrategy --timerange 20240101-20250101
```

### vectorbt

Save as CSV, load with pandas:

```python
import vectorbt as vbt
import pandas as pd

df = pd.read_csv('{{FILE_PATH}}', index_col='datetime', parse_dates=True)
close = df['close']

# Example: SMA crossover
fast_ma = vbt.MA.run(close, window=10)
slow_ma = vbt.MA.run(close, window=30)

entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

pf = vbt.Portfolio.from_signals(close, entries, exits, init_cash=10000)
print(pf.stats())
```

## Intent Parsing

| User says | Action |
|-----------|--------|
| `BTC for backtrader` | Fetch 1D 365 bars, save as backtrader CSV |
| `AAPL 1h 1000 vectorbt` | Fetch 60m 1000 bars, save as vectorbt CSV |
| `get ETH data` | Fetch, then ask which framework before saving |
| `backtest BTC sma crossover` | Fetch, save, generate strategy skeleton |

## Rules

- Always ask which framework before saving (unless already specified).
- Include the framework code snippet with the correct file path filled in.
- Default: 1D timeframe, 365 bars (one year of daily data).
- For freqtrade, use millisecond timestamps. For others, use ISO dates.
- If the user mentions a strategy, generate a minimal working skeleton for that framework.
