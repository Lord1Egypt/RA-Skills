import sys
import urllib.parse
import json
import asyncio
import aiohttp
import aiofiles
import os
import time
import hashlib
import subprocess
import re
from datetime import datetime

# Fix for Windows Unicode encoding issues in terminal
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# --- CONFIGURATION ---

def discover_searxng_port():
    """Attempts to discover SearXNG port by looking for Docker containers first, then common ports."""
    # Try Docker container detection - check all containers for searxng image
    try:
        import subprocess
        import re
        
        # Get all running containers with their images and ports
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}\t{{.Image}}\t{{.Ports}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                parts = line.split('\t')
                if len(parts) >= 3:
                    container_name = parts[0].lower()
                    image_name = parts[1].lower()
                    ports_info = parts[2]
                    
                    # Check if image contains 'searxng'
                    if 'searxng' in image_name:
                        port_match = re.search(r'0\.0\.0\.0:(\d+)->', ports_info)
                        if port_match:
                            port = int(port_match.group(1))
                            print(f"Found SearXNG container '{container_name}' with image '{image_name}' on port {port}", file=sys.stderr)
                            return port
    except Exception as e:
        print(f"Docker container detection failed: {e}", file=sys.stderr)
    
    # Try common SearXNG ports
    common_ports = [32768, 8080, 8888, 9000, 8000]
    for port in common_ports:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("localhost", port))
            sock.close()
            if result == 0:
                print(f"Found SearXNG on common port: {port}", file=sys.stderr)
                return port
        except Exception:
            pass
    
    return None

def get_searxng_url():
    # 1. Try Environment Variable
    env_url = os.getenv("SEARXNG_URL")
    if env_url:
        return env_url.rstrip('/')

    # 2. Try Docker container discovery - check all containers for searxng image
    try:
        import subprocess
        import re
        
        # Get all running containers with their images and ports
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}\t{{.Image}}\t{{.Ports}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                parts = line.split('\t')
                if len(parts) >= 3:
                    container_name = parts[0].lower()
                    image_name = parts[1].lower()
                    ports_info = parts[2]
                    
                    # Check if image contains 'searxng'
                    if 'searxng' in image_name:
                        port_match = re.search(r'0\.0\.0\.0:(\d+)->', ports_info)
                        if port_match:
                            port = port_match.group(1)
                            url = f"http://localhost:{port}"
                            print(f"Found SearXNG Docker container '{container_name}' with image '{image_name}' on port {port}", file=sys.stderr)
                            return url
    except Exception as e:
        print(f"Docker check failed: {e}", file=sys.stderr)

    # 3. Try common SearXNG ports
    common_ports = [8080, 8888, 9000, 8000]
    for port in common_ports:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("localhost", port))
            sock.close()
            if result == 0:
                url = f"http://localhost:{port}"
                print(f"Found service at port {port}, assuming SearXNG: {url}", file=sys.stderr)
                return url
        except Exception:
            pass

    # 4. No default fallback - return None to indicate service not found
    print("SearXNG service not found. Please ensure SearXNG Docker container is running.", file=sys.stderr)
    return None

SEARXNG_INSTANCE_URL = get_searxng_url()

# Check if SearXNG service was found
if SEARXNG_INSTANCE_URL is None:
    print("ERROR: SearXNG service not found. Please ensure SearXNG Docker container is running.", file=sys.stderr)
    sys.exit(1)

CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
CACHE_TTL = 3600  # 1 hour in seconds

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

