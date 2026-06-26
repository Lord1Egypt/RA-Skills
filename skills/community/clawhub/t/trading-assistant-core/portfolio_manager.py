#!/usr/bin/env python3
"""
Portfolio Manager - 持仓管理
独立版本，不依赖 TradingAgents
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import requests

# Security: Do not load .env files at runtime.
# API keys must be set via standard environment variables only.
# This prevents accidental exposure of unrelated secrets.

PORTFOLIO_FILE = Path(__file__).parent / "portfolio" / "holdings.json"
WATCHLIST_FILE = Path(__file__).parent / "watchlist.txt"

def load_portfolio():
    if not PORTFOLIO_FILE.exists():
        return create_default_portfolio()
    with open(PORTFOLIO_FILE) as f:
        return json.load(f)

def save_portfolio(portfolio):
    portfolio["last_updated"] = datetime.now().isoformat()
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=2, ensure_ascii=False)
    print(f"✅ 持仓已保存：{PORTFOLIO_FILE}")

def create_default_portfolio():
    portfolio = {
        "holdings": [],
        "total_market_value": 0,
        "total_cost_basis": 0,
        "total_unrealized_pnl": 0,
        "total_unrealized_pnl_pct": 0,
        "cash": 0,
        "last_updated": None
    }
    
    if WATCHLIST_FILE.exists():
        with open(WATCHLIST_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    symbol = parts[0].strip()
                    name = parts[1].strip() if len(parts) > 1 else symbol
                    notes = parts[2].strip() if len(parts) > 2 else ""
                    
                    portfolio["holdings"].append({
                        "symbol": symbol,
                        "name": name,
                        "shares": 0,
                        "avg_cost": 0,
                        "current_price": 0,
                        "market_value": 0,
                        "cost_basis": 0,
                        "unrealized_pnl": 0,
                        "unrealized_pnl_pct": 0,
                        "weight": 0,
                        "notes": notes
                    })
    
    save_portfolio(portfolio)
    return portfolio

def get_current_price(symbol):
    """Get price from Twelve Data API directly."""
    api_key = os.environ.get("TWELVE_DATA_API_KEY")
    if not api_key:
        return None
    
    try:
        import requests
        url = "https://api.twelvedata.com/price"
        params = {
            "symbol": symbol,
            "apikey": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "price" in data:
            return float(data["price"])
    except Exception as e:
        print(f"  ⚠️ {symbol}: {e}")
    
    return None

def update_prices(portfolio):
    """Update all prices."""
    print("📊 更新持仓价格...")
    
    for holding in portfolio["holdings"]:
        symbol = holding["symbol"]
        price = get_current_price(symbol)
        
        if price:
            old_price = holding["current_price"]
            holding["current_price"] = price
            holding["market_value"] = holding["shares"] * price
            holding["cost_basis"] = holding["shares"] * holding["avg_cost"]
            
            if holding["cost_basis"] > 0:
                holding["unrealized_pnl"] = holding["market_value"] - holding["cost_basis"]
                holding["unrealized_pnl_pct"] = (holding["unrealized_pnl"] / holding["cost_basis"]) * 100
            else:
                holding["unrealized_pnl"] = 0
                holding["unrealized_pnl_pct"] = 0
            
            change = ((price - old_price) / old_price * 100) if old_price > 0 else 0
            print(f"  {symbol}: ${old_price:.2f} → ${price:.2f} ({change:+.2f}%)")
        else:
            print(f"  ⚠️ {symbol}: 价格获取失败")
    
    portfolio["total_market_value"] = sum(h["market_value"] for h in portfolio["holdings"])
    portfolio["total_cost_basis"] = sum(h["cost_basis"] for h in portfolio["holdings"])
    portfolio["total_unrealized_pnl"] = sum(h["unrealized_pnl"] for h in portfolio["holdings"])
    
    if portfolio["total_cost_basis"] > 0:
        portfolio["total_unrealized_pnl_pct"] = (
            portfolio["total_unrealized_pnl"] / portfolio["total_cost_basis"]
        ) * 100
    
    total_value = portfolio["total_market_value"]
    for holding in portfolio["holdings"]:
        holding["weight"] = (holding["market_value"] / total_value * 100) if total_value > 0 else 0
    
    save_portfolio(portfolio)
    return portfolio

def add_holding(symbol, name, shares, avg_cost, notes=""):
    """Add or update holding."""
    portfolio = load_portfolio()
    
    for holding in portfolio["holdings"]:
        if holding["symbol"] == symbol:
            holding["shares"] = shares
            holding["avg_cost"] = avg_cost
            holding["notes"] = notes
            holding["name"] = name
            print(f"✅ 更新：{symbol}")
            save_portfolio(portfolio)
            return
    
    portfolio["holdings"].append({
        "symbol": symbol,
        "name": name,
        "shares": shares,
        "avg_cost": avg_cost,
        "current_price": 0,
        "market_value": 0,
        "cost_basis": 0,
        "unrealized_pnl": 0,
        "unrealized_pnl_pct": 0,
        "weight": 0,
        "notes": notes
    })
    print(f"✅ 添加：{symbol}")
    save_portfolio(portfolio)

def show_portfolio(portfolio=None):
    """Display portfolio."""
    if not portfolio:
        portfolio = load_portfolio()
    
    print("\n" + "=" * 80)
    print("📊 持仓概览")
    print("=" * 80)
    
    if not portfolio["holdings"]:
        print("⚠️ 暂无持仓")
        return
    
    print(f"\n{'股票':<8} {'名称':<35} {'数量':>8} {'成本':>10} {'现价':>10} {'市值':>12} {'盈亏':>12} {'占比':>8}")
    print("-" * 80)
    
    for h in portfolio["holdings"]:
        if h["shares"] == 0:
            continue
        
        pnl_str = f"{h['unrealized_pnl']:+,.2f}"
        pnl_pct_str = f"({h['unrealized_pnl_pct']:+.2f}%)"
        
        print(f"{h['symbol']:<8} {h['name'][:35]:<35} {h['shares']:>8,.0f} ${h['avg_cost']:>9.2f} ${h['current_price']:>9.2f} ${h['market_value']:>11,.2f} {pnl_str:>12} {pnl_pct_str:<6} {h['weight']:>5.1f}%")
    
    print("-" * 80)
    print(f"{'总计':<44} ${portfolio['total_market_value']:>11,.2f} {portfolio['total_unrealized_pnl']:>+12,.2f} ({portfolio['total_unrealized_pnl_pct']:+.2f}%)")
    print(f"{'总成本':<44} ${portfolio['total_cost_basis']:>11,.2f}")
    print("=" * 80)

def main():
    if len(sys.argv) < 2:
        print("用法：python3 portfolio_manager.py <command> [args]")
        print("\n命令:")
        print("  show                  - 显示持仓")
        print("  update                - 更新价格")
        print("  add <SYM> <NAME> <SHARES> <COST> [NOTES]")
        print("                        - 添加/更新持仓")
        print("  init                  - 从 watchlist 初始化")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "show":
        portfolio = load_portfolio()
        update_prices(portfolio)
        show_portfolio(portfolio)
    
    elif cmd == "update":
        portfolio = load_portfolio()
        update_prices(portfolio)
        show_portfolio(portfolio)
    
    elif cmd == "add":
        if len(sys.argv) < 6:
            print("用法：python3 portfolio_manager.py add <SYM> <NAME> <SHARES> <COST> [NOTES]")
            sys.exit(1)
        
        symbol = sys.argv[2].upper()
        name = sys.argv[3]
        shares = float(sys.argv[4])
        cost = float(sys.argv[5])
        notes = sys.argv[6] if len(sys.argv) > 6 else ""
        
        add_holding(symbol, name, shares, cost, notes)
    
    elif cmd == "init":
        print("🔄 从 watchlist 初始化...")
        create_default_portfolio()
        print("✅ 完成")
    
    else:
        print(f"❌ 未知命令：{cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
