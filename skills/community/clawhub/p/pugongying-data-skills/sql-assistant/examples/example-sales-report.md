# 示例：销售报表SQL开发完整流程

## 场景描述

业务需求：统计2024年Q1各区域销售情况，包含销售额、订单量、客单价、同比增长率

## 阶段1：SQL生成

**输入**：
```
/sql-gen 使用PostgreSQL语法，统计2024年Q1各区域的销售额、订单量、客单价，
         计算同比增长率（对比2023年Q1），只包含已完成订单，按销售额降序排列
```

**输出**：
```sql
-- ============================================
-- 查询目的：统计2024年Q1各区域销售情况及同比增长
-- 目标数据库：PostgreSQL 15
-- 生成时间：2025-03-17
-- ============================================

WITH q1_2024 AS (
    -- 2024年Q1销售数据
    SELECT
        region_code,
        region_name,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(total_amount) AS sales_amount,
        AVG(total_amount) AS avg_order_value
    FROM orders
    WHERE order_date >= '2024-01-01'
        AND order_date < '2024-04-01'
        AND status = 'completed'
    GROUP BY region_code, region_name
),

q1_2023 AS (
    -- 2023年Q1销售数据
    SELECT
        region_code,
        SUM(total_amount) AS sales_amount
    FROM orders
    WHERE order_date >= '2023-01-01'
        AND order_date < '2023-04-01'
        AND status = 'completed'
    GROUP BY region_code
)

SELECT
    a.region_code AS 区域编码,
    a.region_name AS 区域名称,
    a.order_count AS 订单量,
    ROUND(a.sales_amount, 2) AS 销售总额,
    ROUND(a.avg_order_value, 2) AS 平均客单价,
    ROUND(b.sales_amount, 2) AS 去年同期销售额,
    CASE
        WHEN b.sales_amount > 0 THEN
            ROUND((a.sales_amount - b.sales_amount) * 100.0 / b.sales_amount, 2)
        ELSE NULL
    END AS 同比增长率
FROM q1_2024 a
LEFT JOIN q1_2023 b ON a.region_code = b.region_code
ORDER BY a.sales_amount DESC;

-- ============================================
-- 执行建议：
-- ============================================
-- 1. 建议索引：
--    CREATE INDEX idx_orders_date_status_region
--    ON orders(order_date, status, region_code)
--    INCLUDE (total_amount);

-- 2. 预计扫描行数：2024年Q1订单数（假设50万单）

-- 3. 预期执行时间：有索引 < 500ms，无索引 3-5秒
```

---

## 阶段2：SQL审查

**输入**：
```
/sql-review [上一步生成的SQL]
```

**输出摘要**：

| 维度 | 评分 | 状态 |
|------|------|------|
| 性能优化 | 8/10 | 🟢 良好 |
| 代码可读性 | 9/10 | 🟢 良好 |
| 健壮性 | 8/10 | 🟢 良好 |
| 安全性 | 10/10 | 🟢 良好 |
| **综合评分** | **8.8/10** | - |

**发现的问题**：
- 🟢 无严重问题
- 🟡 警告：CTE `q1_2023` 可能被多次引用时重复计算（当前场景无此问题）
- 🟢 建议：可考虑使用窗口函数一次性计算多年数据（更灵活）

---

## 阶段3：执行计划分析

**输入**：
```
/sql-explain
[粘贴 PostgreSQL EXPLAIN (ANALYZE, BUFFERS) 结果]
```

**执行计划（简化）**：
```
Hash Left Join (cost=3456.00..5678.90 rows=50 width=120)
  (actual time=245.3..389.2 rows=35 loops=1)
  Hash Cond: (a.region_code = b.region_code)
  Buffers: shared hit=2340 read=560
  ->  Subquery Scan on a (cost=1728.00..2876.45 rows=50 width=88)
        ->  HashAggregate (cost=1728.00..1828.00 rows=50 width=56)
              Group Key: orders.region_code, orders.region_name
              Buffers: shared hit=1170 read=280
              ->  Bitmap Heap Scan on orders
                    Recheck Cond: ((order_date >= '2024-01-01') AND ...)
                    Buffers: shared hit=1170 read=280
                    ->  Bitmap Index Scan on idx_orders_date_status
                          Index Cond: ((order_date >= '2024-01-01') AND ...)
  ->  Hash (cost=1728.00..1728.00 rows=50 width=16)
        Buckets: 1024  Batches: 1  Memory Usage: 10kB
        ->  HashAggregate (cost=1628.00..1728.00 rows=50 width=16)
              Group Key: orders.region_code
              Buffers: shared hit=1170 read=280
              ->  Bitmap Heap Scan on orders orders_1
                    Recheck Cond: ((order_date >= '2023-01-01') AND ...)
                    Buffers: shared hit=1170 read=280
                    ->  Bitmap Index Scan on idx_orders_date_status
                          Index Cond: ((order_date >= '2023-01-01') AND ...)
Planning Time: 0.523 ms
Execution Time: 389.5 ms
```

**分析结果摘要**：

| 指标 | 数值 | 评级 |
|------|------|------|
| 总执行时间 | 389.5 ms | 🟢 良好 |
| 规划时间 | 0.523 ms | 🟢 优秀 |
| I/O操作 | 560次读取 | 🟡 一般 |
| 缓存命中率 | 80.7% | 🟢 良好 |

**关键发现**：
- 🟢 使用了Bitmap Index Scan，索引有效
- 🟡 两次Bitmap Heap Scan可以优化（考虑物化视图缓存年度数据）
- 🟢 Hash Join选择正确

**优化建议**：
```sql
-- 如果该查询频繁执行，建议创建物化视图
CREATE MATERIALIZED VIEW mv_quarterly_sales AS
SELECT
    DATE_TRUNC('quarter', order_date) AS quarter,
    region_code,
    region_name,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(total_amount) AS sales_amount
FROM orders
WHERE status = 'completed'
GROUP BY DATE_TRUNC('quarter', order_date), region_code, region_name;

-- 创建索引
CREATE INDEX idx_mv_quarterly ON mv_quarterly_sales(quarter, region_code);

-- 定时刷新（每晚）
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_quarterly_sales;
```

---

## 完整开发流程总结

```
需求理解 (2分钟)
    │
    ▼
SQL生成 /sql-gen (30秒)
    │
    ▼
SQL审查 /sql-review (1分钟)
    │ ← 8.8/10分，无需修改
    ▼
测试环境执行 + EXPLAIN (2分钟)
    │
    ▼
执行计划分析 /sql-explain (1分钟)
    │ ← 389ms，性能达标
    ▼
生产部署
    │
    ▼
监控运行情况
```

**总耗时**：约6-7分钟完成一个复杂报表SQL的开发和优化

**对比传统方式**：
| 步骤 | 传统方式 | AI辅助 | 节省时间 |
|------|----------|--------|----------|
| SQL编写 | 15分钟 | 30秒 | 97% |
| 代码审查 | 10分钟 | 1分钟 | 90% |
| 性能优化 | 20分钟 | 3分钟 | 85% |
| **总计** | **45分钟** | **6.5分钟** | **85%** |
