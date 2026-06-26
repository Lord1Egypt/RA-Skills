#!/usr/bin/env python3
"""
热点话题追踪器 - 发现和监控热门讨论话题
"""

import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
from collections import defaultdict
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Topic:
    """话题"""
    keyword: str
    mention_count: int
    engagement: int
    sentiment_score: float
    growth_rate: float
    top_posts: List[Dict]
    first_seen: datetime
    platforms: List[str]

class TrendingTopicsTracker:
    """热点话题追踪器"""
    
    def __init__(self):
        self.crypto_keywords = [
            'airdrop', '空投', 'launch', '上线',
            'partnership', '合作', 'integration', '集成',
            'upgrade', '升级', 'fork', '分叉',
            'hack', '黑客', 'exploit', '漏洞',
            'listing', '上市', 'binance', 'coinbase',
            'ETF', '现货', 'futures', '期货',
            'regulation', '监管', 'SEC', '政策'
        ]
    
    def discover_trending(self, hours: int = 24, top_n: int = 10) -> List[Topic]:
        """发现热门话题"""
        topics = []
        
        # 模拟热门话题数据
        mock_topics = [
            {'keyword': 'Ethereum ETF', 'base_count': 5000},
            {'keyword': 'BTC Halving', 'base_count': 3500},
            {'keyword': 'Solana Airdrop', 'base_count': 2800},
            {'keyword': 'Layer 2', 'base_count': 2200},
            {'keyword': 'DeFi Yield', 'base_count': 1800},
            {'keyword': 'NFT Marketplace', 'base_count': 1500},
            {'keyword': 'Cross-chain Bridge', 'base_count': 1200},
            {'keyword': 'GameFi Launch', 'base_count': 1000},
            {'keyword': 'DAO Governance', 'base_count': 800},
            {'keyword': 'Privacy Coin', 'base_count': 600},
        ]
        
        base_time = datetime.now() - timedelta(hours=hours)
        
        for mock in mock_topics[:top_n]:
            # 添加随机波动
            mention_count = int(mock['base_count'] * random.uniform(0.8, 1.2))
            engagement = int(mention_count * random.uniform(2, 5))
            
            topic = Topic(
                keyword=mock['keyword'],
                mention_count=mention_count,
                engagement=engagement,
                sentiment_score=random.uniform(40, 80),
                growth_rate=random.uniform(-20, 100),
                top_posts=self._generate_mock_posts(mock['keyword'], 3),
                first_seen=base_time + timedelta(hours=random.uniform(0, hours)),
                platforms=random.sample(['twitter', 'reddit', 'telegram'], k=random.randint(1, 3))
            )
            
            topics.append(topic)
        
        # 按提及量排序
        topics.sort(key=lambda x: x.mention_count, reverse=True)
        return topics
    
    def _generate_mock_posts(self, keyword: str, num: int) -> List[Dict]:
        """生成模拟帖子"""
        posts = []
        
        templates = [
            f"{keyword} is trending! 🚀",
            f"What do you think about {keyword}?",
            f"Just saw the news about {keyword}, bullish!",
            f"{keyword} could be huge for crypto adoption",
            f"Don't miss out on {keyword}",
        ]
        
        for i in range(num):
            posts.append({
                'content': random.choice(templates),
                'likes': random.randint(10, 1000),
                'shares': random.randint(1, 100),
                'platform': random.choice(['twitter', 'reddit']),
                'author': f"user_{random.randint(1000, 9999)}"
            })
        
        return posts
    
    def track_keywords(self, keywords: List[str], hours: int = 24) -> Dict:
        """追踪特定关键词"""
        results = {}
        
        for keyword in keywords:
            # 模拟追踪数据
            mention_count = random.randint(100, 5000)
            
            results[keyword] = {
                'mention_count': mention_count,
                'engagement': int(mention_count * random.uniform(2, 5)),
                'sentiment': random.uniform(30, 80),
                'growth_24h': random.uniform(-50, 200),
                'top_sources': random.sample(['twitter', 'reddit', 'telegram'], k=random.randint(1, 3))
            }
        
        return results
    
    def detect_viral_content(self, min_engagement: int = 1000) -> List[Dict]:
        """检测病毒式内容"""
        viral_posts = []
        
        # 模拟病毒内容
        mock_viral = [
            {
                'content': "Bitcoin just broke $100K! 🚀🚀🚀",
                'engagement': 50000,
                'platform': 'twitter',
                'author': 'CryptoInfluencer',
                'shares': 12000
            },
            {
                'content': "Ethereum merge completed successfully!",
                'engagement': 35000,
                'platform': 'twitter',
                'author': 'VitalikButerin',
                'shares': 8000
            },
            {
                'content': "New DeFi protocol with 1000% APY",
                'engagement': 25000,
                'platform': 'reddit',
                'author': 'DeFiDegen',
                'shares': 5000
            }
        ]
        
        for post in mock_viral:
            if post['engagement'] >= min_engagement:
                viral_posts.append(post)
        
        return viral_posts
    
    def analyze_sentiment_by_topic(self, topic: str) -> Dict:
        """分析特定话题的情绪"""
        return {
            'topic': topic,
            'positive': random.uniform(30, 60),
            'negative': random.uniform(10, 30),
            'neutral': random.uniform(20, 40),
            'sentiment_score': random.uniform(40, 75)
        }
    
    def print_trending_report(self, topics: List[Topic]):
        """打印热门话题报告"""
        print(f"\n{'='*80}")
        print(f"🔥 热门话题报告 (过去24小时)")
        print(f"{'='*80}")
        
        for i, topic in enumerate(topics[:10], 1):
            # 增长指示器
            if topic.growth_rate > 50:
                growth_emoji = "🔥"
            elif topic.growth_rate > 0:
                growth_emoji = "📈"
            else:
                growth_emoji = "📉"
            
            # 情绪指示器
            if topic.sentiment_score > 65:
                sentiment_emoji = "🟢"
            elif topic.sentiment_score < 35:
                sentiment_emoji = "🔴"
            else:
                sentiment_emoji = "⚪"
            
            print(f"\n{i}. {topic.keyword}")
            print(f"   提及量: {topic.mention_count:,} | "
                  f"互动量: {topic.engagement:,} | "
                  f"平台: {', '.join(topic.platforms)}")
            print(f"   {growth_emoji} 增长: {topic.growth_rate:+.1f}% | "
                  f"{sentiment_emoji} 情绪: {topic.sentiment_score:.0f}/100")
            
            # 热门帖子预览
            if topic.top_posts:
                print(f"   💬 热门讨论:")
                for post in topic.top_posts[:2]:
                    print(f"      • {post['content'][:50]}... "
                          f"(👍 {post['likes']}, 🔄 {post['shares']})")
        
        print(f"{'='*80}\n")
    
    def print_keyword_tracking(self, results: Dict):
        """打印关键词追踪结果"""
        print(f"\n{'='*80}")
        print(f"🔍 关键词追踪报告")
        print(f"{'='*80}")
        print(f"{'关键词':<20} {'提及量':<12} {'互动量':<12} {'情绪':<10} {'增长':<12}")
        print(f"{'-'*80}")
        
        for keyword, data in results.items():
            growth_emoji = "📈" if data['growth_24h'] > 0 else "📉"
            print(f"{keyword:<20} {data['mention_count']:<12,} "
                  f"{data['engagement']:<12,} {data['sentiment']:<10.0f} "
                  f"{growth_emoji} {data['growth_24h']:+.1f}%")
        
        print(f"{'='*80}\n")
    
    def print_viral_content(self, posts: List[Dict]):
        """打印病毒内容"""
        print(f"\n{'='*80}")
        print(f"🚀 病毒式传播内容")
        print(f"{'='*80}")
        
        for i, post in enumerate(posts, 1):
            print(f"\n{i}. {post['content']}")
            print(f"   作者: {post['author']} | 平台: {post['platform']}")
            print(f"   👍 {post['engagement']:,} | 🔄 {post['shares']:,}")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("🔥 热点话题追踪器 - 演示")
    print("="*80)
    
    tracker = TrendingTopicsTracker()
    
    # 发现热门话题
    print("\n🔍 发现热门话题...")
    trending = tracker.discover_trending(hours=24, top_n=10)
    tracker.print_trending_report(trending)
    
    # 追踪关键词
    print("\n🔍 追踪特定关键词...")
    keywords = ['Ethereum', 'Bitcoin', 'Solana', 'Airdrop']
    keyword_results = tracker.track_keywords(keywords)
    tracker.print_keyword_tracking(keyword_results)
    
    # 检测病毒内容
    print("\n🚀 检测病毒式内容...")
    viral = tracker.detect_viral_content(min_engagement=1000)
    tracker.print_viral_content(viral)
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
