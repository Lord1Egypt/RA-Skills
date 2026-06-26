---
title: time_series_data - 时序数据表
type: entity
tags: [table, time-dimension, metric]
sources: [salesclaw.db schema + 2条示例数据]
related: [[salesclaw/knowledge/entities/ontology_objects]], [[salesclaw/knowledge/entities/doctors]], [[salesclaw/knowledge/entities/products]]
---

# time_series_data - 时序数据表

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | INTEGER PK | `1` |
| `object_id` | VARCHAR | `d1`（医生/产品/医院ID）|
| `series_name` | VARCHAR | `prescriptionVolume` |
| `timestamp` | VARCHAR | `2025-10`（YYYY-MM 格式）|
| `value` | FLOAT | `120.0` |

## 示例数据

```
id=1  | object_id=d1 | series_name=prescriptionVolume | timestamp=2025-10 | value=120.0
id=2  | object_id=d1 | series_name=prescriptionVolume | timestamp=2025-11 | value=115.0
id=3  | object_id=d1 | series_name=prescriptionVolume | timestamp=2025-12 | value=108.0
```

## ⚠️ series_name 使用 camelCase

| 正确 | 错误 |
|------|------|
| `prescriptionVolume` | `prescription_volume` |
| `visitFrequency` | `visit_frequency` |
| `marketShare` | `market_share` |
| `actualValue` | `actual_value` |

## series_name 取值清单（已验证）

| series_name | 实体类型 | 说明 |
|------------|---------|------|
| `prescriptionVolume` | Doctor | 医生处方量 |
| `visitFrequency` | Doctor | 拜访频次 |
| `sentimentScore` | Doctor | 态度评分 |
| `performance` | Doctor/SalesRep | 绩效 |
| `actualValue` | Product | 实际销售额 |
| `forecastValue` | Product | 预测值 |
| `marketShare` | Product | 市场份额 |
| `usedAmount` | Any | 使用量 |

## 正确查询

```sql
-- 医生处方量趋势
SELECT ts.timestamp, ts.value
FROM time_series_data ts
WHERE ts.object_id = 'd1'
  AND ts.series_name = 'prescriptionVolume'
  AND ts.timestamp >= '2025-10'
ORDER BY ts.timestamp ASC;

-- 产品市场份额趋势
SELECT ts.timestamp, ts.value
FROM time_series_data ts
JOIN ontology_objects o ON o.id = ts.object_id
WHERE ts.series_name = 'marketShare'
  AND o.object_type = 'Product'
ORDER BY ts.timestamp ASC;
```

## 错误写法

```sql
-- ❌ 用 snake_case（这个表用 camelCase）
SELECT * FROM time_series_data WHERE series_name = 'prescription_volume'
```

---

*关联：[[salesclaw/knowledge/entities/ontology_objects]]*
