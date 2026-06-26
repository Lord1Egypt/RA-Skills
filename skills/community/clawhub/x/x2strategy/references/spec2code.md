# Spec2Code — Agent-Driven Strategy Code Generation

> Metrics extraction patterns verified against backtrader source code.
> See [backtrader_patterns.md](backtrader_patterns.md) for full analyzer return structures.

Convert structured strategy specifications into executable Backtrader code.
The agent generates code, runs it directly, and analyzes the output.

## Philosophy

The agent IS the LLM. It does not need prompt templates, executor wrappers,
or analysis modules — it generates code by reading the spec, runs it in the
terminal, and reasons about the results natively. The `spec2code/` package
provides only tools the agent cannot do itself:

- **`validator.py`** — AST parsing + structural checks (agent can't parse AST)
- **`models.py`** — Serializable data structures for structured output
- **`config.py`** — Environment variable management

## Agent Workflow

### Phase 1: Read the Spec

Load `spec.json` from the paper's library directory. Each strategy has:

```json
{
  "strategy_name": "Minimum Distance Pairs Trading",
  "strategy_type": "technical",
  "asset_class": ["equity"],
  "indicators": [...],
  "logic_pipeline": [...],
  "execution_plan": [...],
  "risk_management": [...],
  "expected_performance": {"sharpe": 1.8, "annual_return": 0.15}
}
```

**Key fields to understand before generating code:**

#### Indicators → `__init__()`
Each indicator has: `name`, `formula`, `inputs`, `parameters`, `scope`.

Mapping examples:
```
Spec: {"name": "SMA_20", "formula": "SMA(close, 20)", "parameters": {"period": 20}}
Code: self.sma20 = bt.indicators.SMA(self.data.close, period=20)

Spec: {"name": "RSI_14", "formula": "RSI(close, 14)", "parameters": {"period": 14}}
Code: self.rsi = bt.indicators.RSI(self.data.close, period=14)

Spec: {"name": "spread_zscore", "formula": "(spread - mean(spread, N)) / std(spread, N)"}
Code: Custom indicator class or inline computation
```

Common spec indicator categories and their Backtrader mappings:
- **Moving averages** (SMA, EMA, WMA) → `bt.indicators.SMA/EMA/WMA`
- **Momentum** (RSI, MACD, ROC) → `bt.indicators.RSI/MACD/ROC`
- **Volatility** (ATR, Bollinger) → `bt.indicators.ATR/BollingerBands`
- **Custom/composite** → Define as `bt.Indicator` subclass or compute in `next()`
- **Cross-sectional** (ranks, z-scores) → Compute across data feeds in `next()`

#### Logic Pipeline → `next()`
Each step has: `function`, `description`, `expression`, `inputs`, `output`.

Example:
```
Spec: {"function": "compare_sma", "expression": "close > SMA_200", "output": "trend_filter"}
Code: if self.data.close[0] > self.sma200[0]:  # trend_filter
```

#### Execution Plan → Order Logic
Each plan entry has: `trigger`, `action`, `position_sizing`.
Map trigger → entry/exit conditions, action → `self.buy()`/`self.sell()`,
sizing → `self.broker.getvalue()` calculations.

### Phase 2: Generate Code

Generate a **single self-contained Python file** (`strategy.py`) that includes:

1. **Imports** — `backtrader as bt`, `yfinance`, `datetime`, `json`
2. **Data loading** — Download OHLCV data via yfinance/akshare
3. **Strategy class** — `class MyStrategy(bt.Strategy)` with `__init__` and `next`
4. **Cerebro setup** — Broker config, analyzers, initial cash
5. **Metrics output** — Print key metrics as JSON to stdout
6. **`if __name__ == "__main__"` guard**

Read [backtrader_patterns.md](backtrader_patterns.md) for canonical patterns.
Read [indicator_cookbook.md](indicator_cookbook.md) for indicator implementations.
Read [data_sources.md](data_sources.md) for data API usage.

#### Strategy File Template Structure

```python
import backtrader as bt
import yfinance as yf
import json
import datetime

class MyStrategy(bt.Strategy):
    params = (...)

    def __init__(self):
        # Map spec indicators to bt.indicators
        ...

    def next(self):
        # Map spec logic_pipeline to trading decisions
        ...

def run_backtest():
    cerebro = bt.Cerebro()

    # Load data
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)

    # Configure
    cerebro.broker.setcash(100000)
    cerebro.addstrategy(MyStrategy)

    # Add standard analyzers for metrics
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe',
                        riskfreerate=0.01)  # default is 0.01, explicit
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annual')

    results = cerebro.run()
    strat = results[0]

    # Extract metrics using .get() dict access — verified against source code.
    # Analyzer.get_analysis() returns AutoOrderedDict; use .get() to avoid
    # KeyError on no-trade runs. See backtrader_patterns.md for full details.
    initial_cash = 100000
    final_value = cerebro.broker.getvalue()
    trades = strat.analyzers.trades.get_analysis()
    sharpe = strat.analyzers.sharpe.get_analysis()
    dd = strat.analyzers.drawdown.get_analysis()
    ret = strat.analyzers.returns.get_analysis()

    metrics = {
        'final_value': round(final_value, 2),
        'total_return': round((final_value / initial_cash - 1) * 100, 2),
        'sharpe_ratio': round(sharpe.get('sharperatio'), 4)
                        if sharpe.get('sharperatio') is not None else None,
        'max_drawdown_pct': round(dd.get('max', {}).get('drawdown', 0), 2),
        'num_trades': trades.get('total', {}).get('closed', 0),
        'won_trades': trades.get('won', {}).get('total', 0),
        'lost_trades': trades.get('lost', {}).get('total', 0),
        'normalized_annual_return': round(
            ret.get('rnorm100', 0), 2),  # rnorm × 100
        'sqn': round(strat.analyzers.sqn.get_analysis().get('sqn', 0), 4),
    }

    print(json.dumps(metrics, indent=2))

if __name__ == '__main__':
    run_backtest()
```

### Phase 3: Validate

Before running, validate the code:

```bash
uv run python scripts/validate_strategy.py library/<paper>/strategy_1.py
```

This checks:
- AST syntax (parses without error)
- `import backtrader` present
- `bt.Strategy` subclass defined
- `cerebro` runner exists
- `if __name__` guard present
- **Indicator existence** — all `bt.indicators.X` / `bt.ind.X` references
  are verified against the installed backtrader version

If validation fails:
- **Errors** (syntax, invalid indicators): must fix before running
- **Warnings** (missing structure): review but may be acceptable

Fix the errors and re-validate. Do not proceed to Phase 4 with errors.

### Phase 4: Run Directly

Run the strategy file directly in the terminal:

```bash
cd library/<paper>/
uv run python strategy_1.py
```

Read stdout for metrics JSON. Read stderr for errors.

**Important**: The strategy file should be self-contained — it fetches its
own data, runs the backtest, and prints results. No external executor needed.

If the strategy requires backtrader/yfinance that aren't in the skill's
main venv, create a dedicated venv in the library subdirectory:

```bash
cd library/<paper>/
uv venv && uv pip install backtrader yfinance akshare
uv run python strategy_1.py
```

### Phase 5: Diagnose

Compare the backtest output against the spec's `expected_performance`:

1. Read the metrics from stdout (JSON)
2. Read `expected_performance` from spec.json (sharpe, annual_return, max_drawdown)
3. Compare and report deviations

**Deviation thresholds** (guidelines, not hard rules):
- Sharpe ratio: >20% deviation → investigate signal logic
- Annual return: >20% deviation → check data source and time period
- Max drawdown: >10pp absolute difference → check risk management
- Zero trades → strategy logic is likely broken

**Common causes of deviation:**
- Different data source (paper used Bloomberg, we use yfinance)
- Different time period
- Transaction costs / slippage not modeled
- Survivorship bias in paper's data

If diagnosis reveals issues, iterate: read the spec again, identify the
mismatch, regenerate the problematic section of code, re-validate, re-run.

### Phase 5.5: Debug Runtime Errors

When the strategy crashes or produces unexpected output, follow this triage flow:

**Step 1 — Classify the error from stderr:**

| Error Pattern | Category | Typical Fix |
|--------------|----------|-------------|
| `ModuleNotFoundError: No module named 'xxx'` | Missing dependency | `uv pip install xxx` in strategy venv |
| `HTTPError` / `ConnectionError` / `No data found` | Data fetch failure | Check ticker symbol, date range, yfinance vs akshare |
| `IndexError: array assignment index is out of range` | Indicator warmup | Add `if len(self) < self.p.period: return` at top of `next()` |
| `ValueError: ...` in indicator init | Bad parameters | Cross-check indicator params with [indicator_cookbook.md](indicator_cookbook.md) |
| Strategy runs but `num_trades: 0` | Dead logic | Entry conditions too strict, or data period doesn't contain signals |
| `bt.indicators.XXX` does not exist | Invalid indicator | Use validator's indicator check; see [indicator_cookbook.md](indicator_cookbook.md) for valid names |
| `KeyError` in analyzer | Missing analyzer | Ensure all 6 standard analyzers are added (see Phase 2 template) |

**Step 2 — Fix and retry loop:**

1. Read the full stderr output
2. Identify the error category from the table above
3. Apply the targeted fix (do NOT rewrite the entire file)
4. Re-validate (`scripts/validate_strategy.py`)
5. Re-run the strategy
6. If error persists after 3 attempts, re-read the spec and consider whether
   the strategy logic needs a fundamentally different approach

**Step 3 — Zero-trade debugging:**

Zero trades is the most common "silent failure". Debug checklist:
- Print `self.data.close[0]` and indicator values in `next()` to verify data flow
- Check if conditions use `[0]` indexing (current bar) not `[-1]` (previous)
- Verify the data period overlaps with the strategy's intended market regime
- Check `cerebro.broker.getvalue()` vs `setcash()` — if equal, no trades executed

### Phase 6: Present Results to User

After a successful backtest, present results in this format:

**1. Summary table** (always include):

```
策略: {strategy_name}
数据: {ticker} ({start_date} → {end_date})
初始资金: {initial_cash:,}

| 指标 | 回测结果 | 论文预期 | 偏差 |
|------|---------|---------|------|
| 总收益率 | {total_return}% | {expected_return}% | {dev}% |
| 年化收益 | {annual}% | {exp_annual}% | {dev}% |
| 夏普比率 | {sharpe} | {exp_sharpe} | {dev} |
| 最大回撤 | {max_dd}% | {exp_dd}% | {dev}pp |
| 总交易数 | {num_trades} | — | — |
| 胜率 | {win_rate}% | — | — |
| SQN | {sqn} | — | — |

最终资产: {final_value:,}
```

**2. Match assessment** (always include):
- State whether results are **匹配** (within thresholds), **部分匹配**, or **不匹配**
- For deviations, explain likely causes (data source, time period, costs)

**3. Generated files** (list paths):
- `strategy_1.py` — self-contained strategy code
- `spec.json` — strategy specification
- Key metrics as JSON (already printed to stdout)

**4. Optional — if user requests:**
- Plot: `cerebro.plot()` generates a chart. Note this requires matplotlib and
  a display environment. For headless servers, save to file:
  `cerebro.plot(style='bar')[0][0].savefig('backtest_plot.png')`
- Detailed trade log: Add `bt.observers.Trades` or iterate `strat.analyzers.trades`
- Equity curve: Extract from `bt.observers.Broker` or compute from daily returns

## Output Structure

```
library/<paper>/
├── spec.json              # From paper2spec
├── strategy_1.py          # Generated code (self-contained)
└── metadata.json
```

## Validation Tool

The validator runs AST-level checks that the agent cannot do natively.
Use it via CLI before executing any generated strategy:

```bash
uv run python scripts/validate_strategy.py <strategy.py>
```

Checks performed:
1. **Syntax** — `ast.parse()` succeeds
2. **Backtrader import** — `import backtrader` or `import backtrader as bt`
3. **Strategy class** — At least one `bt.Strategy` subclass defined
4. **Cerebro runner** — `bt.Cerebro()` instantiation present
5. **Main guard** — `if __name__` block exists
6. **Indicator existence** — All `bt.indicators.X` / `bt.ind.X` / `btind.X` references
   are checked against `inspect.getmembers(bt.indicators)`. Non-existent indicators
   (e.g. `bt.indicators.DEMA` when you mean `bt.indicators.DoubleExponentialMovingAverage`)
   produce hard errors with a sample of valid indicator names. Only runs when
   backtrader is installed (`codegen` extra).

### Data Models (`spec2code.models`)

- **`CodeModules`** — Container for data/signal/backtest code strings
- **`ValidationResult`** — valid + errors + warnings
- **`BacktestMetrics`** — total_return, annual_return, sharpe_ratio, max_drawdown, etc.
- **`BacktestResult`** — status + metrics + stdout/stderr
- **`DiagnosisReport`** — match_status + expected/actual + deviations + recommendations

All models have `to_dict()`, `from_dict()`, `to_json()` for serialization.

## Configuration

| Env Variable | Default | Description |
|-------------|---------|-------------|
| `SPEC2CODE_BACKTEST_TIMEOUT` | `300` | Timeout guidance for agent (not enforced by code) |
| `SPEC2CODE_DATA_CACHE` | `<library>/data_cache` | Suggested cache dir for downloaded data |

These supplement the shared paper2spec config (LLM model, API keys, etc.).
