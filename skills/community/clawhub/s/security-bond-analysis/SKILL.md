---
name: Bond Analysis Expert
slug: security-bond-analysis
description: AI-powered bond analysis expert for China market — covers bond valuation, yield analysis, duration/convexity calculation, credit spread analysis, and bond portfolio management. Built for fixed income analysts, bond traders, and portfolio managers. Keywords: bond analysis, yield curve, duration, convexity, credit spread, China bonds,利率债, 信用债, 国债, 企业债, 城投债, 债券估值, 收益率曲线, 久期, 凸性, 信用利差, 固收, 利率风险, 债券组合.
version: "3.0.1"
---

# Bond Analysis Expert / 债券分析专家

> **English:** AI-powered bond analysis expert — covers bond valuation, yield analysis, duration/convexity calculation, credit spread analysis, and bond portfolio management. Built for fixed income professionals.
>
> **中文:** 债券分析专家——覆盖债券估值、收益率分析、久期/凸性计算、信用利差分析、债券组合管理。适用：固收分析师、债券交易员、组合管理人。

---


### 证券监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 证券监管 | 2026年Q1：信用债市场分化加剧，信用风险识别要求提升 | 债券分析框架需纳入理财新规和地方债务化解动态 |
| 证券监管 | 银行理财'三清'推进，债券投资偏好可能调整 | 债券分析框架需纳入理财新规和地方债务化解动态 |
| 证券监管 | 地方债务化解持续推进，城投债分析逻辑需更新 | 债券分析框架需纳入理财新规和地方债务化解动态 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **收益率计算复杂** | 多种收益率指标容易混淆 | 标准化收益率计算框架 |
| **信用分析耗时** | 发行主体众多，分析量大 | 模板化信用分析框架 |
| **利率风险难测** | 久期/凸性概念抽象 | 可视化风险分析 |
| **城投债信仰** | 城投刚兑预期与违约现实冲突 | 区域财政分析模型 |
| **久期管理难** | 利率变动对组合影响大 | 久期匹配优化工具 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** bond analysis, yield curve, duration, convexity, credit spread, China bonds, fixed income, bond valuation, interest rate risk, credit risk

**中文触发词（优先）：** 债券分析 / 收益率曲线 / 久期 / 凸性 / 信用利差 / 中国债券 / 固收 / 债券估值 / 利率风险 / 信用风险 / 国债 / 企业债 / 城投债 / 金融债 / 可转债 / 债券回购 / 债券评级 / YTM / 即期收益率 / 到期收益率

---

## Core Capabilities / 核心能力

### 1. Bond Valuation Engine / 债券估值引擎

```python
import numpy as np
import pandas as pd

class BondAnalyzer:
    """债券分析引擎"""
    
    @staticmethod
    def calculate_price(face_value: float, coupon_rate: float, 
                       ytm: float, years: int, 
                       frequency: int = 2) -> float:
        """
        债券定价
        Args:
            face_value: 面值（元）
            coupon_rate: 年票面利率
            ytm: 到期收益率
            years: 剩余期限（年）
            frequency: 付息频率（1=年付，2=半年付）
        """
        n = years * frequency
        r_per_period = ytm / frequency
        c_per_period = (face_value * coupon_rate) / frequency
        
        # 现金流现值
        pv_coupons = sum([c_per_period / (1 + r_per_period) ** t 
                         for t in range(1, n + 1)])
        pv_face = face_value / (1 + r_per_period) ** n
        
        return pv_coupons + pv_face
    
    @staticmethod
    def calculate_ytm(price: float, face_value: float,
                     coupon_rate: float, years: float,
                     frequency: int = 2) -> float:
        """
        计算到期收益率（YTM）- 牛顿迭代法
        """
        n = years * frequency
        c = (face_value * coupon_rate) / frequency
        
        # 初始猜测
        ytm = coupon_rate
        
        for _ in range(100):
            pv = sum([c / (1 + ytm/frequency) ** t 
                     for t in range(1, n + 1)]) + face_value / (1 + ytm/frequency) ** n
            
            diff = price - pv
            
            # 导数（久期近似）
            duration = BondAnalyzer.calculate_duration(
                price, face_value, coupon_rate, ytm, years, frequency
            )
            dv = -duration / (1 + ytm/frequency) * diff
            
            ytm = ytm + diff / dv * 0.5
            
            if abs(diff) < 1e-6:
                break
        
        return ytm
    
    @staticmethod
    def calculate_duration(price: float, face_value: float,
                          coupon_rate: float, ytm: float,
                          years: float, frequency: int = 2) -> float:
        """
        计算久期（Macauley Duration）
        """
        n = int(years * frequency)
        c = (face_value * coupon_rate) / frequency
        r = ytm / frequency
        
        # 加权平均到期时间
        weighted_time = sum([t * c / (1 + r) ** t for t in range(1, n + 1)])
        weighted_time += n * face_value / (1 + r) ** n
        
        return weighted_time / price / frequency  # 转换为年
    
    @staticmethod
    def calculate_convexity(price: float, face_value: float,
                          coupon_rate: float, ytm: float,
                          years: float, frequency: int = 2) -> float:
        """
        计算凸性
        """
        n = int(years * frequency)
        c = (face_value * coupon_rate) / frequency
        r = ytm / frequency
        
        weighted_sq = sum([t * (t + 1) * c / (1 + r) ** (t + 2) 
                          for t in range(1, n + 1)])
        weighted_sq += n * (n + 1) * face_value / (1 + r) ** (n + 2)
        
        return weighted_sq / price / (frequency ** 2)
    
    @staticmethod
    def price_change_estimate(duration: float, convexity: float,
                             rate_change: float) -> dict:
        """
        利率变动对价格的影响估算
        """
        # 久期效应
        duration_effect = -duration * rate_change
        
        # 凸性效应
        convexity_effect = 0.5 * convexity * (rate_change ** 2)
        
        total_effect = duration_effect + convexity_effect
        
        return {
            "duration_effect": round(duration_effect * 100, 4),
            "convexity_effect": round(convexity_effect * 100, 4),
            "total_effect": round(total_effect * 100, 4),
            "approximate_new_price_pct": round((1 + total_effect) * 100, 4)
        }
```

