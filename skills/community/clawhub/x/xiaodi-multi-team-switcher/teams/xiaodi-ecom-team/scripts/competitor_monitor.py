#!/usr/bin/env python3
"""
竞品监控器 - 价格追踪、BSR监控、差评分析
支持：Amazon、淘宝等平台
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

# 配置
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
MONITOR_FILE = DATA_DIR / "competitor_monitor.json"


@dataclass
class Competitor:
    """竞品数据"""
    asin: str
    name: str
    url: str
    platform: str = "amazon"
    
    # 价格追踪
    current_price: float = 0
    previous_price: float = 0
    price_history: List[Dict] = field(default_factory=list)
    
    # BSR 追踪
    current_bsr: int = 0
    previous_bsr: int = 0
    bsr_history: List[Dict] = field(default_factory=list)
    
    # 评价
    rating: float = 0
    review_count: int = 0
    
    # Coupon
    has_coupon: bool = False
    coupon_value: float = 0
    
    # 最后更新
    last_updated: str = ""


@dataclass
class Review:
    """评论数据"""
    id: str
    rating: int
    title: str
    content: str
    author: str
    date: str
    verified_purchase: bool = False
    helpful_votes: int = 0


class ReviewAnalyzer:
    """评论分析器"""
    
    # 痛点关键词
    PAIN_POINT_KEYWORDS = {
        "en": [
            "disappointed", "waste", "broken", "doesn't work", "stopped working",
            "poor quality", "cheap", "flimsy", "not worth", "returned",
            "misleading", "different from", "smaller than", "doesn't fit"
        ],
        "zh": [
            "失望", "浪费", "坏了", "不工作", "质量差", "便宜", "退货",
            "误导", "不一样", "太小", "不合身", "不值"
        ]
    }
    
    @classmethod
    def analyze_pain_points(cls, reviews: List[Review], language: str = "en") -> Dict:
        """
        分析评论痛点
        
        Args:
            reviews: 评论列表
            language: 语言
        
        Returns:
            痛点分析结果
        """
        pain_points = {}
        keywords = cls.PAIN_POINT_KEYWORDS.get(language, cls.PAIN_POINT_KEYWORDS["en"])
        
        for review in reviews:
            if review.rating <= 3:  # 只分析低星评论
                content_lower = review.content.lower()
                
                for keyword in keywords:
                    if keyword in content_lower:
                        pain_points[keyword] = pain_points.get(keyword, 0) + 1
        
        # 排序
        sorted_pain_points = sorted(pain_points.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_reviews": len(reviews),
            "low_star_reviews": len([r for r in reviews if r.rating <= 3]),
            "pain_points": sorted_pain_points[:10],
            "pain_point_rate": len([r for r in reviews if r.rating <= 3]) / len(reviews) * 100 if reviews else 0
        }
    
    @classmethod
    def extract_suggestions(cls, reviews: List[Review]) -> List[str]:
        """
        从评论中提取改进建议
        
        Args:
            reviews: 评论列表
        
        Returns:
            改进建议列表
        """
        suggestions = []
        
        for review in reviews:
            if review.rating <= 2:
                # 提取建议模式
                content = review.content
                
                # 模式匹配
                patterns = [
                    (r"I wish (.*?)[\.\!]", "建议：{0}"),
                    (r"would be better if (.*?)[\.\!]", "改进：{0}"),
                    (r"should have (.*?)[\.\!]", "应增加：{0}"),
                    (r"needs (.*?)[\.\!]", "需要：{0}"),
                ]
                
                for pattern, template in patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        suggestions.append(template.format(match.group(1)))
        
        return suggestions[:10]


class CompetitorMonitor:
    """竞品监控器"""
    
    def __init__(self, data_file: str = None):
        self.data_file = Path(data_file or MONITOR_FILE)
        self.competitors: Dict[str, Competitor] = {}
        self.load_data()
    
    def load_data(self):
        """加载历史数据"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for asin, comp_data in data.get("competitors", {}).items():
                    self.competitors[asin] = Competitor(**comp_data)
    
    def save_data(self):
        """保存数据"""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "last_updated": datetime.now().isoformat(),
            "competitors": {
                asin: {
                    "asin": c.asin,
                    "name": c.name,
                    "url": c.url,
                    "platform": c.platform,
                    "current_price": c.current_price,
                    "previous_price": c.previous_price,
                    "price_history": c.price_history[-30:],  # 保留30天
                    "current_bsr": c.current_bsr,
                    "previous_bsr": c.previous_bsr,
                    "bsr_history": c.bsr_history[-30:],
                    "rating": c.rating,
                    "review_count": c.review_count,
                    "has_coupon": c.has_coupon,
                    "coupon_value": c.coupon_value,
                    "last_updated": c.last_updated
                }
                for asin, c in self.competitors.items()
            }
        }
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_competitor(self, asin: str, name: str, url: str, platform: str = "amazon"):
        """添加竞品"""
        self.competitors[asin] = Competitor(
            asin=asin,
            name=name,
            url=url,
            platform=platform
        )
        self.save_data()
    
    def remove_competitor(self, asin: str):
        """移除竞品"""
        if asin in self.competitors:
            del self.competitors[asin]
            self.save_data()
    
    def update_price(self, asin: str, price: float, coupon: float = 0):
        """
        更新价格
        
        Args:
            asin: 产品ASIN
            price: 当前价格
            coupon: 优惠券金额
        """
        if asin not in self.competitors:
            return
        
        comp = self.competitors[asin]
        comp.previous_price = comp.current_price
        comp.current_price = price
        comp.has_coupon = coupon > 0
        comp.coupon_value = coupon
        
        # 记录历史
        comp.price_history.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "price": price,
            "coupon": coupon
        })
        
        comp.last_updated = datetime.now().isoformat()
        self.save_data()
    
    def update_bsr(self, asin: str, bsr: int):
        """更新BSR"""
        if asin not in self.competitors:
            return
        
        comp = self.competitors[asin]
        comp.previous_bsr = comp.current_bsr
        comp.current_bsr = bsr
        
        # 记录历史
        comp.bsr_history.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "bsr": bsr
        })
        
        comp.last_updated = datetime.now().isoformat()
        self.save_data()
    
    def check_price_alerts(self, threshold: float = 0.1) -> List[Dict]:
        """
        检查价格预警
        
        Args:
            threshold: 变动阈值 (百分比)
        
        Returns:
            预警列表
        """
        alerts = []
        
        for asin, comp in self.competitors.items():
            if comp.previous_price > 0:
                change_rate = (comp.current_price - comp.previous_price) / comp.previous_price
                
                if abs(change_rate) >= threshold:
                    alerts.append({
                        "type": "price_alert",
                        "asin": asin,
                        "name": comp.name,
                        "previous_price": comp.previous_price,
                        "current_price": comp.current_price,
                        "change_rate": f"{change_rate * 100:+.1f}%",
                        "direction": "降价" if change_rate < 0 else "涨价"
                    })
        
        return alerts
    
    def get_trend_report(self, days: int = 7) -> Dict:
        """
        获取趋势报告
        
        Args:
            days: 统计天数
        
        Returns:
            趋势报告
        """
        report = {
            "period_days": days,
            "timestamp": datetime.now().isoformat(),
            "competitors": [],
            "summary": {
                "total_tracked": len(self.competitors),
                "price_increased": 0,
                "price_decreased": 0,
                "bsr_improved": 0,
                "bsr_declined": 0
            }
        }
        
        for asin, comp in self.competitors.items():
            price_trend = "stable"
            if comp.current_price < comp.previous_price:
                price_trend = "down"
                report["summary"]["price_decreased"] += 1
            elif comp.current_price > comp.previous_price:
                price_trend = "up"
                report["summary"]["price_increased"] += 1
            
            bsr_trend = "stable"
            if comp.current_bsr < comp.previous_bsr:
                bsr_trend = "improved"
                report["summary"]["bsr_improved"] += 1
            elif comp.current_bsr > comp.previous_bsr:
                bsr_trend = "declined"
                report["summary"]["bsr_declined"] += 1
            
            report["competitors"].append({
                "asin": asin,
                "name": comp.name,
                "current_price": comp.current_price,
                "price_trend": price_trend,
                "current_bsr": comp.current_bsr,
                "bsr_trend": bsr_trend,
                "rating": comp.rating,
                "review_count": comp.review_count
            })
        
        return report
    
    def list_competitors(self) -> List[Dict]:
        """列出所有竞品"""
        return [
            {
                "asin": c.asin,
                "name": c.name,
                "platform": c.platform,
                "current_price": c.current_price,
                "current_bsr": c.current_bsr,
                "rating": c.rating,
                "last_updated": c.last_updated
            }
            for c in self.competitors.values()
        ]


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="竞品监控器")
    parser.add_argument("command", choices=["list", "add", "remove", "alert", "report", "analyze"])
    parser.add_argument("--asin", "-a", help="产品ASIN")
    parser.add_argument("--name", "-n", help="产品名称")
    parser.add_argument("--url", "-u", help="产品链接")
    parser.add_argument("--price", "-p", type=float, help="价格")
    parser.add_argument("--bsr", "-b", type=int, help="BSR排名")
    parser.add_argument("--threshold", "-t", type=float, default=0.1, help="价格变动阈值")
    parser.add_argument("--days", "-d", type=int, default=7, help="统计天数")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    
    args = parser.parse_args()
    
    monitor = CompetitorMonitor()
    
    if args.command == "list":
        competitors = monitor.list_competitors()
        
        if args.json:
            print(json.dumps(competitors, ensure_ascii=False, indent=2))
        else:
            print(f"📋 监控中的竞品 ({len(competitors)} 个)")
            for c in competitors:
                print(f"\n  ASIN: {c['asin']}")
                print(f"  名称: {c['name']}")
                print(f"  价格: ${c['current_price']}")
                print(f"  BSR: {c['current_bsr']}")
    
    elif args.command == "add":
        if not all([args.asin, args.name]):
            print("请提供 --asin 和 --name 参数")
            sys.exit(1)
        
        monitor.add_competitor(
            asin=args.asin,
            name=args.name,
            url=args.url or f"https://www.amazon.com/dp/{args.asin}"
        )
        print(f"✅ 已添加竞品: {args.name} ({args.asin})")
    
    elif args.command == "remove":
        if not args.asin:
            print("请提供 --asin 参数")
            sys.exit(1)
        
        monitor.remove_competitor(args.asin)
        print(f"✅ 已移除竞品: {args.asin}")
    
    elif args.command == "alert":
        alerts = monitor.check_price_alerts(args.threshold)
        
        if args.json:
            print(json.dumps(alerts, ensure_ascii=False, indent=2))
        else:
            if alerts:
                print(f"⚠️ 价格预警 ({len(alerts)} 条)")
                for alert in alerts:
                    print(f"\n  {alert['direction']}: {alert['name']}")
                    print(f"  变动: ${alert['previous_price']} → ${alert['current_price']} ({alert['change_rate']})")
            else:
                print("✅ 无价格预警")
    
    elif args.command == "report":
        report = monitor.get_trend_report(args.days)
        
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"📊 {args.days}天趋势报告")
            print(f"\n汇总:")
            print(f"  监控总数: {report['summary']['total_tracked']}")
            print(f"  价格上涨: {report['summary']['price_increased']}")
            print(f"  价格下降: {report['summary']['price_decreased']}")
            print(f"  BSR提升: {report['summary']['bsr_improved']}")
            print(f"  BSR下降: {report['summary']['bsr_declined']}")
    
    elif args.command == "analyze":
        # 示例：分析差评痛点
        print("📝 差评痛点分析示例")
        
        # 模拟评论数据
        reviews = [
            Review(id="1", rating=2, title="失望", content="Disappointed with the quality. Broke after one week.", author="User1", date="2026-03-20"),
            Review(id="2", rating=1, title="浪费钱", content="Waste of money. Doesn't work as described.", author="User2", date="2026-03-21"),
            Review(id="3", rating=3, title="一般", content="Poor quality but cheap. You get what you pay for.", author="User3", date="2026-03-22")
        ]
        
        analysis = ReviewAnalyzer.analyze_pain_points(reviews)
        suggestions = ReviewAnalyzer.extract_suggestions(reviews)
        
        if args.json:
            print(json.dumps({
                "pain_points": analysis,
                "suggestions": suggestions
            }, ensure_ascii=False, indent=2))
        else:
            print(f"\n痛点分析:")
            for point, count in analysis["pain_points"]:
                print(f"  - {point}: {count}次")
            
            print(f"\n改进建议:")
            for s in suggestions:
                print(f"  - {s}")


if __name__ == "__main__":
    main()