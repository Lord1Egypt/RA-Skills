#!/usr/bin/env python3
"""
股票分析器 - 多维度股票分析工具
支持：基本面分析、技术面分析、舆情分析
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
class StockInfo:
    """股票信息"""
    code: str
    name: str
    market: str  # A股/港股/美股
    price: float = 0
    change_pct: float = 0
    volume: int = 0
    turnover: float = 0
    pe: float = 0
    pb: float = 0
    market_cap: float = 0


@dataclass
class AnalysisResult:
    """分析结果"""
    stock_code: str
    stock_name: str
    fundamental_score: int = 0
    technical_score: int = 0
    sentiment_score: int = 0
    overall_rating: str = "中性"
    target_price: float = 0
    stop_loss: float = 0
    risks: List[str] = None
    opportunities: List[str] = None
    
    def __post_init__(self):
        if self.risks is None:
            self.risks = []
        if self.opportunities is None:
            self.opportunities = []


class TechnicalAnalyzer:
    """技术分析器"""
    
    @classmethod
    def analyze_trend(cls, prices: List[float]) -> str:
        """分析趋势"""
        if len(prices) < 20:
            return "数据不足"
        
        ma5 = sum(prices[-5:]) / 5
        ma10 = sum(prices[-10:]) / 10
        ma20 = sum(prices[-20:]) / 20
        
        if ma5 > ma10 > ma20:
            return "上升趋势"
        elif ma5 < ma10 < ma20:
            return "下降趋势"
        else:
            return "震荡整理"
    
    @classmethod
    def calculate_rsi(cls, prices: List[float], period: int = 14) -> float:
        """计算RSI"""
        if len(prices) < period + 1:
            return 50.0
        
        gains = []
        losses = []
        
        for i in range(1, period + 1):
            change = prices[-i] - prices[-i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)
    
    @classmethod
    def find_support_resistance(cls, prices: List[float]) -> Tuple[float, float]:
        """寻找支撑阻力位"""
        if len(prices) < 20:
            return 0, 0
        
        recent_high = max(prices[-20:])
        recent_low = min(prices[-20:])
        current = prices[-1]
        
        # 简单计算
        support = recent_low
        resistance = recent_high
        
        return round(support, 2), round(resistance, 2)
    
    @classmethod
    def generate_signals(cls, prices: List[float], volume: List[int] = None) -> Dict:
        """生成交易信号"""
        trend = cls.analyze_trend(prices)
        rsi = cls.calculate_rsi(prices)
        support, resistance = cls.find_support_resistance(prices)
        
        signals = {
            "trend": trend,
            "rsi": rsi,
            "support": support,
            "resistance": resistance,
            "signal": "持有"
        }
        
        # RSI信号
        if rsi < 30:
            signals["signal"] = "超卖，考虑买入"
        elif rsi > 70:
            signals["signal"] = "超买，考虑卖出"
        
        return signals


class FundamentalAnalyzer:
    """基本面分析器"""
    
    @classmethod
    def calculate_score(cls, pe: float, pb: float, roe: float, 
                       revenue_growth: float = 0, profit_growth: float = 0) -> int:
        """计算基本面评分"""
        score = 50  # 基础分
        
        # PE评分
        if 0 < pe < 15:
            score += 15
        elif 15 <= pe < 25:
            score += 10
        elif 25 <= pe < 40:
            score += 5
        elif pe >= 60:
            score -= 10
        
        # PB评分
        if 0 < pb < 2:
            score += 10
        elif 2 <= pb < 4:
            score += 5
        elif pb >= 6:
            score -= 5
        
        # ROE评分
        if roe >= 20:
            score += 15
        elif roe >= 15:
            score += 10
        elif roe >= 10:
            score += 5
        elif roe < 5:
            score -= 10
        
        # 增长评分
        if revenue_growth > 20:
            score += 10
        elif revenue_growth > 10:
            score += 5
        
        return max(0, min(100, score))
    
    @classmethod
    def analyze_financial_health(cls, debt_ratio: float, current_ratio: float,
                                 cash_flow: float) -> Dict:
        """分析财务健康度"""
        health = {
            "overall": "健康",
            "issues": []
        }
        
        if debt_ratio > 70:
            health["issues"].append(f"负债率偏高 ({debt_ratio}%)")
            health["overall"] = "关注"
        
        if current_ratio < 1:
            health["issues"].append(f"流动比率偏低 ({current_ratio})")
            health["overall"] = "风险"
        
        if cash_flow < 0:
            health["issues"].append("现金流为负")
        
        return health


class SentimentAnalyzer:
    """舆情分析器"""
    
    # 情绪关键词
    POSITIVE_KEYWORDS = [
        "利好", "增长", "突破", "创新高", "盈利", "扩张",
        "收购", "合作", "中标", "首发", "龙头"
    ]
    
    NEGATIVE_KEYWORDS = [
        "利空", "下跌", "亏损", "减持", "质押", "诉讼",
        "调查", "处罚", "风险", "暴雷", "违约"
    ]
    
    @classmethod
    def analyze_news(cls, news_list: List[str]) -> Dict:
        """分析新闻情绪"""
        positive_count = 0
        negative_count = 0
        
        for news in news_list:
            news_lower = news.lower()
            
            for keyword in cls.POSITIVE_KEYWORDS:
                if keyword in news_lower:
                    positive_count += 1
            
            for keyword in cls.NEGATIVE_KEYWORDS:
                if keyword in news_lower:
                    negative_count += 1
        
        total = len(news_list) if news_list else 1
        
        sentiment_score = 50 + (positive_count - negative_count) * 5
        sentiment_score = max(0, min(100, sentiment_score))
        
        if sentiment_score >= 70:
            sentiment = "积极"
        elif sentiment_score >= 40:
            sentiment = "中性"
        else:
            sentiment = "消极"
        
        return {
            "score": sentiment_score,
            "sentiment": sentiment,
            "positive_count": positive_count,
            "negative_count": negative_count
        }


class StockAnalysisEngine:
    """股票分析引擎"""
    
    def __init__(self):
        self.technical = TechnicalAnalyzer()
        self.fundamental = FundamentalAnalyzer()
        self.sentiment = SentimentAnalyzer()
    
    def analyze(self, stock_code: str, stock_name: str = None) -> AnalysisResult:
        """执行完整分析"""
        # 模拟数据（实际应从API获取）
        result = AnalysisResult(
            stock_code=stock_code,
            stock_name=stock_name or stock_code
        )
        
        # 技术面分析（模拟）
        mock_prices = [100 + i * 0.5 + (i % 3 - 1) * 2 for i in range(30)]
        signals = self.technical.analyze_trend(mock_prices)
        rsi = self.technical.calculate_rsi(mock_prices)
        support, resistance = self.technical.find_support_resistance(mock_prices)
        
        result.technical_score = int(50 + (rsi - 50) * 0.5)
        
        # 基本面分析（模拟）
        result.fundamental_score = self.fundamental.calculate_score(
            pe=25, pb=3.5, roe=18, revenue_growth=15
        )
        
        # 舆情分析（模拟）
        mock_news = [
            f"{stock_name}发布业绩预告",
            f"{stock_name}获得机构增持"
        ]
        sentiment_result = self.sentiment.analyze_news(mock_news)
        result.sentiment_score = sentiment_result["score"]
        
        # 综合评级
        avg_score = (result.fundamental_score + result.technical_score + result.sentiment_score) / 3
        
        if avg_score >= 75:
            result.overall_rating = "买入"
        elif avg_score >= 60:
            result.overall_rating = "增持"
        elif avg_score >= 40:
            result.overall_rating = "持有"
        elif avg_score >= 25:
            result.overall_rating = "减持"
        else:
            result.overall_rating = "卖出"
        
        # 目标价和止损
        current_price = 100  # 模拟
        result.target_price = round(current_price * 1.2, 2)
        result.stop_loss = round(current_price * 0.92, 2)
        
        # 风险和机会
        result.risks = ["市场波动风险", "行业竞争风险"]
        result.opportunities = ["行业增长机遇", "政策支持"]
        
        return result
    
    def generate_report(self, result: AnalysisResult) -> str:
        """生成分析报告"""
        report = f"""# {result.stock_name}({result.stock_code}) 投资分析报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 一、评分概览

