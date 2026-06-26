#!/usr/bin/env python3
"""
Portfolio Optimizer - Rebalance, analyze risk, tax-loss harvest
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yfinance as yf
    import numpy as np
except ImportError:
    print("Install dependencies: pip install yfinance numpy pandas")
    raise

DEFAULT_DATA_DIR = Path.home() / ".openclaw" / "portfolio-optimizer"


def parse_holdings(holdings_str: str) -> dict:
    """Parse holdings string to dict."""
    holdings = {}
    for item in holdings_str.split(","):
        parts = item.strip().split(":")
        symbol = parts[0].upper()
        
        if len(parts) == 2:
            # Dollar value
            value = float(parts[1])
            holdings[symbol] = {"value": value, "shares": None, "cost": None}
        elif len(parts) == 3:
            # Shares and cost basis
            shares = float(parts[1])
            cost = float(parts[2])
            holdings[symbol] = {"value": None, "shares": shares, "cost": cost}
        elif len(parts) == 4:
            # Symbol:shares:cost:current_price (calculated value)
            shares = float(parts[1])
            cost = float(parts[2])
            current = float(parts[3])
            holdings[symbol] = {"value": shares * current, "shares": shares, "cost": cost}
    
    return holdings


def fetch_prices(symbols: list[str]) -> dict:
    """Fetch current prices for symbols."""
    prices = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            prices[symbol] = info.get("currentPrice", info.get("regularMarketPrice", 0))
        except:
            prices[symbol] = 0
    return prices


def calculate_allocation(holdings: dict, prices: dict) -> dict:
    """Calculate current allocation percentages."""
    total = 0
    for symbol, data in holdings.items():
        if data["value"] is None and data["shares"]:
            data["value"] = data["shares"] * prices.get(symbol, 0)
        total += data["value"] or 0
    
    allocation = {}
    for symbol, data in holdings.items():
        value = data["value"] or 0
        allocation[symbol] = {
            "value": value,
            "percent": (value / total * 100) if total > 0 else 0,
            "shares": data["shares"],
            "cost": data["cost"],
        }
    
    return {"total": total, "holdings": allocation}


def analyze_portfolio(holdings_str: str):
    """Analyze portfolio allocation and risk."""
    holdings = parse_holdings(holdings_str)
    symbols = list(holdings.keys())
    prices = fetch_prices(symbols)
    
    # Calculate allocation
    alloc = calculate_allocation(holdings, prices)
    total = alloc["total"]
    
    print(f"\n{'='*60}")
    print("PORTFOLIO ANALYSIS")
    print(f"{'='*60}")
    print(f"Total Value: ${total:,.2f}\n")
    
    print(f"{'Symbol':<10} {'Value':<15} {'Allocation':<12} {'Shares':<10}")
    print("-" * 50)
    
    for symbol, data in alloc["holdings"].items():
        print(f"{symbol:<10} ${data['value']:>12,.2f} {data['percent']:>10.2f}% {data['shares'] or 'N/A':>10}")
    
    # Sector exposure (if available)
    print(f"\n{'='*60}")
    print("SECTOR EXPOSURE")
    print(f"{'='*60}")
    
    sectors = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            sector = ticker.info.get("sector", "Unknown")
            value = holdings.get(symbol, {}).get("value", 0)
            sectors[sector] = sectors.get(sector, 0) + value
        except:
            pass
    
    for sector, value in sorted(sectors.items(), key=lambda x: x[1], reverse=True):
        pct = (value / total * 100) if total > 0 else 0
        print(f"{sector:<25} ${value:>12,.2f} {pct:>8.2f}%")
    
    # Risk metrics
    print(f"\n{'='*60}")
    print("RISK METRICS")
    print(f"{'='*60}")
    
    # Calculate portfolio volatility
    returns = []
    for symbol in symbols[:5]:  # Limit to 5 for speed
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1y")["Close"]
            if len(hist) > 1:
                ret = hist.pct_change().dropna()
                returns.append(ret)
        except:
            pass
    
    if returns:
        # Simple portfolio volatility (equal weighted)
        combined = np.mean(returns, axis=0)
        volatility = combined.std() * np.sqrt(252) * 100
        print(f"Annualized Volatility: {volatility:.2f}%")
        print(f"Daily Volatility: {volatility/np.sqrt(252):.2f}%")
    
    print(f"\nDiversification: {len(holdings)} positions")


def rebalance_portfolio(holdings_str: str, target_str: str):
    """Calculate rebalancing trades."""
    holdings = parse_holdings(holdings_str)
    symbols = list(holdings.keys())
    prices = fetch_prices(symbols)
    
    # Current allocation
    current = calculate_allocation(holdings, prices)
    total = current["total"]
    
    # Parse target allocation
    target = {}
    for item in target_str.split(","):
        symbol, pct = item.strip().split(":")
        target[symbol.upper()] = float(pct)
    
    print(f"\n{'='*60}")
    print("REBALANCING RECOMMENDATION")
    print(f"{'='*60}")
    print(f"Total Portfolio: ${total:,.2f}\n")
    
    print(f"{'Symbol':<10} {'Current %':<12} {'Target %':<12} {'Difference':<12} {'Action':<15}")
    print("-" * 65)
    
    all_symbols = set(current["holdings"].keys()) | set(target.keys())
    
    for symbol in sorted(all_symbols):
        curr_pct = current["holdings"].get(symbol, {}).get("percent", 0)
        target_pct = target.get(symbol, 0)
        diff = target_pct - curr_pct
        dollar_diff = diff / 100 * total
        price = prices.get(symbol, 0)
        shares_diff = int(dollar_diff / price) if price > 0 else 0
        
        if diff > 1:
            action = f"BUY {shares_diff} shares"
        elif diff < -1:
            action = f"SELL {abs(shares_diff)} shares"
        else:
            action = "HOLD"
        
        print(f"{symbol:<10} {curr_pct:>10.2f}% {target_pct:>11}% {diff:>+11.2f}% {action:<15}")
    
    # Calculate trading costs
    print(f"\nNote: Consider tax implications and trading costs before executing.")


def tax_loss_harvest(holdings_str: str):
    """Find tax-loss harvesting opportunities."""
    holdings = parse_holdings(holdings_str)
    symbols = list(holdings.keys())
    prices = fetch_prices(symbols)
    
    print(f"\n{'='*60}")
    print("TAX-LOSS HARVESTING OPPORTUNITIES")
    print(f"{'='*60}\n")
    
    print(f"{'Symbol':<10} {'Cost Basis':<15} {'Current Value':<15} {'Gain/Loss':<15} {'Term':<10}")
    print("-" * 65)
    
    total_loss = 0
    total_gain = 0
    
    for symbol, data in holdings.items():
        if data["shares"] and data["cost"]:
            cost_basis = data["shares"] * data["cost"]
            current_value = data["shares"] * prices.get(symbol, 0)
            gain_loss = current_value - cost_basis
            
            term = "Long"  # Assume long-term for simplicity
            
            if gain_loss < 0:
                total_loss += abs(gain_loss)
                print(f"{symbol:<10} ${cost_basis:>12,.2f} ${current_value:>12,.2f} ${gain_loss:>+12,.2f} {term:<10} 🔽")
            else:
                total_gain += gain_loss
                print(f"{symbol:<10} ${cost_basis:>12,.2f} ${current_value:>12,.2f} ${gain_loss:>+12,.2f} {term:<10} 🔼")
    
    print("-" * 65)
    print(f"Total Losses:   ${total_loss:,.2f}")
    print(f"Total Gains:   ${total_gain:,.2f}")
    print(f"Net:           ${total_gain - total_loss:,.2f}")
    
    if total_loss > 0:
        print(f"\n💡 These losses can offset capital gains or up to $3,000 of ordinary income.")
        print(f"💡 Watch for wash sale rule (30 days before/after sale).")


def main():
    parser = argparse.ArgumentParser(description="Portfolio Optimizer")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analyze portfolio")
    analyze_parser.add_argument("--holdings", required=True, help="Holdings (SYMBOL:VALUE or SYMBOL:SHARES:COST)")
    
    # Rebalance
    rebal_parser = subparsers.add_parser("rebalance", help="Calculate rebalancing trades")
    rebal_parser.add_argument("--holdings", required=True, help="Current holdings")
    rebal_parser.add_argument("--target", required=True, help="Target allocation (SYMBOL:PCT)")
    
    # Tax-loss harvest
    harvest_parser = subparsers.add_parser("harvest", help="Find tax-loss opportunities")
    harvest_parser.add_argument("--holdings", required=True, help="Holdings with cost basis")
    harvest_parser.add_argument("--file", help="JSON file with holdings")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        analyze_portfolio(args.holdings)
    elif args.command == "rebalance":
        rebalance_portfolio(args.holdings, args.target)
    elif args.command == "harvest":
        tax_loss_harvest(args.holdings)


if __name__ == "__main__":
    main()
