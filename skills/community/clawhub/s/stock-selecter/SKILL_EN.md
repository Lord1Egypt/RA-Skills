# stock-selecter · A-Share Stock Screening System v3.3

## Overview

**stock-selecter** is a unified A-share stock screening package integrating 14 investment-grade strategies across fundamentals, technical analysis, and market microstructure. It supports single-strategy screening, multi-strategy combination (AND / OR / SCORE), concurrent execution, and HTML visualization reports.

---

## Available Strategies (14 Total)

### Fundamental Strategies (6)

| Strategy | Name | Core Criteria | Score Dimensions |
|----------|------|---------------|-----------------|
| `roe` | ROE Profitability | ROE ≥ 15%, ROA ≥ 5% | ROE/ROA/gross margin/net margin/debt ratio/ROE trend |
| `dividend` | High Dividend | Div yield ≥ 3%, 3+ consecutive years, ROE ≥ 8% | Div yield/ROE/consecutive years/valuation/payout ratio |
| `valuation` | Low Valuation | PE ≤ 25, PB ≤ 3, PEG ≤ 1.5, ROE ≥ 8% | PE/PB/PEG/ROE/industry discount/PB historical percentile |
| `growth` | Fisher Growth Stock | Rev + profit growth ≥ 20% each, gross margin ≥ 30% | Revenue growth/profit growth/gross margin/ROE |
| `cashflow_quality` | Cash Flow Quality | Operating CF ≥ Net profit for 3+ quarters, goodwill < 30% | Quarters matched/CF ratio/ROE |
| `analyst_target` | Analyst Target Price | Implied target upside ≥ 20% + 2+ consecutive forecasts | Upside/forecast periods/ROE |

### Technical Strategies (5)

| Strategy | Name | Core Criteria | Score Dimensions |
|----------|------|---------------|-----------------|
| `macd` | MACD Bottom Divergence | Price downtrend + MACD uptrend + divergence confirmed + volume surge ≥ 1.5x | K-line slope/MACD slope/volume surge ratio/RSI |
| `trend` | Trend Analysis | MA bullish alignment (MA5 > MA20 > MA60), R² ≥ 0.5, ADX ≥ 25 | Trend slope/R²/ADX/RSI/volatility/MA alignment |
| `pattern` | Candlestick Patterns | At least 1 pattern matched | Double bottom / head & shoulders / flag breakout / golden cross / morning star / bullish engulfing / cup & handle |
| `bollinger` | Bollinger Band Lower Band | Price touches lower band + RSI oversold | Touch depth/RSI/distance to lower band |
| `volume_surge` | Recent Volume Surge | Volume surge ≥ 2x + RSI ≤ 45 + rebound ≥ 3% | Volume surge ratio/RSI/rebound magnitude/consecutive surge days |

### Microstructure Strategy (3)

| Strategy | Name | Core Criteria | Score Dimensions |
|----------|------|---------------|-----------------|
| `shareholder_concentration` | Shareholder Concentration | Shareholder count declining for 3+ consecutive quarters + ROE ≥ 8% | Cumulative decline magnitude/duration/ROE |
| `northbound_flow` | Northbound Flow | Northbound continuous net buy 5+ days + total ≥ 500M CNY | Consecutive days/total net amount/ROE |
| `shareholder_buyback` | Shareholder Buyback | Buyback ratio ≥ 0.5% + ROE ≥ 8% | Buyback ratio/periods/ROE |

### Special

| Strategy | Name | Core Criteria | Score Dimensions |
|----------|------|---------------|-----------------|
| `low_position` | Long-term Low Position | Price percentile ≤ 25% (250-day) + RSI ≤ 40 | Price percentile/RSI/days from low |

---

## Scoring System

All strategies return a unified **0–100 score** (higher = better quality). Multi-strategy combinations aggregate scores as follows:

- **AND mode**: Intersection — stock must pass all strategies. Scored by sum of individual strategy scores.
- **OR mode**: Union — stock passes if it meets any one strategy. Ranked by (number of strategies hit, total score).
- **SCORE mode**: All strategies scored. Ranked by total score across all strategies (most inclusive).

Reference benchmarks: ROE full score ≥ 25%, gross margin ≥ 40–60%, ADX full score ≥ 50, volume surge full score ≥ 3x.

---

## Command Line Usage

```bash
# Single strategy (default AND)
python main.py --strategy roe --roe_threshold 15

# Multi-strategy intersection (strictest)
python main.py --strategy roe,macd,dividend --mode and

# Multi-strategy union (loosest)
python main.py --strategy roe,macd --mode or --top 50

# All strategies综合评分
python main.py --strategy all --mode score --top 50

# Concurrent execution (8 threads, suitable for technical strategies)
python main.py --strategy macd,trend,volume_surge --workers 8

# Generate HTML report
python main.py --strategy roe,macd,dividend --report --output_dir ~/Desktop

# Debug (first 20 stocks only)
python main.py --strategy roe,trend --limit 20 --verbose
```

---

## Python API

```python
from main import execute

# Basic
result = execute({"strategy": "roe", "roe_threshold": 15})

# Multi-strategy AND intersection
result = execute({
    "strategy": "roe,macd,valuation",
    "mode": "and",
    "roe_threshold": 15,
    "max_pe": 20,
})

# All strategies综合评分 + concurrent + HTML
result = execute({
    "strategy": "all",
    "mode": "score",
    "top_n": 50,
    "workers": 8,
    "report": True,
})

# Namespaced strategy-specific parameters
result = execute({
    "strategy": "roe,valuation",
    "roe.roe_threshold": 20,
    "valuation.max_pe": 15,
})
```

---

## Return Format

