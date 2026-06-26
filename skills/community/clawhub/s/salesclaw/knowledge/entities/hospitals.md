---
title: hospitals - 医院表
type: entity
tags: [table, hospital, field, business-key]
sources: [salesclaw.db schema + 2条示例数据]
related: [[salesclaw/knowledge/entities/object_links]], [[salesclaw/knowledge/entities/doctors]]
---

# hospitals - 医院表

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | VARCHAR PK | `h1` |
| `level` | VARCHAR | `三甲` |
| `location` | VARCHAR | `上海` |
| `beds` | INTEGER | `2000` |
| `access_status` | VARCHAR | `approved`（还有 pending/no_access）|
| `procurement_mode` | VARCHAR | `集中采购` |
| `annual_revenue` | INTEGER | `50000000`（可为空）|

## 示例数据

```
h1 | 三甲 | 上海 | 2000 | approved | 集中采购 | 50000000
h2 | 三甲 | 上海 | 2500 | approved | 招标采购 | NULL
```

## 核心业务规则

1. **access_status = `approved`** 才算已准入；`pending`=待准入；`no_access`=未准入
2. **高价值未覆盖**：`annual_revenue > 1000万` 且 `access_status != 'approved'`
3. **查询某代表负责的医院**：通过 `object_links.link_type = 'MANAGES'`

## 正确查询

```sql
-- 医院一览
SELECT h.*, o.name
FROM hospitals h
JOIN ontology_objects o ON o.id = h.id
ORDER BY h.annual_revenue DESC;

-- 高价值未覆盖
SELECT h.*, o.name
FROM hospitals h
JOIN ontology_objects o ON o.id = h.id
WHERE h.annual_revenue > 10000000
  AND h.access_status != 'approved';

-- 某代表负责的医院
SELECT h.*
FROM hospitals h
JOIN object_links ol ON ol.target_id = h.id AND ol.link_type = 'MANAGES'
WHERE ol.source_id = 'r1';
```

---

*关联：[[salesclaw/knowledge/entities/object_links]]*
