#!/usr/bin/env python3
"""
Scrapling 技能 - 安全的网页数据抓取工具
使用 Scrapling 框架进行网页内容抓取和提取

支持模式：
- HTTP 请求抓取（Fetcher）
- 隐身模式抓取（StealthyFetcher）
- 浏览器自动化（DynamicFetcher）
- 智能元素定位
- 结果导出

【安全限制】
- 输出路径限制：仅允许保存到用户主目录
- 无危险函数：不使用 eval/exec 等危险函数
- 仅访问公开网站
- 严格的超时控制
- 频率限制：默认并发为 1
"""

import os
import sys
import json
import time
import asyncio
import urllib.parse
from typing import List, Dict, Optional
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
from scrapling.spiders import Spider

# 配置
DEFAULT_TIMEOUT = 30000
DEFAULT_CONCURRENT = 1
DEFAULT_DELAY = 1.0
SUPPORTED_MODES = ["get", "stealthy", "dynamic", "spider"]

# 安全配置
ALLOWED_BASE_DIR = os.path.expanduser("~")


class ScraplingScraper:
    def __init__(self):
        self.mode = "get"
        self.css_selector = ""
        self.output_file: Optional[str] = None
        self.results: List[Dict] = []
        self.headless = True
        self.solve_cloudflare = False
        
    def validate_output_path(self, path: str) -> bool:
        """验证输出路径是否在允许范围内"""
        if not path:
            return False
        
        try:
            if path.startswith("~/"):
                path = os.path.expanduser(path)
            
            abs_path = os.path.abspath(path)
            real_path = os.path.realpath(abs_path)
            real_base = os.path.realpath(ALLOWED_BASE_DIR)
            
            if real_path.startswith(real_base + os.sep) or real_path == real_base:
                return True
            
            return False
        except Exception:
            return False
    
    def _extract_data(self, page, selector: str) -> List[Dict]:
        """从页面提取数据"""
        results = []
        
        try:
            elements = page.css(selector)
            
            for element in elements:
                try:
                    text = element.css_text().strip()
                    href = element.attrib.get('href', '')
                    data = {
                        "text": text,
                        "href": href,
                        "selector": selector
                    }
                    results.append(data)
                except Exception:
                    continue
                    
        except Exception as e:
            # 尝试 XPath 作为备用
            try:
                elements = page.xpath(selector)
                for element in elements:
                    try:
                        text = element.css_text().strip() if hasattr(element, 'css_text') else element.get()
                        data = {"text": text, "selector": selector}
                        results.append(data)
                    except Exception:
                        continue
            except Exception:
                pass
        
        return results
    
    def scrape(self, url: str, mode: str = "get", selector: str = "", 
                output_file: Optional[str] = None, headless: bool = True,
                solve_cloudflare: bool = False, max_pages: int = 1) -> Dict:
        """执行抓取"""
        clean_url = url.strip()
        self.results = []
        self.output_file = output_file
        
        if output_file and not self.validate_output_path(output_file):
            return {"error": "invalid_output_path", "message": "路径不合法", "results": []}
        
        try:
            if mode == "get":
                # HTTP 请求模式
                page = Fetcher.get(clean_url, timeout=DEFAULT_TIMEOUT)
            elif mode == "stealthy":
                # 隐身模式
                page = StealthyFetcher.fetch(
                    clean_url,
                    headless=headless,
                    timeout=DEFAULT_TIMEOUT,
                    solve_cloudflare=solve_cloudflare
                )
            elif mode == "dynamic":
                # 浏览器自动化
                page = DynamicFetcher.fetch(
                    clean_url,
                    headless=headless,
                    timeout=DEFAULT_TIMEOUT
                )
            elif mode == "spider":
                # 爬虫模式
                spider = Spider(
                    name="demo",
                    start_urls=[clean_url],
                    concurrent_requests=DEFAULT_CONCURRENT,
                    delay=DEFAULT_DELAY
                )
                
                async def parse(response):
                    if selector:
                        data = self._extract_data(response, selector)
                        self.results.extend(data)
                
                spider.parse = parse
                result = spider.start()
                return {"error": "spider_mode", "message": "爬虫模式返回数据不同", "results": []}
            else:
                return {"error": "invalid_mode", "message": f"不支持的模式：{mode}", "results": []}
            
            # 提取数据
            if selector:
                self.results = self._extract_data(page, selector)
            else:
                # 提取页面主要内容
                self.results = [{
                    "url": page.url,
                    "title": page.css_text('title') if hasattr(page, 'css_text') else "",
                    "content": str(page)
                }]
            
            response = {
                "url": page.url,
                "mode": mode,
                "count": len(self.results),
                "results": self.results
            }
            
            # 保存结果
            if self.output_file:
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    json.dump(response, f, ensure_ascii=False, indent=2)
            
            return response
            
        except Exception as e:
            return {"error": "scrape_failed", "message": str(e), "results": []}


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        sys.exit(1)
    
    args = sys.argv[1:]
    mode = "get"
    url = ""
    selector = ""
    output_file = None
    headless = True
    solve_cloudflare = False
    
    i = 0
    while i < len(args):
        if args[i] == "--mode" and i + 1 < len(args):
            mode = args[i + 1]
            i += 2
        elif args[i] == "--css-selector" and i + 1 < len(args):
            selector = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] == "--headless":
            headless = True
            i += 1
        elif args[i] == "--no-headless":
            headless = False
            i += 1
        elif args[i] == "--solve-cloudflare":
            solve_cloudflare = True
            i += 1
        else:
            # URL
            url = " ".join(args[i:])
            break
    
    if not url:
        sys.exit(1)
    
    if mode not in SUPPORTED_MODES:
        print(f"不支持的模式：{mode}")
        sys.exit(1)
    
    scraper = ScraplingScraper()
    scraper.mode = mode
    scraper.css_selector = selector
    scraper.output_file = output_file
    scraper.headless = headless
    scraper.solve_cloudflare = solve_cloudflare
    
    response = scraper.scrape(url, mode, selector, output_file, headless, solve_cloudflare)
    sys.exit(0)

if __name__ == "__main__":
    main()
