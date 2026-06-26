---
title: fct_prescription_flow - 处方流向表
type: entity
tags: [table, prescription, flow, hospital, monthly, field]
sources: [salesclaw_init.sql]
related: [[salesclaw/knowledge/entities/dim_products]], [[salesclaw/knowledge/entities/dim_doctors]], [[salesclaw/knowledge/entities/dim_hospitals]]
---

# fct_prescription_flow - 处方流向表

## 定位

处方的事实表，记录某品种在某医院/某医生某月的处方量数据。是销售闭环分析和渗透率计算的核心数据源。

## 字段说明

| 字段 | 类型 | 示例/说明 |
|------|------|-----------|
| `flow_id` | VARCHAR(50) PK | 流向唯一标识 |
| `product_id` | VARCHAR(50) | 品种ID |
| `doctor_id` | VARCHAR(50) | 医生ID |
| `hospital_id` | VARCHAR(50) | 医院ID |
| `prescription_month` | VARCHAR(7) | 处方月份（格式 YYYY-MM） |
| `prescription_volume` | DECIMAL(12,2) | 处方盒数 |
| `prescription_amount` | DECIMAL(16,2) | 处方金额（元） |
| `patient_count` | INT | 患者数 |
| `avg_dosage` | DECIMAL(10,2) | 平均用量 |
| `new_patient_count` | INT | 新患者数 |
| `repeat_patient_count` | INT | 复诊患者数 |
| `status` | VARCHAR(20) | active/inactive |

## 核心业务指标

```sql
-- 月度处方量趋势（某品种）
SELECT prescription_month, SUM(prescription_volume) as total_volume
FROM fct_prescription_flow
WHERE product_id = 'p1'
GROUP BY prescription_month
ORDER BY prescription_month;

-- 处方量环比变化（用于告警）
WITH monthly AS (
    SELECT prescription_month, SUM(prescription_volume) as vol
    FROM fct_prescription_flow
    WHERE product_id = 'p1'
    GROUP BY prescription_month
)
SELECT
    a.prescription_month,
    a.vol as current_vol,
    b.vol as prev_vol,
    (a.vol - b.vol) / b.vol * 100 as change_pct
FROM monthly a
JOIN monthly b ON a.prescription_month = DATE_FORMAT(DATE_SUB(STR_TO_DATE(CONCAT(a.prescription_month,'-01'),'%Y-%m-%d'), INTERVAL 1 MONTH), '%Y-%m')
ORDER BY a.prescription_month;
```

## 处方量下滑告警

触发条件：`prescription_volume` 环比下降 > 15%，对应诊断规则 DR001。

## 关联关系

- `product_id` → `dim_products.product_id`（品种档案）
- `doctor_id` → `dim_doctors.id`（医生档案）
- `hospital_id` → `dim_hospitals.hospital_id`（医院档案）

## 渗透率计算

```sql
-- 某医院某品种的处方渗透率
SELECT
    pf.hospital_id,
    pf.product_id,
    SUM(pf.prescription_volume) as total_volume,
    dp.prescription_power,
    SUM(pf.prescription_volume) / (dp.prescription_power * 100) as penetration_rate
FROM fct_prescription_flow pf
JOIN dim_products dp ON dp.product_id = pf.product_id
WHERE pf.hospital_id = 'h1' AND pf.product_id = 'p1'
GROUP BY pf.hospital_id, pf.product_id;
```

## 注意事项

- `prescription_month` 是 VARCHAR(7) 类型（如 '2025-03'），不是 DATE，需注意比较操作
- 处方量是盒数，不是金额；需换算时用 `conversion_ratio`