# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
XCrawl Scraper - OpenClaw Skill
XCrawl: AI-Powered Web Scraping API

支持功能:
- 网页爬取 (markdown/html/json/screenshot)
- 搜索
- 网站地图发现
- 站点爬取
"""

import os
import sys
import json
import time
from pathlib import Path

# 添加 SDK 路径
SCRIPT_DIR = Path(__file__).parent
SDK_DIR = SCRIPT_DIR.parent.parent

# 尝试导入 xcrawl
try:
    from xcrawl import XcrawlClient
    from xcrawl import XcrawlError, JobTimeoutError
    XCRAWL_AVAILABLE = True
except ImportError:
    XCRAWL_AVAILABLE = False

# 配置
CONFIG_PATH = SCRIPT_DIR / 'config.json'
DEFAULT_CONFIG = {
    'apiKey': '',
    'apiUrl': 'https://run.xcrawl.com',
    'timeout': 60,
    'defaultFormats': ['markdown'],
    'defaultProxy': ''
}

def load_config():
    """加载配置"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """保存配置"""
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_client():
    """获取 XCrawl 客户端"""
    if not XCRAWL_AVAILABLE:
        print("❌ 请先安装 xcrawl: pip install xcrawl")
        return None
    
    config = load_config()
    if not config.get('apiKey'):
        print("❌ 请先配置 API Key")
        print("   运行: python xcrawl_scraper.py set-key YOUR_API_KEY")
        return None
    
    return XcrawlClient(
        api_key=config['apiKey'],
        api_url=config.get('apiUrl', 'https://run.xcrawl.com'),
        timeout=config.get('timeout', 60)
    )

def scrape(url, formats=None, prompt='', json_schema=None, proxy='', async_mode=False):
    """爬取网页"""
    client = get_client()
    if not client:
        return None
    
    config = load_config()
    formats = formats or config.get('defaultFormats', ['markdown'])
    
    options = {
        'output': {'formats': formats}
    }
    
    # 添加 JSON 结构化提取
    if 'json' in formats and (prompt or json_schema):
        options['output']['json'] = {}
        if prompt:
            options['output']['json']['prompt'] = prompt
        if json_schema:
            options['output']['json']['json_schema'] = json_schema
    
    # 代理
    if proxy or config.get('defaultProxy'):
        options['proxy'] = {'location': proxy or config.get('defaultProxy')}
    
    # 异步模式
    if async_mode:
        options['mode'] = 'async'
    
    try:
        result = client.scrape(url, options)
        
        # 异步模式需要等待
        if async_mode or 'scrape_id' in result:
            scrape_id = result.get('scrape_id')
            print(f"📋 Job ID: {scrape_id}")
            print("⏳ 等待完成...")
            result = client.wait_for_job(scrape_id, timeout=120)
        
        return result
        
    except JobTimeoutError as e:
        print(f"⏱️ Job 超时: {e.job_id}")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def search(query, location='', language='en', limit=10):
    """搜索"""
    client = get_client()
    if not client:
        return None
    
    try:
        result = client.search({
            'query': query,
            'location': location,
            'language': language,
            'limit': limit
        })
        return result
    except Exception as e:
        print(f"❌ 搜索错误: {e}")
        return None

def map_site(url, filter_regex='', limit=1000, include_subdomains=False):
    """网站地图"""
    client = get_client()
    if not client:
        return None
    
    try:
        options = {
            'limit': limit,
            'include_subdomains': include_subdomains
        }
        if filter_regex:
            options['filter'] = filter_regex
        
        result = client.map(url, options)
        return result
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def crawl(url, limit=100, max_depth=3, formats=None):
    """爬取站点"""
    client = get_client()
    if not client:
        return None
    
    config = load_config()
    formats = formats or config.get('defaultFormats', ['markdown'])
    
    try:
        job = client.crawl(url, {
            'crawler': {
                'limit': limit,
                'max_depth': max_depth
            },
            'output': {'formats': formats}
        })
        
        crawl_id = job.get('crawl_id')
        print(f"📋 Crawl ID: {crawl_id}")
        print("⏳ 等待完成...")
        
        # 等待完成
        while True:
            status = client.get_crawl_status(crawl_id)
            print(f"状态: {status.get('status')}")
            if status.get('status') in ['completed', 'failed']:
                return status
            time.sleep(5)
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def set_api_key(key):
    """设置 API Key"""
    config = load_config()
    config['apiKey'] = key
    save_config(config)
    print(f"✅ API Key 已保存")

def show_config():
    """显示配置"""
    config = load_config()
    print("📋 当前配置:")
    api_key = config.get('apiKey', '')
    api_key_display = api_key[:20] + '...' if api_key and len(api_key) > 20 else (api_key if api_key else '(not set)')
    print(f"   API Key: {api_key_display}")
    print(f"   API URL: {config.get('apiUrl', 'https://run.xcrawl.com')}")
    print(f"   Timeout: {config.get('timeout', 60)}s")
    print(f"   默认格式: {config.get('defaultFormats', ['markdown'])}")

def main():
    if len(sys.argv) < 2:
        print("""
