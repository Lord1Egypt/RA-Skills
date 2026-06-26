#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财经网站适配器模块 - 最终版
主力网站使用新创建的抓取器，其他网站保持原样
"""

import re
import json
import time
import random
import subprocess
import tempfile
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import urllib.parse

# 导入新创建的抓取器
try:
    from jrj_hot_news import JRJHotNewsCrawler
    from stcn_hot_news import STCNHotNewsCrawler
    from cls_hot_news import CLSHotNewsCrawler
    NEW_CRAWLERS_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] 无法导入新抓取器: {e}")
    NEW_CRAWLERS_AVAILABLE = False

class BaseWebsiteAdapter:
    """网站适配器基类"""
    
    def __init__(self, name: str, url: str, time_limit_hours: int = 48):
        """
        初始化适配器
        
        Args:
            name: 网站名称
            url: 网站URL
            time_limit_hours: 时间限制（小时），默认48小时
        """
        self.name = name
        self.url = url
        self.time_limit_hours = time_limit_hours
        self.cutoff_time = datetime.now() - timedelta(hours=time_limit_hours)
        self.articles = []
        
    def extract_publish_time_from_content(self, html_content: str, url: str) -> Optional[datetime]:
        """从HTML内容中提取发布时间"""
        try:
            # 查找发布时间模式
            time_patterns = [
                r'发布时间[:：]\s*([0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2})',
                r'时间[:：]\s*([0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2})',
                r'发布日期[:：]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})',
                r'<span class="time">([^<]+)</span>',
                r'<time[^>]*>([^<]+)</time>',
                r'"pubDate":"([^"]+)"',
                r'datetime="([^"]+)"',
                r'class="time"[^>]*>([^<]+)</',
                r'class="date"[^>]*>([^<]+)</',
                r'class="pub-time"[^>]*>([^<]+)</',
                r'class="news-time"[^>]*>([^<]+)</'
            ]
            
            for pattern in time_patterns:
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    time_str = match.group(1).strip()
                    # 尝试解析时间
                    time_formats = [
                        '%Y-%m-%d %H:%M',
                        '%Y/%m/%d %H:%M',
                        '%Y年%m月%d日 %H:%M',
                        '%Y-%m-%d',
                        '%Y/%m/%d',
                        '%Y年%m月%d日',
                        '%H:%M',
                        '%m-%d %H:%M'
                    ]
                    
                    for fmt in time_formats:
                        try:
                            dt = datetime.strptime(time_str, fmt)
                            # 如果只包含时间，添加当前日期
                            if fmt == '%H:%M':
                                now = datetime.now()
                                dt = datetime(now.year, now.month, now.day, dt.hour, dt.minute)
                            return dt
                        except:
                            continue
            
            # 尝试从URL推断
            return self.extract_publish_time_from_url(url)
            
        except:
            return None
    
    def extract_publish_time_from_url(self, url: str) -> Optional[datetime]:
        """从URL中提取发布时间"""
        try:
            # 常见URL时间格式
            patterns = [
                r'/(\d{4})(\d{2})(\d{2})/',
                r'/(\d{4})-(\d{2})-(\d{2})/',
                r'/(\d{4})/(\d{2})/(\d{2})/',
                r'_(\d{4})(\d{2})(\d{2})',
                r'_(\d{4})-(\d{2})-(\d{2})'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    year, month, day = match.groups()[:3]
                    try:
                        dt = datetime(int(year), int(month), int(day))
                        return dt
                    except:
                        continue
            
            return None
        except:
            return None
    
    def filter_by_time(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """根据时间过滤文章"""
        filtered = []
        for article in articles:
            publish_time = article.get('publish_time')
            if publish_time and publish_time >= self.cutoff_time:
                filtered.append(article)
            elif not publish_time:
                # 如果没有发布时间，保留文章
                filtered.append(article)
        
        return filtered
    
    def scrape(self) -> List[Dict[str, Any]]:
        """抓取网站新闻（子类必须实现）"""
        raise NotImplementedError("子类必须实现scrape方法")
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章（子类必须实现）"""
        raise NotImplementedError("子类必须实现extract_articles方法")


