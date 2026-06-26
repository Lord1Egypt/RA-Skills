#!/usr/bin/env python3
"""
Stock Screener - Find stocks matching financial criteria
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yfinance as yf
except ImportError:
    print("Install yfinance: pip install yfinance")
    raise


DEFAULT_DATA_DIR = Path.home() / ".openclaw" / "stock-screener"
DEFAULT_DATA_DIR.mkdir(parents=True, exist_ok=True)


def search_stocks(
    pe_max: Optional[float] = None,
    pe_min: Optional[float] = None,
    dividend_min: Optional[float] = None,
    market_cap_min: Optional[float] = None,
    sector: Optional[str] = None,
    revenue_growth_min: Optional[float] = None,
    momentum_days: int = 30,
    volume_min: int = 0,
) -> list[dict]:
    """
    Search for stocks matching criteria.
    
    Note: yfinance doesn't support direct screening.
    This uses a predefined list and filters locally.
    For production, use a screening API (e.g., Financial Modeling Prep).
    """
    # Sample stock universe (expand with API for full coverage)
    tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "JPM",
        "V", "UNH", "JNJ", "WMT", "PG", "MA", "HD", "DIS", "PYPL",
        "ADBE", "NFLX", "CRM", "INTC", "VZ", "T", "MRK", "PFE", "KO",
        "PEP", "ABT", "TMO", "COST", "NKE", "AVGO", "CSCO", "ACN",
        "TXN", "QCOM", "LLY", "DHR", "MDT", "BMY", "UNP", "LIN",
    ]
    
    results = []
    
    print(f"Scanning {len(tickers)} stocks...")
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Apply filters
            if pe_max and info.get("trailingPE", 999) > pe_max:
                continue
            if pe_min and info.get("trailingPE", 0) < pe_min:
                continue
            if dividend_min and info.get("dividendYield", 0) * 100 < dividend_min:
                continue
            if market_cap_min:
                cap = info.get("marketCap", 0)
                if cap < market_cap_min * 1_000_000_000:
                    continue
            if sector:
                if info.get("sector", "").lower() != sector.lower():
                    continue
            if revenue_growth_min:
                growth = info.get("revenueGrowth", 0) or 0
                if growth * 100 < revenue_growth_min:
                    continue
            if volume_min:
                vol = info.get("volume", 0)
                if vol < volume_min:
                    continue
            
            # Get price data for momentum
            hist = stock.history(period=f"{momentum_days}d")
            if len(hist) > 1:
                momentum = ((hist["Close"].iloc[-1] / hist["Close"].iloc[0]) - 1) * 100
            else:
                momentum = 0
            
            results.append({
                "symbol": ticker,
                "name": info.get("shortName", ticker),
                "price": info.get("currentPrice", 0),
                "pe": info.get("trailingPE"),
                "dividend_yield": (info.get("dividendYield") or 0) * 100,
                "market_cap": info.get("marketCap"),
                "sector": info.get("sector"),
                "momentum": momentum,
                "volume": info.get("volume"),
            })
            
        except Exception as e:
            continue
    
    return results


def format_market_cap(cap: int) -> str:
    """Format market cap in billions."""
    if cap is None:
        return "N/A"
    if cap >= 1_000_000_000_000:
        return f"${cap/1_000_000_000_000:.2f}T"
    elif cap >= 1_000_000_000:
        return f"${cap/1_000_000_000:.2f}B"
    elif cap >= 1_000_000:
        return f"${cap/1_000_000:.2f}M"
    return f"${cap}"


def print_results(results: list[dict]):
    """Print search results in table format."""
    if not results:
        print("No stocks match criteria")
        return
    
    print(f"\n{'Symbol':<8} {'Name':<20} {'Price':<10} {'P/E':<6} {'Div %':<6} {'Cap':<10} {'Momentum':<10}")
    print("-" * 80)
    
    for r in results:
        print(f"{r['symbol']:<8} {r['name'][:19]:<20} ${r['price']:<9.2f} "
              f"{r['pe'] if r['pe'] else 'N/A':<6} "
              f"{r['dividend_yield']:.2f}%  "
              f"{format_market_cap(r['market_cap']):<10} "
              f"{r['momentum']:+.1f}%")


def save_watchlist(name: str, stocks: list[dict]):
    """Save stocks to a watchlist file."""
    watchlist_file = DEFAULT_DATA_DIR / "watchlists" / f"{name}.json"
    watchlist_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(watchlist_file, "w") as f:
        json.dump({
            "name": name,
            "created": datetime.now().isoformat(),
            "stocks": stocks
        }, f, indent=2)
    
    print(f"Saved {len(stocks)} stocks to watchlist '{name}'")


def list_watchlists():
    """List all saved watchlists."""
    watchlist_dir = DEFAULT_DATA_DIR / "watchlists"
    if not watchlist_dir.exists():
        print("No watchlists saved")
        return
    
    files = list(watchlist_dir.glob("*.json"))
    if not files:
        print("No watchlists saved")
        return
    
    print("Watchlists:")
    for f in files:
        with open(f) as file:
            data = json.load(file)
            print(f"  - {data['name']}: {len(data['stocks'])} stocks")


def show_watchlist(name: str):
    """Show stocks in a watchlist."""
    watchlist_file = DEFAULT_DATA_DIR / "watchlists" / f"{name}.json"
    if not watchlist_file.exists():
        print(f"Watchlist '{name}' not found")
        return
    
    with open(watchlist_file) as f:
        data = json.load(f)
    
    print(f"\n# {data['name']}")
    print(f"Created: {data['created']}")
    print_results(data['stocks'])


def main():
    parser = argparse.ArgumentParser(description="Stock Screener")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for stocks")
    search_parser.add_argument("--pe-max", type=float, help="Maximum P/E ratio")
    search_parser.add_argument("--pe-min", type=float, help="Minimum P/E ratio")
    search_parser.add_argument("--dividend-min", type=float, help="Minimum dividend yield %")
    search_parser.add_argument("--market-cap-min", type=float, help="Minimum market cap (billions)")
    search_parser.add_argument("--sector", type=str, help="Sector (e.g., Technology)")
    search_parser.add_argument("--revenue-growth-min", type=float, help="Minimum revenue growth %")
    search_parser.add_argument("--momentum", type=int, default=30, help="Momentum period in days")
    search_parser.add_argument("--volume-min", type=int, default=0, help="Minimum daily volume")
    search_parser.add_argument("--save", type=str, help="Save results to watchlist")
    
    # List watchlists
    subparsers.add_parser("list-watchlists", help="List saved watchlists")
    
    # Show watchlist
    show_parser = subparsers.add_parser("show-watchlist", help="Show stocks in watchlist")
    show_parser.add_argument("name", help="Watchlist name")
    
    args = parser.parse_args()
    
    if args.command == "search":
        results = search_stocks(
            pe_max=args.pe_max,
            pe_min=args.pe_min,
            dividend_min=args.dividend_min,
            market_cap_min=args.market_cap_min,
            sector=args.sector,
            revenue_growth_min=args.revenue_growth_min,
            momentum_days=args.momentum,
            volume_min=args.volume_min,
        )
        print_results(results)
        
        if args.save and results:
            save_watchlist(args.save, results)
    
    elif args.command == "list-watchlists":
        list_watchlists()
    
    elif args.command == "show-watchlist":
        show_watchlist(args.name)


if __name__ == "__main__":
    main()
