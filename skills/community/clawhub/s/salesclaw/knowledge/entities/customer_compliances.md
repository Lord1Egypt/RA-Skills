---
title: customer_compliances - 医生时序指标表（空表！）
type: entity
tags: [table, time-dimension, metric, doctor]
sources: [salesclaw.db schema introspection - 表为空]
related: [[salesclaw/knowledge/entities/time_series_data]], [[salesclaw/knowledge/entities/doctors]]
---

# customer_compliances - 医生时序指标表（空表！）

## ⚠️ 此表为空

**实测结果：0 行数据。** 不要使用此表查询任何数据。

## 实际字段结构（即使为空也记录）

| 字段 | 类型 |
|------|------|
| `id` | VARCHAR PK |
| `meeting_frequency` | INTEGER |
| `real_name_verified` | BOOLEAN |
| `compliance_history` | TEXT |

## ⚠️ 处方量时序的正确来源

**请使用 `time_series_data` 表**，字段如下：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER PK | 自增主键 |
| `object_id` | VARCHAR | 医生/产品 ID |
| `series_name` | VARCHAR | `prescriptionVolume`（camelCase!）|
| `timestamp` | VARCHAR | `2025-10`（YYYY-MM）|
| `value` | FLOAT | 指标值 |

## 正确查询

```sql
-- ✅ 医生处方量时序（查 time_series_data）
SELECT ts.timestamp, ts.value
FROM time_series_data ts
WHERE ts.object_id = 'd1'
  AND ts.series_name = 'prescriptionVolume'
ORDER BY ts.timestamp ASC;
```

## 错误写法

```sql
-- ❌ 此表为空，不要查 customer_compliances
SELECT * FROM customer_compliances WHERE id = 'd1'
```

---

*关联：[[salesclaw/knowledge/entities/time_series_data]]*
