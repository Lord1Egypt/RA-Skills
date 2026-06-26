---
title: sales_targets - 销售目标表
type: entity
tags: [table, kpi, time-dimension, metric]
sources: [salesclaw.db schema + 1条示例数据]
related: [[salesclaw/knowledge/entities/sales_reps]], [[salesclaw/knowledge/entities/sales_flows]]
---

# sales_targets - 销售目标表

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | VARCHAR PK | `t1` |
| `target_type` | VARCHAR | `quarterly` |
| `dimension` | VARCHAR | `product` |
| `target_value` | INTEGER | `15000000` |
| `actual_value` | INTEGER | `12500000` |
| `forecast_value` | INTEGER | `13800000`（季度末预测）|
| `achievement_rate` | FLOAT | `83.3`（%）|
| `risk_level` | VARCHAR | `at_risk` |

## 示例数据

```
t1 | quarterly | product | 15000000 | 12500000 | 13800000 | 83.3 | at_risk
```

## 核心规则

1. **achievement_rate < 70% = 高风险**
2. **forecast_value** 用于预测季度末是否能达标
3. **risk_level** = `at_risk`/`on_track`/`achieved`/`missed`

## 正确查询

```sql
-- 所有目标状态
SELECT st.*, o.name
FROM sales_targets st
JOIN ontology_objects o ON o.id = st.id
ORDER BY
  CASE st.risk_level WHEN 'at_risk' THEN 1 WHEN 'on_track' THEN 2 ELSE 3 END,
  st.achievement_rate ASC;
```

---

*关联：[[salesclaw/knowledge/entities/sales_flows]]*
