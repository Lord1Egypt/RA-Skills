# SQL 模板：品种处方量趋势
type: sql_template
tags: [sql, prescription, trend, product, monthly]
---
# 品种处方量趋势

## 模板元数据
- **模板ID**: prescription_trend
- **适用问题**: "某品种最近趋势" / "处方量下滑" / "哪个月开始下降" / "环比变化"
- **优先级**: P0（最高频）

## 参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| product_id | VARCHAR | 是 | 品种ID |

## SQL（单品种月度趋势）

```sql
SELECT
    prescription_month,
    SUM(prescription_volume) as total_volume,
    SUM(prescription_amount) as total_amount,
    COUNT(DISTINCT hospital_id) as hospital_count
FROM fct_prescription_flow
WHERE product_id = :product_id
GROUP BY prescription_month
ORDER BY prescription_month;
```

## SQL（环比变化）

```sql
WITH monthly AS (
    SELECT
        prescription_month,
        SUM(prescription_volume) as vol
    FROM fct_prescription_flow
    WHERE product_id = :product_id
    GROUP BY prescription_month
)
SELECT
    a.prescription_month,
    a.vol as current_vol,
    b.vol as prev_vol,
    ROUND((a.vol - b.vol) / NULLIF(b.vol, 0) * 100, 2) as change_pct
FROM monthly a
LEFT JOIN monthly b
  ON b.prescription_month = DATE_FORMAT(
      DATE_SUB(
          STR_TO_DATE(CONCAT(a.prescription_month, '-01'), '%Y-%m-%d'),
          INTERVAL 1 MONTH
      ), '%Y-%m')
ORDER BY a.prescription_month;
```

## 衍生查询

```sql
-- 某品种在指定医院的流向
SELECT hospital_id, prescription_month,
       SUM(prescription_volume) as vol
FROM fct_prescription_flow
WHERE product_id = :product_id
  AND hospital_id IN (:hospital_ids)
GROUP BY hospital_id, prescription_month
ORDER BY prescription_month;
```