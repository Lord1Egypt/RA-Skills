---
title: products - 产品表
type: entity
tags: [table, product, field, business-key]
sources: [salesclaw.db schema + 2条示例数据]
related: [[salesclaw/knowledge/entities/sales_flows]], [[salesclaw/knowledge/entities/time_series_data]]
---

# products - 产品表

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | VARCHAR PK | `p1` |
| `category` | VARCHAR | `心血管` |
| `sales` | INTEGER | `50000000` |
| `market_share` | FLOAT | `35.0`（%）|
| `price` | FLOAT | `280.0` |

## 示例数据

```
p1 | 心血管 | 50000000 | 35.0 | 280.0
p2 | 降脂   | 30000000 | 25.0 | 180.0
```

## 正确查询

```sql
-- 产品一览
SELECT p.*, o.name
FROM products p
JOIN ontology_objects o ON o.id = p.id
ORDER BY p.sales DESC;

-- 市场份额趋势（查 time_series_data）
SELECT ts.timestamp, ts.value
FROM time_series_data ts
WHERE ts.object_id = 'p1'
  AND ts.series_name = 'marketShare'
ORDER BY ts.timestamp ASC;
```

---

*关联：[[salesclaw/knowledge/entities/time_series_data]]*
