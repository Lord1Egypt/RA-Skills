# Backtrader Patterns Reference

> Sources: backtrader GitHub source code (tradeanalyzer.py, sharpe.py, drawdown.py,
> returns.py, sqn.py), backtrader.com/docu/ (analyzers, cerebro, broker, orders).

Common patterns for generating correct Backtrader code from strategy specifications.

## Strategy Class Structure

```python
import backtrader as bt

class MyStrategy(bt.Strategy):
    params = (
        ('period', 20),
        ('threshold', 0.02),
    )

    def __init__(self):
        # Compute indicators once — these are lazy (Lines objects)
        self.sma = bt.indicators.SMA(self.data.close, period=self.p.period)
        self.rsi = bt.indicators.RSI(self.data.close, period=14)

    def next(self):
        # Called on every bar after all indicators have enough data
        if not self.position:
            if self.data.close[0] > self.sma[0]:
                self.buy()
        else:
            if self.data.close[0] < self.sma[0]:
                self.sell()
```

## Data Loading Patterns

### Single Symbol (yfinance)
```python
import yfinance as yf
import backtrader as bt

# CRITICAL: yfinance end date is EXCLUSIVE. "2024-01-01" fetches up to 2023-12-31.
# Since yfinance >=0.2.47, download() returns MultiIndex even for single ticker.
# Use auto_adjust=True (default since v1.0) or explicitly set it.
df = yf.download('AAPL', start='2020-01-01', end='2024-01-02',
                 auto_adjust=True, multi_level_index=False)
data = bt.feeds.PandasData(dataname=df)
cerebro.adddata(data)
```

### Multiple Symbols
```python
symbols = ['AAPL', 'MSFT', 'GOOGL']
for sym in symbols:
    df = yf.download(sym, start='2020-01-01', end='2024-01-02',
                     auto_adjust=True, multi_level_index=False)
    data = bt.feeds.PandasData(dataname=df, name=sym)
    cerebro.adddata(data)
```

### Accessing Multiple Data Feeds in Strategy
```python
class MultiStrategy(bt.Strategy):
    def __init__(self):
        # self.datas[0], self.datas[1], etc.  or  self.data0, self.data1
        self.smas = {}
        for d in self.datas:
            self.smas[d._name] = bt.indicators.SMA(d.close, period=20)

    def next(self):
        for i, d in enumerate(self.datas):
            if d.close[0] > d.close[-1]:
                self.buy(data=d)
```

## Position Sizing Patterns

### Equal Weight
```python
def next(self):
    n = len(self.datas)
    for d in self.datas:
        target = 1.0 / n
        self.order_target_percent(data=d, target=target)
```

### Volatility-Scaled
```python
def next(self):
    for d in self.datas:
        atr = self.atrs[d._name][0]
        risk_per_trade = self.broker.getvalue() * 0.01
        size = int(risk_per_trade / atr) if atr > 0 else 0
        self.buy(data=d, size=size)
```

### Long-Short Portfolio
```python
def next(self):
    ranked = sorted(range(len(self.datas)),
                    key=lambda i: self.signals[i][0], reverse=True)
    n_long = len(ranked) // 5
    n_short = len(ranked) // 5

    for i, d in enumerate(self.datas):
        if i in ranked[:n_long]:
            self.order_target_percent(data=d, target=1.0/n_long)
        elif i in ranked[-n_short:]:
            self.order_target_percent(data=d, target=-1.0/n_short)
        else:
            self.order_target_percent(data=d, target=0)
```

## Rebalancing Patterns

### Monthly Rebalancing
```python
class MonthlyRebalance(bt.Strategy):
    def __init__(self):
        self._last_month = -1

    def next(self):
        current_month = self.data.datetime.date(0).month
        if current_month == self._last_month:
            return
        self._last_month = current_month
        # Rebalance logic here
```

### Signal-Driven with Cooldown
```python
class SignalStrategy(bt.Strategy):
    params = (('cooldown', 5),)

    def __init__(self):
        self._bars_since_trade = 0

    def next(self):
        self._bars_since_trade += 1
        if self._bars_since_trade < self.p.cooldown:
            return
        if self.signal_triggered():
            self.buy()
            self._bars_since_trade = 0
```

