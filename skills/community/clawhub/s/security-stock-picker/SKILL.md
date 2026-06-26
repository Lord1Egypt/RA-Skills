---
name: AI-Powered Stock Selection Engine
slug: security-stock-screening
description: AI-powered intelligent stock selection engine for China A-share market — covers quantitative factor screening, fundamental analysis ranking, technical signal detection, sector rotation analysis, and portfolio construction. Built for retail investors, fund managers, and quantitative analysts. Updated 2026 with latest factor models, short-seller vulnerability detection, and AI-enhanced stock screening. Keywords: stock selection, quantitative screening, factor investing, technical analysis, China A-share, stock picker, AI investing, 选股引擎, 量化选股, 因子投资, 技术分析, A股, 智能选股, 选股策略, 量化策略, AI选股, 股票筛选, 价值投资, 成长股, 短线选股.
version: "3.0.1"
---

# AI-Powered Stock Selection Engine / 智能选股引擎

> **English:** AI-powered intelligent stock selection engine for China A-share market — combines quantitative factor screening, fundamental analysis, technical signals, and sector rotation analysis. Solves pain points: information overload, emotional decision-making, and inconsistent stock picking criteria. Built for investors and analysts at all levels.
>
> **中文:** 智能选股引擎——整合量化因子筛选、基本面分析、技术信号检测、行业轮动分析的全流程选股工具。解决痛点：信息过载、情绪化决策、选股标准不统一。适用：各级投资者、基金经理、量化分析师。

---


### 证券监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 证券监管 | 2026年A股量化资金占比30%-40%，选股模型需考虑量化冲击 | 选股引擎需增加量化冲击识别和极端行情风控 |
| 证券监管 | 2026年3月23日量化踩踏案例（单日蒸发4.29万亿），风控需加强 | 选股引擎需增加量化冲击识别和极端行情风控 |
| 证券监管 | 上证周线级别中枢震荡，2026年核心区间3200-4000点 | 选股引擎需增加量化冲击识别和极端行情风控 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **信息过载** | A股5000+股票，无法逐一研究 | 多维度因子筛选，快速缩小范围 |
| **情绪化决策** | 追涨杀跌，高买低卖 | 量化标准选股，避免主观干扰 |
| **选股标准模糊** | 没有系统性方法论 | 完整选股框架+评分模型 |
| **财报造假风险** | 康美药业、瑞幸等案例警示 | 财报异常信号检测+预警 |
| **行业轮动难把握** | 踏错节奏，板块轮动踏空 | 宏观+情绪+资金三维轮动模型 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** stock selection, quantitative screening, factor investing, fundamental analysis, technical analysis, China A-share, stock picker, AI investing, momentum stocks, value investing, growth stocks, sector rotation, portfolio construction

**中文触发词（优先）：** 选股 / 智能选股 / 量化选股 / 因子选股 / 基本面选股 / 技术面选股 / 价值投资 / 成长股 / 蓝筹股 / 小盘股 / 行业轮动 / 板块轮动 / 资金流向 / 北向资金 / 龙虎榜 / 涨停板 / 破净股 / 低估值 / 高成长 / 业绩超预期 / 财报选股 / 研报筛选 / AI选股 / 机器选股 / 组合构建 / 仓位管理 / 止损策略

---

## Core Capabilities / 核心能力

### 1. Quantitative Factor Screening / 量化因子筛选