```python
{
  "success": True,
  "results": [
    {
      "ts_code": "000001.SZ",
      "name": "Ping An Bank",
      "industry": "Banking",
      "score": 78.5,
      "strategies_hit": ["roe", "valuation"],
      "scores": {"roe": 45.2, "valuation": 33.3},
      "roe": 16.5, "roa": 8.2, "gross_margin": 35.1,
      "pe_ttm": 12.3, "pb": 1.1, "peg": 0.74,
    },
    ...
  ],
  "count": 42,
  "message": "[stock-selecter] AND mode, elapsed 89.3s",
  "metadata": {
    "strategies_used": ["roe", "valuation"],
    "mode": "and",
    "execution_time": 89.3,
    "per_strategy_counts": {"roe": 312, "valuation": 185},
    "saved_files": {
      "json": "/path/to/...",
      "csv":  "/path/to/...",
      "html": "/path/to/...",
    }
  }
}
```

---

## Parameters

### Common Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `strategy` | `roe` | Strategy name(s), comma-separated, `all` = all 11 |
| `mode` | `and` | `and` (intersection) / `or` (union) / `score` (ranking) |
| `top_n` | `0` | Result cap (0 = unlimited) |
| `workers` | `1` | Thread count (>1 enables concurrency) |
| `report` | `False` | Generate HTML report |
| `save` | `True` | Save JSON/CSV files |
| `output_dir` | `auto` | Output directory |

### Strategy-Specific Parameters

**ROE**: `roe_threshold`, `roa_threshold`, `include_roa`, `min_report_periods`

**MACD**: `k_slope_max`, `k_r2_min`, `macd_slope_min`, `macd_r2_min`, `require_divergence`, `require_volume_surge`, `volume_surge_weeks`, `volume_surge_threshold`

**Dividend**: `min_dv_ratio`, `min_consecutive_years`, `min_roe`, `max_pe`

**Valuation**: `max_pe`, `max_pb`, `max_peg`, `industry_discount`, `min_roe`

**Growth**: `min_revenue_growth`, `min_profit_growth`, `min_gross_margin`, `min_consecutive_quarters`, `min_roe`

**Low Position**: `lookback_days`, `low_position_pct`, `rsi_max`, `rsi_window`, `data_period_years`

**Volume Surge**: `volume_surge_ratio`, `volume_avg_days`, `rsi_max`, `rebound_pct_min`, `rebound_days`, `price_change_max`, `data_period_years`

**Trend**: `ma_short`, `ma_mid`, `ma_long`, `trend_r2_min`, `adx_min`, `require_ma_bullish`

**Pattern**: `detect_double_bottom`, `detect_head_shoulders_bottom`, `detect_flag_breakout`, `detect_golden_cross`, `detect_morning_star`, `detect_bullish_engulfing`, `detect_cup_handle`, `min_pattern_score`

**Bollinger**: `bb_window`, `bb_std`, `rsi_max`, `rsi_window`, `lookback_days`, `price_change_max`

**Shareholder Concentration**: `min_consecutive_quarters`, `max_holder_growth`, `min_roe`, `data_period_quarters`

**Cashflow Quality**: `min_match_quarters`, `total_periods`, `min_cashflow_ratio`, `min_roe`, `max_goodwill_pct`

**Northbound Flow**: `min_consecutive_days`, `min_daily_net`, `min_total_net`, `lookback_days`, `north_type`

**Shareholder Buyback**: `min_buyback_ratio`, `min_consecutive_periods`, `lookback_days`, `holder_type`, `min_roe`

**Analyst Target**: `min_target_upside`, `min_consecutive_forecasts`, `forecast_years`, `min_roe`

---

## Output Files

Auto-saved to configured output directory:
- `screener_{strategy}_{timestamp}.json` — Full raw data
- `screener_{strategy}_{timestamp}.csv` — Tabular format
- `screener_report_{timestamp}.html` — Interactive visualization (requires `--report`)

---

## Concurrency Guide

- `workers=1` (default): Serial execution, stable and reliable
- `workers>1`: ThreadPoolExecutor concurrency, **ideal for IO-bound** strategies (heavy API call waiting)
- Recommended concurrency settings:
  - Technical strategies (MACD / trend / volume surge / Bollinger / northbound_flow): `--workers 8`
  - Fundamental strategies (ROE / dividend / valuation / growth / analyst_target): `workers=1` (data volume is small)
- Max recommended concurrency: 16 (to avoid API rate limiting)

---

## Directory Structure

```
stock-selecter/
├── main.py
├── SKILL.md / SKILL_EN.md
├── config.json           # Tushare Token configuration
├── requirements.txt
├── README.md
├── stock_utils.py        # Shared utilities + API calls
├── stock_indicators.py   # Technical indicator calculations
├── strategies/
│   ├── base.py           # Abstract base class + concurrency engine
│   ├── roe.py
│   ├── macd.py
│   ├── dividend.py
│   ├── valuation.py
│   ├── growth.py
│   ├── low_position.py
│   ├── volume_surge.py
│   ├── trend.py
│   ├── pattern.py
│   ├── bollinger.py
│   ├── shareholder_concentration.py
│   ├── cashflow_quality.py
│   ├── northbound_flow.py
│   ├── shareholder_buyback.py
│   └── analyst_target.py
└── utils/
    ├── loader.py         # Standalone shared library loader
    └── report.py         # HTML report generator
```

---

## Data Source

- Market data powered by **Tushare Pro** (https://tushare.pro/register)
- Free registration required — obtain your personal token and fill in `config.json`
- Covers all A-share stocks (Shanghai + Shenzhen exchanges)

---

## Requirements

```
tushare>=1.4.0
pandas
numpy
requests
```
