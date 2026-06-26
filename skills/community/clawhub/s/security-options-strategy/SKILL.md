---
name: Options Strategy Master
slug: security-options-strategy
description: AI-powered options strategy master for China market — covers options pricing, Greeks calculation, strategy analysis (covered call, protective put, spreads, straddles), and volatility trading. Built for options traders and risk managers. Keywords: options strategy, options pricing, Greeks, volatility trading, China options, covered call, protective put, iron condor, 50ETF期权, 沪深300期权, 期权策略, 波动率交易, BS定价, Delta, Gamma, Vega, Theta, 期权组合, 备兑开仓, 保护性看跌.
version: "3.0.1"
---

# Options Strategy Master / 期权策略大师

> **English:** AI-powered options strategy master — covers options pricing, Greeks calculation, multi-leg strategies, and volatility trading. Built for options traders and risk managers.
>
> **中文:** 期权策略大师——覆盖期权定价、Greeks计算、多腿策略分析、波动率交易。适用：期权交易者、风险管理人。

---


### 证券监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 证券监管 | 2026年Q1：市场波动加剧，期权对冲策略需求上升 | 期权策略模型需增加波动率冲击和极端行情模块 |
| 证券监管 | A股量化交易占比提升，期权定价模型需调整参数 | 期权策略模型需增加波动率冲击和极端行情模块 |
| 证券监管 | 极端行情频发，期权风险管理需加强希腊字母监控 | 期权策略模型需增加波动率冲击和极端行情模块 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **定价复杂** | BS模型参数选择困难 | 参数解释+敏感性分析 |
| **希腊字母难懂** | Delta/Gamma/Vega傻傻分不清 | 可视化Greeks图形 |
| **策略选择困难** | 不知道用什么策略应对市场 | 情景化策略推荐 |
| **保证金占用** | 资金效率低 | 最优保证金管理 |
| **风险敞口不清晰** | 极端行情爆仓 | 实时风险监控+预警 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** options strategy, options pricing, Greeks, volatility trading, China options, covered call, protective put, spread trading, straddles, collars

**中文触发词（优先）：** 期权策略 / 期权定价 / 希腊字母 / Delta / Gamma / Vega / 备兑开仓 / 保护性看跌 / 价差策略 / 跨式策略 / 勒式策略 / 波动率交易 / 50ETF期权 / 沪深300期权 / 期权开户 / 期权权限 / 权利仓 / 义务仓 / 做市商 / 波动率曲面

---

## Core Capabilities / 核心能力

### 1. Options Pricing Engine / 期权定价引擎

```python
import numpy as np
from scipy.stats import norm

class OptionsPricer:
    """期权定价引擎"""
    
    @staticmethod
    def black_scholes(S, K, T, r, sigma, option_type='call'):
        """
        Black-Scholes期权定价
        Args:
            S: 标的资产价格
            K: 行权价
            T: 到期时间（年）
            r: 无风险利率
            sigma: 波动率
            option_type: 'call' 或 'put'
        """
        if T <= 0:
            if option_type == 'call':
                return max(S - K, 0)
            else:
                return max(K - S, 0)
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
            delta = norm.cdf(d1)
        else:
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
            delta = norm.cdf(d1) - 1
        
        # Greeks计算
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100  # 每1%波动率变化
        theta_call = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - 
                     r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        theta_put = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + 
                    r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
        
        return {
            'price': round(price, 4),
            'delta': round(delta, 4),
            'gamma': round(gamma, 6),
            'vega': round(vega, 4),
            'theta': round(theta_call if option_type == 'call' else theta_put, 4),
            'd1': round(d1, 4),
            'd2': round(d2, 4)
        }
    
    @staticmethod
    def implied_volatility(market_price, S, K, T, r, option_type='call'):
        """计算隐含波动率（牛顿迭代法）"""
        sigma = 0.3  # 初始猜测
        
        for _ in range(100):
            bs_price = OptionsPricer.black_scholes(S, K, T, r, sigma, option_type)['price']
            vega = OptionsPricer.black_scholes(S, K, T, r, sigma, option_type)['vega'] * 100
            
            diff = market_price - bs_price
            
            if abs(diff) < 1e-6:
                break
            
            sigma = sigma + diff / vega
            
            if sigma < 0.01 or sigma > 5:
                return None
        
        return round(sigma * 100, 2)  # 返回百分比
```

### 2. Options Strategy Analysis / 期权策略分析

