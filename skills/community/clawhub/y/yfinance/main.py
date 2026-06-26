"""
OpenClaw YFinance Connector
FastAPI REST server to fetch Yahoo Finance stock data,
optimised for Indonesia stocks (suffix: .JK)
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import yfinance as yf
from datetime import datetime, date
from typing import Optional
import pandas as pd

app = FastAPI(
    title="OpenClaw YFinance Connector",
    description="Fetch Yahoo Finance stock data for Indonesia (IDX) and global markets.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def normalize_ticker(ticker: str) -> str:
    """Auto-append .JK for Indonesia tickers if no suffix present."""
    t = ticker.strip().upper()
    if "." not in t:
        t = f"{t}.JK"
    return t

def df_to_records(df: pd.DataFrame) -> list:
    """Convert DataFrame to list of dicts with ISO date strings."""
    df = df.copy()
    df.index = df.index.strftime("%Y-%m-%d")
    return df.reset_index().rename(columns={"index": "date", "Date": "date"}).to_dict(orient="records")

def format_number(value) -> str:
    """Human-readable large number formatting."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "N/A"
    v = float(value)
    if abs(v) >= 1e12:
        return f"{v/1e12:.2f}T"
    if abs(v) >= 1e9:
        return f"{v/1e9:.2f}B"
    if abs(v) >= 1e6:
        return f"{v/1e6:.2f}M"
    return f"{v:,.2f}"

def safe(value, default=None):
    try:
        if pd.isna(value):
            return default
    except Exception:
        pass
    return value


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {
        "service": "OpenClaw YFinance Connector",
        "status": "ok",
        "note": "Append .JK for Indonesia stocks, e.g. BBCA.JK",
        "endpoints": ["/price", "/history", "/fundamentals", "/dividends", "/splits"],
    }


@app.get("/price", tags=["Price"], summary="Real-time / latest stock price")
def get_price(
    ticker: str = Query(..., description="Stock ticker. Omit .JK for IDX stocks, e.g. BBCA"),
    auto_jk: bool = Query(True, description="Auto-append .JK if no suffix"),
):
    """
    Returns the latest market price, day range, volume and change %.
    Both JSON and formatted text are returned.
    """
    sym = normalize_ticker(ticker) if auto_jk else ticker.upper()
    try:
        stock = yf.Ticker(sym)
        info = stock.info
        fast = stock.fast_info

        price = safe(fast.last_price) or safe(info.get("currentPrice")) or safe(info.get("regularMarketPrice"))
        prev_close = safe(fast.previous_close) or safe(info.get("previousClose"))
        change = round(price - prev_close, 4) if price and prev_close else None
        change_pct = round((change / prev_close) * 100, 2) if change and prev_close else None

        data = {
            "ticker": sym,
            "name": info.get("longName") or info.get("shortName", sym),
            "currency": info.get("currency", "IDR"),
            "exchange": info.get("exchange", "N/A"),
            "price": price,
            "previous_close": prev_close,
            "change": change,
            "change_pct": change_pct,
            "day_high": safe(fast.day_high),
            "day_low": safe(fast.day_low),
            "volume": safe(fast.last_volume),
            "market_cap": safe(fast.market_cap),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        arrow = "▲" if (change_pct or 0) >= 0 else "▼"
        formatted = (
            f"{'─'*45}\n"
            f"  {data['name']} ({sym})\n"
            f"  {data['currency']}  {price:,.2f}  {arrow} {change_pct:+.2f}%\n"
            f"  Day: {safe(fast.day_low, 'N/A'):,} – {safe(fast.day_high, 'N/A'):,}\n"
            f"  Prev Close: {prev_close:,.2f}   Vol: {format_number(safe(fast.last_volume))}\n"
            f"{'─'*45}"
        )

        return {"json": data, "formatted": formatted}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", tags=["History"], summary="Historical OHLCV price data")
def get_history(
    ticker: str = Query(..., description="Stock ticker"),
    period: Optional[str] = Query("1mo", description="Period: 1d 5d 1mo 3mo 6mo 1y 2y 5y 10y ytd max"),
    start: Optional[date] = Query(None, description="Start date YYYY-MM-DD (overrides period)"),
    end: Optional[date] = Query(None, description="End date YYYY-MM-DD"),
    interval: str = Query("1d", description="Interval: 1m 5m 15m 30m 1h 1d 1wk 1mo"),
    auto_jk: bool = Query(True),
):
    """
    Returns OHLCV history. Use `period` OR `start`/`end` pair.
    """
    sym = normalize_ticker(ticker) if auto_jk else ticker.upper()
    try:
        stock = yf.Ticker(sym)
        if start:
            df = stock.history(start=str(start), end=str(end) if end else None, interval=interval)
        else:
            df = stock.history(period=period, interval=interval)

        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for {sym}")

        df = df[["Open", "High", "Low", "Close", "Volume"]]
        records = df_to_records(df)

        # Simple text table (last 5 rows preview)
        preview = df.tail(5)
        lines = [f"{'─'*65}", f"  {sym} — Last {len(df)} candles ({interval})", f"{'─'*65}",
                 f"  {'Date':<12} {'Open':>10} {'High':>10} {'Low':>10} {'Close':>10} {'Volume':>12}",
                 f"  {'─'*63}"]
        for idx, row in preview.iterrows():
            d = idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx)[:10]
            lines.append(f"  {d:<12} {row['Open']:>10,.2f} {row['High']:>10,.2f} {row['Low']:>10,.2f} {row['Close']:>10,.2f} {format_number(row['Volume']):>12}")
        lines.append(f"{'─'*65}")
        formatted = "\n".join(lines)

        return {"json": {"ticker": sym, "interval": interval, "count": len(records), "records": records},
                "formatted": formatted}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fundamentals", tags=["Fundamentals"], summary="Company fundamentals & ratios")
