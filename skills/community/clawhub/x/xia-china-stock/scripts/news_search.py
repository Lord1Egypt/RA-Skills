#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一资讯搜索模块 - Unified News Search Module
优先级：妙想API > 智谱搜索 > Tavily搜索
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any


class NewsSearchResult:
    """资讯搜索结果"""
    
    def __init__(self, query: str, items: List[Dict[str, Any]], source: str):
        self.query = query
        self.items = items  # [{"title": "", "content": "", "date": "", "source": "", "url": ""}]
        self.source = source
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'query': self.query,
            'items': self.items,
            'source': self.source,
            'timestamp': self.timestamp
        }
    
    def format_markdown(self, max_items: int = 5) -> str:
        """格式化为 Markdown"""
        if not self.items:
            return f"**查询**: {self.query}\n\n未找到相关资讯"
        
        lines = [
            f"**查询**: {self.query}",
            f"**数据源**: {self.source}",
            f"**结果数**: {len(self.items)}",
            ""
        ]
        
        for i, item in enumerate(self.items[:max_items], 1):
            lines.append(f"### {i}. {item.get('title', '无标题')}")
            
            meta = []
            if item.get('date'):
                meta.append(f"日期: {item['date']}")
            if item.get('source'):
                meta.append(f"来源: {item['source']}")
            if item.get('rating'):
                meta.append(f"评级: {item['rating']}")
            
            if meta:
                lines.append(" | ".join(meta))
            
            if item.get('content'):
                lines.append("")
                # 限制内容长度
                content = item['content'][:500]
                if len(item['content']) > 500:
                    content += "..."
                lines.append(content)
            
            lines.append("")
        
        return "\n".join(lines)


class NewsSearchBackend:
    """资讯搜索后端基类"""
    
    def __init__(self, name: str, priority: int):
        self.name = name
        self.priority = priority
    
    def is_available(self) -> bool:
        raise NotImplementedError
    
    def search(self, query: str, max_results: int = 5) -> Optional[NewsSearchResult]:
        raise NotImplementedError


class WebSearchBackend(NewsSearchBackend):
    """Web search backend using requests - free, no API key needed"""
    
    def __init__(self):
        super().__init__("Web Search", priority=1)
    
    def is_available(self) -> bool:
        try:
            import requests
            return True
        except ImportError:
            return False
    
    def search(self, query: str, max_results: int = 5) -> Optional[NewsSearchResult]:
        try:
            import requests
            # Use a simple search via multiple free sources
            items = []
            
            # Source 1: Bing news search (no key needed for basic)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            # Try Sina Finance news API for stock-related queries
            if any(kw in query for kw in ['股', 'stock', 'A股', '港股', '基金', '研报']):
                try:
                    # Sina Finance search
                    url = f'https://search.sina.com.cn/news?q={query}&c=news&sort=time'
                    resp = requests.get(url, headers=headers, timeout=10)
                    # Parse basic results from HTML
                    import re
                    titles = re.findall(r'<h2[^>]*><a[^>]*>([^<]+)</a>', resp.text)[:max_results]
                    for title in titles:
                        items.append({'title': title.strip(), 'content': '', 'date': '', 'source': 'Sina', 'rating': '', 'type': 'NEWS', 'url': ''})
                except:
                    pass
            
            if not items:
                # Fallback: generate a note that search requires user's own search tool
                return None
            
            return NewsSearchResult(query, items, self.name)
        except Exception as e:
            print(f"Web search failed: {e}")
            return None


