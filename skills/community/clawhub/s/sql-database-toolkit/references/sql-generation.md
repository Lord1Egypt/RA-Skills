# SQL 生成指南

## 生成流程

### Step 1：理解业务意图
不要急于写 SQL，先把业务问题翻译成数据问题：
- 要查什么实体？（用户、订单、商品...）
- 要什么维度的聚合？（按天、按用户、按地区...）
- 过滤条件是什么？（时间范围、状态、金额...）
- 结果如何排序和限制？

### Step 2：确认 Schema
如果用户没有提供，主动询问：
```
请提供相关表的 DDL，或者告诉我：
- 表名和主要字段
- 哪些字段有索引
- 大概的数据量级
```

### Step 3：生成 SQL（分难度）

---

## 基础查询模式

### 单表聚合
```sql
-- 业务：统计每天的订单数和总金额（近30天）
-- 数据库：MySQL 8.0
-- 性能预期：orders 表千万级，date 字段有索引，<100ms
-- 注意：create_time 为 NULL 的记录会被 WHERE 过滤掉

SELECT
    DATE(create_time)           AS order_date,
    COUNT(*)                    AS order_cnt,
    SUM(amount)                 AS total_amount,
    AVG(amount)                 AS avg_amount,
    COUNT(DISTINCT user_id)     AS uv          -- 去重用户数
FROM orders
WHERE create_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
  AND status != 'cancelled'                    -- 排除取消订单
GROUP BY DATE(create_time)
ORDER BY order_date DESC;
```

### 多表 JOIN
```sql
-- 业务：查询用户最近一次购买的商品信息
-- 数据库：MySQL 8.0
-- 性能预期：需要 user_id 和 create_time 的联合索引
-- 注意：使用子查询取最新订单，避免 GROUP BY 后 JOIN 的数据膨胀

SELECT
    u.user_id,
    u.username,
    o.order_id,
    o.create_time   AS last_order_time,
    p.product_name,
    o.amount
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
INNER JOIN (
    -- 每个用户最新订单
    SELECT user_id, MAX(create_time) AS max_time
    FROM orders
    WHERE status = 'completed'
    GROUP BY user_id
) latest ON o.user_id = latest.user_id
         AND o.create_time = latest.max_time
INNER JOIN products p ON o.product_id = p.product_id
WHERE u.status = 'active';
```

### 窗口函数（生产必备）
```sql
-- 业务：计算每个用户的订单金额排名和累计金额
-- 数据库：MySQL 8.0+ / PostgreSQL
-- 性能预期：窗口函数在大数据量下注意分区粒度

SELECT
    user_id,
    order_id,
    amount,
    -- 排名（并列不跳号用 DENSE_RANK，跳号用 RANK）
    DENSE_RANK() OVER (
        PARTITION BY user_id
        ORDER BY amount DESC
    )                                           AS amount_rank,
    -- 累计金额
    SUM(amount) OVER (
        PARTITION BY user_id
        ORDER BY create_time
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )                                           AS cumulative_amount,
    -- 环比（当前行 vs 上一行）
    amount - LAG(amount, 1, 0) OVER (
        PARTITION BY user_id
        ORDER BY create_time
    )                                           AS amount_diff
FROM orders
WHERE status = 'completed';
```

---

## 进阶查询模式

### 递归 CTE（树形结构）
```sql
-- 业务：查询组织架构树（从某节点向下所有子节点）
-- 数据库：MySQL 8.0+ / PostgreSQL
-- 注意：设置 max_recursion_depth 防止死循环

WITH RECURSIVE org_tree AS (
    -- 锚点：起始节点
    SELECT
        id,
        name,
        parent_id,
        0           AS depth,
        CAST(name AS CHAR(1000)) AS path
    FROM departments
    WHERE id = 1   -- 从根节点开始

    UNION ALL

    -- 递归：向下展开
    SELECT
        d.id,
        d.name,
        d.parent_id,
        ot.depth + 1,
        CONCAT(ot.path, ' > ', d.name)
    FROM departments d
    INNER JOIN org_tree ot ON d.parent_id = ot.id
    WHERE ot.depth < 10   -- 防止无限递归
)
SELECT * FROM org_tree ORDER BY path;
```

