"""
Central validation module: symbol aliases, timeframe validation, bar limit warnings.

Every action script calls these before running. Validation happens here so
error messages are consistent and Claude's SKILL.md recovery logic works.
"""

from __future__ import annotations

VALID_TIMEFRAMES = {"1", "3", "5", "10", "15", "30", "45", "60", "120", "180", "240", "1D", "1W", "1M"}

TIMEFRAME_LABELS: dict[str, str] = {
    "1": "1 min", "3": "3 min", "5": "5 min", "10": "10 min",
    "15": "15 min", "30": "30 min", "45": "45 min",
    "60": "1 hour", "120": "2 hour", "180": "3 hour", "240": "4 hour",
    "1D": "1 day", "1W": "1 week", "1M": "1 month",
}

SYMBOL_ALIASES: dict[str, str] = {
    # Crypto
    "BTC": "BINANCE:BTCUSDT", "BITCOIN": "BINANCE:BTCUSDT",
    "ETH": "BINANCE:ETHUSDT", "ETHEREUM": "BINANCE:ETHUSDT",
    "SOL": "BINANCE:SOLUSDT", "SOLANA": "BINANCE:SOLUSDT",
    "BNB": "BINANCE:BNBUSDT",
    "XRP": "BINANCE:XRPUSDT", "RIPPLE": "BINANCE:XRPUSDT",
    "DOGE": "BINANCE:DOGEUSDT", "DOGECOIN": "BINANCE:DOGEUSDT",
    "ADA": "BINANCE:ADAUSDT", "CARDANO": "BINANCE:ADAUSDT",
    "DOT": "BINANCE:DOTUSDT", "POLKADOT": "BINANCE:DOTUSDT",
    "AVAX": "BINANCE:AVAXUSDT", "AVALANCHE": "BINANCE:AVAXUSDT",
    "LINK": "BINANCE:LINKUSDT", "CHAINLINK": "BINANCE:LINKUSDT",
    "MATIC": "BINANCE:MATICUSDT", "POLYGON": "BINANCE:MATICUSDT",
    "ATOM": "BINANCE:ATOMUSDT", "COSMOS": "BINANCE:ATOMUSDT",
    "UNI": "BINANCE:UNIUSDT", "UNISWAP": "BINANCE:UNIUSDT",
    "BTCD": "CRYPTOCAP:BTC.D", "BTC.D": "CRYPTOCAP:BTC.D",
    "TOTALCAP": "CRYPTOCAP:TOTAL",
    # US Stocks — top 20
    "AAPL": "NASDAQ:AAPL", "APPLE": "NASDAQ:AAPL",
    "MSFT": "NASDAQ:MSFT", "MICROSOFT": "NASDAQ:MSFT",
    "GOOGL": "NASDAQ:GOOGL", "GOOGLE": "NASDAQ:GOOGL",
    "AMZN": "NASDAQ:AMZN", "AMAZON": "NASDAQ:AMZN",
    "TSLA": "NASDAQ:TSLA", "TESLA": "NASDAQ:TSLA",
    "NVDA": "NASDAQ:NVDA", "NVIDIA": "NASDAQ:NVDA",
    "META": "NASDAQ:META", "FACEBOOK": "NASDAQ:META",
    "NFLX": "NASDAQ:NFLX", "NETFLIX": "NASDAQ:NFLX",
    "AMD": "NASDAQ:AMD",
    "INTC": "NASDAQ:INTC", "INTEL": "NASDAQ:INTC",
    "CRM": "NYSE:CRM", "SALESFORCE": "NYSE:CRM",
    "BA": "NYSE:BA", "BOEING": "NYSE:BA",
    "DIS": "NYSE:DIS", "DISNEY": "NYSE:DIS",
    "JPM": "NYSE:JPM", "JPMORGAN": "NYSE:JPM",
    "V": "NYSE:V", "VISA": "NYSE:V",
    "WMT": "NYSE:WMT", "WALMART": "NYSE:WMT",
    "JNJ": "NYSE:JNJ",
    "PG": "NYSE:PG",
    "KO": "NYSE:KO", "COCACOLA": "NYSE:KO",
    # Indices
    "SPX": "SP:SPX", "SP500": "SP:SPX", "S&P500": "SP:SPX", "S&P": "SP:SPX",
    "SPY": "AMEX:SPY",
    "QQQ": "NASDAQ:QQQ",
    "NDX": "NASDAQ:NDX", "NASDAQ100": "NASDAQ:NDX",
    "DJI": "DJ:DJI", "DOW": "DJ:DJI", "DOWJONES": "DJ:DJI",
    "VIX": "CBOE:VIX",
    "RUT": "TVC:RUT", "RUSSELL": "TVC:RUT",
    # Forex
    "EURUSD": "FX:EURUSD", "EUR/USD": "FX:EURUSD",
    "GBPUSD": "FX:GBPUSD", "GBP/USD": "FX:GBPUSD",
    "USDJPY": "FX:USDJPY", "USD/JPY": "FX:USDJPY",
    "AUDUSD": "FX:AUDUSD", "AUD/USD": "FX:AUDUSD",
    "USDCAD": "FX:USDCAD", "USD/CAD": "FX:USDCAD",
    "USDCHF": "FX:USDCHF", "USD/CHF": "FX:USDCHF",
    "NZDUSD": "FX:NZDUSD", "NZD/USD": "FX:NZDUSD",
    "DXY": "TVC:DXY", "DOLLAR": "TVC:DXY",
    # Commodities
    "GOLD": "TVC:GOLD", "XAU": "TVC:GOLD", "XAUUSD": "TVC:GOLD",
    "SILVER": "TVC:SILVER", "XAG": "TVC:SILVER",
    "OIL": "TVC:USOIL", "WTI": "TVC:USOIL", "CRUDE": "TVC:USOIL",
    "BRENT": "TVC:UKOIL",
    "NATGAS": "TVC:NATURALGAS", "NATURALGAS": "TVC:NATURALGAS",
}

