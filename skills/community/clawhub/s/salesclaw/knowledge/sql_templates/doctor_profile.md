# SQL 模板：医生档案查询
type: sql_template
tags: [sql, doctor, hcp, profile]
---
# 医生档案查询

## 模板元数据
- **模板ID**: doctor_profile
- **适用问题**: "查某个医生的信息" / "医生xxx档案" / "某医生处方能力"
- **优先级**: P1

## 参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| doctor_id | VARCHAR | 是 | 医生ID |

## SQL

```sql
-- 医生基本信息（含状态）
SELECT d.id, d.title, d.department, d.prescription_power,
       d.influence_score, d.prescription_volume, d.last_visit_date,
       o.name, o.status, o.lifecycle_stage
FROM dim_doctors d
JOIN ontology_objects o ON o.id = d.id
WHERE d.id = :doctor_id;
```

## 衍生查询

```sql
-- 该医生的处方量时序（趋势要查 time_series_data，不是 doctors 表快照）
SELECT ts.timestamp, ts.value
FROM time_series_data ts
WHERE ts.object_id = :doctor_id
  AND ts.series_name = 'prescriptionVolume'
ORDER BY ts.timestamp ASC;

-- 该医生的关系链接（代表/医院/竞品）
SELECT link_type, target_id, target_name, target_type, link_strength
FROM object_links
WHERE source_id = :doctor_id
ORDER BY link_type;
```