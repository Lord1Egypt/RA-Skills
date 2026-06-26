#!/usr/bin/env python3
"""
Stock Market Data — CLI for Alpha Vantage API.
No dependencies beyond stdlib.

Usage:
  python3 stock_data.py <command> [args]

Commands:
  quote <symbol>                          Real-time stock quote
  search <query>                          Search for ticker symbols
  intraday <symbol> [--interval N]        Intraday time series
  daily <symbol> [--output-size N]        Daily time series
  weekly <symbol>                         Weekly time series
  monthly <symbol>                        Monthly time series
  overview <symbol>                       Company fundamentals
  movers                                  Top gainers, losers, most active
  news [--topic T] [--symbol S]           News & sentiment
  forex <from> <to>                       Currency exchange rate
  crypto <symbol> <market>                Cryptocurrency price
  commodity <name>                        Commodity prices
  gdp                                     Real GDP
  cpi                                     Consumer Price Index
  inflation                               Inflation rate
  treasury                                Treasury yield
  interest                                Federal funds rate
  sma|ema|rsi|macd|bbands|adx|atr|stoch|obv <symbol>  Technical indicators
"""

import json
import sys
import os
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "https://www.alphavantage.co/query"

def get_api_key(options):
    """Get API key from options, env, or default."""
    return options.get("key") or os.environ.get("ALPHA_VANTAGE_KEY", "demo")

def api_request(params, options=None):
    """Make a request to the Alpha Vantage API."""
    if options is None:
        options = {}
    params["apikey"] = get_api_key(options)
    
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "StockMarketData/1.0")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}")
        sys.exit(1)

def output(data, options):
    """Output data as JSON or CSV."""
    if options.get("csv"):
        if isinstance(data, list) and data:
            keys = list(data[0].keys())
            print(",".join(keys))
            for row in data:
                vals = [str(row.get(k, "")).replace(",", ";") for k in keys]
                print(",".join(vals))
        else:
            print(json.dumps(data, indent=2))
    else:
        print(json.dumps(data, indent=2, default=str))

# --- Commands ---

def cmd_quote(symbol, options):
    """Get real-time stock quote."""
    data = api_request({"function": "GLOBAL_QUOTE", "symbol": symbol}, options)
    quote = data.get("Global Quote", {})
    if not quote:
        print(f"No data for {symbol}. Check symbol or API key.")
        return
    
    result = {
        "symbol": quote.get("01. symbol", ""),
        "price": quote.get("05. price", ""),
        "open": quote.get("02. open", ""),
        "high": quote.get("03. high", ""),
        "low": quote.get("04. low", ""),
        "volume": quote.get("06. volume", ""),
        "latest_trading_day": quote.get("07. latest trading day", ""),
        "previous_close": quote.get("08. previous close", ""),
        "change": quote.get("09. change", ""),
        "change_percent": quote.get("10. change percent", "")
    }
    output(result, options)

def cmd_search(query, options):
    """Search for ticker symbols."""
    data = api_request({"function": "SYMBOL_SEARCH", "keywords": query}, options)
    matches = data.get("bestMatches", [])
    results = []
    for m in matches:
        results.append({
            "symbol": m.get("1. symbol", ""),
            "name": m.get("2. name", ""),
            "type": m.get("3. type", ""),
            "region": m.get("4. region", ""),
            "currency": m.get("8. currency", ""),
            "match_score": m.get("9. matchScore", "")
        })
    output(results, options)

def cmd_intraday(symbol, options):
    """Get intraday time series."""
    interval = options.get("interval", "5min")
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "outputsize": options.get("output-size", "compact")
    }
    data = api_request(params, options)
    ts_key = f"Time Series ({interval})"
    ts = data.get(ts_key, {})
    
    results = []
    for date, values in ts.items():
        results.append({
            "datetime": date,
            "open": values.get("1. open", ""),
            "high": values.get("2. high", ""),
            "low": values.get("3. low", ""),
            "close": values.get("4. close", ""),
            "volume": values.get("5. volume", "")
        })
    output(results, options)

