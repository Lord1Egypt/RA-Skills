#!/usr/bin/env python3
"""Stock list manager - add, remove, list stocks"""

import json
import sys
import os
import urllib.request
import urllib.parse
import requests

STOCKS_FILE = os.path.join(os.path.dirname(__file__), 'stocks.json')

def load_stocks():
    if os.path.exists(STOCKS_FILE):
        with open(STOCKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_stocks(stocks):
    with open(STOCKS_FILE, 'w') as f:
        json.dump(stocks, f, indent=2)

def get_stock_name(symbol):
    """Get stock name from Yahoo Finance"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            result = data.get('chart', {}).get('result', [])
            if result:
                return result[0].get('meta', {}).get('longName') or symbol
    except Exception as e:
        print(f"⚠️ 获取名称失败: {e}")
    return symbol

def add_stock(symbol):
    symbol = symbol.upper().strip()
    stocks = load_stocks()
    
    if any(s['symbol'] == symbol for s in stocks):
        print(f"❌ {symbol} 已在监控列表中")
        return
    
    name = get_stock_name(symbol)
    stocks.append({'symbol': symbol, 'name': name})
    save_stocks(stocks)
    print(f"✅ 已添加 {symbol} ({name}) 到监控列表")

def remove_stock(symbol):
    symbol = symbol.upper().strip()
    stocks = load_stocks()
    original_len = len(stocks)
    stocks = [s for s in stocks if s['symbol'] != symbol]
    
    if len(stocks) == original_len:
        print(f"❌ {symbol} 不在监控列表中")
        return
    
    save_stocks(stocks)
    print(f"✅ 已从监控列表删除 {symbol}")

def list_stocks():
    stocks = load_stocks()
    if not stocks:
        print("📭 监控列表为空")
        return
    
    print("📈 监控列表：")
    for s in stocks:
        print(f"  • {s['symbol']} - {s['name']}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: stock_manager.py <add|remove|list> [股票代码]")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == 'add':
        if len(sys.argv) < 3:
            print("请指定股票代码")
            sys.exit(1)
        add_stock(sys.argv[2])
    elif cmd == 'remove':
        if len(sys.argv) < 3:
            print("请指定股票代码")
            sys.exit(1)
        remove_stock(sys.argv[2])
    elif cmd == 'list':
        list_stocks()
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
