#!/usr/bin/env python3
"""
代币情绪分析器 - 分析特定代币的社交媒体情绪
"""

import os
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
from collections import Counter
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SentimentData:
    """情绪数据"""
    timestamp: datetime
    platform: str
    content: str
    sentiment_score: float  # 0-100
    engagement: int  # 点赞+转发+评论
    author_followers: int

@dataclass
class TokenSentiment:
    """代币情绪分析结果"""
    token: str
    overall_score: float
    sentiment_label: str
    bullish_pct: float
    bearish_pct: float
    neutral_pct: float
    volume_24h: int
    engagement_total: int
    trend: str

class TokenSentimentAnalyzer:
    """代币情绪分析器"""
    
    def __init__(self):
        self.bullish_keywords = [
            'moon', 'pump', 'bullish', 'bull', 'gem', '100x', '1000x',
            'buy', 'long', 'hodl', 'hold', 'accumulate', 'diamond hands',
            'rocket', 'liftoff', 'breakout', 'ATH', 'all time high',
            '看涨', '买入', '持有', '火箭', '暴涨'
        ]
        
        self.bearish_keywords = [
            'dump', 'bearish', 'bear', 'crash', 'rug', 'scam', 'ponzi',
            'sell', 'short', 'panic', 'paper hands', 'exit', 'get out',
            'dumping', 'bleeding', 'dead', 'exit liquidity', 'rekt',
            '看跌', '卖出', '暴跌', '骗局', '跑路'
        ]
    
    def fetch_social_data(self, token: str, hours: int = 24) -> List[SentimentData]:
        """获取社交媒体数据（模拟）"""
        data = []
        base_time = datetime.now() - timedelta(hours=hours)
        
        platforms = ['twitter', 'reddit']
        
        # 生成模拟数据
        for platform in platforms:
            num_posts = random.randint(50, 200)
            
            for i in range(num_posts):
                post_time = base_time + timedelta(minutes=random.uniform(0, hours * 60))
                
                # 生成随机情绪
                sentiment_type = random.choice(['bullish', 'bearish', 'neutral'])
                
                if sentiment_type == 'bullish':
                    content = random.choice([
                        f"{token} is going to moon! 🚀",
                        f"Just bought more {token}, this is the gem! 💎",
                        f"{token} looking strong, bullish! 📈",
                    ])
                    sentiment_score = random.uniform(65, 95)
                elif sentiment_type == 'bearish':
                    content = random.choice([
                        f"{token} is dumping hard! 📉",
                        f"Selling all my {token}! 🚨",
                        f"{token} going to zero! ⚠️",
                    ])
                    sentiment_score = random.uniform(5, 35)
                else:
                    content = random.choice([
                        f"Watching {token} closely",
                        f"What do you think about {token}?",
                        f"{token} price update",
                    ])
                    sentiment_score = random.uniform(40, 60)
                
                data.append(SentimentData(
                    timestamp=post_time,
                    platform=platform,
                    content=content,
                    sentiment_score=sentiment_score,
                    engagement=random.randint(0, 1000),
                    author_followers=random.randint(100, 100000)
                ))
        
        return data
    
    def analyze_sentiment(self, token: str, hours: int = 24) -> TokenSentiment:
        """分析代币情绪"""
        data = self.fetch_social_data(token, hours)
        
        if not data:
            return TokenSentiment(
                token=token,
                overall_score=50,
                sentiment_label="neutral",
                bullish_pct=0,
                bearish_pct=0,
                neutral_pct=100,
                volume_24h=0,
                engagement_total=0,
                trend="flat"
            )
        
        # 计算各项统计
        scores = [d.sentiment_score for d in data]
        overall_score = sum(scores) / len(scores)
        
        # 分类统计
        bullish_count = sum(1 for s in scores if s >= 65)
        bearish_count = sum(1 for s in scores if s <= 35)
        neutral_count = len(scores) - bullish_count - bearish_count
        
        total = len(scores)
        bullish_pct = bullish_count / total * 100
        bearish_pct = bearish_count / total * 100
        neutral_pct = neutral_count / total * 100
        
        # 确定情绪标签
        if overall_score >= 75:
            sentiment_label = "extreme_greed"
        elif overall_score >= 60:
            sentiment_label = "greed"
        elif overall_score >= 40:
            sentiment_label = "neutral"
        elif overall_score >= 25:
            sentiment_label = "fear"
        else:
            sentiment_label = "extreme_fear"
        
        # 计算总互动量
        engagement_total = sum(d.engagement for d in data)
        
        # 趋势分析（简化）
        if len(data) > 10:
            half = len(scores) // 2
            early_avg = sum(scores[:half]) / half
            late_avg = sum(scores[half:]) / (len(scores) - half)
            
            if late_avg > early_avg + 5:
                trend = "improving"
            elif late_avg < early_avg - 5:
                trend = "worsening"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return TokenSentiment(
            token=token,
            overall_score=overall_score,
            sentiment_label=sentiment_label,
            bullish_pct=bullish_pct,
            bearish_pct=bearish_pct,
            neutral_pct=neutral_pct,
            volume_24h=len(data),
            engagement_total=engagement_total,
            trend=trend
        )
    
    def get_sentiment_history(self, token: str, days: int = 7) -> List[Dict]:
        """获取情绪历史"""
        history = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            # 模拟历史数据
            score = random.uniform(30, 80)
            
            history.append({
                'date': date.strftime('%Y-%m-%d'),
                'score': score,
                'volume': random.randint(100, 500)
            })
        
        return list(reversed(history))
    
    def print_sentiment_report(self, result: TokenSentiment):
        """打印情绪报告"""
        emoji_map = {
            'extreme_greed': ('🤑', '极度贪婪'),
            'greed': ('😊', '贪婪'),
            'neutral': ('😐', '中性'),
            'fear': ('😰', '恐慌'),
            'extreme_fear': ('😱', '极度恐慌')
        }
        
        emoji, label = emoji_map.get(result.sentiment_label, ('❓', '未知'))
        
        print(f"\n{'='*80}")
        print(f"{emoji} {result.token} 情绪分析报告")
        print(f"{'='*80}")
        
        print(f"\n📊 总体情绪: {label}")
        print(f"   情绪分数: {result.overall_score:.1f}/100")
        
        trend_emoji = {
            'improving': '📈',
            'worsening': '📉',
            'stable': '➡️',
            'insufficient_data': '❓'
        }.get(result.trend, '❓')
        
        print(f"   趋势: {trend_emoji} {result.trend}")
        
        print(f"\n📈 情绪分布:")
        print(f"   🟢 看涨: {result.bullish_pct:.1f}%")
        print(f"   🔴 看跌: {result.bearish_pct:.1f}%")
        print(f"   ⚪ 中性: {result.neutral_pct:.1f}%")
        
        print(f"\n📊 数据指标:")
        print(f"   24h提及量: {result.volume_24h}")
        print(f"   总互动量: {result.engagement_total}")
        
        # 预警提示
        if result.sentiment_label == 'extreme_greed':
            print(f"\n⚠️  警告: 市场极度贪婪，注意回调风险！")
        elif result.sentiment_label == 'extreme_fear':
            print(f"\n💡 提示: 市场极度恐慌，可能存在抄底机会。")
        
        print(f"{'='*80}\n")
    
    def compare_tokens(self, tokens: List[str]) -> Dict:
        """对比多个代币的情绪"""
        comparison = {}
        
        for token in tokens:
            sentiment = self.analyze_sentiment(token)
            comparison[token] = {
                'score': sentiment.overall_score,
                'sentiment': sentiment.sentiment_label,
                'volume': sentiment.volume_24h
            }
        
        return comparison
    
    def print_comparison(self, comparison: Dict):
        """打印对比结果"""
        print(f"\n{'='*80}")
        print(f"📊 代币情绪对比")
        print(f"{'='*80}")
        print(f"{'代币':<10} {'情绪分数':<15} {'情绪标签':<15} {'提及量':<15}")
        print(f"{'-'*80}")
        
        # 按分数排序
        sorted_tokens = sorted(
            comparison.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )
        
        for token, data in sorted_tokens:
            print(f"{token:<10} {data['score']:>12.1f} {data['sentiment']:<15} {data['volume']:<15}")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("📊 代币情绪分析器 - 演示")
    print("="*80)
    
    analyzer = TokenSentimentAnalyzer()
    
    # 分析ETH
    print("\n🔍 分析 ETH...")
    eth_sentiment = analyzer.analyze_sentiment('ETH', hours=24)
    analyzer.print_sentiment_report(eth_sentiment)
    
    # 分析BTC
    print("\n🔍 分析 BTC...")
    btc_sentiment = analyzer.analyze_sentiment('BTC', hours=24)
    analyzer.print_sentiment_report(btc_sentiment)
    
    # 对比
    print("\n📊 对比 ETH vs BTC...")
    comparison = analyzer.compare_tokens(['ETH', 'BTC', 'SOL'])
    analyzer.print_comparison(comparison)
    
    # 历史趋势
    print("\n📈 ETH 7天情绪历史...")
    history = analyzer.get_sentiment_history('ETH', days=7)
    for h in history:
        bar = '█' * int(h['score'] / 5)
        print(f"{h['date']} |{bar:<20}| {h['score']:.0f}")
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
