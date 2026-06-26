#!/usr/bin/env python3
"""
Crypto Monitor - Price alerts, whale tracking, on-chain metrics
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    raise

DEFAULT_DATA_DIR = Path.home() / ".openclaw" / "crypto-monitor"
DEFAULT_DATA_DIR.mkdir(parents=True, exist_ok=True)

# CoinGecko API (free tier)
BASE_URL = "https://api.coingecko.com/api/v3"

# Common crypto mapping (symbol -> id)
CRYPTO_MAP = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "ada": "cardano",
    "xrp": "ripple",
    "dot": "polkadot",
    "matic": "matic-network",
    "avax": "avalanche-2",
    "link": "chainlink",
    "doge": "dogecoin",
    "shib": "shiba-inu",
    "ltc": "litecoin",
    "atom": "cosmos",
    "uni": "uniswap",
    "etc": "ethereum-classic",
}


def get_crypto_id(symbol: str) -> str:
    """Convert symbol to CoinGecko ID."""
    symbol = symbol.lower()
    return CRYPTO_MAP.get(symbol, symbol)


def fetch_prices(symbols: list[str], vs_currency: str = "usd") -> dict:
    """Fetch current prices for cryptocurrencies."""
    ids = [get_crypto_id(s) for s in symbols]
    ids_str = ",".join(ids)
    
    url = f"{BASE_URL}/simple/price"
    params = {
        "ids": ids_str,
        "vs_currencies": vs_currency,
        "include_24hr_change": "true",
        "include_market_cap": "true",
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return {}


def fetch_market_data(symbols: list[str]) -> dict:
    """Fetch detailed market data."""
    ids = [get_crypto_id(s) for s in symbols]
    ids_str = ",".join(ids)
    
    url = f"{BASE_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ids_str,
        "order": "market_cap_desc",
        "per_page": len(ids),
        "page": 1,
        "sparkline": "false",
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return {coin["symbol"].upper(): coin for coin in response.json()}
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return {}


def fetch_onchain_stats(symbol: str) -> dict:
    """Fetch on-chain statistics."""
    coin_id = get_crypto_id(symbol)
    url = f"{BASE_URL}/coins/{coin_id}"
    params = {
        "localization": "false",
        "tickers": "false",
        "community_data": "false",
        "developer_data": "false",
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            "market_data": data.get("market_data", {}),
            "descriptiondescription", {}).": data.get("get("en", "")[:200],
        }
    except Exception as e:
        print(f"Error fetching on-chain stats: {e}")
        return {}


def check_alerts(prices: dict):
    """Check if any alerts should trigger."""
    alerts_file = DEFAULT_DATA_DIR / "alerts.json"
    if not alerts_file.exists():
        return
    
    with open(alerts_file) as f:
        alerts = json.load(f)
    
    triggered = []
    for alert in alerts:
        symbol = alert["symbol"].upper()
        if symbol not in prices:
            continue
        
        price = prices[symbol].get("usd", 0)
        
        if "above" in alert and price >= alert["above"]:
            triggered.append(f"🔔 {symbol} above ${alert['above']:.2f} (now ${price:.2f})")
        if "below" in alert and price <= alert["below"]:
            triggered.append(f"🔔 {symbol} below ${alert['below']:.2f} (now ${price:.2f})")
    
    if triggered:
        print("\n⚠️  TRIGGERED ALERTS:")
        for t in triggered:
            print(f"  {t}")


def show_prices(symbols: list[str]):
    """Display cryptocurrency prices."""
    data = fetch_market_data(symbols)
    
    if not data:
        print("No data found")
        return
    
    print(f"\n{'='*70}")
    print(f"{'Crypto':<10} {'Price':<15} {'24h %':<10} {'Market Cap':<15} {'Volume':<15}")
    print("-" * 70)
    
    for symbol, coin in data.items():
        price = coin.get("current_price", 0)
        change = coin.get("price_change_percentage_24h", 0)
        mcap = coin.get("market_cap", 0)
        volume = coin.get("total_volume", 0)
        
        change_str = f"{change:+.2f}%" if change else "N/A"
        
        print(f"{symbol:<10} ${price:>12,.2f} {change_str:<10} ${mcap/1e9:>12,.2f}B ${volume/1e9:>12,.2f}B")
    
    # Check alerts
    prices = {s.upper(): {"usd": data[s]["current_price"]} for s in data}
    check_alerts(prices)


def manage_alert(symbol: str, above: Optional[float] = None, below: Optional[float] = None):
    """Set a price alert."""
    alerts_file = DEFAULT_DATA_DIR / "alerts.json"
    
    # Load existing alerts
    if alerts_file.exists():
        with open(alerts_file) as f:
            alerts = json.load(f)
    else:
        alerts = []
    
    # Add new alert
    alert = {"symbol": symbol.upper()}
    if above:
        alert["above"] = above
    if below:
        alert["below"] = below
    
    alerts.append(alert)
    
    # Save
    with open(alerts_file, "w") as f:
        json.dump(alerts, f, indent=2)
    
    print(f"✅ Alert set for {symbol.upper()}")
    if above:
        print(f"   Above: ${above:,.2f}")
    if below:
        print(f"   Below: ${below:,.2f}")


def list_alerts():
    """List all active alerts."""
    alerts_file = DEFAULT_DATA_DIR / "alerts.json"
    
    if not alerts_file.exists():
        print("No alerts set")
        return
    
    with open(alerts_file) as f:
        alerts = json.load(f)
    
    print(f"\n{'='*50}")
    print("ACTIVE ALERTS")
    print("=" * 50)
    
    for i, alert in enumerate(alerts, 1):
        conditions = []
        if "above" in alert:
            conditions.append(f"Above ${alert['above']:,.2f}")
        if "below" in alert:
            conditions.append(f"Below ${alert['below']:,.2f}")
        
        print(f"{i}. {alert['symbol']}: {' & '.join(conditions)}")


def show_onchain_stats(symbol: str):
    """Display on-chain statistics."""
    stats = fetch_onchain_stats(symbol)
    
    if not stats:
        print("No data found")
        return
    
    market = stats.get("market_data", {})
    
    print(f"\n{'='*50}")
    print(f"{symbol.upper()} ON-CHAIN STATS")
    print("=" * 50)
    
    print(f"Current Price:    ${market.get('current_price', {}).get('usd', 'N/A'):,.2f}")
    print(f"24h High:         ${market.get('high_24h', {}).get('usd', 'N/A'):,.2f}")
    print(f"24h Low:          ${market.get('low_24h', {}).get('usd', 'N/A'):,.2f}")
    print(f"24h Change:       {market.get('price_change_percentage_24h', 'N/A'):.2f}%")
    print(f"Market Cap:       ${market.get('market_cap', {}).get('usd', 0)/1e9:.2f}B")
    print(f"24h Volume:       ${market.get('total_volume', {}).get('usd', 0)/1e9:.2f}B")
    print(f"Circulating:      {market.get('circulating_supply', 0)/1e6:.2f}M")
    print(f"Total Supply:     {market.get('total_supply', 0)/1e6:.2f}M")
    print(f"Max Supply:       {market.get('max_supply', 'N/A')}")
    
    if market.get("ath"):
        print(f"\nAll-Time High:    ${market['ath']['usd']:,.2f}")
        print(f"ATH Change:       {market['ath_change_percentage']['usd']:.2f}%")


def portfolio(portfolio_str: Optional[str] = None, show: bool = False):
    """Manage crypto portfolio."""
    portfolio_file = DEFAULT_DATA_DIR / "portfolio.json"
    
    if show:
        if not portfolio_file.exists():
            print("No portfolio found")
            return
        
        with open(portfolio_file) as f:
            portfolio = json.load(f)
        
        symbols = list(portfolio.keys())
        prices = fetch_prices(symbols)
        
        total = 0
        print(f"\n{'='*60}")
        print("CRYPTO PORTFOLIO")
        print("=" * 60)
        print(f"{'Asset':<10} {'Amount':<15} {'Price':<12} {'Value':<15} {'P/L':<12}")
        print("-" * 60)
        
        for symbol, data in portfolio.items():
            amount = data["amount"]
            cost_basis = data.get("cost_basis", 0)
            
            price = prices.get(get_crypto_id(symbol), {}).get("usd", 0)
            value = amount * price
            pnl = value - (amount * cost_basis) if cost_basis else 0
            pnl_pct = (pnl / (amount * cost_basis) * 100) if cost_basis and cost_basis > 0 else 0
            
            total += value
            
            pnl_str = f"${pnl:+,} ({pnl_pct:+.1f}%)"
            
            print(f"{symbol.upper():<10} {amount:<15.4f} ${price:<11,.2f} ${value:<14,.2f} {pnl_str:<12}")
        
        print("-" * 60)
        print(f"Total Value:      ${total:,.2f}")
        
        return
    
    # Add to portfolio
    if portfolio_str:
        if portfolio_file.exists():
            with open(portfolio_file) as f:
                portfolio = json.load(f)
        else:
            portfolio = {}
        
        for item in portfolio_str.split(","):
            symbol, amount = item.strip().split(":")
            symbol = symbol.upper()
            amount = float(amount)
            
            portfolio[symbol] = {
                "amount": amount,
                "cost_basis": 0,  # TODO: Add cost basis
                "added": datetime.now().isoformat(),
            }
        
        with open(portfolio_file, "w") as f:
            json.dump(portfolio, f, indent=2)
        
        print(f"✅ Added {amount} {symbol} to portfolio")


def main():
    parser = argparse.ArgumentParser(description="Crypto Monitor")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Price
    price_parser = subparsers.add_parser("price", help="Check prices")
    price_parser.add_argument("symbols", nargs="+", help="Crypto symbols (BTC ETH SOL)")
    
    # Alert
    alert_parser = subparsers.add_parser("alert", help="Set price alert")
    alert_parser.add_argument("--symbol", required=True, help="Crypto symbol")
    alert_parser.add_argument("--above", type=float, help="Alert when price above")
    alert_parser.add_argument("--below", type=float, help="Alert when price below")
    
    # Alerts list
    subparsers.add_parser("alerts", help="List active alerts")
    
    # Stats
    stats_parser = subparsers.add_parser("stats", help="On-chain stats")
    stats_parser.add_argument("symbol", help="Crypto symbol")
    
    # Whales (placeholder)
    whales_parser = subparsers.add_parser("whales", help="Track whale transactions")
    whales_parser.add_argument("--symbol", required=True, help="Crypto symbol")
    whales_parser.add_argument("--min-value", type=float, default=1000000, help="Min transaction value")
    
    # Portfolio
    portfolio_parser = subparsers.add_parser("portfolio", help="Manage portfolio")
    portfolio_parser.add_argument("--add", help="Add to portfolio (SYMBOL:AMOUNT)")
    portfolio_parser.add_argument("--show", action="store_true", help="Show portfolio")
    
    args = parser.parse_args()
    
    if args.command == "price":
        show_prices(args.symbols)
    elif args.command == "alert":
        manage_alert(args.symbol, args.above, args.below)
    elif args.command == "alerts":
        list_alerts()
    elif args.command == "stats":
        show_onchain_stats(args.symbol)
    elif args.command == "whales":
        print("Whale tracking requires blockchain API (Blockstream, Etherscan)")
        print(f"Monitoring {args.symbol} for transactions > ${args.min_value:,}")
    elif args.command == "portfolio":
        portfolio(args.add, args.show)


if __name__ == "__main__":
    main()