### 行转列（PIVOT）
```sql
-- 业务：将每月销售额从行格式转为列格式
-- 数据库：MySQL（无原生 PIVOT，用条件聚合）

SELECT
    product_id,
    SUM(CASE WHEN month = '2024-01' THEN amount ELSE 0 END) AS jan,
    SUM(CASE WHEN month = '2024-02' THEN amount ELSE 0 END) AS feb,
    SUM(CASE WHEN month = '2024-03' THEN amount ELSE 0 END) AS mar,
    SUM(amount)                                              AS total
FROM monthly_sales
WHERE month BETWEEN '2024-01' AND '2024-03'
GROUP BY product_id;

-- PostgreSQL 版本（使用 crosstab，需要 tablefunc 扩展）
-- SELECT * FROM crosstab(...) AS ct(product_id INT, jan NUMERIC, feb NUMERIC, mar NUMERIC);
```

### 去重保留最新记录
```sql
-- 业务：每个用户只保留最新的一条记录（去重）
-- 方案 A：ROW_NUMBER（推荐，语义清晰）
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY create_time DESC
        ) AS rn
    FROM user_logs
)
SELECT * FROM ranked WHERE rn = 1;

-- 方案 B：子查询（兼容性更好，但性能可能差）
SELECT * FROM user_logs ul
WHERE create_time = (
    SELECT MAX(create_time)
    FROM user_logs
    WHERE user_id = ul.user_id
);
-- ⚠️ 方案 B 在大表上是相关子查询，性能极差，慎用
```

---

## 大数据量专项

### 分页优化（LIMIT 大偏移量）
```sql
-- ❌ 错误写法：LIMIT 100000, 20 会扫描 100020 行
SELECT * FROM orders ORDER BY id LIMIT 100000, 20;

-- ✅ 正确写法：延迟关联（Deferred Join）
SELECT o.*
FROM orders o
INNER JOIN (
    SELECT id FROM orders ORDER BY id LIMIT 100000, 20
) ids ON o.id = ids.id;

-- ✅ 更好的写法：游标分页（需要记录上次最大 ID）
SELECT * FROM orders
WHERE id > :last_max_id   -- 上次查询的最大 id
ORDER BY id
LIMIT 20;
```

### 批量 INSERT 优化
```sql
-- ❌ 逐行插入（N 次网络往返）
INSERT INTO logs VALUES (1, 'a', NOW());
INSERT INTO logs VALUES (2, 'b', NOW());

-- ✅ 批量插入（1 次网络往返）
INSERT INTO logs (id, content, create_time) VALUES
    (1, 'a', NOW()),
    (2, 'b', NOW()),
    (3, 'c', NOW());
-- 建议每批 500-1000 行，避免单次事务过大

-- ✅ UPSERT（存在则更新，不存在则插入）
-- MySQL:
INSERT INTO user_stats (user_id, login_cnt)
VALUES (1001, 1)
ON DUPLICATE KEY UPDATE login_cnt = login_cnt + 1;

-- PostgreSQL:
INSERT INTO user_stats (user_id, login_cnt)
VALUES (1001, 1)
ON CONFLICT (user_id)
DO UPDATE SET login_cnt = user_stats.login_cnt + 1;
```

---

## NULL 处理规范

```sql
-- NULL 的三值逻辑：TRUE / FALSE / UNKNOWN
-- NULL != NULL → UNKNOWN（不是 TRUE！）
-- 正确判断 NULL：IS NULL / IS NOT NULL

-- ❌ 错误：WHERE col != 'value' 不会返回 col IS NULL 的行
SELECT * FROM t WHERE col != 'active';

-- ✅ 正确：明确处理 NULL
SELECT * FROM t WHERE col != 'active' OR col IS NULL;

-- COALESCE：返回第一个非 NULL 值
SELECT COALESCE(nickname, username, '匿名用户') AS display_name FROM users;

-- NULL 在聚合中的行为
SELECT
    COUNT(*)        AS total_rows,      -- 包含 NULL 行
    COUNT(col)      AS non_null_cnt,    -- 不含 NULL 行
    SUM(col)        AS sum_val,         -- NULL 被忽略
    AVG(col)        AS avg_val          -- NULL 被忽略（分母也不含 NULL）
FROM t;
```
