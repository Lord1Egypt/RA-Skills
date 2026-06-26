---
title: sales_flows - 销售目标Flow表
type: entity
tags: [table, time-dimension, metric, kpi]
sources: [salesclaw.db schema + 2条示例数据]
related: [[salesclaw/knowledge/entities/sales_targets]], [[salesclaw/knowledge/entities/products]]
---

# sales_flows - 销售目标Flow表

## ⚠️ 不是产品流向表！

存储的是**销售目标达成 flow**，不是"入院→科室→处方"产品流向。

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | VARCHAR PK | `sf1` |
| `flow_type` | VARCHAR | `M1`（产品维度标识）|
| `target_value` | INTEGER | `5000000` |
| `actual_value` | INTEGER | `4200000` |
| `achievement_rate` | FLOAT | `84.0`（%）|
| `yoy_growth` | FLOAT | `15.0`（同比%）|
| `mom_growth` | FLOAT | `5.0`（环比%）|
| `dimension` | VARCHAR | `product`（还有 hospital/rep/territory）|
| `period` | VARCHAR | `2026-Q1`（YYYY-QN 格式）|

## 示例数据

```
sf1 | M1 | 5000000 | 4200000 | 84.0 | 15.0 | 5.0 | product | 2026-Q1
sf2 | M2 | 3000000 | 2800000 | 93.3 | 8.0  | 3.0 | product | 2026-Q1
```

## 核心规则

1. **dimension = `product`**：按产品维度追踪
2. **period 格式是季度**：`YYYY-QN`（如 `2026-Q1`）
3. **达成率 < 70% = 高风险**

## 正确查询

```sql
-- 产品维度达成情况
SELECT sf.*, o.name as flow_name
FROM sales_flows sf
LEFT JOIN ontology_objects o ON o.id = sf.flow_type
WHERE sf.dimension = 'product'
ORDER BY sf.period DESC, sf.achievement_rate ASC;

-- 低于70%达成率
SELECT * FROM sales_flows
WHERE achievement_rate < 70
ORDER BY achievement_rate ASC;
```

## 错误写法

```sql
-- ❌ sales_flows 没有 product_id / hospital_id / department 列
SELECT * FROM sales_flows WHERE product_id = 'p1'
```

---

*关联：[[salesclaw/knowledge/entities/sales_targets]]*