# Anonymous bar limits per timeframe
ANON_BAR_LIMITS: dict[str, int] = {
    "1": 6500, "3": 5500, "5": 5300, "10": 5200, "15": 5200,
    "30": 5100, "45": 5000, "60": 10800, "120": 9000,
    "180": 8000, "240": 7100,
    "1D": 999999, "1W": 999999, "1M": 999999,
}

_INTRADAY = {"1", "3", "5", "10", "15", "30", "45", "60", "120", "180", "240"}


def resolve_symbol(raw: str) -> str:
    """
    Resolve a symbol alias to EXCHANGE:TICKER format.
    If already in EXCHANGE:TICKER format, return as-is.
    If unknown alias with no colon, return as-is (will fail at TV level with helpful error).
    """
    upper = raw.upper().strip()
    if upper in SYMBOL_ALIASES:
        return SYMBOL_ALIASES[upper]
    if ":" in raw:
        return raw.upper()
    return raw.upper()


def validate_timeframe(tf: str) -> str:
    """Validate and return timeframe. Raises ValueError with helpful message."""
    tf = tf.upper() if len(tf) > 1 and tf[-1].isalpha() else tf
    if tf in VALID_TIMEFRAMES:
        return tf
    # Common alternative formats
    alt_map = {
        "1M": "1", "5M": "5", "15M": "15", "30M": "30",
        "1H": "60", "2H": "120", "3H": "180", "4H": "240",
        "D": "1D", "W": "1W", "M": "1M",
    }
    if tf.upper() in alt_map:
        return alt_map[tf.upper()]

    raise ValueError(
        f"Invalid timeframe '{tf}'. "
        f"Valid options: {', '.join(sorted(VALID_TIMEFRAMES, key=lambda x: (x[-1].isalpha(), x)))}\n"
        f"Also accepts: 1M/5M/15M (minutes), 1H/2H/4H (hours), D/W/M"
    )


def parse_bars(raw: str) -> int:
    """
    Parse bar count from string. Supports: '500', '1k', '1K', '5000', '10k'.
    Raises ValueError if invalid.
    """
    raw = raw.strip().lower()
    if raw.endswith("k"):
        return int(float(raw[:-1]) * 1000)
    return int(raw)


def check_bar_limit_warning(timeframe: str, bars: int, is_anonymous: bool) -> str | None:
    """
    Return a warning string if bars exceeds anonymous limit for this timeframe.
    Returns None if no warning needed.
    """
    if not is_anonymous:
        return None
    if timeframe not in _INTRADAY:
        return None
    limit = ANON_BAR_LIMITS.get(timeframe, 999999)
    if bars <= limit:
        return None

    label = TIMEFRAME_LABELS.get(timeframe, timeframe)
    return (
        f"WARNING: Anonymous mode is limited to ~{limit:,} bars at {label} timeframe. "
        f"You requested {bars:,} — you'll receive approximately {limit:,} bars. "
        f"Set TV_AUTH_TOKEN for more intraday data."
    )


def is_intraday(timeframe: str) -> bool:
    """Return True if timeframe is intraday (sub-daily)."""
    return timeframe in _INTRADAY
