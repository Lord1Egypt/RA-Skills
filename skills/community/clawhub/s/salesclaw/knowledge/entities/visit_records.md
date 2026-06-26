---
title: visit_records - 拜访记录表
type: entity
tags: [table, visit, field]
sources: [salesclaw.db schema + 1条示例数据]
related: [[salesclaw/knowledge/entities/object_events]], [[salesclaw/knowledge/entities/doctors]]
---

# visit_records - 拜访记录表

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | VARCHAR PK | `v1` |
| `visit_type` | VARCHAR | `face_to_face` |
| `visit_status` | VARCHAR | `completed`（还有 scheduled/cancelled）|
| `objective` | TEXT | `跟进处方量下降原因` |
| `actual_content` | TEXT | `与张主任深入沟通了...` |
| `key_insights` | TEXT | `竞品渗透严重,需要提供更多学术支持` |
| `compliance_score` | INTEGER | `95`（0-100）|
| `effectiveness_score` | INTEGER | `88`（0-100）|

## 示例数据

```
v1 | face_to_face | completed | 跟进处方量下降原因 | 与张主任深入沟通了近期处方量下降的原因...
  | 竞品渗透严重,需要提供更多学术支持,医生态度担忧副作用 | 95 | 88
```

## ⚠️ 关键设计：没有 doctor_id 外键

**本表没有 `doctor_id` 列，也没有 `visit_date` 列。**

医生与拜访记录的关联需要通过 `object_events` 表：

```
visit_records.id ('v1')
        ↓
object_events.related_object_id = 'v1'
        ↓
object_events.object_id = 'd1'（医生ID）
```

## 正确查询

```sql
-- ✅ 正确：医生完整拜访记录（通过 object_events 关联）
SELECT e.id, e.event_type, e.timestamp, e.description,
       vr.visit_type, vr.objective, vr.key_insights, vr.effectiveness_score,
       o.name as doctor_name
FROM object_events e
JOIN ontology_objects o ON o.id = e.object_id
LEFT JOIN visit_records vr ON vr.id = e.related_object_id
WHERE e.event_type LIKE 'Visit%'
ORDER BY e.timestamp DESC
LIMIT 20;
```

## 错误写法

```sql
-- ❌ visit_records 没有 doctor_id 列
SELECT * FROM visit_records WHERE doctor_id = 'd1'

-- ❌ visit_records 没有 visit_date 列
SELECT * FROM visit_records ORDER BY visit_date DESC
```

---

*关联：[[salesclaw/knowledge/entities/object_events]]*