| 维度 | 评分 | 状态 |
|------|------|------|
| 基本面 | {result.fundamental_score}/100 | {'✅ 良好' if result.fundamental_score >= 60 else '⚠️ 关注'} |
| 技术面 | {result.technical_score}/100 | {'✅ 良好' if result.technical_score >= 60 else '⚠️ 关注'} |
| 舆情 | {result.sentiment_score}/100 | {'✅ 积极' if result.sentiment_score >= 60 else '⚠️ 谨慎'} |

---

## 二、综合评级

**{result.overall_rating}**

---

## 三、价格目标

- 目标价: ¥{result.target_price}
- 止损位: ¥{result.stop_loss}

---

## 四、风险提示

"""
        for risk in result.risks:
            report += f"- {risk}\n"
        
        report += "\n---\n\n## 五、机会点\n\n"
        for opp in result.opportunities:
            report += f"- {opp}\n"
        
        report += f"""
---

## 免责声明

本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。

---

*分析引擎: xiaodi-financial-team*
"""
        
        return report


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="股票分析器")
    parser.add_argument("stock_code", help="股票代码")
    parser.add_argument("--name", "-n", help="股票名称")
    parser.add_argument("--report", "-r", action="store_true", help="生成完整报告")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    
    args = parser.parse_args()
    
    engine = StockAnalysisEngine()
    result = engine.analyze(args.stock_code, args.name)
    
    if args.report:
        print(engine.generate_report(result))
    elif args.json:
        print(json.dumps({
            "stock_code": result.stock_code,
            "stock_name": result.stock_name,
            "fundamental_score": result.fundamental_score,
            "technical_score": result.technical_score,
            "sentiment_score": result.sentiment_score,
            "overall_rating": result.overall_rating,
            "target_price": result.target_price,
            "stop_loss": result.stop_loss,
            "risks": result.risks,
            "opportunities": result.opportunities
        }, ensure_ascii=False, indent=2))
    else:
        print(f"📊 {result.stock_name}({result.stock_code})")
        print(f"   基本面: {result.fundamental_score}/100")
        print(f"   技术面: {result.technical_score}/100")
        print(f"   舆情: {result.sentiment_score}/100")
        print(f"   综合评级: {result.overall_rating}")
        print(f"   目标价: ¥{result.target_price}")


if __name__ == "__main__":
    main()