# pyright: reportMissingImports=false

from datetime import datetime, timedelta

import yfinance as yf

from constants import (
    HISTORY_PERIOD,
    MAX_EVENTS,
    MAX_RELEVANT_NEWS,
    NEWS_FETCH_LIMIT,
    RANGE_WINDOWS,
)
from utils import (
    format_event_date,
    format_market_cap,
    format_number,
    format_range,
    format_volume_summary,
)


def get_price_range(history, days: int) -> dict:
    """Calculate the high and low price over the last N days from historical data."""
    cutoff = datetime.now() - timedelta(days=days)
    filtered = history[history.index >= cutoff.strftime("%Y-%m-%d")]
    if filtered.empty:
        return {"high": None, "low": None}
    return {
        "high": float(filtered["High"].max()),
        "low": float(filtered["Low"].min()),
    }


def extract_upcoming_events(calendar) -> list:
    """Extract up to five upcoming events from calendar data."""
    events = []

    if not calendar:
        return events

    earnings_date = calendar.get("Earnings Date")
    if isinstance(earnings_date, (list, tuple)) and earnings_date:
        earnings_date = earnings_date[0]
    if earnings_date:
        events.append({"type": "Earnings Call", "date": earnings_date})

    ex_dividend_date = calendar.get("Ex-Dividend Date")
    if ex_dividend_date:
        events.append({"type": "Ex-Dividend Date", "date": ex_dividend_date})

    dividend_date = calendar.get("Dividend Date")
    if dividend_date:
        events.append({"type": "Dividend Payment", "date": dividend_date})

    earnings_avg = calendar.get("Earnings Average")
    if earnings_avg is not None:
        events.append(
            {"type": "Earnings EPS Estimate", "date": f"Est. EPS: {earnings_avg}"}
        )

    earnings_high = calendar.get("Earnings High")
    if earnings_high is not None:
        events.append(
            {"type": "Earnings EPS High", "date": f"Est. High EPS: {earnings_high}"}
        )

    return events[:MAX_EVENTS]


def filter_relevant_news(news_list: list, symbol: str, company_name: str) -> list:
    """Filter news articles to show only those relevant to the company."""
    if not news_list:
        return []

    keywords = [symbol.upper(), company_name.upper()]
    if company_name:
        first_word = company_name.split()[0].upper()
        if first_word:
            keywords.append(first_word)

    filtered = []
    for article in news_list:
        if not isinstance(article, dict):
            continue

        content = article.get("content", {})
        if not isinstance(content, dict):
            continue

        title = content.get("title", "").upper()
        summary = content.get("summary", "").upper()
        if any(
            keyword in title or keyword in summary for keyword in keywords if keyword
        ):
            filtered.append(article)

        if len(filtered) >= MAX_RELEVANT_NEWS:
            break

    return filtered


def get_stock_price(symbol: str) -> dict:
    """Get current stock price, company info, historical ranges, news, and events."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info or {}

        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        previous_close = info.get("previousClose")
        change = (
            current_price - previous_close
            if current_price is not None and previous_close is not None
            else None
        )
        change_percent = (
            ((change / previous_close) * 100)
            if change is not None and previous_close not in (None, 0)
            else None
        )

        history = ticker.history(period=HISTORY_PERIOD)
        raw_news = ticker.news[:NEWS_FETCH_LIMIT] if ticker.news else []
        company_name = info.get("longName") or info.get("shortName") or symbol

        ranges = {
            window["key"]: get_price_range(history, window["days"])
            for window in RANGE_WINDOWS
        }

        return {
            "symbol": symbol,
            "company_name": company_name,
            "price": current_price,
            "change": change,
            "change_percent": change_percent,
            "previous_close": previous_close,
            "market_cap": info.get("marketCap"),
            "volume": info.get("volume"),
            "avg_volume": info.get("averageVolume"),
            "day_high": info.get("dayHigh"),
            "day_low": info.get("dayLow"),
            "news": filter_relevant_news(raw_news, symbol, company_name),
            "events": extract_upcoming_events(ticker.calendar),
            **ranges,
        }
    except Exception as exc:
        return {"error": f"Could not get stock price for {symbol}: {str(exc)}"}


def format_recent_news(news: list) -> str:
    """Format recent company news for display."""
    if not news:
        return "Recent News: No relevant news available"

    news_lines = ["Recent News:"]
    for index, article in enumerate(news[:MAX_RELEVANT_NEWS], 1):
        title = "No title"
        url = ""
        content = article.get("content", {})
        if isinstance(content, dict):
            title = content.get("title", "No title")
            click_url = content.get("clickThroughUrl", {})
            if isinstance(click_url, dict):
                url = click_url.get("url", "")

        news_lines.append(f"{index}. {title}")
        if url:
            news_lines.append(f"   Link: {url}")

    return "\n".join(news_lines)


def format_upcoming_events(events: list) -> str:
    """Format upcoming events for display."""
    if not events:
        return "Upcoming Events: None scheduled"

    event_lines = ["Upcoming Events:"]
    for index, event in enumerate(events[:MAX_EVENTS], 1):
        event_type = event.get("type", "Unknown")
        event_date = format_event_date(event.get("date", "Unknown"))
        event_lines.append(f"{index}. {event_type}: {event_date}")

    return "\n".join(event_lines)


def format_output(data: dict) -> str:
    """Format all stock data into the final human-readable output."""
    if "error" in data:
        return f"Error: {data['error']}"

    price_str = f"${format_number(data['price'])}"
    if data["change"] is not None and data["change"] > 0:
        change_str = f"▲${format_number(data['change'])}"
    elif data["change"] is not None and data["change"] < 0:
        change_str = f"▼${format_number(abs(data['change']))}"
    else:
        change_str = "—"

    change_percent_str = (
        f"({format_number(data['change_percent'])}%)"
        if data["change_percent"] is not None
        else "(—)"
    )
    prev_close_str = (
        f"${format_number(data['previous_close'])}"
        if data["previous_close"] is not None
        else "N/A"
    )
    day_high_str = (
        f"${format_number(data['day_high'])}"
        if data.get("day_high") is not None
        else "N/A"
    )
    day_low_str = (
        f"${format_number(data['day_low'])}"
        if data.get("day_low") is not None
        else "N/A"
    )
    range_blocks = "\n\n".join(
        format_range(window["label"], data[window["key"]]) for window in RANGE_WINDOWS
    )

    return (
        f"{data['symbol']}: {data['company_name']}\n"
        f"{price_str} {change_str} {change_percent_str}, Prev Close: {prev_close_str}\n"
        f"{format_volume_summary(data['volume'], data['avg_volume'])} | Mkt Cap: {format_market_cap(data['market_cap'])}\n"
        f"\n"
        f"Today Low: {day_low_str}, High: {day_high_str}\n"
        f"\n"
        f"{range_blocks}\n"
        f"\n"
        f"{format_recent_news(data['news'])}\n"
        f"\n"
        f"{format_upcoming_events(data['events'])}"
    )
