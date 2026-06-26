---
title: dim_reps - 销售代表表
type: entity
tags: [table, rep, salesperson, performance, field]
sources: [salesclaw_init.sql]
related: [[salesclaw/knowledge/entities/dim_territories]], [[salesclaw/knowledge/entities/fct_expense_c2]], [[salesclaw/knowledge/entities/fct_visit_detail]]
---

# dim_reps - 销售代表表

## 定位

销售代表的静态档案表，记录代表的基础信息、所属组织和绩效等级。

## 字段说明

| 字段 | 类型 | 示例/说明 |
|------|------|-----------|
| `rep_id` | VARCHAR(50) PK | `r1` |
| `rep_name` | VARCHAR(100) | `李娜` |
| `gender` / `age` | | 基本信息 |
| `territory_id` / `territory_name` | | 所辖区域 |
| `province` / `city` | | 省市 |
| `hire_date` | DATE | 入职日期 |
| `title` | VARCHAR(50) | 职级 |
| `compliance_score` | DECIMAL(5,2) | 合规评分（0-100） |
| `performance_tier` | VARCHAR(20) | 绩效等级（红/黄/绿） |
| `status` | VARCHAR(20) | active/inactive |
| `manager_id` | VARCHAR(50) | 上级代表ID |
| `region` | VARCHAR(50) | 大区 |
| `product_line` | VARCHAR(50) | 负责产品线 |
| `qualification` | VARCHAR(50) | 资质 |
| `last_visit_date` | DATE | 最后拜访日期 |
| `email` / `phone` | | 联系方式 |

## 绩效等级标准

`performance_tier` 是决策归因的核心字段：

| 等级 | 含义 | 触发条件 |
|------|------|---------|
| 红牌 | 需重点辅导 | 达成率 < 75% 或合规得分 < 85 |
| 黄牌 | 需关注 | 达成率 75%-90% 或合规得分 85-90 |
| 绿牌 | 正常 | 达成率 ≥ 90% 且合规得分 ≥ 90 |

## 关联关系

- `rep_id` → `fct_expense_c2.rep_id`（费用明细）
- `rep_id` → `fct_visit_detail.rep_id`（拜访记录）
- `rep_id` → `dim_rep_territory.territory_id`（区域映射）
- `rep_id` → `object_links.source_id`（关系网络）

## 正确查询

```sql
-- 红黄牌代表列表（用于决策归因）
SELECT rep_id, rep_name, province, performance_tier, compliance_score
FROM dim_reps
WHERE performance_tier IN ('red', 'yellow')
ORDER BY province;

-- 代表负责区域下的医院
SELECT r.rep_id, r.rep_name, t.hospital_name
FROM dim_reps r
LEFT JOIN dim_rep_hospital_mapping rm ON rm.rep_id = r.rep_id
LEFT JOIN dim_hospitals t ON t.hospital_id = rm.hospital_id
WHERE r.rep_id = 'r1';
```

## 错误写法

```sql
-- ❌ 直接用 last_visit_date 判断是否失联（应该用 object_events 时序数据）
SELECT * FROM dim_reps WHERE last_visit_date < DATE_SUB(NOW(), INTERVAL 30 DAY)

-- ❌ 假设 performance_tier 的枚举值未探查
WHERE performance_tier = '红牌'  -- 实际可能是 'red' 或 'RED'
```