class ZhipuSearchBackend(NewsSearchBackend):
    """智谱搜索后端 (优先级2) - 通过MCP"""
    
    def __init__(self):
        super().__init__("智谱搜索", priority=2)
    
    def is_available(self) -> bool:
        # 检查 mcporter 命令是否可用
        try:
            result = subprocess.run(
                ['mcporter', '--help'],
                capture_output=True,
                timeout=5,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def search(self, query: str, max_results: int = 5) -> Optional[NewsSearchResult]:
        try:
            # 调用 mcporter
            result = subprocess.run(
                ['mcporter', 'call', 'zhipu-search.web_search_prime', '--arg', f'query={query}'],
                capture_output=True,
                timeout=30,
                text=True
            )
            
            if result.returncode != 0:
                return None
            
            # 解析 JSON 结果
            output = result.stdout
            data = json.loads(output)
            
            # 转换为统一格式
            items = []
            # 这里需要根据实际的智谱搜索API返回格式进行解析
            # 假设返回格式类似：{"results": [...]}
            for item in data.get('results', [])[:max_results]:
                items.append({
                    'title': item.get('title', ''),
                    'content': item.get('content', item.get('snippet', '')),
                    'date': item.get('date', ''),
                    'source': item.get('source', ''),
                    'rating': '',
                    'type': 'NEWS',
                    'url': item.get('url', '')
                })
            
            if not items:
                return None
            
            return NewsSearchResult(query, items, self.name)
            
        except Exception as e:
            print(f"智谱搜索失败: {e}")
            return None


class TavilySearchBackend(NewsSearchBackend):
    """Tavily搜索后端 (优先级3) - 通过本地脚本"""
    
    def __init__(self):
        super().__init__("Tavily搜索", priority=3)
        self.tavily_script = Path(__file__).parent.parent.parent / "tavily-search-1.0.0" / "scripts" / "search.mjs"
    
    def is_available(self) -> bool:
        return self.tavily_script.exists()
    
    def search(self, query: str, max_results: int = 5) -> Optional[NewsSearchResult]:
        if not self.tavily_script.exists():
            return None
        
        try:
            # 调用 Tavily 脚本
            result = subprocess.run(
                ['node', str(self.tavily_script), query, '--max-results', str(max_results)],
                capture_output=True,
                timeout=30,
                text=True
            )
            
            if result.returncode != 0:
                return None
            
            # 解析 JSON 结果
            output = result.stdout
            data = json.loads(output)
            
            # 转换为统一格式
            items = []
            for item in data.get('results', [])[:max_results]:
                items.append({
                    'title': item.get('title', ''),
                    'content': item.get('content', ''),
                    'date': item.get('published_date', ''),
                    'source': item.get('source', ''),
                    'rating': '',
                    'type': 'NEWS',
                    'url': item.get('url', '')
                })
            
            if not items:
                return None
            
            return NewsSearchResult(query, items, self.name)
            
        except Exception as e:
            print(f"Tavily搜索失败: {e}")
            return None


class NewsSearchManager:
    """统一资讯搜索管理器"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        
        # Initialize all search backends (no API key required)
        self.backends: List[NewsSearchBackend] = [
            WebSearchBackend(),
            ZhipuSearchBackend(),
            TavilySearchBackend()
        ]
        
        # 按优先级排序
        self.backends.sort(key=lambda b: b.priority)
    
    def search(self, query: str, max_results: int = 5) -> Optional[NewsSearchResult]:
        """使用 fallback 机制搜索资讯"""
        for backend in self.backends:
            if not backend.is_available():
                continue
            
            try:
                result = backend.search(query, max_results)
                
                if result and result.items:
                    print(f"✅ 资讯来源: {backend.name} (找到 {len(result.items)} 条)")
                    return result
                    
            except Exception as e:
                print(f"⚠️ {backend.name} 搜索失败: {e}")
                continue
        
        print("❌ 所有资讯源均搜索失败")
        return None
    
    def search_stock_news(self, symbol: str, name: str, max_results: int = 5) -> Optional[NewsSearchResult]:
        """
        搜索股票相关资讯
        :param symbol: 股票代码 (如 002475.SZ)
        :param name: 股票名称 (如 立讯精密)
        :param max_results: 最大结果数
        """
        # 生成搜索查询
        queries = [
            f"{name}最新研报",
            f"{name}机构观点",
            f"{name}最新消息"
        ]
        
        all_results = []
        seen_titles = set()
        
        for query in queries:
            result = self.search(query, max_results=2)
            
            if result:
                for item in result.items:
                    # 去重
                    title = item.get('title', '')
                    if title and title not in seen_titles:
                        seen_titles.add(title)
                        all_results.append(item)
        
        if not all_results:
            return None
        
        # 限制总结果数
        all_results = all_results[:max_results]
        
        return NewsSearchResult(
            query=f"{name}相关资讯",
            items=all_results,
            source="综合搜索"
        )


def search_stock_news(symbol: str, name: str, max_results: int = 5, api_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    便捷函数：搜索股票相关资讯
    :param symbol: 股票代码
    :param name: 股票名称
    :param max_results: 最大结果数
    :param api_key: 妙想API密钥（可选）
    :return: 字典格式的搜索结果
    """
    manager = NewsSearchManager(api_key)
    result = manager.search_stock_news(symbol, name, max_results)
    
    return result.to_dict() if result else None


def main():
    """测试入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='统一资讯搜索模块')
    parser.add_argument('query', nargs='?', help='搜索查询')
    parser.add_argument('--symbol', help='股票代码')
    parser.add_argument('--name', help='股票名称')
    parser.add_argument('--max-results', type=int, default=5, help='最大结果数')
    
    args = parser.parse_args()
    
    if args.symbol and args.name:
        # 搜索股票资讯
        print(f"🔍 搜索 {args.name} ({args.symbol}) 相关资讯...\n")
        result = search_stock_news(args.symbol, args.name, args.max_results)
    elif args.query:
        # 通用搜索
        print(f"🔍 搜索: {args.query}...\n")
        manager = NewsSearchManager()
        result_obj = manager.search(args.query, args.max_results)
        result = result_obj.to_dict() if result_obj else None
    else:
        print("请提供搜索查询或股票代码和名称")
        return
    
    if result:
        print("\n" + "="*80)
        # 格式化输出
        result_obj = NewsSearchResult(
            result['query'],
            result['items'],
            result['source']
        )
        print(result_obj.format_markdown())
    else:
        print("\n❌ 未找到相关资讯")


if __name__ == '__main__':
    import io
    main()
