# 多方言差异速查

## 方言对比矩阵

| 功能 | MySQL | PostgreSQL | Hive | Spark SQL | ClickHouse |
|------|-------|-----------|------|-----------|------------|
| 字符串拼接 | `CONCAT(a,b)` | `a \|\| b` | `CONCAT(a,b)` | `CONCAT(a,b)` | `concat(a,b)` |
| 日期格式化 | `DATE_FORMAT(d,'%Y-%m')` | `TO_CHAR(d,'YYYY-MM')` | `DATE_FORMAT(d,'yyyy-MM')` | `DATE_FORMAT(d,'yyyy-MM')` | `formatDateTime(d,'%Y-%m')` |
| 当前时间 | `NOW()` | `NOW()` | `CURRENT_TIMESTAMP` | `CURRENT_TIMESTAMP` | `now()` |
| 日期差 | `DATEDIFF(a,b)` | `a - b` | `DATEDIFF(a,b)` | `DATEDIFF(a,b)` | `dateDiff('day',b,a)` |
| 字符串截取 | `SUBSTRING(s,1,3)` | `SUBSTRING(s,1,3)` | `SUBSTR(s,1,3)` | `SUBSTR(s,1,3)` | `substring(s,1,3)` |
| 条件表达式 | `IF(cond,a,b)` | `CASE WHEN` | `IF(cond,a,b)` | `IF(cond,a,b)` | `if(cond,a,b)` |
| 行号 | `ROW_NUMBER()` | `ROW_NUMBER()` | `ROW_NUMBER()` | `ROW_NUMBER()` | `row_number()` |
| UPSERT | `ON DUPLICATE KEY` | `ON CONFLICT DO UPDATE` | 不支持 | 不支持 | `INSERT OR REPLACE` |
| 递归 CTE | 8.0+ 支持 | 支持 | 不支持 | 支持 | 支持 |
| JSON 支持 | 5.7+ | 原生 JSONB | 有限 | 有限 | 有限 |
| 窗口函数 | 8.0+ | 完整支持 | 完整支持 | 完整支持 | 完整支持 |

---

## MySQL 特有语法

```sql
-- LIMIT 语法
SELECT * FROM t LIMIT 10;           -- 前10行
SELECT * FROM t LIMIT 10, 20;       -- 跳过10行，取20行（注意：偏移量在前）
SELECT * FROM t LIMIT 20 OFFSET 10; -- 等价写法

-- GROUP_CONCAT（行转列）
SELECT user_id, GROUP_CONCAT(tag ORDER BY tag SEPARATOR ',') AS tags
FROM user_tags GROUP BY user_id;

-- ON DUPLICATE KEY UPDATE
INSERT INTO counters (key, cnt) VALUES ('pv', 1)
ON DUPLICATE KEY UPDATE cnt = cnt + 1;

-- 日期函数
SELECT
    DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s'),  -- 格式化
    DATE_ADD(NOW(), INTERVAL 7 DAY),           -- 加7天
    DATE_SUB(NOW(), INTERVAL 1 MONTH),         -- 减1月
    LAST_DAY(NOW()),                           -- 当月最后一天
    WEEKDAY(NOW()),                            -- 星期几（0=周一）
    QUARTER(NOW());                            -- 季度

-- 字符串函数
SELECT
    FIND_IN_SET('b', 'a,b,c'),    -- 返回 2（位置）
    FIELD('b', 'a', 'b', 'c'),    -- 返回 2（位置）
    ELT(2, 'a', 'b', 'c');        -- 返回 'b'（按位置取值）
```

---

## PostgreSQL 特有语法