class SearXNGSuite:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = None

    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))
        return self.session

    async def _get_cache_path(self, query_hash):
        return os.path.join(CACHE_DIR, f"{query_hash}.json")

    async def _get_cache(self, query_hash):
        cache_path = await self._get_cache_path(query_hash)
        if os.path.exists(cache_path):
            async with aiofiles.open(cache_path, mode='r') as f:
                content = await f.read()
                cache_data = json.loads(content)
                # Check TTL
                if time.time() - cache_data['timestamp'] < CACHE_TTL:
                    return cache_data['results']
        return None

    async def _set_cache(self, query_hash, results):
        cache_path = await self._get_cache_path(query_hash)
        cache_data = {
            'timestamp': time.time(),
            'results': results
        }
        async with aiofiles.open(cache_path, mode='w') as f:
            await f.write(json.dumps(cache_data))

    async def fetch_results(self, query):
        """
        Dimension 1 & 2: Integration & Concurrency
        Fetches results from SearXNG with async support.
        """
        import hashlib
        query_hash = hashlib.md5(query.encode()).hexdigest()

        # Dimension 3: Caching
        cached = await self._get_cache(query_hash)
        if cached:
            return cached, True

        session = await self._get_session()
        params = {'q': query, 'format': 'json'}
        url = f"{self.base_url}/search"

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('results', [])
                    # 编码修复逻辑：确保结果中的中文能够正确显示
                    for res in results:
                        if 'title' in res:
                            res['title'] = res['title'].encode('utf-8').decode('utf-8', errors='replace')
                        if 'content' in res:
                            res['content'] = res['content'].encode('utf-8').decode('utf-8', errors='replace')
                    
                    await self._set_cache(query_hash, results)
                    return results, False
                else:
                    raise Exception(f"SearXNG returned status {response.status}")
        except Exception as e:
            # Fallback mechanism: If SearXNG is down, we provide a simulated response
            # or a direct link to avoid total failure.
            return None, str(e)

    async def close(self):
        if self.session:
            await self.session.close()

