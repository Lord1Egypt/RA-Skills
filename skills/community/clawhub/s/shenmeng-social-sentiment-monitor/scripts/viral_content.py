#!/usr/bin/env python3
"""
病毒内容追踪器 - 发现和分析病毒式传播的内容
"""

import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ViralContent:
    """病毒内容"""
    id: str
    platform: str
    content: str
    author: str
    author_followers: int
    created_at: datetime
    likes: int
    shares: int
    comments: int
    engagement_rate: float
    velocity: float  # 传播速度
    topics: List[str]
    sentiment: str

class ViralContentTracker:
    """病毒内容追踪器"""
    
    def __init__(self):
        self.viral_threshold = {
            'twitter': {'likes': 1000, 'retweets': 500},
            'reddit': {'upvotes': 500, 'comments': 100}
        }
    
    def discover_viral_content(self, platform: str = 'twitter', hours: int = 24, 
                                min_engagement: int = 1000) -> List[ViralContent]:
        """发现病毒内容"""
        viral_posts = []
        base_time = datetime.now() - timedelta(hours=hours)
        
        # 模拟病毒内容
        mock_viral = [
            {
                'content': "Bitcoin just broke $100K! This is history in the making! 🚀",
                'author': 'CryptoKing',
                'followers': 500000,
                'likes': 50000,
                'shares': 15000,
                'comments': 3000,
                'topics': ['BTC', 'bullish'],
                'sentiment': 'bullish'
            },
            {
                'content': "Ethereum merge completed successfully! The future is here. 💎",
                'author': 'ETHMaximalist',
                'followers': 200000,
                'likes': 35000,
                'shares': 8000,
                'comments': 2000,
                'topics': ['ETH', 'technology'],
                'sentiment': 'bullish'
            },
            {
                'content': "MAJOR EXCHANGE HACKED! Withdraw your funds NOW! 🚨",
                'author': 'CryptoWhistleblower',
                'followers': 50000,
                'likes': 25000,
                'shares': 20000,
                'comments': 5000,
                'topics': ['security', 'hack'],
                'sentiment': 'bearish'
            },
            {
                'content': "This new DeFi protocol is giving 1000% APY. Too good to be true? 🤔",
                'author': 'DeFiDegen',
                'followers': 100000,
                'likes': 18000,
                'shares': 6000,
                'comments': 2500,
                'topics': ['DeFi', 'yield'],
                'sentiment': 'neutral'
            },
            {
                'content': "Dogecoin to the moon! Elon was right! 🐕🌙",
                'author': 'DogeArmy',
                'followers': 300000,
                'likes': 45000,
                'shares': 12000,
                'comments': 4000,
                'topics': ['DOGE', 'meme'],
                'sentiment': 'bullish'
            }
        ]
        
        for i, mock in enumerate(mock_viral):
            total_engagement = mock['likes'] + mock['shares'] * 2 + mock['comments'] * 3
            
            if total_engagement >= min_engagement:
                post_time = base_time + timedelta(hours=random.uniform(0, hours))
                
                viral = ViralContent(
                    id=f"viral_{i}",
                    platform=platform,
                    content=mock['content'],
                    author=mock['author'],
                    author_followers=mock['followers'],
                    created_at=post_time,
                    likes=mock['likes'],
                    shares=mock['shares'],
                    comments=mock['comments'],
                    engagement_rate=total_engagement / max(mock['followers'], 1) * 100,
                    velocity=random.uniform(1, 10),
                    topics=mock['topics'],
                    sentiment=mock['sentiment']
                )
                
                viral_posts.append(viral)
        
        # 按总互动量排序
        viral_posts.sort(key=lambda x: x.likes + x.shares + x.comments, reverse=True)
        return viral_posts
    
    def track_spread(self, content_id: str) -> Dict:
        """追踪内容传播路径"""
        # 模拟传播数据
        spread_data = {
            'content_id': content_id,
            'original_post': {
                'author': 'OriginalPoster',
                'timestamp': datetime.now() - timedelta(hours=6),
                'platform': 'twitter'
            },
            'spread_timeline': []
        }
        
        # 生成传播时间线
        for i in range(10):
            spread_data['spread_timeline'].append({
                'time': datetime.now() - timedelta(hours=6-i*0.5),
                'shares': int(1000 * (1.5 ** i)),
                'reach': int(10000 * (1.8 ** i)),
                'platforms': random.sample(['twitter', 'reddit', 'telegram'], 
                                         k=random.randint(1, 3))
            })
        
        return spread_data
    
    def analyze_impact(self, content: ViralContent) -> Dict:
        """分析内容的市场影响"""
        # 模拟影响分析
        impact_score = min(
            (content.likes + content.shares * 2) / 10000,
            100
        )
        
        return {
            'content_id': content.id,
            'impact_score': impact_score,
            'estimated_reach': content.likes * 20,  # 假设每个点赞有20个浏览
            'sentiment_impact': content.sentiment,
            'affected_tokens': content.topics,
            'potential_price_impact': 'high' if impact_score > 50 else 'medium' if impact_score > 20 else 'low'
        }
    
    def detect_manipulation(self, content: ViralContent) -> Optional[Dict]:
        """检测是否为操纵行为"""
        red_flags = []
        
        # 检查作者粉丝与互动比
        if content.author_followers < 1000 and content.likes > 10000:
            red_flags.append('suspicious_engagement_ratio')
        
        # 检查传播速度异常
        if content.velocity > 8:
            red_flags.append('unnatural_velocity')
        
        # 检查内容模式
        if any(word in content.content.lower() for word in ['pump', 'buy now', 'don\'t miss']):
            red_flags.append('pump_language')
        
        if len(red_flags) >= 2:
            return {
                'is_suspicious': True,
                'confidence': min(len(red_flags) * 30, 100),
                'red_flags': red_flags,
                'recommendation': '可能是协调推广，谨慎对待'
            }
        
        return None
    
    def get_trending_hashtags(self, viral_content: List[ViralContent]) -> List[Dict]:
        """获取 trending hashtags"""
        hashtag_counts = {}
        
        for content in viral_content:
            # 从topics提取hashtag
            for topic in content.topics:
                hashtag = f"#{topic}"
                if hashtag not in hashtag_counts:
                    hashtag_counts[hashtag] = {'count': 0, 'engagement': 0}
                hashtag_counts[hashtag]['count'] += 1
                hashtag_counts[hashtag]['engagement'] += content.likes + content.shares
        
        # 转换为列表并排序
        hashtags = [
            {'tag': tag, 'count': data['count'], 'engagement': data['engagement']}
            for tag, data in hashtag_counts.items()
        ]
        
        hashtags.sort(key=lambda x: x['engagement'], reverse=True)
        return hashtags[:10]
    
    def print_viral_report(self, content_list: List[ViralContent]):
        """打印病毒内容报告"""
        print(f"\n{'='*80}")
        print(f"🚀 病毒内容报告")
        print(f"{'='*80}")
        
        for i, content in enumerate(content_list[:5], 1):
            # 检测操纵
            manipulation = self.detect_manipulation(content)
            
            print(f"\n{i}. {content.content[:60]}...")
            print(f"   作者: {content.author} ({content.author_followers:,} 粉丝)")
            print(f"   时间: {content.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"   👍 {content.likes:,} | 🔄 {content.shares:,} | 💬 {content.comments:,}")
            print(f"   互动率: {content.engagement_rate:.2f}% | 传播速度: {content.velocity:.1f}x")
            print(f"   主题: {', '.join(content.topics)} | 情绪: {content.sentiment}")
            
            if manipulation:
                print(f"   ⚠️  可疑标记: {manipulation['confidence']}% 可能是协调推广")
            
            # 影响分析
            impact = self.analyze_impact(content)
            print(f"   📊 影响评分: {impact['impact_score']:.0f}/100 | 预估触达: {impact['estimated_reach']:,}")
        
        # Trending hashtags
        print(f"\n🏷️ Trending Hashtags:")
        hashtags = self.get_trending_hashtags(content_list)
        for tag in hashtags[:5]:
            print(f"   {tag['tag']}: {tag['count']}次出现, {tag['engagement']:,}互动")
        
        print(f"{'='*80}\n")
    
    def print_spread_analysis(self, content_id: str):
        """打印传播分析"""
        spread = self.track_spread(content_id)
        
        print(f"\n{'='*80}")
        print(f"📈 内容传播分析: {content_id}")
        print(f"{'='*80}")
        
        print(f"\n原始发布:")
        print(f"   作者: {spread['original_post']['author']}")
        print(f"   平台: {spread['original_post']['platform']}")
        print(f"   时间: {spread['original_post']['timestamp'].strftime('%Y-%m-%d %H:%M')}")
        
        print(f"\n传播时间线:")
        print(f"{'时间':<20} {'转发量':<12} {'触达人数':<15} {'平台':<20}")
        print(f"{'-'*70}")
        
        for event in spread['spread_timeline']:
            print(f"{event['time'].strftime('%m-%d %H:%M'):<20} "
                  f"{event['shares']:<12,} {event['reach']:<15,} "
                  f"{', '.join(event['platforms']):<20}")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("🚀 病毒内容追踪器 - 演示")
    print("="*80)
    
    tracker = ViralContentTracker()
    
    # 发现病毒内容
    print("\n🔍 发现病毒内容...")
    viral = tracker.discover_viral_content(min_engagement=1000)
    tracker.print_viral_report(viral)
    
    # 追踪传播
    if viral:
        print("\n📈 追踪传播路径...")
        tracker.print_spread_analysis(viral[0].id)
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
