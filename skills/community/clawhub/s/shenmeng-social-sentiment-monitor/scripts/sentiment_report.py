#!/usr/bin/env python3
"""
舆情报告生成器 - 生成综合分析报告
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict
from dataclasses import dataclass
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SentimentReport:
    """舆情报告"""
    token: str
    period: str
    generated_at: datetime
    overall_sentiment: float
    sentiment_trend: str
    mention_volume: int
    engagement_total: int
    key_topics: List[str]
    kol_mentions: int
    fud_alerts: int
    viral_content: int
    recommendations: List[str]

class SentimentReportGenerator:
    """舆情报告生成器"""
    
    def __init__(self):
        self.report_templates = {
            'bullish': [
                "市场情绪积极，看好声音占主导",
                "社区讨论活跃，新项目备受关注",
                "技术面突破引发热议"
            ],
            'bearish': [
                "市场情绪低迷，恐慌情绪蔓延",
                "负面消息集中，需关注风险",
                "卖压较重，观望情绪浓厚"
            ],
            'neutral': [
                "市场情绪平稳，多空分歧不大",
                "缺乏明确方向，等待催化剂",
                "正常波动范围内"
            ]
        }
    
    def generate_report(self, token: str, days: int = 7) -> SentimentReport:
        """生成舆情报告"""
        # 模拟数据生成
        base_sentiment = random.uniform(30, 80)
        
        # 确定趋势
        if base_sentiment > 60:
            trend = 'improving'
            trend_label = '上升'
        elif base_sentiment < 40:
            trend = 'declining'
            trend_label = '下降'
        else:
            trend = 'stable'
            trend_label = '平稳'
        
        # 生成建议
        recommendations = self._generate_recommendations(base_sentiment, trend)
        
        return SentimentReport(
            token=token,
            period=f"{days}天",
            generated_at=datetime.now(),
            overall_sentiment=base_sentiment,
            sentiment_trend=trend,
            mention_volume=random.randint(1000, 50000),
            engagement_total=random.randint(5000, 200000),
            key_topics=random.sample(['DeFi', 'NFT', 'Layer2', 'Staking', 'Governance'], k=3),
            kol_mentions=random.randint(5, 50),
            fud_alerts=random.randint(0, 10),
            viral_content=random.randint(0, 5),
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, sentiment: float, trend: str) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if sentiment > 75:
            recommendations.append("⚠️ 市场过度乐观，注意回调风险")
            recommendations.append("建议分批获利了结")
        elif sentiment > 60:
            recommendations.append("市场情绪积极，可考虑持有")
            recommendations.append("关注突破后的持续性")
        elif sentiment > 40:
            recommendations.append("市场情绪中性，观望为主")
            recommendations.append("等待明确信号")
        elif sentiment > 25:
            recommendations.append("市场情绪低迷，谨慎操作")
            recommendations.append("可考虑分批建仓")
        else:
            recommendations.append("⚠️ 市场极度恐慌，可能是抄底机会")
            recommendations.append("建议逐步积累")
        
        if trend == 'improving':
            recommendations.append("趋势向好，关注持续性")
        elif trend == 'declining':
            recommendations.append("趋势走弱，注意止损")
        
        return recommendations
    
    def compare_tokens(self, tokens: List[str], days: int = 7) -> Dict:
        """对比多个代币"""
        comparison = {}
        
        for token in tokens:
            report = self.generate_report(token, days)
            comparison[token] = {
                'sentiment': report.overall_sentiment,
                'trend': report.sentiment_trend,
                'volume': report.mention_volume,
                'fud_alerts': report.fud_alerts,
                'rank': 0  # 稍后计算
            }
        
        # 计算排名
        sorted_tokens = sorted(
            comparison.items(),
            key=lambda x: x[1]['sentiment'],
            reverse=True
        )
        
        for rank, (token, _) in enumerate(sorted_tokens, 1):
            comparison[token]['rank'] = rank
        
        return comparison
    
    def print_report(self, report: SentimentReport):
        """打印报告"""
        sentiment_emoji = {
            'improving': '📈',
            'declining': '📉',
            'stable': '➡️'
        }.get(report.sentiment_trend, '❓')
        
        sentiment_label = {
            'improving': '上升',
            'declining': '下降',
            'stable': '平稳'
        }.get(report.sentiment_trend, '未知')
        
        # 总体情绪等级
        if report.overall_sentiment >= 75:
            overall_label = "🤑 极度贪婪"
        elif report.overall_sentiment >= 60:
            overall_label = "😊 贪婪"
        elif report.overall_sentiment >= 40:
            overall_label = "😐 中性"
        elif report.overall_sentiment >= 25:
            overall_label = "😰 恐慌"
        else:
            overall_label = "😱 极度恐慌"
        
        print(f"\n{'='*80}")
        print(f"📊 {report.token} 舆情报告 ({report.period})")
        print(f"生成时间: {report.generated_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*80}")
        
        print(f"\n🎯 总体情绪: {overall_label}")
        print(f"   情绪分数: {report.overall_sentiment:.1f}/100")
        print(f"   趋势: {sentiment_emoji} {sentiment_label}")
        
        print(f"\n📈 数据概览:")
        print(f"   提及量: {report.mention_volume:,}")
        print(f"   总互动: {report.engagement_total:,}")
        print(f"   KOL提及: {report.kol_mentions}次")
        print(f"   FUD预警: {report.fud_alerts}次")
        print(f"   病毒内容: {report.viral_content}条")
        
        print(f"\n🏷️ 热门话题:")
        for topic in report.key_topics:
            print(f"   • {topic}")
        
        print(f"\n💡 建议:")
        for rec in report.recommendations:
            print(f"   • {rec}")
        
        print(f"{'='*80}\n")
    
    def print_comparison(self, comparison: Dict, days: int):
        """打印对比报告"""
        print(f"\n{'='*80}")
        print(f"📊 代币情绪对比报告 ({days}天)")
        print(f"{'='*80}")
        print(f"{'排名':<6} {'代币':<10} {'情绪分':<12} {'趋势':<10} {'提及量':<12} {'FUD':<8}")
        print(f"{'-'*80}")
        
        # 按排名排序
        sorted_items = sorted(comparison.items(), key=lambda x: x[1]['rank'])
        
        for token, data in sorted_items:
            trend_emoji = {
                'improving': '📈',
                'declining': '📉',
                'stable': '➡️'
            }.get(data['trend'], '❓')
            
            print(f"{data['rank']:<6} {token:<10} {data['sentiment']:>10.1f} "
                  f"{trend_emoji:<8} {data['volume']:<12,} {data['fud_alerts']:<8}")
        
        print(f"{'='*80}\n")
    
    def export_report(self, report: SentimentReport, filename: str):
        """导出报告为JSON"""
        import json
        
        data = {
            'token': report.token,
            'period': report.period,
            'generated_at': report.generated_at.isoformat(),
            'overall_sentiment': report.overall_sentiment,
            'sentiment_trend': report.sentiment_trend,
            'metrics': {
                'mention_volume': report.mention_volume,
                'engagement_total': report.engagement_total,
                'kol_mentions': report.kol_mentions,
                'fud_alerts': report.fud_alerts,
                'viral_content': report.viral_content
            },
            'key_topics': report.key_topics,
            'recommendations': report.recommendations
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"报告已导出到: {filename}")


def demo():
    """演示"""
    print("📊 舆情报告生成器 - 演示")
    print("="*80)
    
    generator = SentimentReportGenerator()
    
    # 生成单个报告
    print("\n📝 生成 ETH 7天报告...")
    eth_report = generator.generate_report('ETH', days=7)
    generator.print_report(eth_report)
    
    # 生成BTC报告
    print("\n📝 生成 BTC 7天报告...")
    btc_report = generator.generate_report('BTC', days=7)
    generator.print_report(btc_report)
    
    # 对比多个代币
    print("\n📊 对比 ETH, BTC, SOL...")
    comparison = generator.compare_tokens(['ETH', 'BTC', 'SOL'], days=7)
    generator.print_comparison(comparison, days=7)
    
    # 导出报告
    generator.export_report(eth_report, 'eth_sentiment_report.json')
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