### 2. Credit Analysis Framework / 信用分析框架

```markdown
## 信用债分析模板

### 一、发债主体概况
| 项目 | 内容 |
|-----|------|
| 公司名称 | |
| 实际控制人 | |
| 主体评级 | |
| 行业分类 | |
| 主营业务 | |

### 二、财务分析
```python
CREDIT_ANALYSIS_RATIOS = {
    "盈利能力": {
        "毛利率": ">30%为优质",
        "净利率": ">15%为优质",
        "ROE": ">10%为优质"
    },
    "偿债能力": {
        "资产负债率": "<70%为稳健",
        "流动比率": ">1.5为稳健",
        "利息保障倍数": ">3倍为稳健"
    },
    "现金流": {
        "经营现金流/带息债务": ">15%为稳健",
        "经营现金流/资本支出": ">100%为稳健"
    }
}
```

### 三、信用利差分析
```python
def analyze_credit_spread(bond_yield: float, treasury_yield: float,
                         rating: str) -> dict:
    """
    信用利差分析
    """
    spread = bond_yield - treasury_yield
    
    # 评级对应利差参考
    SPREAD_REFERENCE = {
        "AAA": 0.50,  # 50bp
        "AA+": 0.80,
        "AA": 1.20,
        "AA-": 1.50,
        "A+": 2.00,
        "A": 2.50
    }
    
    reference = SPREAD_REFERENCE.get(rating, 2.0)
    
    return {
        "credit_spread": round(spread * 100, 2),
        "reference_spread": reference,
        "relative_value": "低估" if spread < reference else "高估",
        "spread_premium": round((spread - reference) * 100, 2)
    }
```
```

### 3. Bond Portfolio Management / 债券组合管理

```python
class BondPortfolio:
    """债券组合管理"""
    
    def __init__(self):
        self.bonds = []
    
    def add_bond(self, bond: dict):
        """添加债券"""
        # 计算关键指标
        bond["price"] = self._calculate_bond_price(bond)
        bond["ytm"] = self._calculate_ytm(bond)
        bond["duration"] = self._calculate_duration(bond)
        bond["convexity"] = self._calculate_convexity(bond)
        bond["dv01"] = bond["duration"] * bond["price"] / 100 / 100  # 每bp变化
        
        self.bonds.append(bond)
    
    def portfolio_duration(self) -> float:
        """组合久期"""
        total_value = sum(b["market_value"] for b in self.bonds)
        weighted_duration = sum(
            b["duration"] * b["market_value"] for b in self.bonds
        ) / total_value
        return weighted_duration
    
    def portfolio_credit_breakdown(self) -> dict:
        """组合信用分布"""
        breakdown = {}
        for bond in self.bonds:
            rating = bond.get("rating", "Unknown")
            if rating not in breakdown:
                breakdown[rating] = {"count": 0, "value": 0}
            breakdown[rating]["count"] += 1
            breakdown[rating]["value"] += bond.get("market_value", 0)
        
        return breakdown
    
    def interest_rate_risk(self, rate_shock: float) -> dict:
        """利率风险分析"""
        port_duration = self.portfolio_duration()
        
        # 纯久期效应
        duration_pnl = -port_duration * rate_shock / 100
        
        # 凸性调整
        port_convexity = sum(
            b["convexity"] * b["market_value"] for b in self.bonds
        ) / sum(b["market_value"] for b in self.bonds)
        convexity_pnl = 0.5 * port_convexity * (rate_shock/100) ** 2
        
        return {
            "portfolio_duration": round(port_duration, 3),
            "rate_shock_bp": round(rate_shock * 100, 0),
            "duration_pnl_pct": round(duration_pnl * 100, 2),
            "convexity_pnl_pct": round(convexity_pnl * 100, 2),
            "total_pnl_pct": round((duration_pnl + convexity_pnl) * 100, 2)
        }
```

---

## Quick Command Templates / 快速指令模板

**债券定价：**
```
计算债券价格：
- 面值：100元
- 票面利率：4%
- 到期收益率：3.5%
- 剩余期限：5年
- 付息频率：年付
```

**久期分析：**
```
分析债券组合的久期风险：
- 组合总规模：1000万
- 利率上升50bp时的损益
```

---

## Disclaimer

Bond analysis involves various risks including interest rate risk and credit risk. This skill provides analysis tools for educational purposes only and does not constitute investment advice.