```sql
-- RETURNING（返回被修改的行）
INSERT INTO users (name) VALUES ('张三') RETURNING id, name;
UPDATE orders SET status = 'paid' WHERE id = 1 RETURNING *;
DELETE FROM logs WHERE id = 1 RETURNING *;

-- 数组操作
SELECT ARRAY[1,2,3];
SELECT '{1,2,3}'::INT[];
SELECT array_agg(id ORDER BY id) FROM users;  -- 聚合为数组
SELECT unnest(ARRAY[1,2,3]);                  -- 展开数组为行

-- JSONB 操作
SELECT data->'name' AS name FROM users;           -- 取 JSON 字段（返回 JSON）
SELECT data->>'name' AS name FROM users;          -- 取 JSON 字段（返回文本）
SELECT data#>>'{address,city}' AS city FROM users; -- 嵌套路径
UPDATE users SET data = data || '{"vip":true}';   -- 合并 JSON
CREATE INDEX idx_json ON users USING GIN(data);   -- JSON 索引

-- 窗口函数扩展
SELECT
    NTILE(4) OVER (ORDER BY amount) AS quartile,  -- 四分位
    PERCENT_RANK() OVER (ORDER BY amount),         -- 百分比排名
    CUME_DIST() OVER (ORDER BY amount)             -- 累积分布
FROM orders;

-- 物化视图
CREATE MATERIALIZED VIEW mv_daily_stats AS
SELECT DATE(create_time), COUNT(*), SUM(amount)
FROM orders GROUP BY DATE(create_time);

REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_stats;  -- 不锁表刷新

-- 分区表（声明式分区）
CREATE TABLE orders (
    id BIGSERIAL,
    create_time TIMESTAMPTZ NOT NULL,
    amount NUMERIC
) PARTITION BY RANGE (create_time);

CREATE TABLE orders_2024_01 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

---

## Hive / Spark SQL 特有语法

```sql
-- 分区操作
SHOW PARTITIONS table_name;
ALTER TABLE t ADD PARTITION (dt='2024-01-15');
ALTER TABLE t DROP PARTITION (dt='2024-01-01');

-- 动态分区插入
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

INSERT OVERWRITE TABLE dwd_orders PARTITION (dt)
SELECT *, DATE(create_time) AS dt FROM ods_orders;

-- LATERAL VIEW（展开数组/Map）
SELECT user_id, tag
FROM user_tags
LATERAL VIEW EXPLODE(tags_array) tmp AS tag;

-- LATERAL VIEW OUTER（保留空数组的行）
SELECT user_id, tag
FROM user_tags
LATERAL VIEW OUTER EXPLODE(tags_array) tmp AS tag;

-- collect_set / collect_list（聚合为数组）
SELECT user_id,
    collect_set(tag)  AS unique_tags,   -- 去重
    collect_list(tag) AS all_tags       -- 不去重
FROM user_tags GROUP BY user_id;

-- 窗口函数（Hive 特有）
SELECT *,
    FIRST_VALUE(amount) OVER (PARTITION BY user_id ORDER BY create_time) AS first_order_amount,
    LAST_VALUE(amount)  OVER (PARTITION BY user_id ORDER BY create_time
                              ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_order_amount
FROM orders;

-- Hive 性能配置
SET hive.vectorized.execution.enabled = true;   -- 向量化执行
SET hive.cbo.enable = true;                     -- 开启 CBO
SET mapreduce.job.reduces = 200;                -- 设置 Reduce 数量
SET hive.exec.parallel = true;                  -- 并行执行无依赖 Stage
```

---

## ClickHouse 特有语法

```sql
-- 引擎选择（最重要的设计决策）
-- MergeTree：最常用，支持排序键、分区
CREATE TABLE orders (
    order_id    UInt64,
    user_id     UInt32,
    amount      Float64,
    create_time DateTime
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(create_time)   -- 按月分区
ORDER BY (user_id, create_time)       -- 排序键（也是稀疏索引）
TTL create_time + INTERVAL 1 YEAR;   -- 数据过期自动删除

-- ReplacingMergeTree：去重（异步，不保证实时）
ENGINE = ReplacingMergeTree(version_col)

-- AggregatingMergeTree：预聚合
ENGINE = AggregatingMergeTree()

-- 物化视图（实时预聚合）
CREATE MATERIALIZED VIEW mv_daily_orders
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(order_date)
ORDER BY (order_date, user_id)
AS SELECT
    toDate(create_time) AS order_date,
    user_id,
    count() AS order_cnt,
    sum(amount) AS total_amount
FROM orders
GROUP BY order_date, user_id;

-- 数组函数
SELECT arrayJoin([1,2,3]);                    -- 展开数组
SELECT groupArray(amount) FROM orders;         -- 聚合为数组
SELECT arraySum([1,2,3]);                      -- 数组求和
SELECT arrayFilter(x -> x > 10, [5,15,20]);   -- 数组过滤

-- 近似计算（大数据量下极快）
SELECT uniq(user_id) FROM orders;              -- 近似去重计数
SELECT quantile(0.99)(amount) FROM orders;     -- 近似分位数
SELECT topK(10)(product_id) FROM orders;       -- 近似 Top K
```
