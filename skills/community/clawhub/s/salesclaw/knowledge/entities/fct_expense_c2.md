---
title: fct_expense_c2 - 费用明细表（会议费/拜访费）
type: entity
tags: [table, expense, cost, meeting, field]
sources: [salesclaw_init.sql]
related: [[salesclaw/knowledge/entities/dim_reps]], [[salesclaw/knowledge/entities/dim_territories]]
---

# fct_expense_c2 - 费用明细表（会议费/拜访费）

## 定位

费用的事实表，记录每笔费用的明细数据。是 DeltaWeight 告警和归因分析的核心数据源。

## 字段说明

| 字段 | 类型 | 示例/说明 |
|------|------|-----------|
| `expense_id` | VARCHAR(50) PK | 费用唯一标识 |
| `rep_id` / `rep_name` | | 报销代表 |
| `hospital_id` / `hospital_name` | | 关联医院 |
| `product_id` | | 关联品种 |
| `expense_type` | VARCHAR(50) | 费用类型（会议费/交通费/拜访费） |
| `expense_date` | DATE | 费用发生日期 |
| `amount` | DECIMAL(12,2) | 金额（元） |
| `category` / `sub_category` | VARCHAR(50) | 分类/子分类 |
| `description` | TEXT | 费用描述 |
| `vendor` | VARCHAR(200) | 供应商（会议场地等） |
| `receipt_no` / `receipt_url` | | 发票号/发票图片URL |
| `invoice_type` | VARCHAR(30) | 发票类型 |
| `tax_rate` / `tax_amount` | DECIMAL | 税率/税额 |
| `compliance_check` | VARCHAR(50) | 合规检查结果 |
| `approval_status` | VARCHAR(30) | 审批状态（pending/approved/rejected） |
| `approved_by` / `approved_at` | | 审批人/审批时间 |
| `status` | VARCHAR(20) | active/inactive |

## DeltaWeight 计算

```sql
-- 计算某省区某费用类型的 DeltaWeight
WITH national_ratio AS (
    SELECT expense_type, SUM(amount) / SUM(SUM(amount)) OVER () AS national_ratio
    FROM fct_expense_c2 WHERE expense_date >= '2025-01-01'
    GROUP BY expense_type
),
province_ratio AS (
    SELECT province, expense_type,
           SUM(amount) / SUM(SUM(amount)) OVER (PARTITION BY province) AS province_ratio
    FROM fct_expense_c2
    WHERE province IS NOT NULL AND expense_date >= '2025-01-01'
    GROUP BY province, expense_type
)
SELECT p.province, p.expense_type,
       (p.province_ratio - n.national_ratio) * 100 AS delta_weight_ppt
FROM province_ratio p
JOIN national_ratio n ON p.expense_type = n.expense_type
WHERE ABS(p.province_ratio - n.national_ratio) >= 15
ORDER BY ABS(p.province_ratio - n.national_ratio) DESC;
```

## 红黄牌告警触发条件

| 告警级别 | 触发条件 | 响应时间 |
|---------|---------|---------|
| 🔴 红牌 | DeltaWeight ≥ 30ppt 或 单笔金额 > 2×全国P90 | 24h |
| 🟡 黄牌 | DeltaWeight ≥ 15ppt 或 单笔金额 > 1.5×全国P90 | 1周 |

## 关联关系

- `rep_id` → `dim_reps.rep_id`（代表档案）
- `hospital_id` → `dim_hospitals.hospital_id`（医院档案）
- 通过 `province` 字段与 `dim_territories.province` 关联做区域分析

## 注意事项

- `compliance_check` 字段值需探查（如"通过"/"不通过"/"待审"）
- `approval_status` 为 "pending" 的费用不应计入正式分析（未审批）
- 发票 URL 可用于合规审计追溯