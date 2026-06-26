#!/usr/bin/env python3
"""
KOL监控器 - 追踪关键意见领袖的发言
"""

import os
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class KOLPost:
    """KOL发帖"""
    timestamp: datetime
    handle: str
    name: str
    content: str
    likes: int
    retweets: int
    sentiment: str
    mentioned_tokens: List[str]
    is_bullish: Optional[bool] = None

@dataclass
class KOLProfile:
    """KOL资料"""
    handle: str
    name: str
    followers: int
    influence_score: float  # 0-100
    accuracy_score: float   # 历史准确率
    posts: List[KOLPost]
    top_calls: List[Dict]   # 成功预测

class KOLMonitor:
    """KOL监控器"""
    
    def __init__(self):
        self.kol_database = self._load_kol_database()
        self.monitored_kols: Dict[str, KOLProfile] = {}
    
    def _load_kol_database(self) -> Dict:
        """加载KOL数据库"""
        return {
            'VitalikButerin': {
                'name': 'Vitalik Buterin',
                'handle': '@VitalikButerin',
                'followers': 5200000,
                'influence_score': 98,
                'focus': ['Ethereum', 'Layer2', 'Technical']
            },
            'cz_binance': {
                'name': 'CZ 🔶 Binance',
                'handle': '@cz_binance',
                'followers': 8700000,
                'influence_score': 95,
                'focus': ['Binance', 'Market', 'Regulation']
            },
            'SBF_FTX': {
                'name': 'SBF (inactive)',
                'handle': '@SBF_FTX',
                'followers': 1100000,
                'influence_score': 0,
                'focus': [],
                'status': 'inactive'
            },
            'elonmusk': {
                'name': 'Elon Musk',
                'handle': '@elonmusk',
                'followers': 175000000,
                'influence_score': 90,
                'focus': ['Dogecoin', 'Bitcoin', 'Meme']
            },
            'saylor': {
                'name': 'Michael Saylor',
                'handle': '@saylor',
                'followers': 3100000,
                'influence_score': 88,
                'focus': ['Bitcoin', 'Macro']
            }
        }
    
    def add_kol(self, handle: str, name: Optional[str] = None):
        """添加KOL到监控列表"""
        handle = handle.lstrip('@')
        
        if handle in self.kol_database:
            info = self.kol_database[handle]
            profile = KOLProfile(
                handle=info['handle'],
                name=info['name'],
                followers=info['followers'],
                influence_score=info['influence_score'],
                accuracy_score=random.uniform(60, 90),
                posts=[],
                top_calls=[]
            )
            self.monitored_kols[handle] = profile
            logger.info(f"✅ 已添加KOL: {info['name']}")
        else:
            # 未知KOL
            profile = KOLProfile(
                handle=f"@{handle}",
                name=name or handle,
                followers=random.randint(10000, 100000),
                influence_score=random.uniform(50, 80),
                accuracy_score=random.uniform(50, 80),
                posts=[],
                top_calls=[]
            )
            self.monitored_kols[handle] = profile
            logger.info(f"✅ 已添加KOL: {handle}")
    
    def fetch_recent_posts(self, handle: str, hours: int = 24) -> List[KOLPost]:
        """获取KOL最近发帖（模拟）"""
        posts = []
        base_time = datetime.now() - timedelta(hours=hours)
        
        # 根据KOL特点生成不同风格的帖子
        kol_styles = {
            'VitalikButerin': [
                "Layer 2 scaling solutions are making great progress. Excited about the future of Ethereum.",
                "Privacy and decentralization are not optional features, they are essential.",
                "Working on new research for account abstraction.",
            ],
            'cz_binance': [
                "Binance is committed to compliance and user protection.",
                "The crypto industry needs clearer regulations.",
                "4. 🚀",
            ],
            'elonmusk': [
                "Dogecoin to the moon! 🚀🐕",
                "Bitcoin is looking interesting...",
                "Who let the Doge out? 🤔",
            ],
            'saylor': [
                "Bitcoin is digital gold. The best store of value.",
                "Another company just added Bitcoin to their treasury.",
                "Inflation is theft. Bitcoin is the solution.",
            ]
        }
        
        templates = kol_styles.get(handle, [
            f"{handle} posted about crypto markets",
            "Market analysis thread 🧵",
            "New project announcement!",
        ])
        
        num_posts = random.randint(1, 5)
        
        for i in range(num_posts):
            post_time = base_time + timedelta(hours=random.uniform(0, hours))
            
            content = random.choice(templates)
            
            # 检测情绪
            sentiment = self._analyze_post_sentiment(content)
            
            # 检测提及的代币
            mentioned = self._extract_mentions(content)
            
            post = KOLPost(
                timestamp=post_time,
                handle=f"@{handle}",
                name=self.kol_database.get(handle, {}).get('name', handle),
                content=content,
                likes=random.randint(1000, 50000),
                retweets=random.randint(100, 10000),
                sentiment=sentiment,
                mentioned_tokens=mentioned,
                is_bullish=self._is_bullish(content)
            )
            
            posts.append(post)
        
        return sorted(posts, key=lambda x: x.timestamp, reverse=True)
    
    def _analyze_post_sentiment(self, content: str) -> str:
        """分析帖子情绪"""
        bullish_words = ['bullish', 'moon', 'pump', 'buy', 'hodl', '🚀', '看涨']
        bearish_words = ['bearish', 'dump', 'sell', 'crash', 'short', '📉', '看跌']
        
        content_lower = content.lower()
        
        bullish_count = sum(1 for w in bullish_words if w in content_lower)
        bearish_count = sum(1 for w in bearish_words if w in content_lower)
        
        if bullish_count > bearish_count:
            return 'bullish'
        elif bearish_count > bullish_count:
            return 'bearish'
        else:
            return 'neutral'
    
    def _extract_mentions(self, content: str) -> List[str]:
        """提取提及的代币"""
        tokens = []
        token_keywords = {
            'BTC': ['bitcoin', 'btc'],
            'ETH': ['ethereum', 'eth'],
            'DOGE': ['dogecoin', 'doge'],
            'SOL': ['solana', 'sol'],
            'BNB': ['bnb', 'binance coin']
        }
        
        content_lower = content.lower()
        
        for token, keywords in token_keywords.items():
            if any(kw in content_lower for kw in keywords):
                tokens.append(token)
        
        return tokens
    
    def _is_bullish(self, content: str) -> Optional[bool]:
        """判断是否看涨"""
        sentiment = self._analyze_post_sentiment(content)
        if sentiment == 'bullish':
            return True
        elif sentiment == 'bearish':
            return False
        return None
    
    def analyze_kol_influence(self, handle: str) -> Dict:
        """分析KOL影响力"""
        profile = self.monitored_kols.get(handle)
        if not profile:
            return {}
        
        # 计算平均互动量
        if profile.posts:
            avg_likes = sum(p.likes for p in profile.posts) / len(profile.posts)
            avg_retweets = sum(p.retweets for p in profile.posts) / len(profile.posts)
        else:
            avg_likes = 0
            avg_retweets = 0
        
        # 计算看涨/看跌比例
        bullish_posts = [p for p in profile.posts if p.is_bullish is True]
        bearish_posts = [p for p in profile.posts if p.is_bullish is False]
        
        return {
            'handle': handle,
            'name': profile.name,
            'followers': profile.followers,
            'influence_score': profile.influence_score,
            'accuracy_score': profile.accuracy_score,
            'avg_likes': avg_likes,
            'avg_retweets': avg_retweets,
            'recent_posts': len(profile.posts),
            'bullish_ratio': len(bullish_posts) / max(len(profile.posts), 1),
            'bearish_ratio': len(bearish_posts) / max(len(profile.posts), 1),
        }
    
    def detect_sentiment_change(self, handle: str) -> Optional[Dict]:
        """检测情绪转变"""
        profile = self.monitored_kols.get(handle)
        if not profile or len(profile.posts) < 2:
            return None
        
        recent = profile.posts[0]
        previous = profile.posts[1]
        
        if recent.is_bullish != previous.is_bullish and recent.is_bullish is not None:
            return {
                'handle': handle,
                'change': f"{previous.sentiment} -> {recent.sentiment}",
                'recent_post': recent.content,
                'alert_level': 'high' if profile.influence_score > 80 else 'medium'
            }
        
        return None
    
    def print_kol_report(self, handle: str):
        """打印KOL报告"""
        profile = self.monitored_kols.get(handle)
        if not profile:
            print(f"KOL未找到: {handle}")
            return
        
        # 获取最新帖子
        posts = self.fetch_recent_posts(handle)
        profile.posts = posts
        
        analysis = self.analyze_kol_influence(handle)
        
        print(f"\n{'='*80}")
        print(f"👤 KOL报告: {profile.name} ({profile.handle})")
        print(f"{'='*80}")
        
        print(f"\n📊 影响力指标:")
        print(f"   粉丝数: {profile.followers:,}")
        print(f"   影响力评分: {profile.influence_score}/100")
        print(f"   历史准确率: {analysis.get('accuracy_score', 0):.0f}%")
        
        print(f"\n📈 发帖统计:")
        print(f"   平均点赞: {analysis.get('avg_likes', 0):,.0f}")
        print(f"   平均转发: {analysis.get('avg_retweets', 0):,.0f}")
        print(f"   看涨比例: {analysis.get('bullish_ratio', 0)*100:.1f}%")
        print(f"   看跌比例: {analysis.get('bearish_ratio', 0)*100:.1f}%")
        
        print(f"\n📝 最近发言:")
        for post in posts[:5]:
            emoji = "🟢" if post.is_bullish is True else "🔴" if post.is_bullish is False else "⚪"
            print(f"\n   {emoji} {post.timestamp.strftime('%Y-%m-%d %H:%M')}")
            print(f"      {post.content}")
            print(f"      👍 {post.likes:,} | 🔄 {post.retweets:,} | 提及: {', '.join(post.mentioned_tokens) or 'None'}")
        
        # 检测情绪变化
        change = self.detect_sentiment_change(handle)
        if change:
            print(f"\n⚠️  情绪转变警告:")
            print(f"   {change['change']}")
            print(f"   最新: {change['recent_post']}")
        
        print(f"{'='*80}\n")
    
    def print_monitored_list(self):
        """打印监控列表"""
        print(f"\n{'='*80}")
        print(f"📋 监控的KOL列表 ({len(self.monitored_kols)}位)")
        print(f"{'='*80}")
        print(f"{'Handle':<20} {'名称':<25} {'粉丝数':<15} {'影响力':<10}")
        print(f"{'-'*80}")
        
        for handle, profile in self.monitored_kols.items():
            print(f"{profile.handle:<20} {profile.name:<25} "
                  f"{profile.followers:<15,} {profile.influence_score:<10.0f}")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("👤 KOL监控器 - 演示")
    print("="*80)
    
    monitor = KOLMonitor()
    
    # 添加KOL
    print("\n📝 添加KOL到监控列表...")
    monitor.add_kol('VitalikButerin')
    monitor.add_kol('cz_binance')
    monitor.add_kol('elonmusk')
    
    # 显示列表
    monitor.print_monitored_list()
    
    # 分析单个KOL
    print("\n🔍 分析 Vitalik...")
    monitor.print_kol_report('VitalikButerin')
    
    print("\n🔍 分析 Elon Musk...")
    monitor.print_kol_report('elonmusk')
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