## Cerebro & Broker Reference (from backtrader docs)

Key Cerebro behaviors:
- Default starting cash: **10,000** (not 100,000).
- Orders submitted on bar N execute on bar **N+1** (next bar).
- `cerebro.run()` returns a list of strategy instances.
- `cerebro.broker.getvalue()` returns current portfolio value (cash + positions).

Key Broker behaviors:
- Default commission: 0.0 (no commission).
- Slippage: `broker.set_slippage_perc(perc)` or `broker.set_slippage_fixed(fixed)`.
- Order types: `Market` (default), `Close`, `Limit`, `Stop`, `StopLimit`, `StopTrail`.
- Cheat-on-close: `cerebro.broker.set_coc(True)` — fills Close orders at current bar close.
- Cheat-on-open: `cerebro.broker.set_coo(True)` — fills Market orders at current bar open.

```python
def run_backtest():
    cerebro = bt.Cerebro()

    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)
    cerebro.addstrategy(MyStrategy, period=20)

    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.001)

    # Standard analyzers — see "Analyzer Return Structures" below
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe',
                        riskfreerate=0.0, annualize=True)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annual')

    results = cerebro.run()
    return results[0]  # first strategy instance

if __name__ == '__main__':
    run_backtest()
```

## Analyzer Return Structures (FROM SOURCE CODE)

This is the highest-value section. LLMs commonly hallucinate these keys.
All structures below are verified from the backtrader GitHub source.

### TradeAnalyzer (`bt.analyzers.TradeAnalyzer`)

Returns an `AutoOrderedDict`. Keys are created **only when trades occur**.
If there are zero trades, only `total.total = 0` exists — all other keys are absent.

After `stop()`, the analyzer calls `self.rets._close()` which prevents
creating new keys via dot notation.

```
rets.total.total          # int — all trades (open + closed)
rets.total.open           # int — currently open trades
rets.total.closed         # int — closed trades

rets.streak.won.current   # int
rets.streak.won.longest   # int
rets.streak.lost.current  # int
rets.streak.lost.longest  # int

rets.pnl.gross.total      # float — sum of all gross PnL
rets.pnl.gross.average    # float
rets.pnl.net.total        # float — sum of all net PnL (after commission)
rets.pnl.net.average      # float

rets.won.total            # int — count of winning trades
rets.won.pnl.total        # float — sum of winning PnL
rets.won.pnl.average      # float
rets.won.pnl.max          # float — best single trade

rets.lost.total           # int — count of losing trades
rets.lost.pnl.total       # float — sum of losing PnL (NEGATIVE)
rets.lost.pnl.average     # float (NEGATIVE)
rets.lost.pnl.max         # float — worst single trade (NEGATIVE)

rets.long.total           # int
rets.long.pnl.total       # float
rets.long.pnl.average     # float
rets.long.won             # int
rets.long.lost            # int
rets.long.pnl.won.total   # float
rets.long.pnl.lost.total  # float

rets.short.total          # int  (same sub-structure as long)

rets.len.total            # int — total bars in all trades
rets.len.average          # float
rets.len.max              # int
rets.len.min              # int
rets.len.won.total / average / max / min   # for winning trades
rets.len.lost.total / average / max / min  # for losing trades
```

**CRITICAL:** A zero-PnL trade counts as **WON** (source: `won = int(trade.pnlcomm >= 0.0)`).

### SharpeRatio (`bt.analyzers.SharpeRatio`)

Default params: `timeframe=TimeFrame.Years, riskfreerate=0.01, annualize=False,
stddev_sample=False, fund=None`

Annualization factors: `{Days: 252, Weeks: 52, Months: 12, Years: 1}`

```python
analysis = strat.analyzers.sharpe.get_analysis()
# Returns: {'sharperatio': float_or_None}
# Key is literally 'sharperatio' (one word, lowercase).
# Returns None on ZeroDivisionError (zero std dev) or insufficient data.
```

Use `SharpeRatio_A` (alias) for force-annualized variant (`annualize=True`).
When using with specific riskfreerate, set it explicitly:
```python
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe',
                    riskfreerate=0.0, annualize=True)
```

### DrawDown (`bt.analyzers.DrawDown`)

