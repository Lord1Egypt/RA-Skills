---
title: Product Flow 分析
type: concept
tags: [analysis, product, metric, time-dimension]
sources: [analyze.py::analyze_product_flow]
related: [[salesclaw/entities/sales_flows]], [[salesclaw/entities/products]]
---

# Product Flow 分析

## 分析目标

追踪产品在目标达成周期内的 flow（流向）情况，识别下滑产品并归因。

## 数据来源

**⚠️ 重要：** Product Flow 分析的数据来源是 `sales_flows` 表，**不是**传统意义上的"入院→科室→处方"全链路数据。

`sales_flows` 实际结构：
- `dimension = 'product'`：按产品维度追踪
- `period = 'YYYY-QN'`：季度周期
- `target_value / actual_value`：目标和实际

## 趋势判断

基于 `actual_value` 时序，用线性回归斜率判断：

```
slope > 0 → 📈 上升
slope < 0 → 📉 下降
|slope| 很小 → ➡️ 稳定
```

## 达成率分析

```
达成率 = actual_value / target_value × 100%
```

| 达成率 | 风险等级 | 行动 |
|--------|---------|------|
| < 70% | 🚨 高风险 | 立即分析原因 |
| 70% - 90% | ⚠️ 中风险 | 关注趋势 |
| 90% - 110% | ✅ 正常 | 维持 |
| > 110% | 🌟 超额 | 总结经验 |

## 同比/环比

`sales_flows` 自带 `yoy_growth`（同比）和 `mom_growth`（环比）字段，直接使用。

## 注意事项

⚠️ 这个表**不是**真正的产品流向（入院→科室→处方），那需要组合 `object_links` + `doctors` + `customer_compliances`
⚠️ period 是季度格式（`2026-Q1`），做月级别分析需要用 `time_series_data`

---

*关联：[[salesclaw/entities/sales_flows]] / [[salesclaw/entities/products]]*
