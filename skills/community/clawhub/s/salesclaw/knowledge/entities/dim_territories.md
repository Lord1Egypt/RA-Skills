---
title: dim_territories - 区域表
type: entity
tags: [table, territory, region, organization, field]
sources: [salesclaw_init.sql]
related: [[salesclaw/knowledge/entities/dim_reps]], [[salesclaw/knowledge/entities/dim_hospitals]]
---

# dim_territories - 区域表

## 定位

组织层级表，记录从大区到地区的区域结构及其基本信息。是销售组织架构的维度表。

## 字段说明

| 字段 | 类型 | 示例/说明 |
|------|------|-----------|
| `territory_id` | VARCHAR(50) PK | `t1` |
| `territory_name` | VARCHAR(200) | `华东大区-浙江-杭州` |
| `region` | VARCHAR(50) | 大区（如华东/华北） |
| `province` | VARCHAR(50) | 省 |
| `city` | VARCHAR(50) | 城市 |
| `city_tier` | VARCHAR(20) | 城市分级（一线/二线/三线） |
| `hospital_count` | INT | 医院数量（静态统计） |
| `doctor_count` | INT | 医生数量 |
| `rep_count` | INT | 代表人数 |
| `target_sales` | DECIMAL(16,2) | 销售目标 |
| `actual_sales` | DECIMAL(16,2) | 实际销售 |
| `status` | VARCHAR(20) | active/inactive |

## 组织层级关系

```
大区 (region) → 省区 (province) → 地区 (city) →  territory
```

归因分析中，结构归因需要纵向穿透：`region → province → city` 逐层下探。

## 关联关系

- `territory_id` → `dim_rep_territory.territory_id`（代表-区域映射）
- `territory_id` → `dim_territory_mapping.territory_id`（更细粒度的层级映射）
- 通过 `province` 可与 `fct_expense_c2` 的省区字段关联做 DeltaWeight 分析

## 正确查询

```sql
-- 省区维度汇总（用于结构归因）
SELECT province, region,
       COUNT(DISTINCT territory_id) as territory_count,
       SUM(target_sales) as total_target,
       SUM(actual_sales) as total_actual
FROM dim_territories
GROUP BY province, region
ORDER BY region;

-- 某大区下的省区列表
SELECT DISTINCT province FROM dim_territories WHERE region = '华东';
```

## 注意事项

- `hospital_count` / `doctor_count` 是静态快照，不是实时数据
- 区域层级可能存在 2 级（region+province）或 3 级（region+province+city）两种粒度，查询时需确认实际层级