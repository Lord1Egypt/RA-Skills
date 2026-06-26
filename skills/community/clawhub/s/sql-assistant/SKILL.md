---
name: sql-assistant
description: >
  Use this skill when you need to write, review, optimize, or debug SQL
  queries. Covers query construction, performance tuning, index strategy,
  window functions, CTEs, and common anti-patterns for PostgreSQL, MySQL,
  and SQLite.
---

# SQL 查询优化助手

## 核心工作流

### Step 1 — 理解需求

收集上下文：
- 数据库类型（PostgreSQL / MySQL / SQLite / SQL Server）
- 表结构（DDL 或列描述）
- 业务目标（查什么、过滤条件、聚合逻辑）
- 数据量级（小表 <10万 / 中表 <1000万 / 大表 >1000万）
- 性能问题描述（慢查询？错误结果？）

### Step 2 — 查询构建

#### 基础查询框架
```sql
SELECT
  col1,
  col2,
  agg_func(col3) AS alias
FROM table_name t
JOIN other_table o ON t.id = o.fk_id
WHERE condition
GROUP BY col1, col2
HAVING agg_condition
ORDER BY alias DESC
LIMIT 100;
```

#### CTE 模式（复杂逻辑拆分）
```sql
WITH base_data AS (
  SELECT user_id, COUNT(*) AS order_count
  FROM orders
  WHERE created_at >= '2026-01-01'
  GROUP BY user_id
),
ranked AS (
  SELECT *, RANK() OVER (ORDER BY order_count DESC) AS rk
  FROM base_data
)
SELECT * FROM ranked WHERE rk <= 10;
```

### Step 3 — 性能优化策略

#### 索引策略
```sql
-- 单列索引
CREATE INDEX idx_orders_user ON orders(user_id);

-- 复合索引（遵循最左前缀原则）
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- 覆盖索引（避免回表）
CREATE INDEX idx_orders_cover ON orders(user_id, created_at, status, amount);
```

#### EXPLAIN 分析
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM orders WHERE user_id = 42;
```

关注指标：
- `Seq Scan` → 考虑加索引
- `rows` 估算偏差大 → 需要 ANALYZE
- `cost` 高 → 优化 JOIN 顺序或添加索引
- `Buffers: shared hit/read` → 缓存命中率

### Step 4 — 常见优化模式

#### 分页优化（大表 OFFSET 慢）
```sql
-- ❌ 慢：OFFSET 需扫描丢弃前N行
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 100000;

-- ✅ 快：游标分页
SELECT * FROM orders WHERE id > :last_seen_id ORDER BY id LIMIT 20;
```

#### IN 子查询优化
```sql
-- ❌ 可能慢
SELECT * FROM users WHERE id IN (SELECT user_id FROM premium_members);

-- ✅ 用 EXISTS 或 JOIN
SELECT u.* FROM users u
JOIN premium_members pm ON u.id = pm.user_id;
```

#### 避免函数破坏索引
```sql
-- ❌ 函数包装列，索引失效
WHERE YEAR(created_at) = 2026

-- ✅ 范围条件，索引有效
WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'
```

### Step 5 — 窗口函数常用模式

```sql
-- 分组内排名
ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC)

-- 累计求和
SUM(amount) OVER (PARTITION BY user_id ORDER BY created_at)

-- 环比计算
LAG(revenue, 1) OVER (ORDER BY month) AS prev_month_revenue

-- 移动平均
AVG(score) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
```

### Step 6 — 查询审查清单

- [ ] SELECT 只取需要的列（避免 SELECT *）
- [ ] WHERE 条件列有索引
- [ ] JOIN 条件有索引
- [ ] 大表分页用游标而非 OFFSET
- [ ] 聚合前先 WHERE 过滤（减少聚合数据量）
- [ ] 复杂逻辑用 CTE 而非嵌套子查询
- [ ] 无 N+1 查询问题

## 反模式速查

| 反模式 | 修复方式 |
|--------|----------|
| SELECT * | 显式列出需要的列 |
| OFFSET 大分页 | 改用游标/keyset 分页 |
| WHERE 列用函数 | 改用范围条件 |
| 隐式类型转换 | 确保参数类型匹配 |
| 无 LIMIT 的全表扫描 | 加 LIMIT 或索引过滤 |
| OR 替代 UNION | 改用 UNION ALL |
