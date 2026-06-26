"""
增强版热点数据采集器
整合多个免费API源，提供稳定可靠的热点数据

支持的数据源:
- 百度热搜 (api.xcvts.cn / api.guiguiya.com)
- 今日头条 (api.xcvts.cn / tenapi.cn)
- 抖音热搜 (api.xcvts.cn)
- B站热搜/日榜 (api.xcvts.cn)
- 知乎热榜 (api.xcvts.cn - 无需登录)
- 微博热搜 (api.xcvts.cn - 无需登录)
- 掘金热榜 (api.xcvts.cn)
- 网易新闻 (api.xcvts.cn)
- GitHub热榜 (api.xcvts.cn)
- V2EX (直接爬取)
- HackerNews (官方API)
"""

import requests
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import urljoin
import time


@dataclass
class HotTopic:
    """热点话题数据模型"""
    platform: str           # 平台名称
    title: str             # 标题
    url: str               # 链接
    hot_score: float       # 热度值
    rank: int = 0          # 排名
    description: str = ""  # 描述
    extra: dict = None     # 额外信息
    
    # 兼容性字段 (用于heat_algorithm)
    read_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    collect_count: int = 0
    follower_count: int = 0
    publish_time: str = None  # 发布时间
    author: str = ""          # 作者
    category: str = ""        # 分类
    content: str = ""         # 内容
    cover_image: str = ""     # 封面图
    
    def __post_init__(self):
        """初始化后处理 - 从hot_score推断各字段"""
        if self.hot_score > 0:
            base = int(self.hot_score * 1000)
            if self.read_count == 0:
                self.read_count = base
            if self.like_count == 0:
                self.like_count = int(base * 0.1)  # 10%点赞率
            if self.comment_count == 0:
                self.comment_count = int(base * 0.05)  # 5%评论率
            if self.share_count == 0:
                self.share_count = int(base * 0.02)  # 2%分享率
            if self.collect_count == 0:
                self.collect_count = int(base * 0.03)  # 3%收藏率
        
        # 设置默认发布时间
        if self.publish_time is None:
            from datetime import datetime
            self.publish_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self) -> dict:
        return asdict(self)


class BaseCollector:
    """采集器基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集数据，子类必须实现"""
        raise NotImplementedError


class XiaoChenCollector(BaseCollector):
    """
    小尘API采集器 - 支持20+平台
    接口: http://api.xcvts.cn/api/hotlist
    """
    
    API_BASE = "http://api.xcvts.cn/api/hotlist"
    
    # 平台映射表
    PLATFORM_MAP = {
        '百度': 'baidu',
        '微博': 'weibo',
        '知乎': 'zhihu',
        '抖音': 'douyin',
        'B站热搜': 'bilihot',
        'B站日榜': 'biliall',
        '今日头条': 'toutiao',
        '掘金': 'juejin',
        'CSDN': 'csdn',
        '网易新闻': 'netease_news',
        'GitHub': 'github',
        '少数派': 'sspai',
        '搜狗': 'sogou',
        '懂球帝': 'dongqiudi',
        '爱范儿': 'ifanr',
        'ACFUN': 'acfun',
        '安全客': 'ker',
        '51CTO': '51cto',
    }
    
    def __init__(self, platform_name: str):
        super().__init__(platform_name)
        self.type_code = self.PLATFORM_MAP.get(platform_name, 'baidu')
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """从小尘API采集数据"""
        try:
            url = f"{self.API_BASE}?type={self.type_code}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            topics = []
            if isinstance(data, list):
                items = data[:limit]
            elif isinstance(data, dict) and 'data' in data:
                items = data['data'][:limit]
            else:
                return []
            
            for idx, item in enumerate(items, 1):
                title = item.get('title', item.get('name', ''))
                if not title:
                    continue
                
                # 解析热度值 (处理 "123万" 格式)
                hot_val = item.get('hot', item.get('heat', 50 - idx))
                try:
                    if isinstance(hot_val, str):
                        hot_val = hot_val.replace('万', '0000').replace(',', '')
                        hot_val = float(hot_val)
                    else:
                        hot_val = float(hot_val)
                except:
                    hot_val = float(50 - idx)
                    
                topics.append(HotTopic(
                    platform=self.name,
                    title=title,
                    url=item.get('url', item.get('link', '')),
                    hot_score=hot_val,
                    rank=idx,
                    description=item.get('desc', ''),
                    extra=item
                ))
            
            return topics
            
        except Exception as e:
            print(f"[{self.name}] 小尘API采集失败: {e}")
            return []