def get_fundamentals(
    ticker: str = Query(..., description="Stock ticker"),
    auto_jk: bool = Query(True),
):
    """
    Returns key financial fundamentals: P/E, P/B, EPS, market cap, revenue, etc.
    """
    sym = normalize_ticker(ticker) if auto_jk else ticker.upper()
    try:
        info = yf.Ticker(sym).info

        fields = {
            "longName": "name",
            "exchange": "exchange",
            "currency": "currency",
            "sector": "sector",
            "industry": "industry",
            "marketCap": "market_cap",
            "trailingPE": "pe_ratio_ttm",
            "forwardPE": "pe_ratio_forward",
            "priceToBook": "pb_ratio",
            "trailingEps": "eps_ttm",
            "forwardEps": "eps_forward",
            "dividendYield": "dividend_yield",
            "payoutRatio": "payout_ratio",
            "returnOnEquity": "roe",
            "returnOnAssets": "roa",
            "debtToEquity": "debt_to_equity",
            "totalRevenue": "revenue",
            "grossProfits": "gross_profit",
            "ebitda": "ebitda",
            "freeCashflow": "free_cashflow",
            "52WeekChange": "52w_change",
            "fiftyTwoWeekHigh": "52w_high",
            "fiftyTwoWeekLow": "52w_low",
            "beta": "beta",
            "sharesOutstanding": "shares_outstanding",
            "bookValue": "book_value_per_share",
        }

        data = {"ticker": sym}
        for src, dst in fields.items():
            data[dst] = safe(info.get(src))

        # Percent formatting
        for pct_key in ["dividend_yield", "payout_ratio", "roe", "roa", "52w_change"]:
            v = data.get(pct_key)
            if v is not None:
                data[pct_key] = round(v * 100, 2)

        # Formatted text
        lines = [
            f"{'═'*50}",
            f"  {data.get('name', sym)} ({sym})",
            f"  {data.get('sector','N/A')} › {data.get('industry','N/A')}",
            f"{'─'*50}",
            f"  Market Cap        : {format_number(data.get('market_cap'))} {data.get('currency','')}",
            f"  P/E (TTM)         : {data.get('pe_ratio_ttm','N/A')}",
            f"  P/E (Forward)     : {data.get('pe_ratio_forward','N/A')}",
            f"  P/B               : {data.get('pb_ratio','N/A')}",
            f"  EPS (TTM)         : {data.get('eps_ttm','N/A')}",
            f"  Dividend Yield    : {data.get('dividend_yield','N/A')}%",
            f"  ROE               : {data.get('roe','N/A')}%",
            f"  ROA               : {data.get('roa','N/A')}%",
            f"  Debt/Equity       : {data.get('debt_to_equity','N/A')}",
            f"  Revenue           : {format_number(data.get('revenue'))} {data.get('currency','')}",
            f"  Free Cash Flow    : {format_number(data.get('free_cashflow'))} {data.get('currency','')}",
            f"  Beta              : {data.get('beta','N/A')}",
            f"  52W High/Low      : {data.get('52w_high','N/A')} / {data.get('52w_low','N/A')}",
            f"{'═'*50}",
        ]
        formatted = "\n".join(lines)

        return {"json": data, "formatted": formatted}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dividends", tags=["Corporate Actions"], summary="Dividend history")
def get_dividends(
    ticker: str = Query(..., description="Stock ticker"),
    auto_jk: bool = Query(True),
):
    """Returns full dividend payment history."""
    sym = normalize_ticker(ticker) if auto_jk else ticker.upper()
    try:
        stock = yf.Ticker(sym)
        divs = stock.dividends

        if divs.empty:
            return {"json": {"ticker": sym, "count": 0, "records": []},
                    "formatted": f"No dividend history found for {sym}."}

        divs.index = divs.index.strftime("%Y-%m-%d")
        records = [{"date": d, "dividend": round(v, 6)} for d, v in divs.items()]

        lines = [f"{'─'*35}", f"  {sym} — Dividend History ({len(records)} payments)", f"{'─'*35}"]
        for r in records[-10:]:
            lines.append(f"  {r['date']}    {r['dividend']:>12,.4f}")
        if len(records) > 10:
            lines.append(f"  ... and {len(records)-10} more earlier payments")
        lines.append(f"{'─'*35}")

        return {"json": {"ticker": sym, "count": len(records), "records": records},
                "formatted": "\n".join(lines)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/splits", tags=["Corporate Actions"], summary="Stock split history")
def get_splits(
    ticker: str = Query(..., description="Stock ticker"),
    auto_jk: bool = Query(True),
):
    """Returns full stock split history."""
    sym = normalize_ticker(ticker) if auto_jk else ticker.upper()
    try:
        stock = yf.Ticker(sym)
        splits = stock.splits

        if splits.empty:
            return {"json": {"ticker": sym, "count": 0, "records": []},
                    "formatted": f"No split history found for {sym}."}

        splits.index = splits.index.strftime("%Y-%m-%d")
        records = [{"date": d, "ratio": v} for d, v in splits.items()]

        lines = [f"{'─'*35}", f"  {sym} — Split History", f"{'─'*35}"]
        for r in records:
            lines.append(f"  {r['date']}    {r['ratio']:.2f}:1 split")
        lines.append(f"{'─'*35}")

        return {"json": {"ticker": sym, "count": len(records), "records": records},
                "formatted": "\n".join(lines)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
