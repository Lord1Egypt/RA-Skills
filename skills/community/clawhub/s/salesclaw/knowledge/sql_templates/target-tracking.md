---
title: 目标追踪（Target Tracking）
type: sql_template
tags: [sql, target, sales, pdca, attainment]
---

# SQL 模板：目标追踪

## 用途

追踪代表/省区/区域的销售目标达成进度，用于PDCA闭环。

```sql
-- 代表目标达成（按产品线）
SELECT
    r.rep_id, r.rep_name, r.province,
    r.product_line,
    t.target_value,
    COALESCE(SUM(f.prescription_amount), 0) as actual_value,
    ROUND(COALESCE(SUM(f.prescription_amount), 0) / NULLIF(t.target_value, 0) * 100, 2) as attainment_pct
FROM dim_reps r
LEFT JOIN sales_targets t ON t.rep_id = r.rep_id
LEFT JOIN fct_prescription_flow f ON f.doctor_id IN (
    SELECT target_id FROM object_links WHERE source_id = r.rep_id AND link_type = 'RESPONSIBLE_FOR'
)
WHERE r.status = 'active'
  AND (:period IS NULL OR t.period_value = :period)
GROUP BY r.rep_id, r.rep_name, r.province, r.product_line, t.target_value
ORDER BY attainment_pct ASC
LIMIT 50;

-- 省区达成汇总
SELECT
    r.province,
    SUM(t.target_value) as total_target,
    SUM(COALESCE(SUM(f.prescription_amount), 0)) as total_actual,
    ROUND(SUM(COALESCE(SUM(f.prescription_amount), 0)) / NULLIF(SUM(t.target_value), 0) * 100, 2) as attainment_pct
FROM dim_reps r
LEFT JOIN sales_targets t ON t.rep_id = r.rep_id
LEFT JOIN fct_prescription_flow f ON f.doctor_id IN (
    SELECT target_id FROM object_links WHERE source_id = r.rep_id AND link_type = 'RESPONSIBLE_FOR'
)
WHERE r.status = 'active'
GROUP BY r.province
ORDER BY attainment_pct ASC;
```

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `period` | VARCHAR | 周期（如 2025Q2，可选）|