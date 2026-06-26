---
title: object_events - 事件记录表
type: entity
tags: [table, time-dimension, analysis, compliance]
sources: [salesclaw.db schema + 2条示例数据]
related: [[salesclaw/knowledge/entities/doctors]], [[salesclaw/knowledge/entities/visit_records]], [[salesclaw/knowledge/entities/ontology_objects]]
---

# object_events - 事件记录表

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | VARCHAR PK | `e1` |
| `object_id` | VARCHAR | `d1`（事件主体，如医生ID）|
| `event_type` | VARCHAR | `Visit`、`SentimentChange` |
| `timestamp` | VARCHAR | `2026-02-01 14:00` |
| `description` | TEXT | `完成学术拜访` |
| `related_object_id` | VARCHAR | `v1`（关联的拜访记录ID）|
| `related_object_name` | VARCHAR | `学术拜访-0201` |

## 示例数据

```
e1 | d1 | Visit          | 2026-02-01 14:00 | 完成学术拜访                   | v1 | 学术拜访-0201
e2 | d1 | SentimentChange| 2026-02-15 10:00 | 态度从中性转为关注             | d1 | 张主任
e3 | d1 | PrescriptionDrop| 2026-03-01 08:00| 处方量下降25%                 | d1 | 张主任
```

## event_type 取值清单

| event_type | 主体 | 说明 |
|-----------|------|------|
| `Visit` | Doctor | 拜访发生 |
| `SentimentChange` | Doctor | 医生态度变化 |
| `PrescriptionDrop` | Doctor | 处方量下降事件 |
| `AcademicPublication` | Doctor | 学术发表 |
| `AccessGranted` | Hospital | 准入获批 |
| `VisitCompleted` | Doctor | 拜访完成 |
| `TargetMissed` | SalesRep | 目标未达成 |

## 核心作用：连接 object 和 visit_records

```
object_events.object_id = 'd1'
object_events.related_object_id = 'v1'（visit_records.id）
        ↓
visit_records.id = 'v1'
```

这是查询医生拜访记录的正确路径。

## 正确查询

```sql
-- 某医生的所有事件
SELECT * FROM object_events
WHERE object_id = 'd1'
ORDER BY timestamp DESC;

-- 拜访记录（通过 object_events 关联 visit_records）
SELECT e.*, vr.visit_type, vr.key_insights
FROM object_events e
LEFT JOIN visit_records vr ON vr.id = e.related_object_id
WHERE e.object_id = 'd1'
  AND e.event_type LIKE 'Visit%'
ORDER BY e.timestamp DESC;
```

---

*关联：[[salesclaw/knowledge/entities/doctors]] / [[salesclaw/knowledge/entities/visit_records]]*
