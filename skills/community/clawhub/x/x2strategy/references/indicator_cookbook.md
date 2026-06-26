# Indicator Implementation Cookbook

> Sources: backtrader.com/docu/indautoref/ (verified indicator parameters, aliases,
> output line names). All defaults below are from the actual source code.

Quick reference for translating common technical indicators into Backtrader code.
Used during signal module code generation.

## Built-in Indicators — Verified Params & Lines

### Moving Averages

| Indicator | Code | Default Params | Output Lines | Aliases |
|-----------|------|----------------|-------------|---------|
| SMA | `bt.indicators.SMA(data, period=30)` | period=30 | `sma` | MovingAverageSimple, SimpleMovingAverage |
| EMA | `bt.indicators.EMA(data, period=30)` | period=30 | `ema` | MovingAverageExponential, ExponentialMovingAverage |
| WMA | `bt.indicators.WMA(data, period=30)` | period=30 | `wma` | MovingAverageWeighted, WeightedMovingAverage |
| DEMA | `bt.indicators.DEMA(data, period=30)` | period=30 | `dema` | DoubleExponentialMovingAverage |
| TEMA | `bt.indicators.TEMA(data, period=30)` | period=30 | `tema` | TripleExponentialMovingAverage |
| HMA | `bt.indicators.HullMA(data, period=30)` | period=30 | `hma` | HullMovingAverage |
| KAMA | `bt.indicators.KAMA(data, period=30)` | period=30, fast=2, slow=30 | `kama` | AdaptiveMovingAverage |
| ZLEMA | `bt.indicators.ZeroLagExponentialMovingAverage(data)` | period=30 | `zlema` | ZeroLagEma |
| SMMA | `bt.indicators.SmoothedMovingAverage(data)` | period=30 | `smma` | WilderMA, MovingAverageSmoothed |

