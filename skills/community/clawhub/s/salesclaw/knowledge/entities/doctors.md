---
title: doctors - 医生表（HCP）
type: entity
tags: [table, doctor, hcp, field, business-key]
sources: [salesclaw.db schema + 2条示例数据]
related: [[salesclaw/knowledge/entities/ontology_objects]], [[salesclaw/knowledge/entities/object_events]], [[salesclaw/knowledge/entities/time_series_data]]
---

# doctors - 医生表（HCP）

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | VARCHAR PK | `d1` |
| `title` | VARCHAR | `主任医师` |
| `department` | VARCHAR | `心内科` |
| `specialty` | TEXT | `冠心病,心力衰竭` |
| `prescription_power` | INTEGER | `95`（1-10，处方潜力评分）|
| `influence_score` | INTEGER | `88`（1-10，学术影响力）|
| `prescription_volume` | INTEGER | `120`（可以是 NULL）|
| `last_visit_date` | VARCHAR | `2026-02-01` |
| `next_recommended_visit_date` | VARCHAR | `2026-05-22` |

## 示例数据

```
d1 | 主任医师 | 心内科 | 冠心病,心力衰竭 | 95 | 88 | 120 | 2026-02-01 | 2026-05-22
d2 | 副主任医师 | 神经内科 | 帕金森,阿尔茨海默症 | 82 | 75 | NULL | 2026-03-10 | 2026-04-10
```

## 核心业务规则

1. **KOL 识别**：`influence_score ≥ 7` 且 `prescription_volume` 非 NULL 为重点维护对象
2. **久未拜访**：`last_visit_date` 超过 30 天需优先安排
3. **处方量趋势**：查看趋势必须用 `time_series_data`（`series_name = 'prescriptionVolume'`），doctors 表的 `prescription_volume` 是快照
4. **推荐下次拜访**：`next_recommended_visit_date` 由系统根据历史间隔自动计算

## 关联关系

- `id` → `ontology_objects.id`（获取 name/status/sentiment）
- `id` → `object_events.object_id`（获取事件）
- `id` → `object_links.source_id`（获取关系）
- `id` → `time_series_data.object_id`（获取时序数据）

## 正确查询

```sql
-- 医生画像（含状态）
SELECT d.*, o.name, o.status, o.sentiment, o.lifecycle_stage
FROM doctors d
JOIN ontology_objects o ON o.id = d.id
WHERE d.id = 'd1';

-- 处方量趋势（查 time_series_data，不是 doctors 表的快照）
SELECT ts.timestamp, ts.value
FROM time_series_data ts
WHERE ts.object_id = 'd1'
  AND ts.series_name = 'prescriptionVolume'
ORDER BY ts.timestamp ASC;
```

## 错误写法

```sql
-- ❌ doctors.prescription_volume 是快照，看趋势无效
SELECT * FROM doctors ORDER BY prescription_volume DESC

-- ❌ 拜访记录不在 doctors 表，查 object_events
SELECT * FROM doctors WHERE last_visit_date > '2026-01-01'
```

---

*关联：[[salesclaw/knowledge/entities/time_series_data]] / [[salesclaw/knowledge/entities/object_events]]*
