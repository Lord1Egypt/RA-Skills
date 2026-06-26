# yfinance Skill

## Overview

The yfinance skill provides a convenient client for querying US and Hong Kong stock data using Yahoo Finance. It wraps the `yfinance` library to offer a simplified interface for retrieving financial data, market information, and analyst insights.

## Features

### Supported Markets
- **US Stocks**: Symbols like AAPL, MSFT, GOOGL, etc.
- **Hong Kong Stocks**: Symbols like 0700.HK (Tencent), 9988.HK (Alibaba), etc. Can use either 4-digit (0700) or full format (0700.HK)

### Data Types

| Category | Methods |
|----------|---------|
| **Price & History** | `get_price`, `get_history`, `get_fast_info` |
| **Company Info** | `get_company_info`, `get_company_summary`, `get_major_holders` |
| **Financials** | `get_financials`, `get_balance_sheet`, `get_cashflow`, `get_earnings` |
| **Analyst Data** | `get_recommendations`, `get_analyst_price_targets`, `get_earnings_estimate` |
| **Insider & News** | `get_insider_transactions`, `get_news` |
| **Dividends & Splits** | `get_dividends`, `get_splits`, `get_actions` |
| **Sector & Industry** | `get_sector`, `get_industry` |
| **Screener** | `get_screener` (predefined queries like day_gainers, most_actives) |
| **Options** | `get_options`, `get_option_chain` |
| **Search** | `search` |

## Usage

### Installation

```bash
pip install yfinance pandas
```

### Basic Usage

```python
from yfinance_skill import YFinanceClient

# Create client
client = YFinanceClient()

# Get stock price
price = client.get_price("AAPL")
print(f"AAPL price: ${price}")

# Get historical data
history = client.get_history("AAPL", period="1mo")
print(history.tail())

# Get company info
info = client.get_company_info("AAPL")
print(f"Industry: {info.get('industry')}")
print(f"Sector: {info.get('sector')}")

# Get recommendations
recs = client.get_recommendations("MSFT")
print(recs)

# Get day gainers
gainers = client.get_screener("day_gainers")
print(gainers.head())

# Hong Kong stocks
hk_price = client.get_price("0700.HK")  # Tencent
hk_info = client.get_company_info("0700")
```

### Key Methods

#### get_price(symbol)
Returns the current stock price as a float.

#### get_history(symbol, period="1mo", interval="1d", start=None, end=None)
Returns historical OHLCV data.

- `period`: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
- `interval`: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 1wk, 1mo

#### get_company_info(symbol)
Returns a dictionary with comprehensive company information including:
- Company name, industry, sector
- Market cap, PE ratio, dividend yield
- 52-week high/low, 50-day average
- Analyst ratings, target price
- And many more fields

#### get_screener(query_name)
Returns screener results. Available queries:
- `day_gainers` - Top gaining stocks today
- `day_losers` - Top losing stocks today
- `most_actives` - Most actively traded stocks
- `most_shorted_stocks` - Most shorted stocks
- `growth_technology_stocks` - Technology growth stocks
- `undervalued_large_caps` - Undervalued large caps
- And more...

#### get_sector(sector_name) / get_industry(industry_key)
Returns sector/industry information with top companies.

## Error Handling

The client may raise exceptions for invalid symbols or network errors. Always handle exceptions appropriately in production code.

```python
from yfinance_skill import YFinanceClient

client = YFinanceClient()

try:
    price = client.get_price("INVALID_SYMBOL")
except Exception as e:
    print(f"Error: {e}")
```

## Notes

- Some data may not be available for all stocks, especially HK stocks
- Rate limiting may apply for frequent requests
- Delayed quotes may be returned for some data types
- Options data is only available for US stocks