class TenAPICollector(BaseCollector):
    """
    TenAPI采集器
    接口: https://tenapi.cn/v2/
    """
    
    API_ENDPOINTS = {
        '今日头条': 'toutiaohot',
        '微博': 'weibohot',
        '知乎': 'zhihuhot',
        '抖音': 'douyinhot',
        '百度': 'baiduhot',
    }
    
    def __init__(self, platform_name: str):
        super().__init__(platform_name)
        self.endpoint = self.API_ENDPOINTS.get(platform_name)
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """从TenAPI采集数据"""
        if not self.endpoint:
            return []
        
        try:
            url = f"https://tenapi.cn/v2/{self.endpoint}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') != 200:
                return []
            
            topics = []
            items = data.get('data', [])[:limit]
            
            for idx, item in enumerate(items, 1):
                title = item.get('name', '')
                if not title:
                    continue
                    
                topics.append(HotTopic(
                    platform=self.name,
                    title=title,
                    url=item.get('url', ''),
                    hot_score=float(100 - idx * 2),
                    rank=idx,
                    extra=item
                ))
            
            return topics
            
        except Exception as e:
            print(f"[{self.name}] TenAPI采集失败: {e}")
            return []


class V2EXCollector(BaseCollector):
    """V2EX热门话题采集器"""
    
    API_URL = "https://www.v2ex.com/api/topics/hot.json"
    
    def __init__(self):
        super().__init__("V2EX")
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集V2EX热门话题"""
        try:
            response = self.session.get(self.API_URL, timeout=10)
            response.raise_for_status()
            items = response.json()[:limit]
            
            topics = []
            for idx, item in enumerate(items, 1):
                topics.append(HotTopic(
                    platform=self.name,
                    title=item['title'],
                    url=item['url'],
                    hot_score=float(item.get('replies', 0)),
                    rank=idx,
                    description=f"回复: {item.get('replies', 0)}",
                    extra=item
                ))
            
            return topics
            
        except Exception as e:
            print(f"[{self.name}] 采集失败: {e}")
            return []


class HackerNewsCollector(BaseCollector):
    """HackerNews热门采集器"""
    
    API_BASE = "https://hacker-news.firebaseio.com/v0"
    
    def __init__(self):
        super().__init__("HackerNews")
    
    def collect(self, limit: int = 50) -> List[HotTopic]:
        """采集HackerNews热门"""
        try:
            # 获取热门故事ID列表
            response = self.session.get(
                f"{self.API_BASE}/topstories.json",
                timeout=10
            )
            response.raise_for_status()
            story_ids = response.json()[:limit]
            
            topics = []
            for idx, story_id in enumerate(story_ids, 1):
                try:
                    story_resp = self.session.get(
                        f"{self.API_BASE}/item/{story_id}.json",
                        timeout=5
                    )
                    story = story_resp.json()
                    
                    if story and story.get('title'):
                        topics.append(HotTopic(
                            platform=self.name,
                            title=story['title'],
                            url=story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            hot_score=float(story.get('score', 0)),
                            rank=idx,
                            description=f"Points: {story.get('score', 0)}, Comments: {story.get('descendants', 0)}",
                            extra=story
                        ))
                except:
                    continue
            
            return topics
            
        except Exception as e:
            print(f"[{self.name}] 采集失败: {e}")
            return []


class EnhancedCollector:
    """
    增强版统一数据采集管理器
    整合多个API源，自动故障转移
    """
    
    # 数据源配置 (优先级从高到低)
    SOURCE_CONFIG = {
        # 百度热搜
        '百度': [
            ('xiaochen', '百度'),
            ('tenapi', '百度'),
        ],
        # 微博热搜
        '微博': [
            ('xiaochen', '微博'),
            ('tenapi', '微博'),
        ],
        # 知乎热榜
        '知乎': [
            ('xiaochen', '知乎'),
            ('tenapi', '知乎'),
        ],
        # 今日头条
        '今日头条': [
            ('xiaochen', '今日头条'),
            ('tenapi', '今日头条'),
        ],
        # 抖音热搜
        '抖音': [
            ('xiaochen', '抖音'),
            ('tenapi', '抖音'),
        ],
        # B站
        'B站热搜': [('xiaochen', 'B站热搜')],
        'B站日榜': [('xiaochen', 'B站日榜')],
        # 技术社区
        '掘金': [('xiaochen', '掘金')],
        'CSDN': [('xiaochen', 'CSDN')],
        'GitHub': [('xiaochen', 'GitHub')],
        'V2EX': [('v2ex', None)],
        'HackerNews': [('hackernews', None)],
        # 新闻资讯
        '网易新闻': [('xiaochen', '网易新闻')],
        '少数派': [('xiaochen', '少数派')],
        '爱范儿': [('xiaochen', '爱范儿')],
    }
    
    def __init__(self):
        self.collectors = {}
        self._init_collectors()
    
    def _init_collectors(self):
        """初始化所有采集器"""
        # 小尘API采集器
        for name in XiaoChenCollector.PLATFORM_MAP.keys():
            key = f"xiaochen_{name}"
            self.collectors[key] = XiaoChenCollector(name)
        
        # TenAPI采集器
        for name in TenAPICollector.API_ENDPOINTS.keys():
            key = f"tenapi_{name}"
            self.collectors[key] = TenAPICollector(name)
        
        # 独立采集器
        self.collectors['v2ex_None'] = V2EXCollector()
        self.collectors['hackernews_None'] = HackerNewsCollector()
    
    def collect(self, platform: str, limit: int = 50) -> List[HotTopic]:
        """
        采集指定平台的数据
        自动尝试多个数据源，直到成功
        """
        sources = self.SOURCE_CONFIG.get(platform, [])
        
        for source_type, source_name in sources:
            key = f"{source_type}_{source_name}"
            collector = self.collectors.get(key)
            
            if collector:
                topics = collector.collect(limit)
                if topics:
                    print(f"[{platform}] 从 {source_type} 采集成功，获取 {len(topics)} 条")
                    return topics
                time.sleep(0.5)  # 避免请求过快
        
        print(f"[{platform}] 所有数据源均失败")
        return []
    
    def collect_merged(self, platforms: List[str], limit_per_platform: int = 50) -> List[HotTopic]:
        """
        采集多个平台的数据并合并
        
        Args:
            platforms: 平台名称列表
            limit_per_platform: 每个平台采集数量
            
        Returns:
            合并后的热点话题列表
        """
        all_topics = []
        
        for platform in platforms:
            topics = self.collect(platform, limit_per_platform)
            all_topics.extend(topics)
            time.sleep(0.3)  # 礼貌性延迟
        
        # 按热度排序
        all_topics.sort(key=lambda x: x.hot_score, reverse=True)
        return all_topics
    
    def get_available_platforms(self) -> List[str]:
        """获取所有可用平台列表"""
        return list(self.SOURCE_CONFIG.keys())
    
    def quick_scan(self, limit: int = 30) -> Dict[str, List[HotTopic]]:
        """
        快速扫描主要平台
        
        Returns:
            各平台热点数据字典
        """
        primary_platforms = ['百度', '微博', '知乎', '今日头条', '抖音', 'B站热搜']
        results = {}
        
        for platform in primary_platforms:
            topics = self.collect(platform, limit)
            if topics:
                results[platform] = topics
        
        return results


# 便捷函数
def collect_hot_topics(platforms: List[str] = None, limit: int = 50) -> List[HotTopic]:
    """
    便捷函数：采集热点话题
    
    Args:
        platforms: 平台列表，默认 ['百度', '微博', '知乎']
        limit: 每平台数量
        
    Returns:
        热点话题列表
    """
    if platforms is None:
        platforms = ['百度', '微博', '知乎']
    
    collector = EnhancedCollector()
    return collector.collect_merged(platforms, limit)


def quick_scan() -> Dict[str, List[HotTopic]]:
    """快速扫描主要平台"""
    collector = EnhancedCollector()
    return collector.quick_scan()


# 测试代码
if __name__ == "__main__":
    print("=" * 60)
    print("增强版热点数据采集器测试")
    print("=" * 60)
    
    collector = EnhancedCollector()
    
    # 测试各平台
    test_platforms = ['百度', '微博', '知乎', '今日头条', '抖音', 'B站热搜', '掘金', 'V2EX']
    
    for platform in test_platforms:
        print(f"\n[测试] 采集: {platform}")
        topics = collector.collect(platform, 5)
        if topics:
            for t in topics[:3]:
                print(f"  {t.rank}. {t.title[:40]}... (热度: {t.hot_score})")
        else:
            print("  [失败] 采集失败")
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
