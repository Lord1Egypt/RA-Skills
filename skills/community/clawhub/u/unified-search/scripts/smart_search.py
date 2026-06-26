#!/usr/bin/env python3
"""
智能搜索脚本 - 集成多种数据源
支持：百度搜索、Bing搜索、CoinGecko加密货币价格等
"""
import sys
import io
import json
import urllib.parse
import requests
import re
from bs4 import BeautifulSoup

# 修复 Windows 控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def is_crypto_query(query):
    """判断是否是加密货币相关查询"""
    crypto_keywords = ['btc', 'bitcoin', '比特币', 'eth', 'ethereum', '以太坊',
                       'crypto', '加密货币', '价格', 'price', '行情']
    query_lower = query.lower()
    return any(kw in query_lower for kw in crypto_keywords)

def get_crypto_price(query):
    """从 CoinGecko 获取加密货币实时价格"""
    try:
        # 确定要查询的币种
        coin_id = 'bitcoin'  # 默认 BTC
        if 'eth' in query.lower() or '以太坊' in query:
            coin_id = 'ethereum'
        
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd,cny&include_24hr_change=true&include_market_cap=true"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if coin_id in data:
            coin_data = data[coin_id]
            coin_name = "比特币" if coin_id == 'bitcoin' else "以太坊"
            symbol = "BTC" if coin_id == 'bitcoin' else "ETH"
            
            return [{
                "title": f"📊 {coin_name} ({symbol}) 实时价格",
                "url": "https://www.coingecko.com",
                "snippet": (
                    f"💰 美元: ${coin_data.get('usd', 'N/A'):,} USD | "
                    f"💴 人民币: ¥{coin_data.get('cny', 'N/A'):,} CNY | "
                    f"📈 24h变化: {coin_data.get('usd_24h_change', 0):+.2f}%"
                ),
                "source": "CoinGecko",
                "is_realtime": True
            }]
    except Exception as e:
        print(f"获取加密货币价格失败: {e}", file=sys.stderr)
    
    return []

def search_bing(query, max_results=5):
    """使用 Bing 搜索作为备选"""
    try:
        search_url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for result in soup.find_all('li', class_='b_algo'):
            title_elem = result.find('h2')
            link_elem = title_elem.find('a') if title_elem else None
            snippet_elem = result.find('p')
            
            if title_elem and link_elem:
                results.append({
                    "title": link_elem.get_text(strip=True),
                    "url": link_elem.get('href', ''),
                    "snippet": snippet_elem.get_text(strip=True) if snippet_elem else '',
                    "source": "Bing"
                })
                if len(results) >= max_results:
                    break
        
        return results
    except Exception as e:
        print(f"Bing搜索失败: {e}", file=sys.stderr)
        return []

def search_baidu(query, max_results=10):
    """使用百度搜索"""
    try:
        search_url = f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}&ie=utf-8"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        session = requests.Session()
        response = session.get(search_url, headers=headers, timeout=15, allow_redirects=True)
        
        # 检查是否有验证
        if 'verify' in response.url or '验证码' in response.text[:500]:
            return []
        
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for result in soup.find_all('div', class_='c-container'):
            title_elem = result.find('h3')
            if not title_elem:
                continue
            link_elem = title_elem.find('a')
            if not link_elem:
                continue
                
            title = link_elem.get_text(strip=True)
            url = link_elem.get('href', '')
            snippet = ""
            
            snippet_elem = result.find('div', class_='c-abstract')
            if snippet_elem:
                snippet = snippet_elem.get_text(strip=True)
            
            if url.startswith('//'):
                url = 'https:' + url
                
            if title and url and url.startswith('http'):
                results.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                    "source": "百度"
                })
                if len(results) >= max_results:
                    break
        
        return results
    except Exception as e:
        print(f"百度搜索失败: {e}", file=sys.stderr)
        return []

def smart_search(query):
    """智能搜索 - 根据查询类型选择最佳数据源"""
    all_results = []
    
    # 1. 检查是否是加密货币查询
    if is_crypto_query(query):
        print("检测到加密货币查询，使用 CoinGecko API...", file=sys.stderr)
        crypto_results = get_crypto_price(query)
        all_results.extend(crypto_results)
    
    # 2. 尝试百度搜索
    print("尝试百度搜索...", file=sys.stderr)
    baidu_results = search_baidu(query, max_results=5)
    all_results.extend(baidu_results)
    
    # 3. 如果百度结果少，补充 Bing 搜索
    if len(all_results) < 3:
        print("补充 Bing 搜索...", file=sys.stderr)
        bing_results = search_bing(query, max_results=5)
        all_results.extend(bing_results)
    
    # 4. 如果都没有结果，返回建议
    if not all_results:
        return [{
            "title": "💡 建议使用浏览器搜索",
            "url": "https://www.bing.com",
            "snippet": "建议使用 ClawX 的 browser 工具进行搜索，可以获得更完整的结果。",
            "suggestion": "browser"
        }]
    
    return all_results

def print_results_formatted(results):
    """格式化输出结果"""
    if not results:
        print("未找到搜索结果")
        return
        
    for i, result in enumerate(results, 1):
        if 'error' in result:
            print(f"❌ {result['error']}")
            if 'suggestion' in result:
                print(f"💡 {result['suggestion']}")
            continue
            
        source = result.get('source', '')
        source_tag = f" [{source}]" if source else ""
        
        print(f"\n{i}. {result.get('title', '无标题')}{source_tag}")
        if result.get('url'):
            print(f"   🔗 {result['url']}")
        if result.get('snippet'):
            snippet = result['snippet'][:250] + ('...' if len(result['snippet']) > 250 else '')
            print(f"   📝 {snippet}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Please provide a search query"}))
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    results = smart_search(query)
    
    if '--format' in sys.argv or '-f' in sys.argv:
        print_results_formatted(results)
    else:
        print(json.dumps(results, ensure_ascii=False))
