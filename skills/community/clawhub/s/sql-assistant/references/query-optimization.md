# SQL 性能调优完整指南

## 查询执行计划解读

### PostgreSQL EXPLAIN 输出解读

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 1;
```

输出示例：
```
Index Scan using idx_orders_user on orders
  (cost=0.43..8.45 rows=1 width=64)
  (actual time=0.021..0.023 rows=1 loops=1)
  Index Cond: (user_id = 1)
Buffers: shared hit=3
Planning Time: 0.5 ms
Execution Time: 0.05 ms
```

关键字段说明：
| 字段 | 含义 | 优化方向 |
|------|------|----------|
| Seq Scan | 全表扫描 | 添加索引 |
| Index Scan | 索引扫描（回表） | 考虑覆盖索引 |
| Index Only Scan | 仅索引（最优） | 目标状态 |
| Hash Join | 哈希连接 | 大表连接正常 |
| Nested Loop | 嵌套循环 | 小表驱动大表时有效 |
| rows（估算vs实际差异大） | 统计信息不准 | 运行 ANALYZE |

### MySQL EXPLAIN 关键字段

```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 1\G
```

| Extra 字段 | 含义 |
|-----------|------|
| Using index | 覆盖索引，最优 |
| Using where | 过滤条件在存储引擎层 |
| Using filesort | 内存/磁盘排序，考虑索引 |
| Using temporary | 使用临时表，性能警告 |
| NULL | 正常全表扫描 |

---

## 索引设计原则

### 索引选择性
- 选择性 = 不同值数量 / 总行数
- 选择性 > 0.1 的列适合建索引
- 性别、状态等低选择性列不适合单独建索引

### 复合索引最左前缀规则

```sql
-- 索引：(a, b, c)
SELECT * FROM t WHERE a = 1;              -- ✅ 用到索引
SELECT * FROM t WHERE a = 1 AND b = 2;   -- ✅ 用到索引
SELECT * FROM t WHERE b = 2;             -- ❌ 不用索引
SELECT * FROM t WHERE a = 1 AND c = 3;   -- ✅ 仅用到 a 部分
SELECT * FROM t WHERE a > 1 AND b = 2;   -- ✅ a范围查询，b可能用不到
```

### 索引设计口诀
1. **等值查询**列放前面
2. **范围查询**列放后面
3. **ORDER BY**列放最后（与查询顺序一致）
4. **高选择性**列优先

---

## 慢查询诊断流程

### Step 1：开启慢查询日志
```sql
-- MySQL
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1; -- 超过1秒记录

-- PostgreSQL (postgresql.conf)
log_min_duration_statement = 1000  -- 毫秒
```

### Step 2：分析慢查询
```bash
# MySQL 慢查询分析工具
pt-query-digest /var/log/mysql/slow.log

# 或用 mysqldumpslow
mysqldumpslow -s t -t 10 /var/log/mysql/slow.log
```

### Step 3：EXPLAIN 分析
```sql
EXPLAIN FORMAT=JSON SELECT ...\G  -- MySQL
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT ...;  -- PostgreSQL
```

### Step 4：优化并验证
- 添加索引 → 再次 EXPLAIN 确认使用索引
- 重写查询 → 对比执行时间
- 更新统计信息：`ANALYZE TABLE orders;`（MySQL）或 `ANALYZE orders;`（PG）

---

## 常见业务场景 SQL 模式

### 分组取最新记录（每用户最后一条订单）
```sql
-- 方法1：窗口函数（推荐）
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) rn
  FROM orders
) t WHERE rn = 1;

-- 方法2：关联子查询
SELECT o.* FROM orders o
WHERE o.created_at = (
  SELECT MAX(created_at) FROM orders WHERE user_id = o.user_id
);
```

### 统计连续登录天数
```sql
WITH login_gaps AS (
  SELECT
    user_id,
    login_date,
    login_date - INTERVAL (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date)) DAY AS grp
  FROM user_logins
),
streaks AS (
  SELECT user_id, grp, COUNT(*) AS consecutive_days
  FROM login_gaps
  GROUP BY user_id, grp
)
SELECT user_id, MAX(consecutive_days) AS max_streak
FROM streaks
GROUP BY user_id;
```

### 同比环比计算
```sql
SELECT
  month,
  revenue,
  LAG(revenue, 1) OVER (ORDER BY month) AS prev_month,
  ROUND((revenue - LAG(revenue, 1) OVER (ORDER BY month)) * 100.0
        / LAG(revenue, 1) OVER (ORDER BY month), 2) AS mom_growth_pct,
  LAG(revenue, 12) OVER (ORDER BY month) AS same_month_last_year,
  ROUND((revenue - LAG(revenue, 12) OVER (ORDER BY month)) * 100.0
        / LAG(revenue, 12) OVER (ORDER BY month), 2) AS yoy_growth_pct
FROM monthly_revenue
ORDER BY month;
```
