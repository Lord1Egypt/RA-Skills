#!/usr/bin/env python3
"""Detect peer companies for a ticker using sector/industry data. Outputs JSON."""
import argparse
import json
import sys

# Hardcoded fallbacks for common tickers
FALLBACK_PEERS = {
    "GOOG": ["MSFT", "META", "AMZN"],
    "GOOGL": ["MSFT", "META", "AMZN"],
    "TSLA": ["RIVN", "GM", "F"],
    "TIGR": ["FUTU", "IBKR"],
    "AAPL": ["MSFT", "GOOG", "SAMSUNG"],
    "MSFT": ["AAPL", "GOOG", "ORCL"],
    "META": ["GOOG", "SNAP", "PINS"],
    "AMZN": ["WMT", "SHOP", "BABA"],
    "NVDA": ["AMD", "INTC", "AVGO"],
}

# Industry -> representative tickers for peer discovery
INDUSTRY_PEERS = {
    "Semiconductors": ["NVDA", "AMD", "INTC", "AVGO", "QCOM", "TXN", "MU"],
    "Internet Content & Information": ["GOOG", "META", "SNAP", "PINS", "BIDU"],
    "Software - Infrastructure": ["MSFT", "ORCL", "CRM", "NOW", "ADBE"],
    "Software - Application": ["CRM", "ADBE", "NOW", "INTU", "WDAY"],
    "Consumer Electronics": ["AAPL", "SONY", "HPQ", "DELL"],
    "Auto Manufacturers": ["TSLA", "GM", "F", "TM", "RIVN", "HMC"],
    "Internet Retail": ["AMZN", "BABA", "JD", "SHOP", "MELI", "PDD"],
    "Capital Markets": ["GS", "MS", "SCHW", "IBKR", "FUTU", "TIGR"],
    "Drug Manufacturers - General": ["JNJ", "PFE", "MRK", "LLY", "ABBV"],
    "Banks - Diversified": ["JPM", "BAC", "WFC", "C", "USB"],
    "Aerospace & Defense": ["LMT", "BA", "RTX", "NOC", "GD"],
    "Oil & Gas Integrated": ["XOM", "CVX", "SHEL", "BP", "TTE"],
    "Telecom Services": ["T", "VZ", "TMUS", "CMCSA"],
    "Restaurants": ["MCD", "SBUX", "YUM", "CMG", "DRI"],
    "Discount Stores": ["WMT", "COST", "TGT", "DG", "DLTR"],
}


def main():
    parser = argparse.ArgumentParser(description="Detect peer companies for a stock ticker.")
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--count", type=int, default=5, help="Max number of peers (default: 5)")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run with: uv run --with yfinance", file=sys.stderr)
        sys.exit(1)

    ticker = args.ticker.upper()
    t = yf.Ticker(ticker)
    info = t.info

    sector = info.get("sector", "")
    industry = info.get("industry", "")
    market_cap = info.get("marketCap", 0)

    peers = []
    source = "unknown"

    # Strategy 1: Use industry lookup table
    if industry in INDUSTRY_PEERS:
        candidates = [p for p in INDUSTRY_PEERS[industry] if p != ticker]
        peers = candidates[:args.count]
        source = "industry_table"

    # Strategy 2: Hardcoded fallback
    if not peers and ticker in FALLBACK_PEERS:
        peers = FALLBACK_PEERS[ticker][:args.count]
        source = "hardcoded_fallback"

    # Strategy 3: Search by sector/industry via yfinance screener-style lookup
    if not peers and sector and industry:
        # Use a broader industry table match by checking partial matches
        for ind, tickers_list in INDUSTRY_PEERS.items():
            if ind.lower() in industry.lower() or industry.lower() in ind.lower():
                candidates = [p for p in tickers_list if p != ticker]
                if candidates:
                    peers = candidates[:args.count]
                    source = "partial_industry_match"
                    break

    # Enrich peer data
    enriched_peers = []
    for p in peers:
        try:
            pt = yf.Ticker(p)
            pi = pt.info
            enriched_peers.append({
                "ticker": p,
                "name": pi.get("shortName", p),
                "market_cap": pi.get("marketCap"),
                "sector": pi.get("sector", ""),
                "industry": pi.get("industry", ""),
                "trailing_pe": pi.get("trailingPE"),
                "forward_pe": pi.get("forwardPE"),
                "profit_margins": pi.get("profitMargins"),
            })
        except Exception:
            enriched_peers.append({"ticker": p, "name": p})

    result = {
        "ticker": ticker,
        "name": info.get("shortName", ticker),
        "sector": sector,
        "industry": industry,
        "market_cap": market_cap,
        "peer_count": len(enriched_peers),
        "peer_source": source,
        "peers": enriched_peers,
    }
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
