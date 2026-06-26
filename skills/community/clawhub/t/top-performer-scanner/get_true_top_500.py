#!/usr/bin/env python3
"""
Get True Top Performers by Year

Downloads the complete list of US-traded symbols from the NASDAQ FTP directory,
filters by liquidity (top N daily dollar volume), and ranks by annual returns.
This avoids survivorship bias by starting from the full symbol universe each year.
"""

import argparse
import io
import urllib.request
import warnings

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find the true top-performing US stocks per year by liquidity-ranked universe."
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=500,
        help="Number of most liquid stocks to include in the universe each year (default: 500)",
    )
    parser.add_argument(
        "--min-price",
        type=float,
        default=5.0,
        help="Minimum stock price at the start of the year to exclude penny stocks (default: 5.0)",
    )
    parser.add_argument(
        "--start-year",
        type=int,
        default=2020,
        help="First year to analyze (default: 2020)",
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=2025,
        help="Last year to analyze, inclusive (default: 2025)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="top_performers.csv",
        help="Output CSV file path (default: top_performers.csv)",
    )
    parser.add_argument(
        "--top-per-year",
        type=int,
        default=15,
        help="Number of top performers to display per year (default: 15)",
    )
    return parser.parse_args()


def download_nasdaq_symbols():
    """Download all US-traded symbols from the NASDAQ FTP directory."""
    print("1. Downloading all US traded symbols from NASDAQ FTP...")
    url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqtraded.txt"
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode("utf-8")
        df_sym = pd.read_csv(io.StringIO(data), sep="|")
    except Exception as e:
        print(f"Failed to download or parse NASDAQ directory: {e}")
        exit(1)

    # Filter out ETFs and test issues
    if "ETF" in df_sym.columns and "Test Issue" in df_sym.columns:
        df_sym = df_sym[(df_sym["ETF"] == "N") & (df_sym["Test Issue"] == "N")]

    # Keep only common stock tickers: alphabetic, up to 4 characters
    tickers = df_sym["Symbol"].dropna().unique().tolist()
    tickers = [t for t in tickers if type(t) == str and len(t) <= 4 and t.isalpha()]
    return tickers


def download_price_data(tickers, start_year, end_year):
    """Download historical price and volume data for the required date range."""
    # Fetch data starting from ~2 weeks before start_year to ensure first trading day is covered
    download_start = f"{start_year - 1}-12-15"
    download_end = f"{end_year + 1}-02-28"

    print(
        f"2. Found {len(tickers)} potential US equities. "
        f"Downloading historical data ({download_start} to {download_end})..."
    )
    data = yf.download(
        tickers, start=download_start, end=download_end, progress=False, threads=True
    )
    df_close = data["Close"]
    df_vol = data["Volume"]
    return df_close, df_vol


def analyze_year(df_close, df_vol, year, top_n, min_price, top_per_year):
    """Analyze a single year: find the top N liquid stocks and rank by return."""
    year_start = f"{year}-01-01"
    year_end = f"{year}-12-31"

    close_year = df_close.loc[year_start:year_end]
    vol_year = df_vol.loc[year_start:year_end]

    if close_year.empty:
        print(f"  No data for {year}, skipping.")
        return []

    # Calculate average daily dollar volume for the year
    dollar_vol = (close_year * vol_year).mean()
    dollar_vol = dollar_vol.dropna().sort_values(ascending=False)

    # Select the top N most liquid tickers
    top_liquid = dollar_vol.head(top_n).index.tolist()

    # Get first and last available close prices for the year
    first_close = close_year[top_liquid].apply(lambda col: col.dropna().iloc[0] if col.dropna().shape[0] > 0 else None)
    last_close = close_year[top_liquid].apply(lambda col: col.dropna().iloc[-1] if col.dropna().shape[0] > 0 else None)

    # Filter by minimum price at start of year
    valid = first_close[first_close >= min_price].index
    first_close = first_close[valid]
    last_close = last_close[valid]

    # Calculate annual return
    annual_return = (last_close / first_close) - 1
    annual_return = annual_return.dropna().sort_values(ascending=False)

    # Collect results for top performers
    results = []
    top_tickers = annual_return.head(top_per_year)
    for rank, (ticker, ret) in enumerate(top_tickers.items(), 1):
        avg_vol_m = dollar_vol.get(ticker, 0) / 1e6
        results.append(
            {
                "year": year,
                "rank": rank,
                "ticker": ticker,
                "return": round(ret * 100, 1),
                "avg_daily_vol_m": round(avg_vol_m, 0),
            }
        )

    return results


def main():
    args = parse_args()
    years = list(range(args.start_year, args.end_year + 1))

    tickers = download_nasdaq_symbols()
    df_close, df_vol = download_price_data(tickers, args.start_year, args.end_year)

    all_results = []
    for year in years:
        print(f"\n{'='*80}")
        print(
            f" TOP {args.top_per_year} PERFORMERS OF {year} "
            f"(Among Top {args.top_n} by Liquidity, min price ${args.min_price})"
        )
        print(f"{'='*80}")

        year_results = analyze_year(
            df_close, df_vol, year, args.top_n, args.min_price, args.top_per_year
        )
        all_results.extend(year_results)

        for r in year_results:
            print(
                f"  {r['rank']:>2}. {r['ticker']:<6}: "
                f"{r['return']:>7.1f}% "
                f"(Avg Daily Vol: ${r['avg_daily_vol_m']:.0f}M)"
            )

    # Save to CSV
    df_out = pd.DataFrame(all_results)
    df_out.to_csv(args.output, index=False)
    print(f"\nResults saved to {args.output}")
    print(f"Total records: {len(all_results)} ({len(years)} years x up to {args.top_per_year} per year)")


if __name__ == "__main__":
    main()
