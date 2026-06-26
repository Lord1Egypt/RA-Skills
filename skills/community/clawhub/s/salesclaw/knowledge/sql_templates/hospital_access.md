# SQL 模板：医院准入状态
type: sql_template
tags: [sql, hospital, access, vbp, tender, market]
---
# 医院准入状态

## 模板元数据
- **模板ID**: hospital_access
- **适用问题**: "某品种进院情况" / "准入状态" / "VBP中选品种覆盖" / "哪家医院有药"
- **优先级**: P1

## 参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|
| product_id | VARCHAR | 否 | 品种ID（不填则查所有）|
| hospital_id | VARCHAR | 否 | 医院ID |
| access_status | VARCHAR | 否 | 准入状态 |

## SQL（品种进院汇总）

```sql
SELECT
    access_status,
    COUNT(*) as hospital_count,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM dim_hospital_access
WHERE product_id = :product_id
GROUP BY access_status;
```

## SQL（某品种在某医院的准入详情）

```sql
SELECT
    ha.access_id,
    h.hospital_id,
    h.hospital_name,
    h.province,
    h.level,
    ha.access_status,
    ha.access_date,
    ha.purchase_type,
    ha.price,
    ha.reimbursement,
    ha.stock_status
FROM dim_hospital_access ha
JOIN dim_hospitals h ON h.hospital_id = ha.hospital_id
WHERE ha.product_id = :product_id
  AND ha.hospital_id = :hospital_id;
```

## SQL（VBP 中选品种覆盖）

```sql
SELECT
    h.province,
    h.level,
    COUNT(DISTINCT ha.hospital_id) as hospital_count,
    COUNT(DISTINCT ha.product_id) as product_count
FROM dim_hospital_access ha
JOIN dim_hospitals h ON h.hospital_id = ha.hospital_id
WHERE ha.access_status LIKE '%VBP%'
GROUP BY h.province, h.level
ORDER BY hospital_count DESC;
```

## 注意事项

- `access_status` 枚举值必须先探查：`SELECT DISTINCT access_status FROM dim_hospital_access`
- 常见值：待进院 / 已进院 / 已进医保 / VBP中选 / VBP落选