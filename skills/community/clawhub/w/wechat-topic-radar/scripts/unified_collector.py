#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一数据采集模块
支持多种数据源: 今日热榜(tophub.today)、V2EX、HackerNews、百度热搜等
"""

import requests
import json
import time
import random
import re
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class HotTopic:
    """热点话题数据模型"""
    platform: str
    title: str
    url: str
    hot_score: float
    read_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    share_count: Optional[int] = None
    category: Optional[str] = None
    publish_time: Optional[datetime] = None
    author: Optional[str] = None
    tags: List[str] = None
    rank: int = 0
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class BaseCollector:
    """数据采集基类"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
    
    def _safe_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """安全请求，带重试机制"""
        max_retries = 3
        for i in range(max_retries):
            try:
                time.sleep(random.uniform(0.5, 1.5))
                if method.upper() == 'GET':
                    response = self.session.get(url, timeout=15, **kwargs)
                else:
                    response = self.session.post(url, timeout=15, **kwargs)
                response.raise_for_status()
                return response
            except Exception as e:
                logger.warning(f"请求失败 ({i+1}/{max_retries}): {e}")
                if i == max_retries - 1:
                    return None
                time.sleep(2 ** i)
        return None


class BaiduHotCollector(BaseCollector):
    """百度热搜采集器"""
    
    def __init__(self):
        super().__init__("百度")
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集百度热搜"""
        topics = []
        try:
            # 百度热搜API
            url = "https://top.baidu.com/board?tab=realtime"
            response = self._safe_request(url)
            if not response:
                return topics
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找热搜条目
            items = soup.select('.category-wrap_iQLoo')[:limit]
            
            for idx, item in enumerate(items, 1):
                try:
                    title_elem = item.select_one('.c-single-text-ellipsis')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # 提取热度
                    hot_elem = item.select_one('.hot-index_1Bl1a')
                    hot_score = 0.0
                    if hot_elem:
                        hot_text = hot_elem.get_text(strip=True)
                        hot_score = self._parse_hot_score(hot_text)
                    
                    # 提取链接
                    link_elem = item.select_one('a[href]')
                    url = link_elem.get('href', '') if link_elem else ''
                    
                    topic = HotTopic(
                        platform="百度",
                        title=title,
                        url=url,
                        hot_score=hot_score or (100 - idx * 2),
                        rank=idx
                    )
                    topics.append(topic)
                    
                except Exception as e:
                    logger.warning(f"解析百度条目失败: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"采集百度热搜失败: {e}")
        
        logger.info(f"百度采集完成，获取 {len(topics)} 条数据")
        return topics
    
    def _parse_hot_score(self, text: str) -> float:
        """解析热度值"""
        try:
            numbers = re.findall(r'[\d.]+', text.replace(',', ''))
            if numbers:
                return float(numbers[0])
        except:
            pass
        return 0.0


class V2EXCollector(BaseCollector):
    """V2EX热门采集器"""
    
    def __init__(self):
        super().__init__("V2EX")
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集V2EX热门"""
        topics = []
        try:
            url = "https://www.v2ex.com/api/topics/hot.json"
            response = self._safe_request(url)
            if not response:
                return topics
            
            data = response.json()
            
            for idx, item in enumerate(data[:limit], 1):
                try:
                    topic = HotTopic(
                        platform="V2EX",
                        title=item.get('title', ''),
                        url=item.get('url', ''),
                        hot_score=float(item.get('replies', 0)) * 10,
                        comment_count=item.get('replies', 0),
                        author=item.get('member', {}).get('username', ''),
                        category=item.get('node', {}).get('title', ''),
                        rank=idx
                    )
                    topics.append(topic)
                except Exception as e:
                    logger.warning(f"解析V2EX条目失败: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"采集V2EX热门失败: {e}")
        
        logger.info(f"V2EX采集完成，获取 {len(topics)} 条数据")
        return topics


class HackerNewsCollector(BaseCollector):
    """HackerNews热门采集器"""
    
    def __init__(self):
        super().__init__("HackerNews")
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集HackerNews热门"""
        topics = []
        try:
            # 获取热门故事ID
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = self._safe_request(url)
            if not response:
                return topics
            
            story_ids = response.json()[:limit]
            
            for idx, story_id in enumerate(story_ids, 1):
                try:
                    # 获取故事详情
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_response = self._safe_request(story_url)
                    if not story_response:
                        continue
                    
                    story = story_response.json()
                    if not story:
                        continue
                    
                    topic = HotTopic(
                        platform="HackerNews",
                        title=story.get('title', ''),
                        url=story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        hot_score=float(story.get('score', 0)),
                        comment_count=story.get('descendants', 0),
                        author=story.get('by', ''),
                        rank=idx
                    )
                    topics.append(topic)
                    
                except Exception as e:
                    logger.warning(f"解析HackerNews条目失败: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"采集HackerNews热门失败: {e}")
        
        logger.info(f"HackerNews采集完成，获取 {len(topics)} 条数据")
        return topics


class WeiboHotCollector(BaseCollector):
    """微博热搜采集器 (通过网页版)"""
    
    def __init__(self):
        super().__init__("微博")
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集微博热搜"""
        topics = []
        try:
            # 使用微博热搜网页
            url = "https://s.weibo.com/top/summary"
            response = self._safe_request(url)
            if not response:
                return topics
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找热搜条目
            items = soup.select('#pl_top_realtimehot tbody tr')[:limit+1]
            
            for idx, item in enumerate(items[1:], 1):  # 跳过表头
                try:
                    title_elem = item.select_one('td.td-02 a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    if url and not url.startswith('http'):
                        url = f"https://s.weibo.com{url}"
                    
                    # 提取热度
                    hot_elem = item.select_one('td.td-02 span')
                    hot_score = 0.0
                    if hot_elem:
                        hot_text = hot_elem.get_text(strip=True)
                        hot_score = self._parse_hot_score(hot_text)
                    
                    # 提取标签
                    tag_elem = item.select_one('td.td-03 i')
                    tag = tag_elem.get_text(strip=True) if tag_elem else ''
                    
                    topic = HotTopic(
                        platform="微博",
                        title=title,
                        url=url,
                        hot_score=hot_score or (100 - idx * 2),
                        tags=[tag] if tag else [],
                        rank=idx
                    )
                    topics.append(topic)
                    
                except Exception as e:
                    logger.warning(f"解析微博条目失败: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"采集微博热搜失败: {e}")
        
        logger.info(f"微博采集完成，获取 {len(topics)} 条数据")
        return topics
    
    def _parse_hot_score(self, text: str) -> float:
        """解析热度值"""
        try:
            if '万' in text:
                return float(text.replace('万', '')) * 10000
            elif '亿' in text:
                return float(text.replace('亿', '')) * 100000000
            else:
                return float(text)
        except:
            return 0.0


class ZhihuHotCollector(BaseCollector):
    """知乎热榜采集器 (通过网页版)"""
    
    def __init__(self):
        super().__init__("知乎")
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集知乎热榜"""
        topics = []
        try:
            # 知乎热榜API (无需认证)
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.zhihu.com/hot'
            }
            response = self._safe_request(url, headers=headers)
            if not response:
                return topics
            
            data = response.json()
            items = data.get('data', [])[:limit]
            
            for idx, item in enumerate(items, 1):
                try:
                    card = item.get('target', {})
                    
                    # 解析热度值
                    hot_text = item.get('detail_text', '0')
                    hot_score = self._parse_hot_score(hot_text)
                    
                    topic = HotTopic(
                        platform="知乎",
                        title=card.get('title', ''),
                        url=card.get('url', ''),
                        hot_score=hot_score,
                        comment_count=card.get('answer_count', 0),
                        like_count=card.get('follower_count', 0),
                        category=card.get('excerpt', '')[:50] if card.get('excerpt') else None,
                        rank=idx
                    )
                    topics.append(topic)
                    
                except Exception as e:
                    logger.warning(f"解析知乎条目失败: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"采集知乎热榜失败: {e}")
        
        logger.info(f"知乎采集完成，获取 {len(topics)} 条数据")
        return topics
    
    def _parse_hot_score(self, text: str) -> float:
        """解析热度值"""
        try:
            text = str(text)
            if '万' in text:
                return float(text.replace('万', '').replace('热度', '')) * 10000
            elif '亿' in text:
                return float(text.replace('亿', '').replace('热度', '')) * 100000000
            else:
                return float(text.replace('热度', ''))
        except:
            return 0.0


class UnifiedCollector:
    """统一数据采集管理器
    
    支持的数据源:
    - 百度: 百度热搜 (可用)
    - V2EX: V2EX热门话题 (可用)
    - HackerNews: HackerNews热门 (可用)
    - 知乎: 知乎热榜 (需要登录态，当前不可用)
    - 微博: 微博热搜 (需要登录态，当前不可用)
    """
    
    def __init__(self):
        self.collectors = {
            '百度': BaiduHotCollector(),
            'V2EX': V2EXCollector(),
            'HackerNews': HackerNewsCollector(),
        }
    
    def collect_all(self, platforms: List[str] = None, limit_per_platform: int = 50) -> Dict[str, List[HotTopic]]:
        """采集多个平台数据"""
        if platforms is None:
            platforms = list(self.collectors.keys())
        
        results = {}
        for platform in platforms:
            if platform in self.collectors:
                logger.info(f"开始采集 {platform}...")
                try:
                    topics = self.collectors[platform].collect(limit_per_platform)
                    results[platform] = topics
                except Exception as e:
                    logger.error(f"采集 {platform} 失败: {e}")
                    results[platform] = []
            else:
                logger.warning(f"未知平台: {platform}")
                results[platform] = []
        
        return results
    
    def collect_merged(self, platforms: List[str] = None, limit_per_platform: int = 50) -> List[HotTopic]:
        """采集并合并所有平台数据"""
        results = self.collect_all(platforms, limit_per_platform)
        all_topics = []
        for platform_topics in results.values():
            all_topics.extend(platform_topics)
        
        # 按热度排序
        all_topics.sort(key=lambda x: x.hot_score, reverse=True)
        return all_topics


# 便捷函数
def collect_hot_topics(platforms: List[str] = None, limit: int = 50) -> List[HotTopic]:
    """便捷函数：采集热点话题"""
    collector = UnifiedCollector()
    return collector.collect_merged(platforms, limit)


if __name__ == "__main__":
    # 测试采集
    collector = UnifiedCollector()
    
    print("="*60)
    print("统一数据采集器测试")
    print("="*60)
    
    # 测试采集所有平台
    results = collector.collect_all(limit_per_platform=10)
    
    for platform, topics in results.items():
        print(f"\n[{platform}] {len(topics)} 条")
        for topic in topics[:3]:
            print(f"  {topic.rank}. {topic.title[:35]}... (热度: {topic.hot_score})")
