---
name: Securities Equity Research Report Generator
slug: security-equity-research
description: AI-powered equity research report generator for China A-share market — covers industry research, company coverage initiation, earnings analysis, valuation modeling (DCF/DDM/PE-band), and investment thesis synthesis. Built for China equity research analysts, buy-side analysts, and investment bank researchers. Updated 2026 with latest ESG integration requirements, short-seller report response templates, and cross-sector comparison frameworks. Keywords: equity research, A-share research, investment report, short-seller defense, ESG integration, valuation model, China stock analysis, 研报生成, 行业研究, 个股覆盖, 估值建模, 投研报告, 行研, 财报分析, 盈利预测, 目标价, 评级, 深度报告, 事件点评, 新股分析.
version: "3.0.1"
---

# Securities Equity Research Report Generator / 证券投研报告生成器

> **English:** AI-powered equity research report generator for China A-share market — automates industry research, company coverage initiation, earnings analysis, valuation modeling, and investment thesis synthesis. Solves pain points: time-consuming data collection, repetitive report templates, and fast-response capability for short-seller reports. Built for equity research analysts and buy-side researchers.
>
> **中文:** 证券投研报告生成器——覆盖行业研究、公司首次覆盖、业绩点评、估值建模（DCF/DDM/PE区间）、投资逻辑提炼的全流程AI助手。解决痛点：数据收集耗时、报告模板重复、快速响应做空报告需求。适用：中国A股研究员、买方分析师、投资银行研究人员。

---


### 证券监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 证券监管 | 2026年Q1：证监会持续强化上市公司信息披露质量监管 | 研究报告模板需纳入信披合规和量化冲击分析 |
| 证券监管 | 业绩预告披露质量被重点关注，研究需加强信披合规分析 | 研究报告模板需纳入信披合规和量化冲击分析 |
| 证券监管 | A股量化资金占比30%-40%，研究报告需关注量化冲击因素 | 研究报告模板需纳入信披合规和量化冲击分析 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **数据收集耗时** | 分析师60%时间花在数据整理 | 自动抓取财报/宏观/行业数据库，一键生成数据底稿 |
| **报告模板重复** | 每次撰写覆盖报告都要重新排版 | 内置研报标准模板，30秒生成初稿框架 |
| **估值建模复杂** | DCF/DDM参数调整耗时长 | 参数化估值模型，输入假设自动计算 |
| **做空报告应急** | 做空机构突袭需24小时内回应 | 紧急响应模板，快速组织反驳论据 |
| **研报合规风险** | 监管对研报质量要求越来越高 | 内置合规检查清单，自动识别风险表述 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** equity research, A-share research, investment report, coverage initiation, earnings review, valuation model, DCF, DDM, PE band, short-seller response, ESG integration, China stock analysis, industry research report, buy-side research

**中文触发词（优先）：** 投研报告 / 行业研究 / 个股分析 / 首次覆盖 / 业绩点评 / 估值建模 / DCF / DDM / PE区间 / 做空报告回应 / ESG整合 / 投研框架 / 研究报告 / 买方研报 / 券商研报 / 宏观策略 / 行业比较 / 公司对比 / 盈利预测 / 目标价 / 评级调整 / 研究报告审查 / 研报合规检查 / 研报降重 / 研报改写

---

## Core Capabilities / 核心能力

### 1. Research Report Templates / 研报模板库

**标准研报结构（证监会/中证协规范格式）：**

```markdown
# [公司简称]（[股票代码]）深度报告
**报告日期**: YYYY-MM-DD
**研究员**: [姓名]
**联系方式**: [邮箱/电话]

## 核心观点
[3-5句话概括投资亮点和核心风险]

## 投资逻辑
### 逻辑1：[一句话]
### 逻辑2：[一句话]
### 逻辑3：[一句话]

## 关键假设
| 假设项 | 数值 | 依据 |
|-------|------|------|
| 收入增速 | XX% | [市场/公司历史数据] |
| 毛利率 | XX% | [行业趋势/竞争格局] |
| 费用率 | XX% | [历史均值/管理变革] |

## 盈利预测
| 指标 | 2024A | 2025E | 2026E | 2027E |
|------|-------|-------|-------|-------|
| 营业收入（亿元） | | | | |
| 归母净利润（亿元） | | | | |
| EPS（元） | | | | |
| YoY增速 | | | | |

## 估值分析
### DCF估值
- WACC: XX%
- 永续增长率: XX%
- 绝对估值区间: [XX-XX]元

### 相对估值
| 可比公司 | P/E | P/B | P/S |
|---------|-----|-----|-----|
| [公司A] | | | |
| [公司B] | | | |
| 行业中位数 | | | |

## 风险提示
1. [风险1]
2. [风险2]
3. [风险3]
```