```python
class OptionsStrategy:
    """期权策略分析"""
    
    STRATEGIES = {
        "covered_call": {
            "name": "备兑开仓",
            "description": "持有标的+卖出看涨期权",
            "use_case": "预期横盘/小幅上涨，想增加收益",
            "max_profit": "股价 - 行权价 + 权利金",
            "max_loss": "无限（理论上）"
        },
        "protective_put": {
            "name": "保护性看跌",
            "description": "持有标的+买入看跌期权",
            "use_case": "担心下跌，想锁定损失",
            "max_profit": "无限",
            "max_loss": "行权价 - 股价 + 权利金"
        },
        "bull_call_spread": {
            "name": "牛市看涨价差",
            "description": "买入低行权价看涨+卖出高行权价看涨",
            "use_case": "看涨但涨幅有限",
            "max_profit": "行权价差 - 净权利金",
            "max_loss": "净权利金"
        },
        "bear_put_spread": {
            "name": "熊市看跌价差",
            "description": "买入高行权价看跌+卖出低行权价看跌",
            "use_case": "看跌但跌幅有限",
            "max_profit": "行权价差 - 净权利金",
            "max_loss": "净权利金"
        },
        "straddle": {
            "name": "跨式策略",
            "description": "同时买入同行权价的看涨+看跌",
            "use_case": "预期大幅波动但方向不明",
            "max_profit": "无限（上涨）或标的 - 行权价（下跌）",
            "max_loss": "两倍权利金"
        },
        "strangle": {
            "name": "勒式策略",
            "description": "买入高行权价看涨+低行权价看跌",
            "use_case": "预期大幅波动但方向不明（成本低于跨式）",
            "max_profit": "无限",
            "max_loss": "两倍权利金"
        },
        "iron_condor": {
            "name": "铁鹰策略",
            "description": "卖出价差+买入更宽价差保护",
            "use_case": "预期标的在一定范围内波动",
            "max_profit": "净权利金",
            "max_loss": "两个价差幅度 - 净权利金"
        }
    }
    
    def analyze_strategy(self, strategy_name: str, 
                        underlying_price: float,
                        params: dict) -> dict:
        """分析策略损益"""
        if strategy_name not in self.STRATEGIES:
            return {"error": "未知策略"}
        
        strategy = self.STRATEGIES[strategy_name]
        analysis = {
            "strategy": strategy["name"],
            "description": strategy["description"],
            "use_case": strategy["use_case"]
        }
        
        # 计算不同标的价格下的盈亏
        price_range = np.linspace(
            underlying_price * 0.7,
            underlying_price * 1.3,
            100
        )
        
        pnl_curve = self._calculate_pnl(strategy_name, price_range, params)
        
        # 关键指标
        breakeven = self._find_breakeven(pnl_curve, price_range)
        max_profit = self._find_max_profit(pnl_curve, price_range)
        max_loss = self._find_max_loss(pnl_curve, price_range)
        
        return {
            **analysis,
            "breakeven": round(breakeven, 2),
            "max_profit": round(max_profit, 2),
            "max_loss": round(max_loss, 2),
            "profit_table": {
                "大幅下跌(-20%)": round(self._pnl_at_price(strategy_name, 
                    underlying_price * 0.8, params), 2),
                "小幅下跌(-10%)": round(self._pnl_at_price(strategy_name, 
                    underlying_price * 0.9, params), 2),
                "横盘(0%)": round(self._pnl_at_price(strategy_name, 
                    underlying_price, params), 2),
                "小幅上涨(+10%)": round(self._pnl_at_price(strategy_name, 
                    underlying_price * 1.1, params), 2),
                "大幅上涨(+20%)": round(self._pnl_at_price(strategy_name, 
                    underlying_price * 1.2, params), 2)
            }
        }
```

### 3. Volatility Trading / 波动率交易

```markdown
## 波动率交易框架

### 波动率微笑/曲面分析
```python
def analyze_volatility_smile(option_chain: dict) -> dict:
    """
    分析波动率微笑曲面
    识别相对高估/低估期权
    """
    # 计算各行权价的隐含波动率
    iv_curve = {
        strike: calculate_iv(option_price, spot, strike, days_to_expiry, r)
        for strike, option_price in option_chain.items()
    }
    
    # 波动率偏斜分析
    atm_iv = iv_curve[get_atm_strike(spot)]
    skew = {
        otm_put_10: atm_iv - iv_curve[otm_put_10],
        otm_call_10: iv_curve[otm_call_10] - atm_iv
    }
    
    return {
        "iv_curve": iv_curve,
        "atm_volatility": atm_iv,
        "skew": skew,
        "opportunity": "IV高估卖出" if skew > threshold else "IV低估买入"
    }
```
```

---

## Quick Command Templates / 快速指令模板

**期权定价：**
```
计算50ETF期权定价：
- 标的价格：2.8元
- 行权价：2.85元
- 到期日：30天后
- 波动率：20%
- 类型：看涨期权
```

**分析策略：**
```
分析牛市看涨价差策略：
- 买入行权价：3.0元，权利金：0.05元
- 卖出行权价：3.2元，权利金：0.02元
- 标的现价：2.9元
```

---

## Disclaimer

Options trading involves substantial risk and is not suitable for all investors. Losses can exceed initial investment. This skill is for educational purposes only and does not constitute investment advice.
