# SQL 模板：省区费用红黄绿灯（DeltaWeight）
type: sql_template
tags: [sql, expense, deltaweight, alert, red-yellow-green]
---
# 省区费用红黄绿灯（DeltaWeight）

## 模板元数据
- **模板ID**: expense_red_green
- **适用问题**: "哪些省区费用异常" / "费用超限" / "会议费偏高" / "费用率预警"
- **优先级**: P0

## 背景说明

DeltaWeight = 某省区某费用类型占比 - 全国该费用类型占比

- 🔴 红灯：DeltaWeight ≥ 30ppt
- 🟡 黄灯：DeltaWeight ≥ 15ppt

## 参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| start_date | DATE | 否 | 起始日期（默认本年） |
| end_date | DATE | 否 | 截止日期（默认本年） |

## SQL（DeltaWeight 计算）

```sql
WITH national_ratio AS (
    SELECT
        expense_type,
        SUM(amount) / SUM(SUM(amount)) OVER () AS national_ratio
    FROM fct_expense_c2
    WHERE expense_date BETWEEN :start_date AND :end_date
      AND approval_status = 'approved'
      AND expense_type IS NOT NULL
    GROUP BY expense_type
),
province_ratio AS (
    SELECT
        province,
        expense_type,
        SUM(amount) / SUM(SUM(amount)) OVER (PARTITION BY province) AS province_ratio
    FROM fct_expense_c2
    WHERE expense_date BETWEEN :start_date AND :end_date
      AND approval_status = 'approved'
      AND province IS NOT NULL
      AND expense_type IS NOT NULL
    GROUP BY province, expense_type
)
SELECT
    p.province,
    p.expense_type,
    ROUND(p.province_ratio * 100, 2) as province_pct,
    ROUND(n.national_ratio * 100, 2) as national_pct,
    ROUND((p.province_ratio - n.national_ratio) * 100, 2) AS delta_weight_ppt,
    CASE
        WHEN ABS(p.province_ratio - n.national_ratio) >= 0.30 THEN '🔴 红灯'
        WHEN ABS(p.province_ratio - n.national_ratio) >= 0.15 THEN '🟡 黄灯'
        ELSE '🟢 绿灯'
    END AS alert_level
FROM province_ratio p
JOIN national_ratio n ON p.expense_type = n.expense_type
WHERE ABS(p.province_ratio - n.national_ratio) >= 0.15
ORDER BY ABS(p.province_ratio - n.national_ratio) DESC;
```

## SQL（某省区费用明细）

```sql
SELECT
    expense_type,
    category,
    SUM(amount) as total_amount,
    COUNT(*) as expense_count,
    AVG(amount) as avg_amount
FROM fct_expense_c2
WHERE province = :province
  AND expense_date BETWEEN :start_date AND :end_date
  AND approval_status = 'approved'
GROUP BY expense_type, category
ORDER BY total_amount DESC;
```