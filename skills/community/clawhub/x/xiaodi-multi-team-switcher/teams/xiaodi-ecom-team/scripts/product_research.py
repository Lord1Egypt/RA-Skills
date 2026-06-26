#!/usr/bin/env python3
"""
选品分析器 - 多平台选品数据整合分析
支持：Amazon BSR分析、销量预估、趋势追踪
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# 配置
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"


@dataclass
class Product:
    """产品数据结构"""
    name: str
    platform: str
    category: str
    bsr: Optional[int] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    monthly_sales_estimate: Optional[Tuple[int, int]] = None
    source_url: Optional[str] = None
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []


class BSRConverter:
    """BSR 转销量转换器"""
    
    # BSR 区间对应的月销量估算
    BSR_SALES_MAPPING = {
        (1, 100): (2000, 5000),
        (101, 500): (1000, 2000),
        (501, 1000): (500, 1000),
        (1001, 5000): (200, 500),
        (5001, 10000): (100, 200),
        (10001, 20000): (50, 100),
        (20001, 50000): (20, 50),
        (50001, 100000): (10, 20),
        (100001, float('inf')): (1, 10)
    }
    
    @classmethod
    def estimate_sales(cls, bsr: int) -> Tuple[int, int]:
        """
        根据 BSR 估算月销量
        
        Args:
            bsr: Best Seller Rank
        
        Returns:
            (最低销量, 最高销量)
        """
        for (low, high), (sales_low, sales_high) in cls.BSR_SALES_MAPPING.items():
            if low <= bsr <= high:
                return (sales_low, sales_high)
        
        return (1, 10)


class ProfitCalculator:
    """利润计算器"""
    
    # 平台费率
    PLATFORM_FEES = {
        "amazon_us": {"commission": 0.15, "fba_base": 2.5, "fba_per_lb": 0.5},
        "amazon_uk": {"commission": 0.15, "fba_base": 2.0, "fba_per_kg": 1.0},
        "amazon_de": {"commission": 0.15, "fba_base": 2.5, "fba_per_kg": 1.2},
        "taobao": {"commission": 0.03},
        "jd": {"commission": 0.05},
        "pdd": {"commission": 0.006},
    }
    
    # 汇率
    EXCHANGE_RATES = {
        "USD": 7.2,
        "GBP": 9.1,
        "EUR": 7.8,
        "CNY": 1.0
    }
    
    @classmethod
    def calculate_profit(
        cls,
        purchase_cost: float,  # 采购成本 (CNY)
        selling_price: float,  # 售价 (外币)
        shipping_cost: float,  # 头程物流 (外币)
        weight_lb: float = 0.5,  # 重量 (磅)
        platform: str = "amazon_us",
        ad_rate: float = 0.15,  # 广告占比
        currency: str = "USD"
    ) -> Dict:
        """
        计算利润
        
        Args:
            purchase_cost: 采购成本 (人民币)
            selling_price: 售价 (外币)
            shipping_cost: 头程物流费用 (外币)
            weight_lb: 产品重量 (磅)
            platform: 平台
            ad_rate: 广告占比
            currency: 货币
        
        Returns:
            利润分析结果
        """
        exchange_rate = cls.EXCHANGE_RATES.get(currency, 7.2)
        fees = cls.PLATFORM_FEES.get(platform, cls.PLATFORM_FEES["amazon_us"])
        
        # 售价换算人民币
        price_cny = selling_price * exchange_rate
        
        # 佣金
        commission = price_cny * fees.get("commission", 0.15)
        
        # FBA 费用 (仅亚马逊)
        fba_fee = 0
        if platform.startswith("amazon"):
            fba_fee = fees.get("fba_base", 2.5) + fees.get("fba_per_lb", 0.5) * weight_lb
            fba_fee *= exchange_rate
        
        # 物流费用换算
        shipping_cny = shipping_cost * exchange_rate
        
        # 广告成本
        ad_cost = price_cny * ad_rate
        
        # 总成本
        total_cost = purchase_cost + shipping_cny + commission + fba_fee + ad_cost
        
        # 利润
        profit = price_cny - total_cost
        profit_margin = (profit / price_cny * 100) if price_cny > 0 else 0
        
        return {
            "purchase_cost": purchase_cost,
            "selling_price_cny": round(price_cny, 2),
            "selling_price_local": round(selling_price, 2),
            "currency": currency,
            "commission": round(commission, 2),
            "fba_fee": round(fba_fee, 2),
            "shipping_cost": round(shipping_cny, 2),
            "ad_cost": round(ad_cost, 2),
            "total_cost": round(total_cost, 2),
            "profit": round(profit, 2),
            "profit_margin": round(profit_margin, 1),
            "roi": round((profit / total_cost * 100), 1) if total_cost > 0 else 0
        }


class ProductResearcher:
    """选品分析器"""
    
    def __init__(self):
        self.products: List[Product] = []
    
    def analyze_category(self, category: str, mode: str = "cross_border") -> Dict:
        """
        分析类目选品机会
        
        Args:
            category: 类目名称
            mode: 模式 (cross_border / domestic)
        
        Returns:
            选品分析报告
        """
        report = {
            "category": category,
            "mode": mode,
            "timestamp": datetime.now().isoformat(),
            "trends": self._get_trends(category),
            "recommendations": [],
            "hot_keywords": self._get_keywords(category)
        }
        
        return report
    
    def _get_trends(self, category: str) -> List[Dict]:
        """获取趋势数据（模拟）"""
        # 实际应从 API 获取
        trends = [
            {
                "product": f"{category}热门产品1",
                "trend": "up",
                "growth": "+45%",
                "source": "小红书/TikTok"
            },
            {
                "product": f"{category}热门产品2",
                "trend": "stable",
                "growth": "+12%",
                "source": "Amazon BSR"
            }
        ]
        return trends
    
    def _get_keywords(self, category: str) -> List[str]:
        """获取热门关键词"""
        # 实际应从 API 获取
        return [f"{category}关键词1", f"{category}关键词2", f"{category}关键词3"]
    
    def analyze_product(self, product_url: str) -> Dict:
        """
        分析单个产品
        
        Args:
            product_url: 产品链接
        
        Returns:
            产品分析结果
        """
        # 解析平台
        platform = self._detect_platform(product_url)
        
        # 模拟数据（实际应抓取）
        analysis = {
            "url": product_url,
            "platform": platform,
            "timestamp": datetime.now().isoformat(),
            "product": {
                "name": "示例产品",
                "price": 29.99,
                "rating": 4.5,
                "review_count": 1234,
                "bsr": 5000
            },
            "sales_estimate": BSRConverter.estimate_sales(5000),
            "opportunity_score": self._calculate_opportunity_score(4.5, 1234, 5000)
        }
        
        return analysis
    
    def _detect_platform(self, url: str) -> str:
        """检测平台"""
        if "amazon" in url.lower():
            return "Amazon"
        elif "taobao" in url.lower():
            return "Taobao"
        elif "jd" in url.lower():
            return "JD"
        elif "pinduoduo" in url.lower():
            return "PDD"
        return "Unknown"
    
    def _calculate_opportunity_score(self, rating: float, reviews: int, bsr: int) -> int:
        """计算机会评分"""
        score = 50
        
        # 评分影响
        if rating >= 4.5:
            score += 10
        elif rating < 3.5:
            score -= 15
        
        # 评论数影响
        if reviews < 100:
            score += 15  # 竞争较小
        elif reviews > 1000:
            score -= 10  # 竞争激烈
        
        # BSR 影响
        if bsr < 1000:
            score += 10
        elif bsr > 10000:
            score -= 5
        
        return max(0, min(100, score))
    
    def compare_products(self, products: List[Dict]) -> Dict:
        """
        对比多个产品
        
        Args:
            products: 产品列表
        
        Returns:
            对比报告
        """
        comparison = {
            "timestamp": datetime.now().isoformat(),
            "products": products,
            "winner": None,
            "analysis": {}
        }
        
        if products:
            # 简单评分选择
            best_score = -1
            for p in products:
                score = p.get("opportunity_score", 0)
                if score > best_score:
                    best_score = score
                    comparison["winner"] = p
        
        return comparison


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="选品分析器")
    parser.add_argument("command", choices=["analyze", "profit", "bsr", "compare"])
    parser.add_argument("--category", "-c", help="类目名称")
    parser.add_argument("--url", "-u", help="产品链接")
    parser.add_argument("--bsr", "-b", type=int, help="BSR 排名")
    parser.add_argument("--purchase", "-p", type=float, help="采购成本")
    parser.add_argument("--price", "-P", type=float, help="售价")
    parser.add_argument("--shipping", "-s", type=float, default=5, help="物流成本")
    parser.add_argument("--mode", "-m", choices=["cross_border", "domestic"], default="cross_border")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 输出")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        if not args.category:
            print("请提供 --category 参数")
            sys.exit(1)
        
        researcher = ProductResearcher()
        report = researcher.analyze_category(args.category, args.mode)
        
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"📊 {args.category} 选品分析报告")
            print(f"模式: {args.mode}")
            print(f"\n趋势产品:")
            for t in report["trends"]:
                print(f"  - {t['product']}: {t['growth']} ({t['source']})")
    
    elif args.command == "profit":
        if not all([args.purchase, args.price]):
            print("请提供 --purchase 和 --price 参数")
            sys.exit(1)
        
        result = ProfitCalculator.calculate_profit(
            purchase_cost=args.purchase,
            selling_price=args.price,
            shipping_cost=args.shipping
        )
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("💰 利润计算结果")
            print(f"采购成本: ¥{result['purchase_cost']}")
            print(f"售价: ${result['selling_price_local']} (¥{result['selling_price_cny']})")
            print(f"佣金: ¥{result['commission']}")
            print(f"FBA费用: ¥{result['fba_fee']}")
            print(f"物流: ¥{result['shipping_cost']}")
            print(f"广告: ¥{result['ad_cost']}")
            print(f"总成本: ¥{result['total_cost']}")
            print(f"利润: ¥{result['profit']}")
            print(f"毛利率: {result['profit_margin']}%")
            print(f"ROI: {result['roi']}%")
    
    elif args.command == "bsr":
        if not args.bsr:
            print("请提供 --bsr 参数")
            sys.exit(1)
        
        sales_low, sales_high = BSRConverter.estimate_sales(args.bsr)
        
        if args.json:
            print(json.dumps({
                "bsr": args.bsr,
                "monthly_sales_estimate": [sales_low, sales_high]
            }, ensure_ascii=False, indent=2))
        else:
            print(f"📈 BSR {args.bsr} 对应月销量估算: {sales_low}-{sales_high} 件")
    
    elif args.command == "compare":
        # 示例对比
        researcher = ProductResearcher()
        products = [
            {"name": "产品A", "opportunity_score": 75},
            {"name": "产品B", "opportunity_score": 82},
            {"name": "产品C", "opportunity_score": 68}
        ]
        result = researcher.compare_products(products)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()