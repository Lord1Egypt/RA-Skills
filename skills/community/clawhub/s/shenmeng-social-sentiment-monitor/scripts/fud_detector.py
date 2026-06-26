#!/usr/bin/env python3
"""
FUD检测器 - 检测负面舆情和恐慌情绪
"""

import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
from collections import Counter
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class FUDAlert:
    """FUD预警"""
    timestamp: datetime
    token: str
    alert_level: str  # 'low', 'medium', 'high', 'critical'
    fud_type: str
    description: str
    sources: List[Dict]
    sentiment_score: float
    spread_velocity: float  # 传播速度

class FUDDetector:
    """FUD检测器"""
    
    def __init__(self):
        self.fud_keywords = [
            'scam', 'rug', 'rugpull', 'ponzi', 'fake',
            'hack', 'exploit', 'stolen', 'drained',
            'dump', 'crash', 'collapse', 'dead',
            'investigation', 'SEC', 'lawsuit', 'ban',
            'panic', 'sell', 'exit', 'get out',
            '骗局', '跑路', '黑客', '暴跌', '崩盘'
        ]
        
        self.fud_patterns = {
            'hack': ['hacked', 'exploit', 'drained', 'stolen funds'],
            'rugpull': ['rug', 'dev sold', 'team dumped', 'lp removed'],
            'regulation': ['SEC', 'regulation', 'banned', 'illegal'],
            'technical': ['bug', 'vulnerability', 'failed', 'broken'],
            'fud_campaign': ['coordinated fud', 'paid fud', 'fake news']
        }
        
        self.alert_history: List[FUDAlert] = []
    
    def analyze_content(self, content: str) -> Dict:
        """分析内容的FUD程度"""
        content_lower = content.lower()
        
        # 计算FUD关键词匹配
        fud_matches = [kw for kw in self.fud_keywords if kw in content_lower]
        
        # 检测FUD类型
        detected_types = []
        for fud_type, patterns in self.fud_patterns.items():
            if any(p in content_lower for p in patterns):
                detected_types.append(fud_type)
        
        # 计算FUD分数 (0-100)
        base_score = len(fud_matches) * 10
        type_bonus = len(detected_types) * 15
        fud_score = min(base_score + type_bonus, 100)
        
        return {
            'fud_score': fud_score,
            'matched_keywords': fud_matches,
            'detected_types': detected_types,
            'is_fud': fud_score >= 30
        }
    
    def monitor_token(self, token: str, hours: int = 24, sensitivity: str = 'medium') -> List[FUDAlert]:
        """监控代币的负面信息"""
        alerts = []
        base_time = datetime.now() - timedelta(hours=hours)
        
        # 根据敏感度设置阈值
        thresholds = {
            'low': 50,
            'medium': 30,
            'high': 20
        }
        threshold = thresholds.get(sensitivity, 30)
        
        # 生成模拟数据
        mock_posts = self._generate_mock_posts(token)
        
        for post in mock_posts:
            analysis = self.analyze_content(post['content'])
            
            if analysis['is_fud'] and analysis['fud_score'] >= threshold:
                # 确定预警级别
                if analysis['fud_score'] >= 80:
                    level = 'critical'
                elif analysis['fud_score'] >= 60:
                    level = 'high'
                elif analysis['fud_score'] >= 40:
                    level = 'medium'
                else:
                    level = 'low'
                
                alert = FUDAlert(
                    timestamp=post['timestamp'],
                    token=token,
                    alert_level=level,
                    fud_type=analysis['detected_types'][0] if analysis['detected_types'] else 'general',
                    description=f"检测到{analysis['fud_score']:.0f}分的FUD内容",
                    sources=[post],
                    sentiment_score=analysis['fud_score'],
                    spread_velocity=random.uniform(1, 10)
                )
                
                alerts.append(alert)
        
        # 按严重程度排序
        alert_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        alerts.sort(key=lambda x: alert_order.get(x.alert_level, 4))
        
        return alerts
    
    def _generate_mock_posts(self, token: str) -> List[Dict]:
        """生成模拟帖子"""
        posts = []
        base_time = datetime.now() - timedelta(hours=24)
        
        # 正常帖子
        normal_templates = [
            f"What do you think about {token}?",
            f"{token} price analysis",
            f"Holding {token} for long term",
        ]
        
        # FUD帖子
        fud_templates = [
            f"{token} is a scam! Don't buy!",
            f"{token} devs just dumped their bags",
            f"{token} hacked! Funds drained!",
            f"SEC investigating {token}",
            f"{token} contract has a bug, stay away!",
            f"Rugpull confirmed for {token}",
        ]
        
        # 生成帖子
        for i in range(50):
            post_time = base_time + timedelta(minutes=random.uniform(0, 1440))
            
            if random.random() < 0.3:  # 30%概率是FUD
                content = random.choice(fud_templates)
            else:
                content = random.choice(normal_templates)
            
            posts.append({
                'timestamp': post_time,
                'content': content,
                'platform': random.choice(['twitter', 'reddit']),
                'engagement': random.randint(10, 1000)
            })
        
        return posts
    
    def detect_coordinated_fud(self, alerts: List[FUDAlert]) -> Optional[Dict]:
        """检测协调FUD攻击"""
        if len(alerts) < 5:
            return None
        
        # 检查时间集中度
        timestamps = [a.timestamp for a in alerts]
        time_range = max(timestamps) - min(timestamps)
        
        if time_range < timedelta(hours=2):
            return {
                'detected': True,
                'type': 'coordinated_fud',
                'description': f'检测到可能的协调FUD攻击，{len(alerts)}条负面信息在{time_range}内集中出现',
                'recommendation': '建议核实信息来源，谨慎对待'
            }
        
        return None
    
    def verify_fud(self, alert: FUDAlert) -> Dict:
        """验证FUD信息的真实性"""
        # 模拟验证过程
        verification_score = random.uniform(0, 100)
        
        if verification_score >= 70:
            status = 'confirmed'
            confidence = 'high'
        elif verification_score >= 40:
            status = 'unverified'
            confidence = 'medium'
        else:
            status = 'likely_false'
            confidence = 'high'
        
        return {
            'status': status,
            'confidence': confidence,
            'verification_score': verification_score,
            'sources_checked': random.randint(3, 10),
            'official_response': random.choice([True, False])
        }
    
    def get_fud_statistics(self, alerts: List[FUDAlert]) -> Dict:
        """获取FUD统计"""
        if not alerts:
            return {}
        
        by_level = Counter(a.alert_level for a in alerts)
        by_type = Counter(a.fud_type for a in alerts)
        
        return {
            'total_alerts': len(alerts),
            'by_level': dict(by_level),
            'by_type': dict(by_type),
            'avg_sentiment_score': sum(a.sentiment_score for a in alerts) / len(alerts),
            'highest_severity': min(alerts, key=lambda x: {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}.get(x.alert_level, 4)).alert_level
        }
    
    def print_fud_report(self, token: str, alerts: List[FUDAlert]):
        """打印FUD报告"""
        if not alerts:
            print(f"\n✅ {token}: 未检测到显著FUD信息")
            return
        
        print(f"\n{'='*80}")
        print(f"🚨 {token} FUD检测报告")
        print(f"{'='*80}")
        
        # 统计
        stats = self.get_fud_statistics(alerts)
        print(f"\n📊 统计概况:")
        print(f"   总预警数: {stats['total_alerts']}")
        print(f"   严重等级分布: {stats['by_level']}")
        print(f"   FUD类型: {stats['by_type']}")
        print(f"   平均负面情绪分: {stats['avg_sentiment_score']:.1f}")
        
        # 检测协调攻击
        coordinated = self.detect_coordinated_fud(alerts)
        if coordinated:
            print(f"\n⚠️  {coordinated['description']}")
        
        # 详细预警
        print(f"\n🔍 详细预警:")
        for alert in alerts[:10]:  # 显示前10条
            emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🔵'}.get(alert.alert_level, '⚪')
            print(f"\n   {emoji} [{alert.alert_level.upper()}] {alert.timestamp.strftime('%m-%d %H:%M')}")
            print(f"      类型: {alert.fud_type}")
            print(f"      描述: {alert.description}")
            print(f"      传播速度: {alert.spread_velocity:.1f}x")
            
            # 验证结果
            verification = self.verify_fud(alert)
            if verification['status'] == 'likely_false':
                print(f"      ✅ 疑似谣言 (可信度: {verification['confidence']})")
        
        # 建议
        print(f"\n💡 建议:")
        if stats['highest_severity'] in ['critical', 'high']:
            print(f"   ⚠️  发现严重负面信息，建议立即核实并评估风险")
        else:
            print(f"   负面信息可控，持续监控即可")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("🚨 FUD检测器 - 演示")
    print("="*80)
    
    detector = FUDDetector()
    
    # 监控ETH
    print("\n🔍 监控 ETH...")
    eth_alerts = detector.monitor_token('ETH', sensitivity='medium')
    detector.print_fud_report('ETH', eth_alerts)
    
    # 监控一个高风险代币
    print("\n🔍 监控 RANDOM_TOKEN (高风险)...")
    random_alerts = detector.monitor_token('RANDOM_TOKEN', sensitivity='high')
    detector.print_fud_report('RANDOM_TOKEN', random_alerts)
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