### 2. Valuation Models / 估值模型

#### 2.1 DCF Model / 现金流折现模型

```python
import numpy as np
import pandas as pd
from scipy.optimize import brentq

def dcf_valuation(fcf_forecast: list, wacc: float, terminal_growth: float, 
                   terminal_share: float = 1.0) -> dict:
    """
    DCF估值模型
    Args:
        fcf_forecast: 未来5年自由现金流预测（亿元）
        wacc: 加权平均资本成本（%）
        terminal_growth: 永续增长率（%）
        terminal_share: 终值折现系数
    Returns:
        估值结果字典
    """
    # 预测期现值
    discount_factors = [(1 + wacc/100) ** t for t in range(1, len(fcf_forecast) + 1)]
    pv_forecast = sum([fcf / df for fcf, df in zip(fcf_forecast, discount_factors)])
    
    # 终值计算
    terminal_fcf = fcf_forecast[-1] * (1 + terminal_growth / 100)
    terminal_value = terminal_fcf / (wacc / 100 - terminal_growth / 100)
    pv_terminal = terminal_value / discount_factors[-1] * terminal_share
    
    # 企业价值 & 股权价值
    enterprise_value = pv_forecast + pv_terminal
    equity_value = enterprise_value  # 简化：无净负债调整
    
    # 敏感性分析
    sensitivity = {}
    for wacc_adj in [-0.5, 0, 0.5]:
        for tg_adj in [-0.5, 0, 0.5]:
            adj_wacc = wacc + wacc_adj
            adj_tg = terminal_growth + tg_adj
            if adj_wacc > adj_tg:
                adj_tv = terminal_fcf * (1 + adj_tg/100) / (adj_wacc/100 - adj_tg/100)
                adj_pv_tv = adj_tv / discount_factors[-1] * terminal_share
                adj_pv_f = sum([fcf / ((1 + adj_wacc/100) ** t) 
                               for t, fcf in enumerate(fcf_forecast, 1)])
                sensitivity[f"WACC={adj_wacc}%, g={adj_tg}%"] = adj_pv_f + adj_pv_tv
    
    return {
        "enterprise_value": round(enterprise_value, 2),
        "equity_value": round(equity_value, 2),
        "pv_forecast": round(pv_forecast, 2),
        "pv_terminal": round(pv_terminal, 2),
        "terminal_value": round(terminal_value, 2),
        "sensitivity_table": sensitivity
    }

# 使用示例
result = dcf_valuation(
    fcf_forecast=[5.2, 6.1, 7.3, 8.5, 9.8],  # 未来5年FCF（亿元）
    wacc=9.5,  # WACC 9.5%
    terminal_growth=2.5,  # 永续增长率 2.5%
    terminal_share=0.8  # 终值折现系数
)
print(f"企业价值: {result['enterprise_value']} 亿元")
print(f"股权价值: {result['equity_value']} 亿元")
```

#### 2.2 DDM Model / 股利贴现模型

```python
def ddm_valuation(current_dps: float, dividend_growth: list, 
                  required_return: float, terminal_growth: float) -> dict:
    """
    DDM估值模型（两阶段）
    Args:
        current_dps: 当前每股股利（元）
        dividend_growth: 高增长阶段各年增长率（%）
        required_return: 必要收益率（%）
        terminal_growth: 永续增长率（%）
    """
    pv_dividends = []
    cumulative_dps = current_dps
    
    for i, g in enumerate(dividend_growth, 1):
        cumulative_dps *= (1 + g / 100)
        pv = cumulative_dps / ((1 + required_return / 100) ** i)
        pv_dividends.append(pv)
    
    # 永续价值
    terminal_dps = cumulative_dps * (1 + terminal_growth / 100)
    terminal_value = terminal_dps / (required_return / 100 - terminal_growth / 100)
    pv_terminal = terminal_value / ((1 + required_return / 100) ** len(dividend_growth))
    
    intrinsic_value = sum(pv_dividends) + pv_terminal
    
    return {
        "intrinsic_value": round(intrinsic_value, 2),
        "pv_dividends": [round(p, 4) for p in pv_dividends],
        "terminal_value": round(terminal_value, 2),
        "pv_terminal": round(pv_terminal, 2)
    }
```

