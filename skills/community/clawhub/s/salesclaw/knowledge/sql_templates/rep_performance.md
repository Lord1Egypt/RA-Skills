# SQL 模板：代表绩效红黄牌
type: sql_template
tags: [sql, rep, performance, red-yellow, attainment]
---
# 代表绩效红黄牌

## 模板元数据
- **模板ID**: rep_performance
- **适用问题**: "哪些代表绩效差" / "红黄牌名单" / "代表达成率" / "需重点辅导的代表"
- **优先级**: P0

## 背景说明

绩效等级由 `performance_tier` 字段判断：
- 红牌：达成率 < 75% 或合规得分 < 85
- 黄牌：达成率 75%-90% 或合规得分 85-90
- 绿牌：达成率 ≥ 90% 且合规得分 ≥ 90

## SQL（红黄牌代表列表）

```sql
SELECT
    rep_id,
    rep_name,
    province,
    title,
    performance_tier,
    compliance_score,
    last_visit_date
FROM dim_reps
WHERE status = 'active'
  AND performance_tier IN ('red', 'yellow', 'RED', 'YELLOW', '红牌', '黄牌')
ORDER BY
    CASE performance_tier
        WHEN 'red' THEN 1 WHEN 'RED' THEN 1 WHEN '红牌' THEN 1
        WHEN 'yellow' THEN 2 WHEN 'YELLOW' THEN 2 WHEN '黄牌' THEN 2
        ELSE 3
    END,
    compliance_score ASC;
```

## SQL（代表目标达成）

```sql
-- 注意：目标达成需联合 sales_targets 和 fct_prescription_flow
SELECT
    r.rep_id,
    r.rep_name,
    r.province,
    r.performance_tier,
    COALESCE(SUM(f.prescription_amount), 0) as actual_sales,
    t.target_value,
    ROUND(COALESCE(SUM(f.prescription_amount), 0) / NULLIF(t.target_value, 0) * 100, 2) as attainment_pct
FROM dim_reps r
LEFT JOIN sales_targets t ON t.rep_id = r.rep_id
LEFT JOIN fct_prescription_flow f ON f.doctor_id IN (
    SELECT target_id FROM object_links
    WHERE source_id = r.rep_id AND link_type = 'RESPONSIBLE_FOR'
)
WHERE r.status = 'active'
  AND (:period IS NULL OR t.period_value = :period)
GROUP BY r.rep_id, r.rep_name, r.province, r.performance_tier, t.target_value
ORDER BY attainment_pct ASC;
```

## SQL（久未拜访代表）

```sql
SELECT
    rep_id,
    rep_name,
    province,
    last_visit_date,
    DATEDIFF(CURDATE(), last_visit_date) as days_since_visit
FROM dim_reps
WHERE status = 'active'
  AND last_visit_date IS NOT NULL
  AND DATEDIFF(CURDATE(), last_visit_date) > 30
ORDER BY days_since_visit DESC;
```