```python
analysis = strat.analyzers.drawdown.get_analysis()
# Keys (dot-accessible):
analysis.drawdown          # float — current drawdown %
analysis.moneydown         # float — current drawdown $
analysis.len               # int — current drawdown duration (bars)
analysis.max.drawdown      # float — maximum drawdown %
analysis.max.moneydown     # float — maximum drawdown $
analysis.max.len           # int — longest drawdown duration
```

**WARNING:** `TimeDrawDown` (the time-based variant) uses DIFFERENT key names:
`maxdrawdown` and `maxdrawdownperiod` (no dots). Do NOT confuse them.

### Returns (`bt.analyzers.Returns`)

Annualization factors: `{Days: 252.0, Weeks: 52.0, Months: 12.0, Years: 1.0}`

```python
analysis = strat.analyzers.returns.get_analysis()
analysis['rtot']     # float — total compound return (logarithmic)
analysis['ravg']     # float — average period return
analysis['rnorm']    # float — annualized return
analysis['rnorm100'] # float — annualized return as % (rnorm * 100)
```

### SQN — System Quality Number (`bt.analyzers.SQN`)

Formula: `sqrt(N) * avg(pnl) / stddev(pnl)` where N = trade count.
Returns `sqn=0` if N <= 1.

```python
analysis = strat.analyzers.sqn.get_analysis()
analysis['sqn']     # float — the SQN value
analysis['trades']  # int — number of trades used
```

### AnnualReturn (`bt.analyzers.AnnualReturn`)

```python
analysis = strat.analyzers.annual.get_analysis()
# Returns OrderedDict: {2020: 0.15, 2021: -0.03, ...}
# Values are DECIMALS (0.15 = 15%), NOT percentages.
```

## Metrics Extraction (Critical Pattern)

This function uses verified access patterns from source code:

```python
def extract_metrics(strat, cerebro):
    """Extract metrics from backtrader analyzers as a flat dict.

    Uses try/except throughout because AutoOrderedDict keys only exist
    when populated. Zero-trade runs have almost no keys.
    """
    metrics = {}

    # --- Portfolio value ---
    start_val = cerebro.broker.startingcash
    final_val = cerebro.broker.getvalue()
    metrics['start_value'] = start_val
    metrics['final_value'] = round(final_val, 2)
    metrics['total_return'] = round((final_val / start_val - 1) * 100, 2)

    # --- Sharpe Ratio ---
    # Source: sharpe.py returns {'sharperatio': float_or_None}
    try:
        sr = strat.analyzers.sharpe.get_analysis().get('sharperatio')
        metrics['sharpe_ratio'] = round(sr, 4) if sr is not None else None
    except Exception:
        metrics['sharpe_ratio'] = None

    # --- Drawdown ---
    # Source: drawdown.py keys: max.drawdown, max.moneydown, max.len
    try:
        dd = strat.analyzers.drawdown.get_analysis()
        metrics['max_drawdown_pct'] = round(dd.max.drawdown, 2)
        metrics['max_drawdown_money'] = round(dd.max.moneydown, 2)
        metrics['max_drawdown_len'] = dd.max.len
    except Exception:
        metrics['max_drawdown_pct'] = None

    # --- Returns (logarithmic) ---
    # Source: returns.py keys: rtot, ravg, rnorm, rnorm100
    try:
        ret = strat.analyzers.returns.get_analysis()
        metrics['total_return_log'] = round(ret.get('rtot', 0) * 100, 2)
        metrics['annualized_return'] = round(ret.get('rnorm100', 0), 2)
    except Exception:
        pass

    # --- SQN ---
    # Source: sqn.py keys: sqn, trades. Returns sqn=0 if trades <=1.
    try:
        sqn = strat.analyzers.sqn.get_analysis()
        metrics['sqn'] = round(sqn.get('sqn', 0), 4)
    except Exception:
        pass

    # --- Trade Statistics ---
    # Source: tradeanalyzer.py — keys only exist when trades occur.
    # With zero trades, only total.total=0 exists.
    try:
        ta = strat.analyzers.trades.get_analysis()
        total_closed = ta.get('total', {}).get('closed', 0)
        metrics['num_trades'] = total_closed
        if total_closed > 0:
            # NOTE: won includes zero-PnL trades (pnlcomm >= 0.0)
            won_count = ta.get('won', {}).get('total', 0)
            metrics['win_rate'] = round(won_count / total_closed * 100, 2)
            # Profit factor
            gross_profit = ta.get('won', {}).get('pnl', {}).get('total', 0)
            gross_loss = abs(ta.get('lost', {}).get('pnl', {}).get('total', 0))
            metrics['profit_factor'] = (
                round(gross_profit / gross_loss, 2) if gross_loss > 0 else None
            )
            # Average trade PnL
            metrics['avg_trade_pnl'] = round(
                ta.get('pnl', {}).get('net', {}).get('average', 0), 2
            )
        else:
            metrics['win_rate'] = None
            metrics['profit_factor'] = None
    except Exception:
        metrics['num_trades'] = 0
        metrics['win_rate'] = None
        metrics['profit_factor'] = None

    # --- Annual Return ---
    try:
        annual = strat.analyzers.annual.get_analysis()
        if annual:
            avg = sum(annual.values()) / len(annual)
            metrics['avg_annual_return'] = round(avg * 100, 2)
        else:
            metrics['avg_annual_return'] = None
    except Exception:
        metrics['avg_annual_return'] = None

    return metrics
```