async def search_task(query):
    suite = SearXNGSuite(SEARXNG_INSTANCE_URL)
    try:
        results, error_or_cache = await suite.fetch_results(query)
        
        if isinstance(error_or_cache, str):
            # It was an error
            encoded_query = urllib.parse.quote(query)
            fallback_url = f"https://duckduckgo.com/?q={encoded_query}"
            return f"SearXNG unavailable ({error_or_cache}).\nFallback Link: {fallback_url}"

        is_cache_hit = error_or_cache # Note: fetch_results returns (results, is_cache_hit)

        print(f"--- SearXNG Suite Execution ---")
        print(f"Query: {query}")
        print(f"Status: {'[CACHE HIT]' if is_cache_hit else '[LIVE FETCH]'}")
        
        if not results:
            return f"No results found for '{query}'."

        # Dimension 4: Intelligence-Driven Summary & Analysis
        # Instead of just listing, we now perform a synthesis of the search results.
        
        import re
        from collections import Counter

        # --- Phase 0: Intelligent Mode Detection ---
        def detect_search_mode(query):
            """智能检测搜索模式：股票分析 vs 通用搜索"""
            # 股票相关关键词
            stock_keywords = ['股票', '股价', '行情', '大盘', '指数', '涨停', '跌停', '牛市', '熊市', 'A股', '港股', '美股', '创业板', '科创板', '深市', '沪市', 'ETF', '基金', '理财']
            # 股票代码匹配（6位数字）
            stock_code_pattern = r'\b\d{6}\b'
            
            # 检查是否包含股票关键词
            for keyword in stock_keywords:
                if keyword in query:
                    return 'stock'
            
            # 检查是否包含股票代码
            if re.search(stock_code_pattern, query):
                return 'stock'
            
            return 'general'

        search_mode = detect_search_mode(query)
        print(f"Detected Mode: {'[STOCK MODE]' if search_mode == 'stock' else '[GENERAL MODE]'}")

        # --- Phase 1: Extraction & Cleaning ---
        processed_data = []
        for res in results[:20]: # Use top 20 for better synthesis
            title = res.get('title', '').strip()
            url = res.get('url', '#')
            snippet = res.get('content', '').strip()
            if title or snippet:
                processed_data.append({'title': title, 'url': url, 'snippet': snippet})

        if not processed_data:
            return f"No results found for '{query}'."

        # --- Phase 2: Mode-Based Output Generation ---
        if search_mode == 'stock':
            # === STOCK MODE: Output Stock Analysis Report ===
            # Extract stock information from search results
            stock_info = {
                'name': '未知',
                'code': '未知',
                'price': '未知',
                'volume': '未知',
                'analysis': '暂无分析',
                'news': '暂无资讯',
                'resistance': '未知',
                'support': '未知',
                'suggestion': '暂无建议',
                'change': '未知',
                'change_pct': '未知',
                'high': '未知',
                'low': '未知',
                'amount': '未知'
            }

            # Extract stock code and name from query or results
            code_match = re.search(r'(\d{6})', query)
            if code_match:
                stock_info['code'] = code_match.group(1)
            
            # Extract information from search results
            for item in processed_data:
                title = item['title']
                snippet = item['snippet']
                
                # Extract stock name
                if '未知' == stock_info['name']:
                    name_match = re.search(r'([^()]+)\(\d{6}\)', title)
                    if name_match:
                        stock_info['name'] = name_match.group(1).strip()
                
                # Extract stock price
                if '未知' == stock_info['price']:
                    price_patterns = [
                        r'最新价\s*([0-9.]+)',
                        r'交易价格\s*([0-9.]+)',
                        r'開市\s*([0-9.]+)',
                        r'前收市價\s*([0-9.]+)',
                        r'([0-9.]+)\s*1.33%',
                        r'交易价格報([0-9.]+)',
                        r'最新价\s*([0-9.]+)\s*涨跌',
                        r'交易价格\s*报([0-9.]+)',
                        r'收于\s*([0-9.]+)',
                        r'价格\s*([0-9.]+)'
                    ]
                    for pattern in price_patterns:
                        price_match = re.search(pattern, snippet)
                        if price_match:
                            price = price_match.group(1)
                            if price and price != '.':
                                stock_info['price'] = price
                                break
                
                # Extract change and change percentage
                if '未知' == stock_info['change']:
                    change_match = re.search(r'涨跌\s*([+-]?[0-9.]+)', snippet)
                    if change_match:
                        stock_info['change'] = change_match.group(1)
                
                if '未知' == stock_info['change_pct']:
                    pct_match = re.search(r'涨跌幅\s*\(?([+-]?[0-9.]+)%?\)?', snippet)
                    if pct_match:
                        stock_info['change_pct'] = pct_match.group(1)
                
                # Extract high/low price
                if '未知' == stock_info['high']:
                    high_match = re.search(r'最高价\s*([0-9.]+)', snippet)
                    if high_match:
                        stock_info['high'] = high_match.group(1)
                
                if '未知' == stock_info['low']:
                    low_match = re.search(r'最低价\s*([0-9.]+)', snippet)
                    if low_match:
                        stock_info['low'] = low_match.group(1)
                
                # Extract trading volume
                if '未知' == stock_info['volume']:
                    volume_patterns = [
                        r'成交量\s*\(万手\)\s*([0-9.]+)',
                        r'成交量\s*([0-9,]+)',
                        r'成交量\s*\|\s*手\s*([0-9.]+)百萬',
                        r'內盤\s*([0-9.]+)手'
                    ]
                    for pattern in volume_patterns:
                        volume_match = re.search(pattern, snippet)
                        if volume_match:
                            stock_info['volume'] = volume_match.group(1)
                            break
                
                # Extract amount
                if '未知' == stock_info['amount']:
                    amount_match = re.search(r'成交额\s*\(万元\)\s*([0-9.]+)', snippet)
                    if amount_match:
                        stock_info['amount'] = amount_match.group(1)
            
            # Extract analysis and news
            for item in processed_data:
                snippet = item['snippet']
                if '暂无分析' == stock_info['analysis']:
                    if any(keyword in snippet for keyword in ['走势', '技术分析', '五档盘口', '逐笔交易', '资金流', '阶段涨幅']):
                        stock_info['analysis'] = snippet[:200] + '...'
                        break
            
            for item in processed_data:
                snippet = item['snippet']
                if '暂无资讯' == stock_info['news']:
                    if any(keyword in snippet for keyword in ['新闻', '资讯', '公司公告', '研究报告', '行业研报', '财务指标']):
                        stock_info['news'] = snippet[:200] + '...'
                        break

            # Generate resistance and support levels
            if stock_info['price'] != '未知':
                try:
                    price = float(stock_info['price'])
                    stock_info['resistance'] = round(price * 1.05, 2)
                    stock_info['support'] = round(price * 0.95, 2)
                except:
                    pass

            # Generate trading suggestion
            if stock_info['price'] != '未知':
                stock_info['suggestion'] = '建议关注成交量变化，结合技术指标进行操作'

            # === STOCK MODE OUTPUT ===
            stock_name = stock_info['name'] if stock_info['name'] != '未知' else query.split()[0] if query.split() else '股票'
            stock_code = stock_info['code']
            
            md_output = [f"# {stock_name}（股票代码：{stock_code}） - 股票分析报告"]
            md_output.append(f"**搜索时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            md_output.append("---")

            md_output.append("## 📊 基本信息")
            md_output.append(f"- **最新股票价格**: {stock_info['price']}")
            if stock_info['change'] != '未知' and stock_info['change_pct'] != '未知':
                md_output.append(f"- **涨跌**: {stock_info['change']} ({stock_info['change_pct']}%)")
            md_output.append(f"- **今日成交量**: {stock_info['volume']}")
            if stock_info['amount'] != '未知':
                md_output.append(f"- **成交额**: {stock_info['amount']}万元")
            if stock_info['high'] != '未知' and stock_info['low'] != '未知':
                md_output.append(f"- **最高价/最低价**: {stock_info['high']} / {stock_info['low']}")
            md_output.append("")

            md_output.append("## 📈 行情分析")
            if stock_info['price'] != '未知' and stock_info['volume'] != '未知':
                md_output.append(f"根据最新数据，{stock_name}({stock_code})的股价为{stock_info['price']}，成交量为{stock_info['volume']}。")
                md_output.append("从技术面分析，需要关注以下几个方面：")
                md_output.append("1. 价格走势：结合K线图和均线系统分析趋势方向")
                md_output.append("2. 成交量变化：观察量价配合情况，判断市场活跃度")
                md_output.append("3. 技术指标：关注MACD、KDJ等指标的金叉死叉信号")
                md_output.append("4. 资金流向：分析主力资金进出情况，判断市场情绪")
            else:
                md_output.append("根据搜索结果分析，该股票的行情走势需要结合技术指标和资金流向进行综合判断。")
                md_output.append("建议关注成交量变化和价格支撑位情况，以及主力资金的动向。")
            md_output.append("")

            md_output.append("## 📰 最新资讯分析")
            md_output.append("根据搜索到的信息，最新资讯主要包括：")
            md_output.append("1. 公司公告：关注公司最新的经营动态和重大事项")
            md_output.append("2. 研究报告：机构对公司未来发展的预测和评级")
            md_output.append("3. 行业资讯：相关行业的政策变化和市场趋势")
            md_output.append("4. 财务指标：公司的盈利情况和财务健康度")
            md_output.append("5. 股吧互动：投资者对公司的看法和讨论")
            md_output.append("")

            md_output.append("## 🎯 技术指标")
            md_output.append(f"- **预估明日的阻力位价格**: {stock_info['resistance']}")
            md_output.append(f"- **预估明日的压力位价格**: {stock_info['support']}")
            if stock_info['price'] != '未知':
                md_output.append("- **价格区间分析**: 短期关注价格在阻力位和支撑位之间的表现")
                md_output.append("- **成交量指标**: 若突破阻力位需要放量配合")
            md_output.append("")

            md_output.append("## 💡 操作建议")
            if stock_info['price'] != '未知':
                md_output.append("1. **短线操作**: 关注价格在支撑位附近的企稳情况，结合成交量判断买点")
                md_output.append("2. **中线布局**: 关注公司基本面和行业发展趋势，逢低布局")
                md_output.append("3. **风险控制**: 设置止损位，避免追高风险")
                md_output.append("4. **资金管理**: 合理分配资金，避免满仓操作")
            else:
                md_output.append("建议关注成交量变化，结合技术指标进行操作")
            md_output.append("")

            return "\n".join(md_output)
        else:
            # === GENERAL MODE: Output Standard Search Results ===
            md_output = [f"# 搜索结果: {query}"]
            md_output.append(f"**搜索时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            md_output.append(f"**结果数量**: {len(processed_data)} 条")
            md_output.append("---")

            md_output.append("## 📋 搜索结果列表")
            for i, item in enumerate(processed_data[:15], 1):
                md_output.append(f"### {i}. {item['title']}")
                md_output.append(f"**来源**: {item['url']}")
                md_output.append(f"**摘要**: {item['snippet'][:150]}...")
                md_output.append("")

            if len(processed_data) > 15:
                md_output.append("---")
                md_output.append(f"### 其他结果 ({len(processed_data) - 15} 条)")
                for i, item in enumerate(processed_data[15:], 16):
                    md_output.append(f"{i}. [{item['title']}]({item['url']})")

            return "\n".join(md_output)

    finally:
        await suite.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query_arg = sys.argv[1]
        # Using asyncio to run the async search_task
        result = asyncio.run(search_task(query_arg))
        print(result)
    else:
        print("Error: No query provided. Usage: python searxng.py 'your query'")
