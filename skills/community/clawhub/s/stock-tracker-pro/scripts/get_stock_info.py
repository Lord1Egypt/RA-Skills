#!/usr/bin/env python3
"""Get stock info from Yahoo Finance - uses requests"""

import sys
import json
import requests
import urllib.parse
import subprocess
import os
import re

def get_company_news(company_name, symbol):
    """Get recent news about the company using Tavily Search"""
    try:
        # Search for recent news about the company
        query = f"{company_name} {symbol} stock news 2026"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try to find tavily script in workspace
        tavily_script = "/home/frank/.openclaw/workspace/skills/openclaw-tavily-search/scripts/tavily_search.py"
        
        result = subprocess.run(
            ["python3", tavily_script, "--query", query, "--max-results", "3", "--format", "brave"],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                news_items = data.get('results', [])
                if news_items:
                    output = []
                    for i, item in enumerate(news_items[:3], 1):
                        title = item.get('title', 'N/A')
                        url = item.get('url', '')
                        # Clean up snippet - remove HTML and limit length
                        snippet = item.get('snippet', '')
                        snippet = re.sub(r'<[^>]+>', '', snippet)  # Remove HTML tags
                        snippet = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', snippet)  # Convert markdown links to text
                        snippet = ' '.join(snippet.split())  # Normalize whitespace
                        snippet = snippet[:200] + '...' if len(snippet) > 200 else snippet
                        output.append(f"{i}. {title}\n   {snippet}\n   🔗 {url}")
                    return '\n\n'.join(output)
                return None
            except:
                return None
        return None
    except Exception as e:
        return None

def get_stock_info(symbol):
    symbol = symbol.upper().strip()
    
    try:
        # Yahoo Finance Chart API
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            print(f"❌ 获取失败: HTTP {r.status_code}")
            return
        
        data = r.json()
        result = data.get('chart', {}).get('result', [])
        
        if not result:
            print(f"❌ 未找到股票: {symbol}")
            return
        
        meta = result[0].get('meta', {})
        
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return
    
    # Extract data from meta
    name = meta.get('longName') or meta.get('shortName') or symbol
    price = meta.get('regularMarketPrice')
    prev_close = meta.get('previousClose')
    open_price = meta.get('regularMarketOpen')
    day_high = meta.get('regularMarketDayHigh')
    day_low = meta.get('regularMarketDayLow')
    volume = meta.get('regularMarketVolume')
    week52_high = meta.get('fiftyTwoWeekHigh')
    week52_low = meta.get('fiftyTwoWeekLow')
    currency = meta.get('currency', 'USD')
    exchange = meta.get('exchangeName')
    
    # Try to get additional info from quote endpoint
    try:
        url2 = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={urllib.parse.quote(symbol)}"
        r2 = requests.get(url2, headers=headers, timeout=10)
        if r2.status_code == 200:
            data2 = r2.json()
            quotes = data2.get('quoteResponse', {}).get('result', [])
            if quotes:
                q = quotes[0]
                market_cap = q.get('marketCap')
                pe_ratio = q.get('trailingPE')
                eps = q.get('epsTrailingTwelveMonths')
                dividend_yield = q.get('dividendYield')
                dividend_rate = q.get('dividendRate')
                pb_ratio = q.get('priceToBook')
                profit_margin = q.get('profitMargin')
                peg_ratio = q.get('pegRatio')
                beta = q.get('beta')
                sector = q.get('sector')
                industry = q.get('industry')
                avg_volume = q.get('averageVolume')
            else:
                market_cap = pe_ratio = eps = dividend_yield = dividend_rate = pb_ratio = profit_margin = peg_ratio = beta = sector = industry = avg_volume = None
        else:
            market_cap = pe_ratio = eps = dividend_yield = dividend_rate = pb_ratio = profit_margin = peg_ratio = beta = sector = industry = avg_volume = None
    except:
        market_cap = pe_ratio = eps = dividend_yield = dividend_rate = pb_ratio = profit_margin = peg_ratio = beta = sector = industry = avg_volume = None
    
    # Print results
    print(f"📊 {name} ({symbol})")
    print("=" * 45)
    
    if price:
        print(f"\n💰 价格信息 ({currency}):")
        print(f"   当前: ${price:.2f}")
        if open_price:
            print(f"   开盘: ${open_price:.2f}")
        if prev_close:
            change = price - prev_close
            change_pct = (change / prev_close) * 100
            color = "🟢" if change >= 0 else "🔴"
            sign = "+" if change >= 0 else ""
            print(f"   昨收: ${prev_close:.2f}")
            print(f"   涨跌: {color} ${sign}{change:.2f} ({sign}{change_pct:.2f}%)")
        if day_high and day_low:
            print(f"   日内: ${day_low:.2f} ~ ${day_high:.2f}")
    
    if market_cap:
        print(f"\n📈 市值: {format_market_cap(market_cap)}")
    
    if volume:
        print(f"   成交量: {format_num(volume)}")
    if avg_volume:
        print(f"   平均成交量: {format_num(avg_volume)}")
    
    if week52_high or week52_low:
        print(f"\n📅 52周区间: ${week52_low:.2f} ~ ${week52_high:.2f}")
    
    print(f"\n💵 估值指标:")
    if pe_ratio:
        print(f"   市盈率 (PE): {pe_ratio:.2f}")
    if pb_ratio:
        print(f"   市净率 (PB): {pb_ratio:.2f}")
    if eps:
        print(f"   每股收益 (EPS): ${eps:.2f}")
    if profit_margin:
        print(f"   利润率: {profit_margin*100:.2f}%")
    if peg_ratio:
        print(f"   PEG: {peg_ratio:.2f}")
    if beta:
        print(f"   Beta: {beta:.2f}")
    
    if dividend_yield or dividend_rate:
        print(f"\n💸 股息:")
        if dividend_rate:
            print(f"   股息: ${dividend_rate:.2f}/股")
        if dividend_yield:
            print(f"   收益率: {dividend_yield*100:.2f}%")
    
    if sector or industry:
        print(f"\n🏢 行业: {sector or 'N/A'}")
        if industry:
            print(f"   子行业: {industry}")
    if exchange:
        print(f"   交易所: {exchange}")
    
    # Get company news
    print(f"\n📰 最新新闻:")
    news = get_company_news(name, symbol)
    if news:
        print(news)
    else:
        print("   暂无新闻")
    
    print()

def format_market_cap(mc):
    if not mc:
        return "N/A"
    if mc >= 1e12:
        return f"${mc/1e12:.2f}T"
    elif mc >= 1e9:
        return f"${mc/1e9:.2f}B"
    elif mc >= 1e6:
        return f"${mc/1e6:.2f}M"
    return f"${mc:,.0f}"

def format_num(n):
    if not n:
        return "N/A"
    if n >= 1e9:
        return f"{n/1e9:.2f}B"
    elif n >= 1e6:
        return f"{n/1e6:.2f}M"
    elif n >= 1e3:
        return f"{n/1e3:.2f}K"
    return str(n)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: get_stock_info.py <股票代码>")
        sys.exit(1)
    
    get_stock_info(sys.argv[1])
