# Python API Quick Reference

## Setup

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
```

## Data layer

```python
from data_engine import get_stock_pool, get_kline, get_fundamentals
from data_engine import get_fund_pool, get_fund_nav

pool = get_stock_pool("A")
kline = get_kline("600519", "A", days=365)
fund = get_fundamentals("600519", "A")
nav = get_fund_nav("510300", days=365)
```

## Analysis

```python
from factors.composite import CompositeAnalyzer
result = CompositeAnalyzer("600519", "A").analyze()
# total_score (0-100), factors dict, f_score (0-9)

from strategies.aggregator import StrategyAggregator
signals = StrategyAggregator("600519", "A").analyze_all()
# final_signal, final_score, confidence, signals list

from advisor.diagnosis import StockDiagnosis
report = StockDiagnosis("600519", "A").full_report()
# full diagnosis dict with all sections

from advisor.scanner import MarketScanner
scanner = MarketScanner()
results = scanner.scan_top("A", top_n=20)
```

## Portfolio and backtest

```python
from portfolio.builder import PortfolioBuilder
from portfolio.backtest_engine import AlphaMomentumBacktest

builder = PortfolioBuilder("My Portfolio", capital=1_000_000)
builder.add_from_strategy("600519", "A")
portfolio = builder.build()

engine = AlphaMomentumBacktest(capital=1_000_000, low_vol_min=0.4)
result = engine.run()
```

## Cache management

```python
from cache import get_cache
cache = get_cache()
removed = cache.cleanup(max_age_days=30, max_size_mb=500)
# Returns {"daily_price": N, "sentiment": N, "factor_snapshot": N}
```

## Code structure

```
scripts/
├── config.py              # Pure-Python config with dot-path access
├── cache.py               # SQLite cache manager with TTL, cleanup
├── data_engine.py         # Data engine with AKShare + fallbacks
├── models.py              # Data classes (StockInfo, KlineData, etc.)
├── utils.py               # Code normalization, market detection
├── run.py                 # CLI entry point
├── backtest_enhanced.py   # Enhanced core-satellite backtest
├── factors/               # 7-factor analysis modules
├── strategies/            # 6 quantitative strategies
├── portfolio/             # Portfolio management (builder, allocator, risk)
├── sentiment/             # Market sentiment aggregation
├── advisor/               # Smart advisory (diagnosis, scanner)
└── tools/                 # Utilities
```
