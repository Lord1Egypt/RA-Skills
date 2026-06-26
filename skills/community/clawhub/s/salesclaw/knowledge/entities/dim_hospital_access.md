---
title: dim_hospital_access - 医院准入表
type: entity
tags: [table, access, hospital, tender, vbp, field]
sources: [salesclaw_init.sql]
related: [[salesclaw/knowledge/entities/dim_products]], [[salesclaw/knowledge/entities/dim_hospitals]]
---

# dim_hospital_access - 医院准入表

## 定位

记录品种在医院准入状态的明细数据，是 VBP 分析和市场渗透率计算的核心数据源。

## 字段说明

| 字段 | 类型 | 示例/说明 |
|------|------|-----------|
| `access_id` | VARCHAR(50) PK | 准入唯一标识 |
| `hospital_id` | VARCHAR(50) | 医院ID |
| `product_id` | VARCHAR(50) | 品种ID |
| `access_status` | VARCHAR(30) | 准入状态（待进院/已进院/已进医保/VBP中选等） |
| `access_date` | DATE | 准入日期 |
| `purchase_type` | VARCHAR(50) | 采购类型（基药/医保/VBP/自费） |
| `stock_status` | VARCHAR(20) | 库存状态（有库存/缺货） |
| `price` | DECIMAL(10,2) | 价格 |
| `reimbursement` | VARCHAR(20) | 医保报销类型 |
| `notes` | TEXT | 备注 |

## 准入状态枚举（需探查确认）

常见取值：`待进院` / `已进院` / `已进医保` / `VBP中选` / `VBP落选` / `自费`

**注意**：`access_status` 的实际枚举值必须先探查，不能假设：
```sql
SELECT DISTINCT access_status FROM dim_hospital_access;
```

## VBP 分析

VBP（药品集中带量采购）中选品种的 `access_status` 会变为 `VBP中选`，价格大幅下降，但获得医院承诺采购量。

```sql
-- 某品种进院情况
SELECT access_status, COUNT(*) as hospital_count
FROM dim_hospital_access
WHERE product_id = 'p1'
GROUP BY access_status;

-- VBP 中选品种的价格变化
SELECT ha.hospital_id, ha.price, dp.contract_price, dp.retail_price
FROM dim_hospital_access ha
JOIN dim_products dp ON dp.product_id = ha.product_id
WHERE ha.product_id = 'p1' AND ha.access_status LIKE '%VBP%';
```

## 关联关系

- `hospital_id` → `dim_hospitals.hospital_id`（医院档案）
- `product_id` → `dim_products.product_id`（品种档案）
- 通过 `access_status` 可判断市场覆盖状态