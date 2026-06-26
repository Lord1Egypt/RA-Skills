#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日热榜 (tophub.today) 数据采集模块
聚合知乎、微博、微信、百度、B站、抖音等平台的热门内容
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
    rank: int = 0  # 排名
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class TopHubCollector:
    """今日热榜采集器"""
    
    BASE_URL = "https://tophub.today"
    
    # 平台映射配置 (node ID -> 平台名称)
    PLATFORM_MAP = {
        'QqGDoY8v': '知乎',      # 知乎热榜
        'KqndgxeLl9': '微博',    # 微博热搜
        'WnBe01o371': '微信',    # 微信24h热文
        '5VaobgvAj1': '百度',    # 百度实时热点
        '74KvxwokxM': 'B站',     # 哔哩哔哩
        'DpQvNABoNE': '抖音',    # 抖音总榜
        'rYqoXQp4vM': '36氪',    # 36氪
        'G2me15ndDj': '虎嗅',    # 虎嗅网
        '3QeLxvmE': 'IT之家',    # IT之家
        'nBe0y5zAjw': '掘金',    # 掘金
        'Na2WrgQ6v1': '豆瓣',    # 豆瓣电影
        '4KZbaN8x': '雪球',      # 雪球
        '7Gj2Xvnq': '澎湃新闻',  # 澎湃
        'YqoXQp4v': '今日头条',  # 今日头条
        'mDOv9n8e': '百度贴吧',  # 百度贴吧
        'wWmoO5Rd4E': 'GitHub',  # GitHub
        '6A7J6v4j': 'CSDN',      # CSDN
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self._nodes_cache = None
    
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
    
    def _get_nodes(self) -> Dict[str, str]:
        """获取所有可用的节点列表"""
        if self._nodes_cache:
            return self._nodes_cache
        
        try:
            response = self._safe_request(f"{self.BASE_URL}/c/news")
            if not response:
                return self.PLATFORM_MAP
            
            soup = BeautifulSoup(response.text, 'html.parser')
            nodes = {}
            
            # 查找所有节点链接
            for link in soup.find_all('a', href=re.compile(r'/n/\w+')):
                href = link.get('href', '')
                node_id = href.split('/')[-1] if '/n/' in href else ''
                name = link.get_text(strip=True)
                if node_id and name:
                    nodes[node_id] = name
            
            self._nodes_cache = nodes or self.PLATFORM_MAP
            return self._nodes_cache
            
        except Exception as e:
            logger.error(f"获取节点列表失败: {e}")
            return self.PLATFORM_MAP
    
    def _extract_from_html(self, html: str, node_id: str) -> List[HotTopic]:
        """从HTML中提取热点数据"""
        topics = []
        platform_name = self.PLATFORM_MAP.get(node_id, '未知')
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 尝试多种选择器模式
            rows = soup.select('table.table tr') or soup.select('.table tr') or soup.select('tr')
            
            for idx, row in enumerate(rows[:50], 1):  # 最多取前50条
                try:
                    # 提取标题
                    title_elem = row.select_one('td a, .topic-title a, a[href*="/l/"]')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    
                    # 处理相对URL
                    if url and url.startswith('/'):
                        url = f"{self.BASE_URL}{url}"
                    elif url and not url.startswith('http'):
                        url = f"{self.BASE_URL}/l/{url}"
                    
                    # 提取热度
                    hot_score = 0.0
                    hot_elem = row.select_one('td:nth-child(3), .heat, .score')
                    if hot_elem:
                        hot_text = hot_elem.get_text(strip=True)
                        hot_score = self._parse_hot_score(hot_text)
                    
                    # 如果没有热度值，根据排名估算
                    if hot_score == 0:
                        hot_score = max(100 - idx * 2, 10)
                    
                    topic = HotTopic(
                        platform=platform_name,
                        title=title,
                        url=url,
                        hot_score=hot_score,
                        rank=idx
                    )
                    topics.append(topic)
                    
                except Exception as e:
                    logger.warning(f"解析条目失败: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"解析HTML失败: {e}")
        
        return topics
    
    def _parse_hot_score(self, text: str) -> float:
        """解析热度值"""
        try:
            # 移除非数字字符，保留小数点
            numbers = re.findall(r'[\d.]+', text.replace(',', ''))
            if numbers:
                value = float(numbers[0])
                # 处理单位
                if '万' in text:
                    value *= 10000
                elif '亿' in text:
                    value *= 100000000
                return value
        except:
            pass
        return 0.0
    
    def collect_node(self, node_id: str, limit: int = 50) -> List[HotTopic]:
        """采集指定节点的数据"""
        url = f"{self.BASE_URL}/n/{node_id}"
        response = self._safe_request(url)
        
        if not response:
            logger.error(f"无法获取节点数据: {node_id}")
            return []
        
        topics = self._extract_from_html(response.text, node_id)
        logger.info(f"[{self.PLATFORM_MAP.get(node_id, node_id)}] 采集到 {len(topics)} 条数据")
        return topics[:limit]
    
    def collect_all(self, platforms: List[str] = None, limit_per_platform: int = 50) -> Dict[str, List[HotTopic]]:
        """
        采集多个平台的数据
        
        Args:
            platforms: 平台列表，如 ['知乎', '微博', '微信']，None表示全部
            limit_per_platform: 每个平台采集数量
        
        Returns:
            按平台分组的热点数据
        """
        results = {}
        
        # 根据平台名称筛选节点
        target_nodes = {}
        if platforms:
            for node_id, name in self.PLATFORM_MAP.items():
                if any(p in name for p in platforms):
                    target_nodes[node_id] = name
        else:
            target_nodes = self.PLATFORM_MAP
        
        logger.info(f"开始采集 {len(target_nodes)} 个平台...")
        
        for node_id, platform_name in target_nodes.items():
            try:
                topics = self.collect_node(node_id, limit_per_platform)
                results[platform_name] = topics
            except Exception as e:
                logger.error(f"采集 {platform_name} 失败: {e}")
                results[platform_name] = []
        
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
def collect_from_tophub(platforms: List[str] = None, limit: int = 50) -> List[HotTopic]:
    """便捷函数：从今日热榜采集热点"""
    collector = TopHubCollector()
    return collector.collect_merged(platforms, limit)


def collect_hot_topics(platforms: List[str] = None, limit: int = 50) -> List[HotTopic]:
    """兼容原接口的便捷函数"""
    return collect_from_tophub(platforms, limit)


if __name__ == "__main__":
    # 测试采集
    collector = TopHubCollector()
    
    # 测试采集知乎热榜
    print("="*60)
    print("测试采集知乎热榜")
    print("="*60)
    zhihu_topics = collector.collect_node('QqGDoY8v', limit=10)
    for topic in zhihu_topics[:5]:
        print(f"{topic.rank}. {topic.title[:40]}... (热度: {topic.hot_score})")
    
    # 测试采集微博热搜
    print("\n" + "="*60)
    print("测试采集微博热搜")
    print("="*60)
    weibo_topics = collector.collect_node('KqndgxeLl9', limit=10)
    for topic in weibo_topics[:5]:
        print(f"{topic.rank}. {topic.title[:40]}... (热度: {topic.hot_score})")
    
    # 测试采集多个平台
    print("\n" + "="*60)
    print("测试采集多个平台")
    print("="*60)
    results = collector.collect_all(['知乎', '微博', '微信'], limit_per_platform=5)
    for platform, topics in results.items():
        print(f"\n[{platform}] {len(topics)} 条")
        for topic in topics[:3]:
            print(f"  - {topic.title[:35]}...")
