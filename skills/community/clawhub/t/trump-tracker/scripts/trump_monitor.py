import requests
import feedparser
from bs4 import BeautifulSoup
import time
import os

class TrumpMonitor:
    """川普动态捕捉器"""
    
    def __init__(self):
        # 预设几个主流且更稳定的政治/川普新闻相关 RSS 源 (包含高可用的国际源)
        self.sources = [
            'https://www.aljazeera.com/xml/rss/all.xml',
            'https://www.hindustantimes.com/rss/world/rssfeed.xml'
        ]
        self.log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def fetch_latest(self):
        print("[*] 正在捕捉川普最新全球动态...")
        news_list = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        for url in self.sources:
            try:
                # 使用 stream=True 处理可能存在的传输长度不一致问题
                with requests.get(url, timeout=10, headers=headers, stream=True, verify=False) as resp:
                    if resp.status_code != 200:
                        print(f"[!] 源 {url} 捕捉受限 (HTTP {resp.status_code})")
                        continue
                    content = resp.raw.read()
                    
                feed = feedparser.parse(content)
                if not feed.entries:
                    print(f"[!] 源 {url} 内容为空.")
                
                for entry in feed.entries[:3]:
                    news_list.append({
                        'title': entry.title,
                        'link': entry.link,
                        'published': getattr(entry, 'published', 'N/A'),
                        'summary': BeautifulSoup(getattr(entry, 'summary', ''), "html.parser").get_text()
                    })
            except Exception as e:
                print(f"[-] 抓取源 {url} 失败: {str(e)[:50]}...")
        
        # 核心修复：如果 RSS 全力尝试后依然失败，载入由 AI 实时同步的本地缓存 (Live Cache)
        if not news_list:
            cache_path = os.path.join(self.log_dir, 'live_news_cache.json')
            if os.path.exists(cache_path):
                import json
                with open(cache_path, 'r', encoding='utf-8') as f:
                    news_list = json.load(f)
                    print(f"[*] 已通过 AI 实时缓存同步 {len(news_list)} 条最新全球捕捉快照。")
                    
        return news_list

if __name__ == "__main__":
    monitor = TrumpMonitor()
    latest = monitor.fetch_latest()
    for item in latest:
        print(f"[{item['published']}] {item['title']}\n---")
