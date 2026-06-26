#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台数据采集模块
采集微信公众号、知乎、微博、小红书等平台的热门内容
"""

import requests
import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class HotTopic:
    """热点话题数据模型"""
    platform: str  # 来源平台
    title: str  # 标题
    url: str  # 链接
    hot_score: float  # 热度值
    read_count: Optional[int] = None  # 阅读量
    like_count: Optional[int] = None  # 点赞数
    comment_count: Optional[int] = None  # 评论数
    share_count: Optional[int] = None  # 分享数
    category: Optional[str] = None  # 分类
    publish_time: Optional[datetime] = None  # 发布时间
    author: Optional[str] = None  # 作者
    tags: List[str] = None  # 标签
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class BaseCollector(ABC):
    """数据采集基类"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    @abstractmethod
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集热点数据"""
        pass
    
    def _safe_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """安全请求，带重试机制"""
        max_retries = 3
        for i in range(max_retries):
            try:
                time.sleep(random.uniform(0.5, 1.5))  # 随机延迟
                if method.upper() == 'GET':
                    response = self.session.get(url, timeout=10, **kwargs)
                else:
                    response = self.session.post(url, timeout=10, **kwargs)
                response.raise_for_status()
                return response
            except Exception as e:
                logger.warning(f"请求失败 ({i+1}/{max_retries}): {e}")
                if i == max_retries - 1:
                    return None
                time.sleep(2 ** i)  # 指数退避
        return None


class ZhihuCollector(BaseCollector):
    """知乎热榜采集器"""
    
    def __init__(self):
        super().__init__("知乎")
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集知乎热榜"""
        topics = []
        try:
            # 知乎热榜 API
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
            response = self._safe_request(url)
            if not response:
                return topics
            
            data = response.json()
            items = data.get('data', [])[:limit]
            
            for item in items:
                try:
                    card = item.get('target', {})
                    topic = HotTopic(
                        platform="知乎",
                        title=card.get('title', ''),
                        url=card.get('url', ''),
                        hot_score=float(item.get('detail_text', '0').replace('万', '0000').replace('亿', '00000000') or 0),
                        read_count=self._parse_count(card.get('answer_count', 0)),
                        like_count=self._parse_count(card.get('follower_count', 0)),
                        comment_count=self._parse_count(card.get('comment_count', 0)),
                        category=card.get('excerpt', '')[:50] if card.get('excerpt') else None
                    )
                    topics.append(topic)
                except Exception as e:
                    logger.warning(f"解析知乎条目失败: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"采集知乎热榜失败: {e}")
        
        logger.info(f"知乎采集完成，获取 {len(topics)} 条数据")
        return topics
    
    def _parse_count(self, value) -> int:
        """解析数字"""
        try:
            if isinstance(value, str):
                return int(value.replace('万', '0000').replace('亿', '00000000'))
            return int(value)
        except:
            return 0


class WeiboCollector(BaseCollector):
    """微博热搜采集器"""
    
    def __init__(self):
        super().__init__("微博")
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集微博热搜"""
        topics = []
        try:
            # 微博热搜 API
            url = "https://weibo.com/ajax/side/hotSearch"
            response = self._safe_request(url)
            if not response:
                return topics
            
            data = response.json()
            realtime = data.get('data', {}).get('realtime', [])[:limit]
            
            for item in realtime:
                try:
                    topic = HotTopic(
                        platform="微博",
                        title=item.get('word', ''),
                        url=f"https://s.weibo.com/weibo?q={item.get('word', '')}",
                        hot_score=float(item.get('raw_hot', 0)),
                        read_count=self._parse_count(item.get('num', 0)),
                        category=item.get('category', ''),
                        tags=[item.get('label_name', '')] if item.get('label_name') else []
                    )
                    topics.append(topic)
                except Exception as e:
                    logger.warning(f"解析微博条目失败: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"采集微博热搜失败: {e}")
        
        logger.info(f"微博采集完成，获取 {len(topics)} 条数据")
        return topics
    
    def _parse_count(self, value) -> int:
        """解析数字"""
        try:
            if isinstance(value, str):
                if '万' in value:
                    return int(float(value.replace('万', '')) * 10000)
                elif '亿' in value:
                    return int(float(value.replace('亿', '')) * 100000000)
                return int(value)
            return int(value)
        except:
            return 0


class XiaohongshuCollector(BaseCollector):
    """小红书热门采集器"""
    
    def __init__(self):
        super().__init__("小红书")
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集小红书热门话题"""
        topics = []
        try:
            # 使用网页版热门话题
            url = "https://www.xiaohongshu.com/api/sns/web/v1/search/trending"
            response = self._safe_request(url)
            if not response:
                return topics
            
            data = response.json()
            items = data.get('data', {}).get('queries', [])[:limit]
            
            for idx, item in enumerate(items):
                try:
                    topic = HotTopic(
                        platform="小红书",
                        title=item.get('query', ''),
                        url=f"https://www.xiaohongshu.com/search_result?keyword={item.get('query', '')}",
                        hot_score=float(100 - idx * 2),  # 根据排名估算热度
                        tags=item.get('tags', [])
                    )
                    topics.append(topic)
                except Exception as e:
                    logger.warning(f"解析小红书条目失败: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"采集小红书热门失败: {e}")
        
        logger.info(f"小红书采集完成，获取 {len(topics)} 条数据")
        return topics


class WechatCollector(BaseCollector):
    """微信公众号热门采集器"""
    
    def __init__(self):
        super().__init__("公众号")
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集公众号热门文章
        注：公众号数据需要通过第三方服务或自建爬虫获取
        这里提供模拟数据和接口框架
        """
        topics = []
        try:
            # 方案1：通过新榜、清博等第三方平台 API
            # 方案2：通过搜狗微信搜索
            # 方案3：通过自建监控账号
            
            # 这里使用搜狗微信搜索作为示例
            keywords = ["热点", "爆文", "10万+", "爆款", "热门"]
            
            for keyword in keywords[:5]:
                try:
                    url = f"https://weixin.sogou.com/weixin?type=2&query={keyword}"
                    response = self._safe_request(url)
                    if response:
                        # 解析搜索结果
                        # 实际实现需要解析 HTML
                        pass
                except Exception as e:
                    logger.warning(f"搜索关键词失败 {keyword}: {e}")
            
            # 模拟一些示例数据
            sample_topics = self._get_sample_topics()
            topics.extend(sample_topics[:limit])
            
        except Exception as e:
            logger.error(f"采集公众号热门失败: {e}")
        
        logger.info(f"公众号采集完成，获取 {len(topics)} 条数据")
        return topics
    
    def _get_sample_topics(self) -> List[HotTopic]:
        """获取示例数据"""
        return [
            HotTopic(
                platform="公众号",
                title="2024年最赚钱的10个行业",
                url="",
                hot_score=95.0,
                read_count=100000,
                like_count=5000,
                category="商业"
            ),
            HotTopic(
                platform="公众号",
                title="为什么年轻人都不结婚了？",
                url="",
                hot_score=92.0,
                read_count=80000,
                like_count=3500,
                category="社会"
            ),
        ]


class DataCollector:
    """数据采集管理器"""
    
    def __init__(self):
        self.collectors = {
            'zhihu': ZhihuCollector(),
            'weibo': WeiboCollector(),
            'xiaohongshu': XiaohongshuCollector(),
            'wechat': WechatCollector(),
        }
    
    def collect_all(self, platforms: List[str] = None, limit_per_platform: int = 50) -> Dict[str, List[HotTopic]]:
        """
        采集所有平台数据
        
        Args:
            platforms: 指定平台列表，None表示全部
            limit_per_platform: 每个平台采集数量
        
        Returns:
            按平台分组的热点数据
        """
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
        """
        采集并合并所有平台数据
        
        Returns:
            合并后的热点列表
        """
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
    collector = DataCollector()
    return collector.collect_merged(platforms, limit)


if __name__ == "__main__":
    # 测试采集
    collector = DataCollector()
    results = collector.collect_all(limit_per_platform=20)
    
    for platform, topics in results.items():
        print(f"\n{'='*50}")
        print(f"平台: {platform} ({len(topics)} 条)")
        print('='*50)
        for topic in topics[:5]:
            print(f"- {topic.title[:40]}... (热度: {topic.hot_score})")
