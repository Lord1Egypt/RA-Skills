---
name: Portfolio Risk Analysis Expert
slug: security-portfolio-risk
description: AI-powered portfolio risk analysis expert for China market — covers VaR calculation, stress testing, tail risk measurement, factor exposure analysis, and risk decomposition. Built for fund managers, risk analysts, and institutional investors. Keywords: portfolio risk, VaR, stress testing, risk decomposition, China A-share, factor risk, tail risk, 组合风险, 风险分析, VaR, 压力测试, 风险分解, 风险管理, 最大回撤, 夏普比率, 收益风险比, 资产配置, 风险预算.
version: "3.0.1"
---

# Portfolio Risk Analysis Expert / 组合风险分析专家

> **English:** AI-powered portfolio risk analysis expert — covers VaR calculation, stress testing, tail risk measurement, factor exposure, and risk attribution. Built for fund managers and risk analysts.
>
> **中文:** 组合风险分析专家——覆盖VaR计算、压力测试、尾部风险度量、因子敞口分析、风险归因。适用：基金经理、风险分析师、机构投资者。

---


### 证券监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 证券监管 | 2026年Q1：市场波动加剧，组合风险管理要求提升 | 组合风险模型需增加量化冲击和ESG风险维度 |
| 证券监管 | 量化资金共振风险增加，极端行情止损策略需更新 | 组合风险模型需增加量化冲击和ESG风险维度 |
| 证券监管 | ESG投资分析要求扩大，组合风险需纳入ESG因素 | 组合风险模型需增加量化冲击和ESG风险维度 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **系统风险难预测** | 黑天鹅事件导致大幅回撤 | 极端情景压力测试+尾部风险分析 |
| **因子敞口不清晰** | 不知道组合暴露在哪些风险上 | 因子归因模型+敞口分解 |
| **回撤控制困难** | 持有人体验差，资金赎回压力 | 动态回撤监控+预警机制 |
| **相关性突变** | 平时低相关的资产大跌时齐跌 | 相关性压力测试+分散化效果评估 |
| **合规要求高** | 资管新规净值化要求 | 标准风险指标+监管报告 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** portfolio risk, VaR, stress testing, risk decomposition, factor exposure, tail risk, risk attribution, China A-share, fund management, risk management

**中文触发词（优先）：** 组合风险 / 风险分析 / VaR / 压力测试 / 回撤控制 / 风险归因 / 因子敞口 / 尾部风险 / 风险分解 / 风险预警 / 资产配置 / 分散化 / 相关性分析 / 最大回撤 / 夏普比率 / 波动率 / 风险调整收益 / 风险预算 / VaR计算 / CVaR / ES

---

## Core Capabilities / 核心能力

### 1. VaR & Risk Metrics / VaR与风险指标

```python
import numpy as np
import pandas as pd
from scipy import stats

class PortfolioRiskAnalyzer:
    """组合风险分析引擎"""
    
    def __init__(self, returns: pd.DataFrame, weights: np.ndarray):
        """
        Args:
            returns: 收益率序列（列=资产，行=日期）
            weights: 资产权重向量
        """
        self.returns = returns
        self.weights = weights
        self.n_assets = len(weights)
    
    def calculate_var(self, confidence: float = 0.95, 
                      method: str = "historical") -> dict:
        """计算VaR（Value at Risk）"""
        portfolio_returns = (self.returns * self.weights).sum(axis=1)
        
        if method == "historical":
            var = np.percentile(portfolio_returns, (1 - confidence) * 100)
        elif method == "parametric":
            mu = portfolio_returns.mean()
            sigma = portfolio_returns.std()
            var = stats.norm.ppf(1 - confidence, mu, sigma)
        elif method == "modified":
            # Cornish-Fisher调整
            mu = portfolio_returns.mean()
            sigma = portfolio_returns.std()
            skew = stats.skew(portfolio_returns)
            kurt = stats.kurtosis(portfolio_returns)
            z = stats.norm.ppf(1 - confidence)
            z_cf = (z + (z**2 - 1) * skew / 6 + 
                   (z**3 - 3*z) * kurt / 24 - 
                   (2*z**3 - 5*z) * skew**2 / 36)
            var = mu + sigma * z_cf
        
        return {
            "var": round(var * 100, 2),  # 百分比
            "var_amount": round(var * 1000000, 2),  # 假设100万组合
            "confidence": confidence,
            "method": method,
            "interpretation": f"在{confidence*100}%置信度下，最大损失为{abs(var)*100:.2f}%"
        }
    
    def calculate_cvar(self, confidence: float = 0.95) -> dict:
        """计算CVaR（Conditional VaR / Expected Shortfall）"""
        portfolio_returns = (self.returns * self.weights).sum(axis=1)
        var = np.percentile(portfolio_returns, (1 - confidence) * 100)
        
        cvar = portfolio_returns[portfolio_returns <= var].mean()
        
        return {
            "cvar": round(cvar * 100, 2),
            "cvar_amount": round(cvar * 1000000, 2),
            "interpretation": f"超过VaR时的平均损失为{abs(cvar)*100:.2f}%"
        }
    
    def calculate_max_drawdown(self) -> dict:
        """计算最大回撤"""
        cumulative = (1 + self.returns @ self.weights).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        
        max_dd = drawdown.min()
        max_dd_end = drawdown.idxmin()
        max_dd_start = cumulative[:max_dd_end].idxmax()
        
        return {
            "max_drawdown": round(max_dd * 100, 2),
            "peak_date": str(max_dd_start.date()),
            "trough_date": str(max_dd_end.date()),
            "recovery_date": None  # 需后续计算
        }
    
    def factor_risk_attribution(self, factor_returns: pd.DataFrame) -> dict:
        """因子风险归因"""
        portfolio_returns = self.returns @ self.weights
        
        # 回归分析
        X = factor_returns.values
        X = np.column_stack([np.ones(len(X)), X])
        y = portfolio_returns.values
        
        coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
        residuals = y - X @ coeffs
        
        # 分解方差
        total_var = np.var(y)
        factor_var = np.var(X[:, 1:] @ coeffs[1:])
        specific_var = np.var(residuals)
        
        return {
            "factor_exposure": {
                "market": round(coeffs[1], 3),
                "factors": {
                    col: round(coef, 3) 
                    for col, coef in zip(factor_returns.columns, coeffs[2:])
                }
            },
            "risk_contribution": {
                "factor_risk": round(factor_var / total_var * 100, 2),
                "specific_risk": round(specific_var / total_var * 100, 2)
            },
            "r_squared": round(1 - specific_var / total_var, 4)
        }
```