class STCNAdapter(BaseWebsiteAdapter):
    """证券时报网适配器 - 使用新创建的STCN抓取器"""
    
    def __init__(self, name: str = "证券时报网", url: str = "https://www.stcn.com/"):
        super().__init__(name, url)
    
    def scrape(self) -> List[Dict[str, Any]]:
        """使用新创建的STCN抓取器抓取新闻"""
        print(f"抓取 {self.name} ({self.url})...")
        
        if not NEW_CRAWLERS_AVAILABLE:
            print("[ERROR] 新抓取器不可用，无法继续")
            return []
        
        try:
            # 创建STCN抓取器实例
            crawler = STCNHotNewsCrawler()
            
            # 运行抓取
            articles = crawler.crawl()
            
            if not articles:
                print(f"[WARNING] 未抓取到文章")
                return []
            
            print(f"[SUCCESS] 抓取到 {len(articles)} 篇文章")
            
            # 标准化文章格式
            standardized_articles = []
            for article in articles:
                standardized = self._standardize_article(article)
                if standardized:
                    standardized_articles.append(standardized)
            
            # 应用时间过滤
            filtered_articles = self.filter_by_time(standardized_articles)
            
            print(f"时间过滤: {len(standardized_articles)} → {len(filtered_articles)} 篇文章 (48小时内)")
            
            return filtered_articles
            
        except Exception as e:
            print(f"[ERROR] 抓取失败: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _standardize_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """标准化文章格式"""
        standardized = {
            'title': article.get('title', '').strip(),
            'url': article.get('url', '').strip(),
            'summary': article.get('summary', '').strip(),
            'publish_time': article.get('publish_time'),
            'source': self.name,
            'category': article.get('category', '综合').strip(),
            'type': article.get('type', '新闻').strip(),
            'keywords': article.get('keywords', []),
            'within_48h': article.get('within_48h', False)
        }
        
        # 清理空值
        for key in list(standardized.keys()):
            if standardized[key] in [None, '', [], {}]:
                del standardized[key]
        
        return standardized
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章（兼容旧接口）"""
        # 这个方法现在只是调用scrape的包装器
        return self.scrape()


class JRJAdapter(BaseWebsiteAdapter):
    """金融界适配器 - 使用新创建的JRJ抓取器"""
    
    def __init__(self, name: str = "金融界", url: str = "https://www.jrj.com.cn/"):
        super().__init__(name, url)
    
    def scrape(self) -> List[Dict[str, Any]]:
        """使用新创建的JRJ抓取器抓取新闻"""
        print(f"抓取 {self.name} ({self.url})...")
        
        if not NEW_CRAWLERS_AVAILABLE:
            print("[ERROR] 新抓取器不可用，无法继续")
            return []
        
        try:
            # 创建JRJ抓取器实例
            crawler = JRJHotNewsCrawler()
            
            # 运行抓取
            articles = crawler.crawl()
            
            if not articles:
                print(f"[WARNING] 未抓取到文章")
                return []
            
            print(f"[SUCCESS] 抓取到 {len(articles)} 篇文章")
            
            # 标准化文章格式
            standardized_articles = []
            for article in articles:
                standardized = self._standardize_article(article)
                if standardized:
                    standardized_articles.append(standardized)
            
            # 应用时间过滤
            filtered_articles = self.filter_by_time(standardized_articles)
            
            print(f"时间过滤: {len(standardized_articles)} → {len(filtered_articles)} 篇文章 (48小时内)")
            
            return filtered_articles
            
        except Exception as e:
            print(f"[ERROR] 抓取失败: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _standardize_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """标准化文章格式"""
        standardized = {
            'title': article.get('title', '').strip(),
            'url': article.get('url', '').strip(),
            'summary': article.get('summary', '').strip(),
            'publish_time': article.get('publish_time'),
            'source': self.name,
            'category': article.get('category', '综合').strip(),
            'type': article.get('type', '新闻').strip(),
            'keywords': article.get('keywords', []),
            'within_48h': article.get('within_48h', False)
        }
        
        # 清理空值
        for key in list(standardized.keys()):
            if standardized[key] in [None, '', [], {}]:
                del standardized[key]
        
        return standardized
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章（兼容旧接口）"""
        # 这个方法现在只是调用scrape的包装器
        return self.scrape()


class CLSAdapter(BaseWebsiteAdapter):
    """财联社适配器 - 使用新创建的CLS抓取器"""
    
    def __init__(self, name: str = "财联社", url: str = "https://www.cls.cn/depth?id=1000"):
        super().__init__(name, url)
    
    def scrape(self) -> List[Dict[str, Any]]:
        """使用新创建的CLS抓取器抓取新闻"""
        print(f"抓取 {self.name} ({self.url})...")
        
        if not NEW_CRAWLERS_AVAILABLE:
            print("[ERROR] 新抓取器不可用，无法继续")
            return []
        
        try:
            # 创建CLS抓取器实例
            crawler = CLSHotNewsCrawler()
            
            # 运行抓取（CLS使用run方法而不是crawl）
            articles = crawler.run()
            
            if not articles:
                print(f"[WARNING] 未抓取到文章")
                return []
            
            print(f"[SUCCESS] 抓取到 {len(articles)} 篇文章")
            
            # 标准化文章格式
            standardized_articles = []
            for article in articles:
                standardized = self._standardize_article(article)
                if standardized:
                    standardized_articles.append(standardized)
            
            # 应用时间过滤
            filtered_articles = self.filter_by_time(standardized_articles)
            
            print(f"时间过滤: {len(standardized_articles)} → {len(filtered_articles)} 篇文章 (48小时内)")
            
            return filtered_articles
            
        except Exception as e:
            print(f"[ERROR] 抓取失败: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _standardize_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """标准化文章格式"""
        standardized = {
            'title': article.get('title', '').strip(),
            'url': article.get('url', '').strip(),
            'summary': article.get('summary', '').strip(),
            'publish_time': article.get('publish_time'),
            'source': self.name,
            'category': article.get('category', '综合').strip(),
            'type': article.get('type', '新闻').strip(),
            'keywords': article.get('keywords', []),
            'within_48h': article.get('within_48h', False)
        }
        
        # 清理空值
        for key in list(standardized.keys()):
            if standardized[key] in [None, '', [], {}]:
                del standardized[key]
        
        return standardized
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章（兼容旧接口）"""
        # 这个方法现在只是调用scrape的包装器
        return self.scrape()


# 简化的其他适配器（保持兼容性）
class SinaFinanceAdapter(BaseWebsiteAdapter):
    """新浪财经适配器"""
    
    def __init__(self, name: str = "新浪财经", url: str = "https://finance.sina.com.cn/"):
        super().__init__(name, url)
    
    def scrape(self) -> List[Dict[str, Any]]:
        """抓取新浪财经新闻"""
        print(f"抓取 {self.name} ({self.url})...")
        # 简化实现，返回空列表
        return []
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章"""
        return []


class WallStreetCNAdapter(BaseWebsiteAdapter):
    """华尔街见闻适配器"""
    
    def __init__(self, name: str = "华尔街见闻", url: str = "https://wallstreetcn.com/"):
        super().__init__(name, url)
    
    def scrape(self) -> List[Dict[str, Any]]:
        """抓取华尔街见闻新闻"""
        print(f"抓取 {self.name} ({self.url})...")
        return []
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章"""
        return []


class HexunAdapter(BaseWebsiteAdapter):
    """和讯网适配器"""
    
    def __init__(self, name: str = "和讯网", url: str = "https://www.hexun.com/"):
        super().__init__(name, url)
    
    def scrape(self) -> List[Dict[str, Any]]:
        """抓取和讯网新闻"""
        print(f"抓取 {self.name} ({self.url})...")
        return []
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章"""
        return []


class Jingji21Adapter(BaseWebsiteAdapter):
    """21财经适配器"""
    
    def __init__(self, name: str = "21财经", url: str = "https://www.21jingji.com/"):
        super().__init__(name, url)
    
    def scrape(self) -> List[Dict[str, Any]]:
        """抓取21财经新闻"""
        print(f"抓取 {self.name} ({self.url})...")
        return []
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章"""
        return []


class YicaiAdapter(BaseWebsiteAdapter):
    """第一财经适配器"""
    
    def __init__(self, name: str = "第一财经", url: str = "https://www.yicai.com/"):
        super().__init__(name, url)
    
    def scrape(self) -> List[Dict[str, Any]]:
        """抓取第一财经新闻"""
        print(f"抓取 {self.name} ({self.url})...")
        return []
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章"""
        return []


class CaixinAdapter(BaseWebsiteAdapter):
    """财新网适配器"""
    
    def __init__(self, name: str = "财新网", url: str = "https://www.caixin.com/"):
        super().__init__(name, url)
    
    def scrape(self) -> List[Dict[str, Any]]:
        """抓取财新网新闻"""
        print(f"抓取 {self.name} ({self.url})...")
        return []
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章"""
        return []


class GenericAdapter(BaseWebsiteAdapter):
    """通用适配器"""
    
    def __init__(self, name: str = "通用网站", url: str = ""):
        super().__init__(name, url)
    
    def scrape(self) -> List[Dict[str, Any]]:
        """抓取通用网站新闻"""
        print(f"抓取 {self.name} ({self.url})...")
        return []
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章"""
        return []


def create_adapter(adapter_type: str, **kwargs) -> BaseWebsiteAdapter:
    """创建适配器实例"""
    adapter_map = {
        'stcn': STCNAdapter,
        'jrj': JRJAdapter,
        'cls': CLSAdapter,
        'sina': SinaFinanceAdapter,
        'wallstreetcn': WallStreetCNAdapter,
        'hexun': HexunAdapter,
        'jingji21': Jingji21Adapter,
        'yicai': YicaiAdapter,
        'caixin': CaixinAdapter,
        'generic': GenericAdapter
    }
    
    adapter_class = adapter_map.get(adapter_type.lower(), GenericAdapter)
    return adapter_class(**kwargs)


# 测试代码
if __name__ == "__main__":
    print("测试新适配器...")
    
    # 测试三个主力网站适配器
    adapters_to_test = [
        ('stcn', '证券时报网', 'https://www.stcn.com/'),
        ('jrj', '金融界', 'https://www.jrj.com.cn/'),
        ('cls', '财联社', 'https://www.cls.cn/depth?id=1000')
    ]
    
    for adapter_type, name, url in adapters_to_test:
        print(f"\n测试 {name} 适配器...")
        try:
            adapter = create_adapter(adapter_type, name=name, url=url)
            articles = adapter.scrape()
            print(f"  抓取结果: {len(articles)} 篇文章")
            
            if articles:
                print(f"  示例文章: {articles[0].get('title', '无标题')[:60]}...")
        except Exception as e:
            print(f"  测试失败: {type(e).__name__}: {e}")
    
    print("\n适配器测试完成!")