#### 2.3 PE Band Analysis / PE估值区间分析

```python
def pe_band_analysis(eps_history: list, price_history: list, 
                     forecast_eps: float) -> dict:
    """
    PE估值区间分析
    基于历史估值分布给出当前估值水位
    """
    # 计算历史PE
    pe_history = [p / e for p, e in zip(price_history, eps_history) if e > 0]
    
    # 统计分布
    pe_stats = {
        "min": np.min(pe_history),
        "q25": np.percentile(pe_history, 25),
        "median": np.median(pe_history),
        "q75": np.percentile(pe_history, 75),
        "max": np.max(pe_history),
        "mean": np.mean(pe_history)
    }
    
    # 估值区间
    valuation_band = {
        "极度低估 (PE < Q25)": forecast_eps * pe_stats["q25"],
        "偏低估 (Q25 < PE < Median)": forecast_eps * pe_stats["median"],
        "合理区间 (Median < PE < Q75)": forecast_eps * pe_stats["q75"],
        "偏高估 (PE > Q75)": forecast_eps * pe_stats["max"]
    }
    
    return {
        "pe_statistics": pe_stats,
        "valuation_band": {k: round(v, 2) for k, v in valuation_band.items()}
    }
```

### 3. Industry Research Framework / 行业研究框架

```markdown
## 行业研究标准框架

### 一、行业概述
- 行业定义与边界
- 产业链结构图
- 行业发展阶段（导入期/成长期/成熟期/衰退期）

### 二、竞争格局
- 市场集中度（CR3/CR5/CR10）
- 波特五力分析
- 竞争格局演变趋势

### 三、驱动因素
- 需求侧：市场规模、增速、渗透率
- 供给侧：产能扩张、技术迭代
- 政策面：监管政策、扶持政策
- 宏观面：经济周期、人口结构

### 四、核心标的
- 龙头公司竞争优势
- 二线公司差异化
- 潜在黑马

### 五、风险因素
- 周期性风险
- 政策风险
- 技术替代风险
- 竞争加剧风险
```

### 4. Short-Seller Response Template / 做空报告回应模板

```markdown
# 关于[做空机构名称]做空报告的声明

**公司声明日期**: YYYY-MM-DD
**股票代码**: [代码]
**声明人**: [公司名称]投资者关系部

## 一、核心回应

[机构]于[日期]发布的做空报告，存在严重的事实错误和误导性陈述。
本公司特此声明如下：

### 1. 关于[指控1]的回应
**事实**: [澄清事实]
**证据**: [提供证据]
**结论**: [明确结论]

### 2. 关于[指控2]的回应
[同上格式]

## 二、补充信息

### 财务数据核实
| 指标 | 公司公告数据 | 做空报告数据 | 差异说明 |
|-----|-------------|-------------|---------|
| | | | |

## 三、风险提示

本声明不构成投资建议。投资者应仔细阅读公司过往公告，
审慎判断投资风险。

---
联系方式：[IR邮箱]
```

---

## Compliance Checklist / 合规检查清单

| 检查项 | 依据 | 通过标准 |
|-------|------|---------|
| 盈利预测合理性 | 《证券研究报告执业规范》 | 预测区间不超过合理范围 |
| 风险提示完整性 | 《证券法》第79条 | 必须包含3项以上风险提示 |
| 利益冲突披露 | 证监会相关规定 | 持有股票需披露 |
| 评级定义一致性 | 《证券研究报告执业规范》 | 评级定义需与公司标准一致 |
| 数据来源合规 | 交易所规则 | 引用数据需标注来源 |

---

## Usage Examples / 使用示例

**启动研报撰写：**
```
分析[行业名称]的竞争格局和投资机会，生成行业研究报告模板
```

**估值建模：**
```
帮我用DCF模型对[公司名称]估值：
- 未来5年FCF预测：[X]亿/[X]亿/[X]亿/[X]亿/[X]亿
- WACC：[X]%
- 永续增长率：[X]%
```

**做空报告应急：**
```
[机构]刚发布做空报告指控[公司]，需24小时内回应，
帮我生成回应初稿框架，重点反驳以下3点：
1. [指控点1]
2. [指控点2]
3. [指控点3]
```

---

## Disclaimer

This skill provides research report templates and valuation models for educational and reference purposes. Investment decisions should be based on independent research and professional advice. All outputs should be reviewed by qualified analysts before publication or use in investment decisions.