```python
import pandas as pd
import numpy as np
from typing import List, Dict, Optional

class StockScreener:
    """智能选股引擎"""
    
    def __init__(self):
        self.factors = {
            # 估值因子
            "pe": {"name": "市盈率", "weight": 0.15, "direction": "low_better", "bounds": (0, 100)},
            "pb": {"name": "市净率", "weight": 0.10, "direction": "low_better", "bounds": (0, 10)},
            "ps": {"name": "市销率", "weight": 0.05, "direction": "low_better", "bounds": (0, 20)},
            "pcf": {"name": "市现率", "weight": 0.05, "direction": "low_better", "bounds": (0, 30)},
            
            # 成长因子
            "revenue_growth": {"name": "营收增速", "weight": 0.15, "direction": "high_better", "bounds": (-50, 100)},
            "profit_growth": {"name": "利润增速", "weight": 0.15, "direction": "high_better", "bounds": (-100, 200)},
            "gross_margin": {"name": "毛利率", "weight": 0.08, "direction": "high_better", "bounds": (0, 100)},
            
            # 质量因子
            "roe": {"name": "ROE", "weight": 0.12, "direction": "high_better", "bounds": (-20, 50)},
            "debt_ratio": {"name": "资产负债率", "weight": 0.05, "direction": "low_better", "bounds": (0, 100)},
            "current_ratio": {"name": "流动比率", "weight": 0.03, "direction": "high_better", "bounds": (0.5, 10)},
            
            # 动量因子
            "momentum_20d": {"name": "20日动量", "weight": 0.05, "direction": "high_better", "bounds": (-30, 50)},
            "momentum_60d": {"name": "60日动量", "weight": 0.02, "direction": "high_better", "bounds": (-50, 100)}
        }
    
    def screen(self, stocks: pd.DataFrame, 
               criteria: Dict[str, tuple],
               min_score: float = 60) -> pd.DataFrame:
        """
        量化筛选主函数
        Args:
            stocks: 股票数据（含各因子列）
            criteria: 筛选条件 {因子名: (最小值, 最大值)}
            min_score: 最低综合评分
        Returns:
            符合条件的股票
        """
        result = stocks.copy()
        
        # Step 1: 硬性条件筛选
        for factor, (min_val, max_val) in criteria.items():
            if factor in result.columns:
                result = result[(result[factor] >= min_val) & (result[factor] <= max_val)]
        
        # Step 2: 因子打分
        result = self._factor_scoring(result)
        
        # Step 3: 综合评分排序
        result = result[result["综合评分"] >= min_score].sort_values("综合评分", ascending=False)
        
        return result
    
    def _factor_scoring(self, df: pd.DataFrame) -> pd.DataFrame:
        """因子打分（百分制）"""
        scores = pd.DataFrame(index=df.index)
        
        for factor, config in self.factors.items():
            if factor in df.columns:
                raw = df[factor].copy()
                min_val, max_val = config["bounds"]
                
                # 标准化到0-100
                normalized = (raw - min_val) / (max_val - min_val) * 100
                normalized = normalized.clip(0, 100)
                
                # 方向调整（部分因子越低越好）
                if config["direction"] == "low_better":
                    normalized = 100 - normalized
                
                scores[factor] = normalized * config["weight"]
        
        df["综合评分"] = scores.sum(axis=1)
        return df
```

### 2. Thematic Stock Screening / 主题投资筛选

```python
THEMATIC_SCREENING = {
    "AI人工智能": {
        "核心标的": ["科大讯飞", "海康威视", "中科曙光", "寒武纪", "商汤-W"],
        "概念股池": {
            "基础层": ["芯片", "算力", "服务器"],
            "技术层": ["大模型", "算法", "API"],
            "应用层": ["办公", "医疗", "金融", "教育"]
        },
        "筛选标准": {
            "市值": ">100亿",
            "研发投入": ">10%",
            "AI收入占比": ">30%"
        },
        "风险提示": "技术迭代快，竞争格局未定，估值波动大"
    },
    
    "新能源汽车": {
        "核心标的": ["比亚迪", "宁德时代", "理想汽车-W", "小鹏汽车-W"],
        "筛选维度": {
            "整车": ["销量增速", "毛利率", "智能化水平"],
            "电池": ["能量密度", "成本", "产能"],
            "配件": ["单车价值量", "客户集中度"]
        },
        "政策催化": "以旧换新补贴、购置税减免、新能源渗透率目标"
    },
    
    "创新药": {
        "核心标的": ["恒瑞医药", "百济神州", "信达生物", "药明康德"],
        "筛选标准": {
            "管线丰富度": ">10个临床管线",
            "first-in-class": "至少1个",
            "BD能力": "有海外授权记录"
        },
        "风险因素": "医保谈判降价、临床失败风险、同靶点竞争"
    }
}
```

### 3. Technical Signal Detection / 技术信号检测