### 2. Stress Testing / 压力测试

```python
class StressTestScenarios:
    """压力测试情景库"""
    
    SCENARIOS = {
        "2015股灾重演": {
            "description": "假设上证指数单周下跌20%",
            "market_shock": -0.20,
            "sector_impacts": {
                "金融": -0.25,
                "房地产": -0.30,
                "消费": -0.15,
                "科技": -0.20,
                "医药": -0.10
            },
            "liquidity_shock": 0.5  # 流动性降至50%
        },
        
        "利率急升": {
            "description": "假设基准利率上调100bp",
            "rate_shock": 0.01,
            "bond_impact": -0.08,
            "equity_impact": -0.10,
            "bank_impact": -0.05
        },
        
        "人民币急贬": {
            "description": "假设USD/CNY一日升值5%",
            "fx_shock": 0.05,
            "export_related": -0.15,
            "import_related": 0.05,
            "domestic_consumer": -0.08
        },
        
        "黑天鹅-新冠": {
            "description": "类似2020年初疫情冲击",
            "market_shock": -0.12,
            "travel": -0.30,
            "retail": -0.20,
            "healthcare": 0.10,
            "online": 0.05
        }
    }
    
    def run_stress_test(self, portfolio: dict, scenario: str) -> dict:
        """执行压力测试"""
        if scenario not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}")
        
        s = self.SCENARIOS[scenario]
        positions = portfolio["positions"]
        
        stressed_pnl = 0
        stressed_values = []
        
        for pos in positions:
            sector = pos.get("sector", "general")
            weight = pos["weight"]
            
            # 根据情景调整
            if "sector_impacts" in s and sector in s["sector_impacts"]:
                shock = s["sector_impacts"][sector]
            else:
                shock = s.get("market_shock", -0.10)
            
            pos_stressed = weight * (1 + shock)
            stressed_values.append(pos_stressed)
            stressed_pnl += weight * shock
        
        total_value = sum(stressed_values)
        portfolio_stress_loss = total_value - 1  # 假设初始为1
        
        return {
            "scenario": scenario,
            "description": s["description"],
            "portfolio_loss": round(portfolio_stress_loss * 100, 2),
            "portfolio_value_after": round(total_value * 100, 2),
            "position_impacts": [
                {"name": pos["name"], "weight": pos["weight"], 
                 "shock": round(shock * 100, 2), "impact": "loss" if shock < 0 else "gain"}
                for pos, shock in zip(positions, 
                    [s.get("sector_impacts", {}).get(pos.get("sector", ""), 
                     s.get("market_shock", -0.10)) for pos in positions])
            ]
        }
```

### 3. Risk Contribution Analysis / 风险贡献分析

```python
    def risk_contribution_by_asset(self) -> dict:
        """计算各资产风险贡献"""
        cov_matrix = self.returns.cov()
        portfolio_vol = np.sqrt(self.weights @ cov_matrix.values @ self.weights)
        
        # 边际风险贡献 (MCTR)
        mctr = (cov_matrix.values @ self.weights) / portfolio_vol
        
        # 风险贡献
        risk_contrib = self.weights * mctr
        
        return {
            "portfolio_volatility": round(portfolio_vol * 100, 2),
            "asset_risk_contribution": {
                self.returns.columns[i]: round(rc * 100, 2)
                for i, rc in enumerate(risk_contrib)
            },
            "concentration_risk": {
                "max_concentration": round(max(risk_contrib) * 100, 2),
                "diversification_benefit": round(
                    (sum([self.returns[col].std() * w 
                         for col, w in zip(self.returns.columns, self.weights)]) - 
                     portfolio_vol) * 100, 2)
            }
        }
```

---

## Quick Command Templates / 快速指令模板

**组合风险评估：**
```
分析以下组合的风险：
- 总规模：1000万
- 持仓：[股票A 30%, 股票B 20%, 债券B 50%]
- 置信度：95%
```

**压力测试：**
```
执行"2015股灾重演"情景压力测试
```

---

## Disclaimer

This skill provides risk analysis tools for educational purposes. Risk metrics are based on historical data and statistical models, which do not guarantee future accuracy. Investment decisions should be made based on comprehensive analysis and professional advice.