**Required analyzers** (add ALL of these to cerebro):
```python
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe',
                    riskfreerate=0.0, annualize=True)
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annual')
```

## Analyzer Gotchas (Verified from Source)

1. **SharpeRatio key**: `'sharperatio'` (one word) — NOT `'sharpe_ratio'` or `'sharpe'`.
   Can return `None` (not `NaN`) when std dev is zero or insufficient data.
2. **SharpeRatio default risk-free rate**: 0.01 (1%) — set `riskfreerate=0.0`
   explicitly if you want 0%.
3. **TradeAnalyzer missing keys**: If zero trades, only `total.total = 0` exists.
   Accessing `ta.won.total` when no winning trades creates a new empty
   `AutoOrderedDict` entry — it's truthy but not a number. Use `.get()` dict access.
4. **TradeAnalyzer won/lost definition**: `won = (pnlcomm >= 0.0)`. A trade with
   exactly zero PnL (after commission) counts as WON, not lost.
5. **DrawDown vs TimeDrawDown**: `DrawDown` uses `max.drawdown`, `max.len`.
   `TimeDrawDown` uses `maxdrawdown`, `maxdrawdownperiod`. Different keys!
6. **AnnualReturn values**: Decimals, not percentages (0.15 means 15%).
7. **AutoOrderedDict after stop()**: `_close()` is called in `stop()` —
   after that, attribute access can't auto-create new keys.
8. **Returns analyzer**: Logarithmic calculation. `rnorm100` is the annualized
   return already multiplied by 100.

## Common Pitfalls

1. **Data alignment**: When using multiple data feeds, Backtrader auto-aligns
   by datetime. Ensure all feeds have overlapping date ranges.
2. **Warmup period**: Indicators need N bars before producing values. Don't
   trade until `len(self) >= max_period`.
3. **Order execution timing**: Orders placed in `next()` at bar N execute at
   bar N+1 by default. Use `cerebro.broker.set_coc(True)` for same-bar close.
4. **Order types**: `self.buy()` creates a Market order. For Limit:
   `self.buy(exectype=bt.Order.Limit, price=p)`. For Stop:
   `self.buy(exectype=bt.Order.Stop, price=p)`. For StopTrail:
   `self.buy(exectype=bt.Order.StopTrail, trailpercent=0.02)`.
5. **Position check**: Always check `self.position` or `self.getposition(data)`
   before placing orders to to avoid doubling up.
6. **yfinance MultiIndex**: Since v0.2.47, `yf.download()` returns MultiIndex
   columns even for a single ticker. Use `multi_level_index=False` or
   `df.droplevel(1, axis=1)` to flatten.
7. **yfinance auto_adjust**: Since v1.0, `auto_adjust=True` is default.
   Not specifying it may trigger a deprecation warning.
8. **Default cash**: Cerebro default starting cash is 10,000 (not 100,000).
   Always call `cerebro.broker.setcash()` explicitly.