```python
class TechnicalSignals:
    """技术信号检测"""
    
    @staticmethod
    def detect_moving_average_signals(prices: pd.Series, 
                                      short_ma: int = 20,
                                      long_ma: int = 60) -> dict:
        """均线信号检测"""
        ma_short = prices.rolling(short_ma).mean()
        ma_long = prices.rolling(long_ma).mean()
        
        # 金叉/死叉判断
        current_ma_diff = ma_short.iloc[-1] - ma_long.iloc[-1]
        prev_ma_diff = ma_short.iloc[-2] - ma_long.iloc[-2]
        
        if current_ma_diff > 0 and prev_ma_diff <= 0:
            signal = "GOLDEN_CROSS"  # 金叉
        elif current_ma_diff < 0 and prev_ma_diff >= 0:
            signal = "DEAD_CROSS"  # 死叉
        else:
            signal = "NEUTRAL"
        
        return {
            "signal": signal,
            "short_ma": round(ma_short.iloc[-1], 2),
            "long_ma": round(ma_long.iloc[-1], 2),
            "ma_diff_pct": round((current_ma_diff / ma_long.iloc[-1]) * 100, 2)
        }
    
    @staticmethod
    def detect_support_resistance(prices: pd.Series, 
                                 lookback: int = 60) -> dict:
        """支撑压力位检测"""
        recent = prices.tail(lookback)
        
        # 计算枢轴点
        pivot = (recent.max() + recent.min() + recent.iloc[-1]) / 3
        
        r1 = 2 * pivot - recent.min()
        s1 = 2 * pivot - recent.max()
        r2 = pivot + (recent.max() - recent.min())
        s2 = pivot - (recent.max() - recent.min())
        
        return {
            "resistance_1": round(r1, 2),
            "resistance_2": round(r2, 2),
            "pivot": round(pivot, 2),
            "support_1": round(s1, 2),
            "support_2": round(s2, 2),
            "current_price": round(prices.iloc[-1], 2)
        }
    
    @staticmethod
    def detect_volume_anomaly(prices: pd.Series, 
                             volumes: pd.Series,
                             threshold: float = 2.0) -> dict:
        """量价异常检测"""
        avg_volume = volumes.tail(20).mean()
        current_volume = volumes.iloc[-1]
        volume_ratio = current_volume / avg_volume
        
        # 价格与成交量背离
        price_change = (prices.iloc[-1] - prices.iloc[-2]) / prices.iloc[-2]
        
        return {
            "volume_ratio": round(volume_ratio, 2),
            "is_volume_surge": volume_ratio > threshold,
            "price_change": round(price_change * 100, 2),
            "divergence": "量价背离" if (price_change > 0 and volume_ratio < 0.5) or
                                      (price_change < 0 and volume_ratio > 2) else "正常"
        }
```

### 4. Financial Fraud Detection / 财报异常检测

```python
class FraudDetection:
    """财报异常信号检测"""
    
    @staticmethod
    def check_revenue_quality(stock_code: str, 
                             financial_data: dict) -> dict:
        """营收质量检测"""
        indicators = {
            # 应收账款异常
            "ar_growth_vs_revenue": financial_data.get("ar_growth", 0) - 
                                    financial_data.get("revenue_growth", 0),
            
            # 存货异常
            "inventory_growth_vs_cost": financial_data.get("inv_growth", 0) - 
                                        financial_data.get("cost_growth", 0),
            
            # 现金流匹配
            "cash_flow_ratio": financial_data.get("cfo", 0) / 
                              max(financial_data.get("net_profit", 1), 1),
            
            # 毛利率异常
            "gross_margin_volatility": financial_data.get("gm_std", 0),
            
            # 关联交易占比
            "related_party_ratio": financial_data.get("rpt_revenue", 0) / 
                                  max(financial_data.get("total_revenue", 1), 1)
        }
        
        # 预警信号
        warnings = []
        if indicators["ar_growth_vs_revenue"] > 30:
            warnings.append("应收账款增速显著高于营收增速，可能存在虚构收入")
        if indicators["cash_flow_ratio"] < 0.5:
            warnings.append("经营现金流显著低于净利润，盈利质量存疑")
        if indicators["related_party_ratio"] > 0.5:
            warnings.append("关联交易占比过高，存在利益输送风险")
        
        return {
            "indicators": indicators,
            "warnings": warnings,
            "overall_risk": "高" if len(warnings) >= 2 else 
                           "中" if warnings else "低"
        }
    
    @staticmethod
    def check_auditor_warnings(audit_reports: list) -> dict:
        """审计意见检测"""
        risk_keywords = ["保留意见", "无法表示意见", "非标准无保留", 
                        "持续经营重大不确定性", "强调事项段"]
        
        findings = []
        for report in audit_reports:
            for keyword in risk_keywords:
                if keyword in report:
                    findings.append({
                        "keyword": keyword,
                        "context": report
                    })
        
        return {
            "has_warnings": len(findings) > 0,
            "findings": findings,
            "risk_level": "高" if findings else "低"
        }
```