def cmd_daily(symbol, options):
    """Get daily time series."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": options.get("output-size", "compact")
    }
    data = api_request(params, options)
    ts = data.get("Time Series (Daily)", {})
    
    results = []
    for date, values in ts.items():
        results.append({
            "date": date,
            "open": values.get("1. open", ""),
            "high": values.get("2. high", ""),
            "low": values.get("3. low", ""),
            "close": values.get("4. close", ""),
            "volume": values.get("5. volume", "")
        })
    output(results, options)

def cmd_weekly(symbol, options):
    """Get weekly time series."""
    data = api_request({"function": "TIME_SERIES_WEEKLY", "symbol": symbol}, options)
    ts = data.get("Weekly Time Series", {})
    results = []
    for date, values in ts.items():
        results.append({
            "date": date,
            "open": values.get("1. open", ""),
            "high": values.get("2. high", ""),
            "low": values.get("3. low", ""),
            "close": values.get("4. close", ""),
            "volume": values.get("5. volume", "")
        })
    output(results, options)

def cmd_monthly(symbol, options):
    """Get monthly time series."""
    data = api_request({"function": "TIME_SERIES_MONTHLY", "symbol": symbol}, options)
    ts = data.get("Monthly Time Series", {})
    results = []
    for date, values in ts.items():
        results.append({
            "date": date,
            "open": values.get("1. open", ""),
            "high": values.get("2. high", ""),
            "low": values.get("3. low", ""),
            "close": values.get("4. close", ""),
            "volume": values.get("5. volume", "")
        })
    output(results, options)

def cmd_overview(symbol, options):
    """Get company fundamentals."""
    data = api_request({"function": "OVERVIEW", "symbol": symbol}, options)
    if not data or "Symbol" not in data:
        print(f"No data for {symbol}.")
        return
    
    output({
        "symbol": data.get("Symbol"),
        "name": data.get("Name"),
        "description": data.get("Description", "")[:200],
        "exchange": data.get("Exchange"),
        "currency": data.get("Currency"),
        "sector": data.get("Sector"),
        "industry": data.get("Industry"),
        "market_cap": data.get("MarketCapitalization"),
        "pe_ratio": data.get("PERatio"),
        "peg_ratio": data.get("PEGRatio"),
        "dividend_yield": data.get("DividendYield"),
        "eps": data.get("EPS"),
        "beta": data.get("Beta"),
        "52_week_high": data.get("52WeekHigh"),
        "52_week_low": data.get("52WeekLow"),
        "50_day_ma": data.get("50DayMovingAverage"),
        "200_day_ma": data.get("200DayMovingAverage"),
        "shares_outstanding": data.get("SharesOutstanding"),
        "revenue_ttm": data.get("RevenueTTM"),
        "profit_margin": data.get("ProfitMargin")
    }, options)

def cmd_movers(options):
    """Get top gainers, losers, and most active."""
    data = api_request({"function": "TOP_GAINERS_LOSERS"}, options)
    
    output({
        "top_gainers": data.get("top_gainers", [])[:5],
        "top_losers": data.get("top_losers", [])[:5],
        "most_actively_traded": data.get("most_actively_traded", [])[:5],
        "last_updated": data.get("last_updated", "")
    }, options)

def cmd_news(options):
    """Get news and sentiment."""
    params = {"function": "NEWS_SENTIMENT"}
    if options.get("topic"):
        params["topics"] = options["topic"]
    if options.get("symbol"):
        params["tickers"] = options["symbol"]
    params["limit"] = options.get("limit", 5)
    
    data = api_request(params, options)
    feed = data.get("feed", [])
    
    results = []
    for item in feed[:int(options.get("limit", 5))]:
        results.append({
            "title": item.get("title", ""),
            "source": item.get("source", ""),
            "time": item.get("time_published", ""),
            "summary": item.get("summary", "")[:200],
            "sentiment": item.get("overall_sentiment_label", ""),
            "url": item.get("url", "")
        })
    output(results, options)

def cmd_forex(from_curr, to_curr, options):
    """Get currency exchange rate."""
    data = api_request({
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": from_curr,
        "to_currency": to_curr
    }, options)
    rate = data.get("Realtime Currency Exchange Rate", {})
    
    output({
        "from": f"{rate.get('1. From_Currency Code', '')} ({rate.get('2. From_Currency Name', '')})",
        "to": f"{rate.get('3. To_Currency Code', '')} ({rate.get('4. To_Currency Name', '')})",
        "rate": rate.get("5. Exchange Rate", ""),
        "last_updated": rate.get("6. Last Refreshed", ""),
        "timezone": rate.get("7. Time Zone", "")
    }, options)

def cmd_crypto(symbol, market, options):
    """Get cryptocurrency exchange rate."""
    data = api_request({
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": symbol,
        "to_currency": market
    }, options)
    rate = data.get("Realtime Currency Exchange Rate", {})
    
    output({
        "crypto": f"{rate.get('1. From_Currency Code', '')} ({rate.get('2. From_Currency Name', '')})",
        "market": f"{rate.get('3. To_Currency Code', '')} ({rate.get('4. To_Currency Name', '')})",
        "rate": rate.get("5. Exchange Rate", ""),
        "last_updated": rate.get("6. Last Refreshed", "")
    }, options)

def cmd_commodity(name, options):
    """Get commodity prices."""
    commodity_map = {
        "oil": ("WTI", "Crude Oil Prices: West Texas Intermediate (WTI)"),
        "brent": ("BRENT", "Crude Oil Prices: Brent - Europe"),
        "natural_gas": ("NATURAL_GAS", "Natural Gas"),
        "gold": ("GOLD", "Gold Price"),
        "silver": ("SILVER", "Silver Price"),
        "copper": ("COPPER", "Global Price of Copper"),
        "aluminum": ("ALUMINUM", "Global Price of Aluminum"),
        "wheat": ("WHEAT", "Global Price of Wheat"),
        "corn": ("CORN", "Global Price of Corn"),
        "cotton": ("COTTON", "Global Price of Cotton"),
        "sugar": ("SUGAR", "Global Price of Sugar"),
        "coffee": ("COFFEE", "Global Price of Coffee"),
        "all_commodities": ("ALL_COMMODITIES", "Global Price of All Commodities")
    }
    
    key = name.lower().replace(" ", "_")
    if key not in commodity_map:
        print(f"Unknown commodity: {name}")
        print(f"Available: {', '.join(commodity_map.keys())}")
        sys.exit(1)
    
    func, label = commodity_map[key]
    data = api_request({"function": func}, options)
    
    # Find the data key
    ts = None
    for k in data:
        if "data" in k.lower() or "price" in k.lower():
            ts = data[k]
            break
    
    if not ts:
        output(data, options)
        return
    
    results = []
    for item in ts[:12]:
        results.append({
            "date": item.get("date", ""),
            "value": item.get("value", "")
        })
    output(results, options)

def cmd_technical(indicator, symbol, options):
    """Get technical indicator."""
    interval = options.get("interval", "daily")
    time_period = options.get("time-period", "50")
    
    params = {
        "function": indicator.upper(),
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period
    }
    
    # Indicator-specific params
    if indicator.upper() in ("MACD", "STOCH", "BBANDS"):
        del params["time_period"]
    if indicator.upper() == "MACD":
        params["series_type"] = options.get("series-type", "close")
    if indicator.upper() == "BBANDS":
        params["time_period"] = time_period
        params["series_type"] = options.get("series-type", "close")
    if indicator.upper() == "RSI":
        params["series_type"] = options.get("series-type", "close")
    if indicator.upper() == "SMA" or indicator.upper() == "EMA":
        params["series_type"] = options.get("series-type", "close")
    
    data = api_request(params, options)
    
    # Find the technical analysis key
    ta_key = None
    for k in data:
        if "Technical" in k or "Analysis" in k:
            ta_key = k
            break
    
    if not ta_key:
        output(data, options)
        return
    
    ts = data[ta_key]
    results = []
    for date, values in list(ts.items())[:20]:
        entry = {"date": date}
        entry.update(values)
        results.append(entry)
    output(results, options)

def cmd_economic(func, options):
    """Get economic indicator."""
    data = api_request({"function": func}, options)
    
    # Find the data key
    ts = None
    for k in data:
        if "data" in k.lower():
            ts = data[k]
            break
    
    if not ts:
        output(data, options)
        return
    
    results = []
    for item in ts[:12]:
        results.append({
            "date": item.get("date", ""),
            "value": item.get("value", "")
        })
    output(results, options)

# --- CLI ---

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    options = {}
    args = sys.argv[2:]
    
    # Parse options from args
    i = 0
    positional = []
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            options["key"] = args[i + 1]; i += 2
        elif args[i] == "--interval" and i + 1 < len(args):
            options["interval"] = args[i + 1]; i += 2
        elif args[i] == "--output-size" and i + 1 < len(args):
            options["output-size"] = args[i + 1]; i += 2
        elif args[i] == "--time-period" and i + 1 < len(args):
            options["time-period"] = args[i + 1]; i += 2
        elif args[i] == "--series-type" and i + 1 < len(args):
            options["series-type"] = args[i + 1]; i += 2
        elif args[i] == "--topic" and i + 1 < len(args):
            options["topic"] = args[i + 1]; i += 2
        elif args[i] == "--symbol" and i + 1 < len(args):
            options["symbol"] = args[i + 1]; i += 2
        elif args[i] == "--limit" and i + 1 < len(args):
            options["limit"] = args[i + 1]; i += 2
        elif args[i] == "--csv":
            options["csv"] = True; i += 1
        else:
            positional.append(args[i]); i += 1
    
    # Technical indicators
    indicators = ["sma", "ema", "rsi", "macd", "bbands", "adx", "atr", "stoch", "obv"]
    
    if cmd == "quote" and positional:
        cmd_quote(positional[0], options)
    elif cmd == "search" and positional:
        cmd_search(" ".join(positional), options)
    elif cmd == "intraday" and positional:
        cmd_intraday(positional[0], options)
    elif cmd == "daily" and positional:
        cmd_daily(positional[0], options)
    elif cmd == "weekly" and positional:
        cmd_weekly(positional[0], options)
    elif cmd == "monthly" and positional:
        cmd_monthly(positional[0], options)
    elif cmd == "overview" and positional:
        cmd_overview(positional[0], options)
    elif cmd == "movers":
        cmd_movers(options)
    elif cmd == "news":
        cmd_news(options)
    elif cmd == "forex" and len(positional) >= 2:
        cmd_forex(positional[0], positional[1], options)
    elif cmd == "crypto" and len(positional) >= 2:
        cmd_crypto(positional[0], positional[1], options)
    elif cmd == "commodity" and positional:
        cmd_commodity(positional[0], options)
    elif cmd == "gdp":
        cmd_economic("REAL_GDP", options)
    elif cmd == "cpi":
        cmd_economic("CPI", options)
    elif cmd == "inflation":
        cmd_economic("INFLATION", options)
    elif cmd == "treasury":
        cmd_economic("TREASURY_YIELD", options)
    elif cmd == "interest":
        cmd_economic("FEDERAL_FUNDS_RATE", options)
    elif cmd in indicators and positional:
        cmd_technical(cmd.upper(), positional[0], options)
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