🕷️ XCrawl Scraper - OpenClaw Skill

使用方法:
  python xcrawl_scraper.py scrape <URL> [formats...]
  python xcrawl_scraper.py search <query>
  python xcrawl_scraper.py map <URL>
  python xcrawl_scraper.py crawl <URL>
  python xcrawl_scraper.py set-key <API_KEY>
  python xcrawl_scraper.py config

示例:
  python xcrawl_scraper.py scrape https://example.com markdown
  python xcrawl_scraper.py scrape https://example.com json "提取标题和价格" {"type":"object","properties":{"title":{"type":"string"}}}
  python xcrawl_scraper.py search "web scraping"
  python xcrawl_scraper.py set-key YOUR_API_KEY
""")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'scrape':
        if len(sys.argv) < 3:
            print("用法: python xcrawl_scraper.py scrape <URL> [formats...]")
            return
        url = sys.argv[2]
        formats = sys.argv[3:] if len(sys.argv) > 3 else ['markdown']
        
        print(f"🔍 正在爬取: {url}")
        result = scrape(url, formats)
        
        if result:
            print("\n✅ 结果:")
            data = result.get('data', {})
            for fmt in formats:
                if fmt in data:
                    content = data[fmt]
                    if isinstance(content, str) and len(content) > 2000:
                        print(f"\n--- {fmt} (前2000字符) ---")
                        print(content[:2000])
                        print("...")
                    else:
                        print(f"\n--- {fmt} ---")
                        print(content)
                elif fmt == 'screenshot':
                    if 'screenshot' in data:
                        print(f"📷 Screenshot available: {data['screenshot'][:100]}...")
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("用法: python xcrawl_scraper.py search <query>")
            return
        query = sys.argv[2]
        
        print(f"🔍 搜索: {query}")
        result = search(query)
        
        if result:
            print("\n✅ 搜索结果:")
            results = result.get('data', {}).get('organic_results', [])
            for i, r in enumerate(results[:10], 1):
                print(f"{i}. {r.get('title', 'N/A')}")
                print(f"   {r.get('url', '')}")
                print()
    
    elif command == 'map':
        if len(sys.argv) < 3:
            print("用法: python xcrawl_scraper.py map <URL>")
            return
        url = sys.argv[2]
        
        print(f"🗺️ 发现网站地图: {url}")
        result = map_site(url)
        
        if result:
            links = result.get('data', {}).get('links', [])
            print(f"\n✅ 发现 {len(links)} 个链接:")
            for link in links[:20]:
                print(f"  - {link}")
            if len(links) > 20:
                print(f"  ... 还有 {len(links) - 20} 个")
    
    elif command == 'crawl':
        if len(sys.argv) < 3:
            print("用法: python xcrawl_scraper.py crawl <URL>")
            return
        url = sys.argv[2]
        
        print(f"🕷️ 开始爬取站点: {url}")
        result = crawl(url)
        
        if result:
            print("\n✅ 爬取完成!")
            data = result.get('data', {})
            pages = data.get('pages', [])
            print(f"   爬取页面数: {len(pages)}")
    
    elif command == 'set-key':
        if len(sys.argv) < 3:
            print("用法: python xcrawl_scraper.py set-key <API_KEY>")
            return
        set_api_key(sys.argv[2])
    
    elif command == 'config':
        show_config()
    
    else:
        print(f"未知命令: {command}")

if __name__ == '__main__':
    main()
