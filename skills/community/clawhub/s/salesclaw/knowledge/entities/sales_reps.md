---
title: sales_reps - 销售代表表
type: entity
tags: [table, sales-rep, field]
sources: [salesclaw.db schema + 2条示例数据]
related: [[salesclaw/knowledge/entities/sales_targets]], [[salesclaw/knowledge/entities/object_links]]
---

# sales_reps - 销售代表表

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | VARCHAR PK | `r1` |
| `region` | VARCHAR | `华东区` |
| `performance` | INTEGER | `92`（0-100 绩效评分）|
| `quota_achievement` | INTEGER | `88`（达成率%）|
| `ytd_sales` | INTEGER | `4500000`（年累计销售，可为空）|

## 示例数据

```
r1 | 华东区 | 92 | 88  | 4500000
r2 | 华东区 | 78 | 82  | NULL
```

## 正确查询

```sql
-- 代表绩效排名
SELECT sr.*, o.name as rep_name
FROM sales_reps sr
JOIN ontology_objects o ON o.id = sr.id
ORDER BY sr.quota_achievement DESC;

-- 某代表负责的医院
SELECT h.*
FROM hospitals h
JOIN object_links ol ON ol.target_id = h.id AND ol.link_type = 'MANAGES'
WHERE ol.source_id = 'r1';
```

---

*关联：[[salesclaw/knowledge/entities/sales_targets]]*
