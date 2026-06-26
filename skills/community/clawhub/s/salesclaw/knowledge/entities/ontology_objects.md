---
title: ontology_objects - 统一实体表
type: entity
tags: [table, field, business-key]
sources: [salesclaw.db schema + 2条示例数据]
related: [[salesclaw/knowledge/entities/doctors]], [[salesclaw/knowledge/entities/hospitals]], [[salesclaw/knowledge/entities/products]]
---

# ontology_objects - 统一实体表

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | VARCHAR PK | `d1`（与各子表 ID 一致）|
| `object_type` | VARCHAR | `Doctor`（还有 Hospital/Product/SalesRep）|
| `name` | VARCHAR | `张主任` |
| `status` | VARCHAR | `critical` |
| `lifecycle_stage` | VARCHAR | `at_risk`（at_risk/mature/new/active/churned）|
| `sentiment` | VARCHAR | `positive`（positive/neutral/negative）|
| `compliance_risk_level` | VARCHAR | `high` |
| `created_at` | DATETIME | `2026-05-14 01:30:39` |
| `updated_at` | DATETIME | `2026-05-14 01:35:13` |

## 示例数据

```
d1 | Doctor | 张主任 | critical | at_risk    | positive | high | 2026-05-14 01:30:39 | 2026-05-14 01:35:13
d2 | Doctor | 李教授 | stable   | mature     | positive | low  | 2026-05-14 01:30:39 | 2026-05-14 01:35:13
```

## 核心规则

1. **`id` 与各子表（doctors/hospitals/products）ID 一致**，通过 `id` JOIN
2. **`status`**：实体的综合状态（critical/stable/warning）
3. **`lifecycle_stage`**：客户生命周期阶段，流失预防核心字段

## 正确查询

```sql
-- 实体完整信息
SELECT * FROM ontology_objects WHERE id = 'd1';

-- 某类型的实体
SELECT * FROM ontology_objects WHERE object_type = 'Doctor';

-- 高风险实体
SELECT * FROM ontology_objects WHERE compliance_risk_level = 'high';
```

---

*关联：[[salesclaw/knowledge/entities/doctors]]*
