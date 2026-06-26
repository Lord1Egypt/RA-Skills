---
title: dim_products - 品种表
type: entity
tags: [table, product, drug, vbp, pricing, field]
sources: [salesclaw_init.sql]
related: [[salesclaw/knowledge/entities/fct_prescription_flow]], [[salesclaw/knowledge/entities/dim_hospital_access]]
---

# dim_products - 品种表（静态层）

## 定位

品种的静态属性表，记录产品本身客观存在的、长期不变化的核心属性。动态层数据（如销量、市占率）由其他 fct 表提供。

## 字段说明

| 字段 | 类型 | 示例/说明 |
|------|------|-----------|
| `product_id` | VARCHAR(50) PK | `p1` |
| `product_name` | VARCHAR(200) | `诺欣妥` |
| `generic_name` | VARCHAR(200) | `沙库巴曲缬沙坦钠片` |
| `brand_name` | VARCHAR(100) | 品牌名 |
| `approval_number` | VARCHAR(50) | 批准文号 |
| `manufacturer` / `manufacturer_name` | VARCHAR(200) | 生产企业 |
| `therapeutic_category` | VARCHAR(100) | 治疗领域（如心血管） |
| `indication_1` / `indication_2` | VARCHAR(100) | 适应症 |
| `dosage_form` | VARCHAR(50) | 剂型（片剂/胶囊/注射液） |
| `specification` | VARCHAR(100) | 规格（如 50mg×7片） |
| `unit` | VARCHAR(20) | 单位 |
| `retail_price` | DECIMAL(10,2) | 零售价 |
| `contract_price` | DECIMAL(10,2) | 合同采购价 |
| `conversion_ratio` | DECIMAL(6,3) | 转换比（件→盒） |
| `reimbursement_type` | VARCHAR(20) | 报销类型（甲类/乙类/丙类） |
| `reimbursement_rate` | DECIMAL(5,4) | 报销比例（如 0.7） |
| `reimbursement_price` | DECIMAL(10,2) | 医保报销价 |
| `status` | VARCHAR(20) | active/inactive |
| `launch_date` | DATE | 上市日期 |
| `offpatent_date` | DATE | 专利到期日 |
| `market_segment` | VARCHAR(50) | 市场细分 |
| `core_indications` | TEXT | 核心适应症描述 |
| `annual_sales` | DECIMAL(16,2) | 年销售额（静态预估） |
| `market_potential` | DECIMAL(16,2) | 市场潜力 |
| `sales_model` | VARCHAR(30) | 销售模式（招商/直营） |
| `product_status` | VARCHAR(20) | 产品状态（如正常/VBP中选/VBP落选） |

## VBP 相关字段

品种分析中最重要的是 `product_status`（VBP 中选/落选/未纳入）和价格相关字段。VBP 中选品种价格大幅下降，但获得医院准入量；落选品种失去医院覆盖。

## 关联关系

- `product_id` → `fct_prescription_flow.product_id`（处方流向）
- `product_id` → `dim_hospital_access.product_id`（准入状态）
- `product_id` → `fct_expense_c2.product_id`（费用关联）

## 正确查询

```sql
-- VBP 品种分析：查所有中选品种及其价格
SELECT product_id, product_name, contract_price, product_status
FROM dim_products
WHERE product_status LIKE '%VBP%' OR product_status LIKE '%中选%';

-- 某品种详细信息
SELECT * FROM dim_products WHERE product_id = 'p1';
```

## 错误写法

```sql
-- ❌ 用 annual_sales 做实时分析（这是静态预估值，不是真实数据）
SELECT product_name, annual_sales FROM dim_products ORDER BY annual_sales DESC

-- ❌ 假设 product_status 枚举值未探查就过滤
WHERE product_status = 'VBP中选'  -- 实际可能是 '中选' 或 'VBP中选品种'
```