**Key MA fact**: ATR and RSI internally use `SmoothedMovingAverage` (Wilder's), not EMA.

### Trend

| Indicator | Code | Params | Lines | Notes |
|-----------|------|--------|-------|-------|
| MACD | `bt.indicators.MACD(data)` | period_me1=12, period_me2=26, period_signal=9 | `macd`, `signal` | MACDHisto adds `histo` line |
| ADX | `bt.indicators.ADX(data, period=14)` | period=14, movav=SmoothedMovingAverage | `adx` | Also: `plus`/`minus` via DirectionalIndicator |
| Ichimoku | `bt.indicators.Ichimoku(data)` | tenkan=9, kijun=26, senkou=52, senkou_lead=26, chikou=26 | `tenkan_sen`, `kijun_sen`, `senkou_span_a`, `senkou_span_b`, `chikou_span` | |

### Momentum

| Indicator | Code | Params | Lines | Notes |
|-----------|------|--------|-------|-------|
| RSI | `bt.indicators.RSI(data, period=14)` | period=14, movav=SmoothedMovingAverage, upperband=70, lowerband=30, safediv=False, safehigh=100.0, safelow=50.0 | `rsi` | Uses SmoothedMovingAverage (**NOT EMA**) |
| RSI_EMA | `bt.indicators.RSI_EMA(data)` | Same but movav=EMA | `rsi` | Variant using EMA |
| RSI_SMA | `bt.indicators.RSI_SMA(data)` | Same but movav=SMA | `rsi` | Cutler's RSI variant |
| Stochastic | `bt.indicators.Stochastic(data)` | period=14, period_dfast=3, movav=SMA, upperband=80, lowerband=20, safediv=False | `percK`, `percD` | %K and %D |
| StochasticFull | `bt.indicators.StochasticFull(data)` | period=14, period_dfast=3, period_dslow=3 | `percK`, `percD`, `percDSlow` | Full stochastic |
| MFI | `bt.indicators.MFI(data, period=14)` | period=14 | `mfi` | MoneyFlowIndicator |
| ROC | `bt.indicators.ROC(data, period=12)` | period=12 | `roc` | RateOfChange100 |
| CCI | `bt.indicators.CCI(data, period=20)` | period=20, factor=0.015, movav=SMA, upperband=100, lowerband=-100 | `cci` | CommodityChannelIndex |
| Williams %R | `bt.indicators.WilliamsR(data)` | period=14, upperband=-20, lowerband=-80 | `percR` | |

### Volatility

| Indicator | Code | Params | Lines | Notes |
|-----------|------|--------|-------|-------|
| ATR | `bt.indicators.ATR(data, period=14)` | period=14, movav=SmoothedMovingAverage | `atr` | AverageTrueRange; uses Wilder MA |
| BollingerBands | `bt.indicators.BollingerBands(data)` | period=20, devfactor=2.0, movav=SMA | `mid`, `top`, `bot` | Alias: BBands |
| StdDev | `bt.indicators.StdDev(data, period=20)` | period=20, movav=SMA, safepow=False | `stddev` | |

### Volume

| Indicator | Code | Params | Lines | Notes |
|-----------|------|--------|-------|-------|
| OBV | `bt.indicators.OBV(data)` | | `obv` | OnBalanceVolume |
| VWAP | *custom* (see below) | | | Not built-in |

### Signal Detection (CrossOver family)

| Indicator | Code | Output | Meaning |
|-----------|------|--------|---------|
| CrossOver | `bt.indicators.CrossOver(fast, slow)` | `crossover` | +1 when fast crosses above slow, -1 when below, 0 otherwise |
| CrossUp | `bt.indicators.CrossUp(fast, slow)` | `crossup` | 1 when fast crosses above slow |
| CrossDown | `bt.indicators.CrossDown(fast, slow)` | `crossdown` | 1 when fast crosses below slow |

## Custom Indicator Patterns

### Z-Score
```python
class ZScore(bt.Indicator):
    lines = ('zscore',)
    params = (('period', 20),)

    def __init__(self):
        mean = bt.indicators.SMA(self.data, period=self.p.period)
        std = bt.indicators.StdDev(self.data, period=self.p.period)
        self.lines.zscore = (self.data - mean) / std
```

### VWAP (not built-in)
```python
class VWAP(bt.Indicator):
    lines = ('vwap',)

    def __init__(self):
        cumvol = bt.indicators.CumSum(self.data.volume)
        cumtp = bt.indicators.CumSum(
            (self.data.high + self.data.low + self.data.close) / 3.0 * self.data.volume
        )
        self.lines.vwap = cumtp / cumvol
```

### Spread / Pair Ratio
```python
class PairSpread(bt.Indicator):
    lines = ('spread', 'zscore')
    params = (('period', 20),)

    def __init__(self):
        self.lines.spread = self.data0.close / self.data1.close
        mean = bt.indicators.SMA(self.lines.spread, period=self.p.period)
        std = bt.indicators.StdDev(self.lines.spread, period=self.p.period)
        self.lines.zscore = (self.lines.spread - mean) / std
```

### Rolling Beta
```python
class RollingBeta(bt.Indicator):
    lines = ('beta',)
    params = (('period', 60),)

    def next(self):
        asset = list(self.data0.close.get(size=self.p.period))
        market = list(self.data1.close.get(size=self.p.period))
        if len(asset) < self.p.period:
            return
        import numpy as np
        ret_a = np.diff(asset) / asset[:-1]
        ret_m = np.diff(market) / market[:-1]
        cov = np.cov(ret_a, ret_m)[0][1]
        var = np.var(ret_m)
        self.lines.beta[0] = cov / var if var > 0 else 0
```

## Signal Generation Patterns

### Crossover (using built-in)
```python
self.cross = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)

def next(self):
    if self.cross[0] > 0:   # fast crossed above slow
        self.buy()
    elif self.cross[0] < 0: # fast crossed below slow
        self.sell()
```

### Threshold Breakout
```python
def next(self):
    if self.rsi[0] < 30 and not self.position:
        self.buy()
    elif self.rsi[0] > 70 and self.position:
        self.sell()
```

### Multi-Factor Composite
```python
def __init__(self):
    self.momentum = bt.indicators.ROC(self.data.close, period=12)
    self.value = -bt.indicators.StdDev(self.data.close, period=20)
    self.quality = bt.indicators.RSI(self.data.close, period=14) - 50

def next(self):
    score = 0.4 * self.momentum[0] + 0.3 * self.value[0] + 0.3 * self.quality[0]
    if score > self.p.threshold:
        self.buy()
```

## Indicator Gotchas (From Source Code)

1. **RSI default MA**: `SmoothedMovingAverage` (Wilder's smoothing), NOT EMA.
   Use `RSI_EMA` if you need EMA-based RSI. Use `RSI_SMA` for Cutler's RSI.
2. **SMA/EMA default period**: 30 (not 20). Always set period explicitly.
3. **BollingerBands lines**: `.top`, `.mid`, `.bot` — NOT `.upper`, `.lower`.
4. **MACD lines**: `.macd`, `.signal` — add `MACDHisto` for `.histo` line.
5. **Stochastic lines**: `.percK`, `.percD` — NOT `.k`, `.d`.
6. **ATR smoothing**: Uses Wilder/SmoothedMovingAverage by default, not SMA.
7. **CCI factor**: Default is 0.015 (Lambert's constant).
8. **CrossOver returns**: +1, -1, or 0 — NOT boolean True/False.
