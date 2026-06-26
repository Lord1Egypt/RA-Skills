# SQL 模板：目标达成追踪
type: sql_template
tags: [sql, target, attainment, pdca, sales]
---
# 目标达成追踪

## 模板元数据
- **模板ID**: target_attainment
- **适用问题**: "某区域目标达成" / "代表达成率" / "完成进度" / "缺口分析"
- **优先级**: P1

## 参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| period | VARCHAR | 否 | 周期，如 2025Q2 |

## SQL（省区维度汇总）

```sql
SELECT
    r.province,
    r.region,
    COUNT(DISTINCT r.rep_id) as rep_count,
    SUM(COALESCE(t.target_value, 0)) as total_target,
    SUM(COALESCE(SUM(f.prescription_amount), 0)) as total_actual,
    ROUND(
        SUM(COALESCE(SUM(f.prescription_amount), 0)) /
        NULLIF(SUM(COALESCE(t.target_value, 0)), 0) * 100, 2
    ) as attainment_pct
FROM dim_reps r
LEFT JOIN sales_targets t ON t.rep_id = r.rep_id
LEFT JOIN fct_prescription_flow f ON f.doctor_id IN (
    SELECT target_id FROM object_links
    WHERE source_id = r.rep_id AND link_type = 'RESPONSIBLE_FOR'
)
WHERE r.status = 'active'
  AND (:period IS NULL OR t.period_value = :period)
GROUP BY r.province, r.region
ORDER BY attainment_pct ASC;
```

## SQL（缺口分析：实际 < 目标的省区）

```sql
WITH province_attainment AS (
    SELECT
        r.province,
        SUM(COALESCE(t.target_value, 0)) as total_target,
        SUM(COALESCE(SUM(f.prescription_amount), 0)) as total_actual
    FROM dim_reps r
    LEFT JOIN sales_targets t ON t.rep_id = r.rep_id
    LEFT JOIN fct_prescription_flow f ON f.doctor_id IN (
        SELECT target_id FROM object_links
        WHERE source_id = r.rep_id AND link_type = 'RESPONSIBLE_FOR'
    )
    WHERE r.status = 'active'
    GROUP BY r.province
)
SELECT
    province,
    total_target,
    total_actual,
    (total_target - total_actual) as gap,
    ROUND((total_target - total_actual) / NULLIF(total_target, 0) * 100, 2) as gap_pct
FROM province_attainment
WHERE total_actual < total_target
ORDER BY gap DESC;
```