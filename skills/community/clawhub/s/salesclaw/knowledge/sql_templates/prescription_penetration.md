# SQL 模板：处方渗透率分析
type: sql_template
tags: [sql, prescription, penetration, hospital, product]
---
# 处方渗透率分析

## 模板元数据
- **模板ID**: prescription_penetration
- **适用问题**: "某品种在医院的渗透率" / "覆盖率" / "上量空间" / "目标医院有哪些在用药"
- **优先级**: P1

## 参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|
| product_id | VARCHAR | 否 | 品种ID |
| hospital_id | VARCHAR | 否 | 医院ID |

## SQL（某品种在目标医院的渗透率）

```sql
SELECT
    pf.hospital_id,
    h.hospital_name,
    h.level,
    SUM(pf.prescription_volume) as total_volume,
    dp.prescription_power,
    ROUND(
        SUM(pf.prescription_volume) /
        NULLIF(dp.prescription_power * 100, 0) * 100, 2
    ) as penetration_rate,
    SUM(pf.new_patient_count) as new_patients
FROM fct_prescription_flow pf
JOIN dim_hospitals h ON h.hospital_id = pf.hospital_id
JOIN dim_products dp ON dp.product_id = pf.product_id
WHERE pf.product_id = :product_id
GROUP BY pf.hospital_id, h.hospital_name, h.level, dp.prescription_power
ORDER BY penetration_rate DESC;
```

## SQL（某医院所有品种的处方量排名）

```sql
SELECT
    pf.product_id,
    p.product_name,
    p.therapeutic_category,
    SUM(pf.prescription_volume) as total_volume,
    SUM(pf.prescription_amount) as total_amount,
    COUNT(DISTINCT pf.doctor_id) as doctor_count,
    SUM(pf.new_patient_count) as new_patients
FROM fct_prescription_flow pf
JOIN dim_products p ON p.product_id = pf.product_id
WHERE pf.hospital_id = :hospital_id
GROUP BY pf.product_id, p.product_name, p.therapeutic_category
ORDER BY total_volume DESC;
```

## SQL（渗透率变化趋势）

```sql
SELECT
    prescription_month,
    hospital_id,
    SUM(prescription_volume) as vol,
    ROUND(
        SUM(prescription_volume) /
        NULLIF(SUM(prescription_volume) OVER (
            PARTITION BY hospital_id ORDER BY prescription_month
        ), 0) * 100, 2
    ) as penetration_pct
FROM fct_prescription_flow
WHERE product_id = :product_id
GROUP BY prescription_month, hospital_id
ORDER BY hospital_id, prescription_month;
```