---
title: 市场渗透率预测
type: concept
tags: [analysis, penetration, product, trend]
sources: [analyze.py::analyze_market_penetration]
related: [[salesclaw/entities/time_series_data]], [[salesclaw/entities/products]], [[salesclaw/entities/object_links]]
---

# 市场渗透率预测（Market Penetration Forecasting）

## 分析目标

基于历史市场份额数据，预测产品在下个周期的渗透率，预警下滑风险。

## 数据来源

`sales_flows.market_share` 或 `time_series_data.series_name='market_share'`

## 预测模型

**简单线性回归**（适用于数据点 ≥ 3）：

```
预测值 = 当前值 + slope × 1期
slope = Σ(xi - x̄)(yi - ȳ) / Σ(xi - x̄)²
```

## 置信度

```
置信度 = min(0.9, 0.5 + 数据点数 × 0.05)
```

数据点越多，线性模型拟合度越高，置信度越高。

## 预警规则

| 条件 | 预警级别 | 说明 |
|------|---------|------|
| `trend = declining` 且 `预测值 < 当前值 × 0.85` | 🚨 高风险 | 市场份额快速下滑 |
| `trend = declining` 且 `slope > 0.05` | ⚠️ 中风险 | 温和下滑 |
| `trend = rising` | ✅ 良好 | 份额增长 |

## 应用场景

1. **竞品进入预警**：竞品入院后立即开始追踪市场份额变化
2. **季度末预测**：用最新数据预测本季度末是否能达成目标
3. **上量效果评估**：学术活动、拜访策略调整后评估份额变化

## 注意事项

⚠️ 线性回归是简化模型，份额变化可能受季节性、政策等非线性因素影响
⚠️ 数据点 < 3 时不进行预测，仅给出趋势描述

---

*关联：[[salesclaw/entities/time_series_data]] / [[salesclaw/entities/products]]*