### 5. Portfolio Construction / 组合构建

```python
class PortfolioBuilder:
    """智能组合构建"""
    
    def __init__(self, target_stocks: List[dict], 
                 total_capital: float = 1000000):
        self.stocks = target_stocks
        self.capital = total_capital
    
    def build_equal_weight(self, max_positions: int = 10) -> dict:
        """等权重配置"""
        selected = self.stocks[:max_positions]
        per_stock = self.capital / len(selected)
        
        positions = []
        for stock in selected:
            shares = int(per_stock / stock["price"] / 100) * 100  # 100股整数
            positions.append({
                "code": stock["code"],
                "name": stock["name"],
                "shares": shares,
                "amount": shares * stock["price"],
                "weight": 1 / len(selected)
            })
        
        return {
            "strategy": "等权重",
            "positions": positions,
            "total_invested": sum(p["amount"] for p in positions),
            "cash_remaining": self.capital - sum(p["amount"] for p in positions),
            "expected_return": sum(s.get("expected_return", 0) for s in selected) / len(selected),
            "estimated_risk": self._calculate_portfolio_risk(positions)
        }
    
    def build_risk_parity(self, max_positions: int = 10) -> dict:
        """风险平价配置"""
        selected = self.stocks[:max_positions]
        
        # 使用波动率倒数作为权重
        inv_vol = [1 / s.get("volatility", 0.3) for s in selected]
        total_inv_vol = sum(inv_vol)
        weights = [v / total_inv_vol for v in inv_vol]
        
        positions = []
        for stock, weight in zip(selected, weights):
            amount = self.capital * weight
            shares = int(amount / stock["price"] / 100) * 100
            positions.append({
                "code": stock["code"],
                "name": stock["name"],
                "shares": shares,
                "amount": shares * stock["price"],
                "weight": round(weight * 100, 2)
            })
        
        return {
            "strategy": "风险平价",
            "positions": positions,
            "total_invested": sum(p["amount"] for p in positions)
        }
    
    def _calculate_portfolio_risk(self, positions: list) -> float:
        """简化组合风险估算"""
        # 假设相关性0.3
        individual_risks = [0.25] * len(positions)  # 默认25%波动率
        correlation = 0.3
        
        portfolio_var = 0
        for i, risk_i in enumerate(individual_risks):
            for j, risk_j in enumerate(individual_risks):
                weight_i = 1 / len(positions)
                weight_j = 1 / len(positions)
                corr = correlation if i != j else 1
                portfolio_var += weight_i * weight_j * risk_i * risk_j * corr
        
        return round(np.sqrt(portfolio_var) * 100, 2)
```

---

## Usage Examples / 使用示例

**启动选股：**
```
用以下条件筛选股票：
- 市盈率 < 30
- 营收增速 > 20%
- ROE > 15%
- 综合评分 > 70
```

**主题选股：**
```
筛选AI人工智能概念中估值最低的10只股票
```

**技术面选股：**
```
找出所有出现均线金叉且放量突破的股票
```

---

## Disclaimer

This skill provides stock screening tools and analysis for educational purposes. Stock selection results are based on quantitative models and historical data, which do not guarantee future performance. All investment decisions should be made based on independent research and professional advice. Past performance does not indicate future results.
