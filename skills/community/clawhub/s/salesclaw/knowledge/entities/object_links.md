---
title: object_links - 关系链接表（核心！）
type: entity
tags: [table, field, business-key, network]
sources: [salesclaw.db schema + 2条示例数据]
related: [[salesclaw/knowledge/entities/doctors]], [[salesclaw/knowledge/entities/hospitals]], [[salesclaw/knowledge/entities/products]]
---

# object_links - 关系链接表（核心！）

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | INTEGER PK | `1` |
| `source_id` | VARCHAR | `d1` |
| `link_type` | VARCHAR | `WORKS_AT`、`PRESCRIBES` |
| `target_id` | VARCHAR | `h1` |
| `target_name` | VARCHAR | `上海瑞金医院` |
| `target_type` | VARCHAR | `Hospital` |
| `link_strength` | FLOAT | `NULL`（可为空，1=最强）|
| `link_frequency` | VARCHAR | `high`（可为空）|
| `link_volume` | INTEGER | `120`（处方盒数，可为空）|
| `confidence` | FLOAT | `NULL`（可为空）|
| `inverse_relation` | VARCHAR | `NULL` |

## 示例数据

```
1  | d1 | WORKS_AT    | h1 | 上海瑞金医院 | Hospital | NULL  | NULL  | NULL  | NULL
2  | d1 | PRESCRIBES | p1 | 诺欣妥      | Product  | NULL  | high  | 120   | NULL
```

## link_type 取值清单

| link_type | 起点 | 终点 | 说明 |
|-----------|------|------|------|
| `WORKS_AT` | Doctor | Hospital | 医生在医院执业 |
| `PRESCRIBES` | Doctor | Product | 医生处方某产品 |
| `DOCTOR_COLLEAGUE` | Doctor | Doctor | 同事关系 |
| `DOCTOR_REPORT_TO` | Doctor | Doctor | 上下级关系 |
| `DOCTOR_MENTOR` | Doctor | Doctor | 师徒关系 |
| `INFLUENCES` | Doctor | Doctor | 处方影响力传递 |
| `MANAGED_BY` | Doctor | SalesRep | 医生由代表管理 |
| `MANAGES` | SalesRep | Hospital | 代表负责医院 |

## 核心业务规则

1. **关系是单向的**：A→B 和 B→A 是两条记录
2. **inverse_relation 可能为 NULL**：需用 link_type 反推
3. **link_strength / confidence 可能为 NULL**：数据质量问题
4. **没有外键约束**：灵活性优先

## 正确查询

```sql
-- 某医生的关系网络
SELECT ol.link_type, ol.link_strength, ol.target_name, ol.target_type
FROM object_links ol
WHERE ol.source_id = 'd1'
ORDER BY ol.link_strength DESC;

-- 某医院的医生（通过 WORKS_AT）
SELECT ol.source_id, o.name
FROM object_links ol
JOIN ontology_objects o ON o.id = ol.source_id
WHERE ol.target_id = 'h1'
  AND ol.link_type = 'WORKS_AT';
```

---

*关联：[[salesclaw/knowledge/entities/doctors]] / [[salesclaw/knowledge/entities/hospitals]]*
