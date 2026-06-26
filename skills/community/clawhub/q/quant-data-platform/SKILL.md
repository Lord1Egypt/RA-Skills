---
name: quant-data-platform
description: Comprehensive quantitative data platform for A-share market. Real-time quotes, historical data, alternative data (sentiment, news, fundamentals), factor data, and data quality monitoring. Essential infrastructure for quantitative trading.
tags:
  - quant
  - data
  - trading
  - a-share
  - realtime
  - alternative-data
version: 1.0.0
author: chenq
---

# Quant Data Platform

Comprehensive data infrastructure for quantitative trading in Chinese A-share market.

## Features

### 1. Real-time Data
- **Live Quotes**: Real-time stock prices, volumes
- **Tick Data**: Level 1 tick-by-tick data
- **Order Book**: Real-time bid/ask data
- **Index Data**: Real-time index values

### 2. Historical Data
- **Daily K-line**: OHLCV data since IPO
- **Minute Data**: 1/5/15/30/60 minute bars
- **Tick History**: Historical tick data
- **Adjustment**: Forward/backward adjustment for dividends

### 3. Alternative Data
- **Sentiment**: Social media, forum sentiment
- **News**: Financial news, announcements
- **Fundamentals**: Financial statements, ratios
- **Insider Trading**: Directors' dealings
- **Short Interest**: Margin trading data

### 4. Factor Data
- **Technical Factors**: 100+ technical indicators
- **Fundamental Factors**: Financial metrics
- **Alternative Factors**: Sentiment, attention
- **Custom Factors**: User-defined factors

### 5. Data Quality
- **Completeness Check**: Missing data detection
- **Accuracy Check**: Outlier detection
- **Timeliness Check**: Delay monitoring
- **Consistency Check**: Cross-source validation

## Installation

```bash
pip install tushare akshare pandas numpy
```

## Configuration

```python
# Set Tushare token
export TUSHARE_TOKEN=your_token_here

# Or in code
from quant_data import DataPlatform
platform = DataPlatform(tushare_token='your_token')
```

## Usage

### Real-time Data

```python
from quant_data import DataPlatform

platform = DataPlatform()

# Get real-time quotes
quotes = platform.get_realtime_quotes(['600519', '000858'])
print(quotes)
#   code    price   change  volume    amount
# 600519  1850.00   +12.50  125000  231250000
# 000858   156.32    +2.18   89000   13912320

# Get tick data
ticks = platform.get_tick_data('600519', date='2026-03-22')

# Get order book
book = platform.get_order_book('600519')
```

### Historical Data

```python
# Get daily K-line
daily = platform.get_daily(
    codes=['600519', '000858'],
    start='2020-01-01',
    end='2026-03-22'
)

# Get minute data
minute = platform.get_minute(
    code='600519',
    freq='5min',
    start='2026-03-01',
    end='2026-03-22'
)

# Get adjusted data
adj = platform.get_daily_adj(code='600519', adjust='qfq')
```

### Alternative Data

```python
# Get sentiment data
sentiment = platform.get_sentiment('600519', days=30)

# Get news
news = platform.get_news('600519', limit=50)

# Get fundamentals
fundamentals = platform.get_fundamentals('600519', years=5)

# Get short interest
short = platform.get_short_interest('600519')
```

### Factor Data

```python
# Get pre-computed factors
factors = platform.get_factors(
    codes=['600519', '000858'],
    factor_list=['pe', 'pb', 'roe', 'momentum_20d', 'volatility_20d']
)

# Calculate custom factors
custom = platform.calculate_factors(
    code='600519',
    factor_config={
        'name': 'my_momentum',
        'formula': 'close / close.shift(20) - 1',
        'params': {}
    }
)
```

### Data Quality

```python
# Check data quality
quality = platform.check_quality('600519', date_range='2026-03')
print(quality)
# {
#   'completeness': 0.98,
#   'accuracy': 0.99,
#   'timeliness': 0.95,
#   'overall': 0.97
# }

# Get data gaps
gaps = platform.find_gaps('600519', start='2026-01-01')

# Validate data
valid = platform.validate('600519', date='2026-03-22')
```

## API Reference

### Real-time
| Method | Description |
|--------|-------------|
| `get_realtime_quotes(codes)` | Get real-time quotes |
| `get_tick_data(code, date)` | Get tick data |
| `get_order_book(code)` | Get order book |
| `subscribe(codes, callback)` | Subscribe to updates |

### Historical
| Method | Description |
|--------|-------------|
| `get_daily(codes, start, end)` | Get daily K-line |
| `get_minute(code, freq, start, end)` | Get minute data |
| `get_daily_adj(code, adjust)` | Get adjusted data |
| `get_trading_dates(start, end)` | Get trading dates |

### Alternative
| Method | Description |
|--------|-------------|
| `get_sentiment(code, days)` | Get sentiment data |
| `get_news(code, limit)` | Get news |
| `get_fundamentals(code, years)` | Get fundamentals |
| `get_short_interest(code)` | Get short interest |

### Factors
| Method | Description |
|--------|-------------|
| `get_factors(codes, factor_list)` | Get factor values |
| `calculate_factors(code, config)` | Calculate custom factors |
| `list_factors()` | List available factors |
| `get_factor_metadata(name)` | Get factor info |

### Quality
| Method | Description |
|--------|-------------|
| `check_quality(code, date_range)` | Check data quality |
| `find_gaps(code, start)` | Find missing data |
| `validate(code, date)` | Validate data point |

## Data Sources

| Type | Source | Update Frequency |
|------|--------|------------------|
| Quotes | Tushare, Akshare | Real-time |
| Fundamentals | Tushare | Daily |
| News | Tushare, Eastmoney | Real-time |
| Sentiment | Custom | Hourly |
| Alternative | Multiple | Varies |

## Caching Strategy

```python
# Configure caching
platform = DataPlatform(
    cache_dir='~/.quant_data/cache',
    cache_expire={
        'daily': '1d',
        'minute': '1h',
        'realtime': '0',
        'fundamentals': '1d'
    }
)
```

## Rate Limiting

| Source | Rate Limit | Strategy |
|--------|------------|----------|
| Tushare | 200/min | Token bucket |
| Akshare | 100/min | Token bucket |
| Custom | Unlimited | N/A |

## Data Schema

### Daily K-line
```
code: str           # Stock code
trade_date: date    # Trading date
open: float         # Open price
high: float         # High price
low: float          # Low price
close: float        # Close price
volume: int         # Volume
amount: float       # Amount
turnover: float     # Turnover rate
```

### Factor Data
```
code: str           # Stock code
trade_date: date    # Trading date
factor_name: str    # Factor name
factor_value: float # Factor value
```

## Use Cases

- **Backtesting**: Historical data for strategy testing
- **Live Trading**: Real-time data for execution
- **Research**: Alternative data for alpha discovery
- **Risk Management**: Quality monitoring for data integrity

## Best Practices

1. **Cache Aggressively**: Reduce API calls
2. **Monitor Quality**: Check data before use
3. **Handle Missing**: Have fallback strategies
4. **Stay Updated**: Sync latest data regularly

## Future Capabilities

- Level 2 data support
- Options/futures data
- Cross-market data (HK, US)
- Real-time streaming API
