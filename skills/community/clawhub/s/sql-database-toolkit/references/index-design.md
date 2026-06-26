# 索引设计策略

## 设计口诀
**最左前缀、区分度高、覆盖查询、避免冗余**

---

## 索引类型速查

| 类型 | 适用场景 | 注意事项 |
|------|---------|---------|
| 主键索引 | 唯一标识行 | 尽量用自增整数，避免 UUID（页分裂） |
| 唯一索引 | 业务唯一约束 | 允许 NULL（多个 NULL 不冲突） |
| 普通索引 | 高频查询列 | 区分度 > 20% 才值得建 |
| 联合索引 | 多列组合查询 | 遵循最左前缀原则 |
| 覆盖索引 | 避免回表 | 把 SELECT 列也加入索引 |
| 前缀索引 | 长字符串列 | `INDEX(col(20))`，节省空间但不能覆盖 |
| 函数索引 | 表达式查询 | MySQL 8.0+ / PostgreSQL 支持 |
| 全文索引 | 文本搜索 | 替代 LIKE '%keyword%' |

---

## 联合索引设计原则

### 最左前缀原则
```sql
-- 假设有联合索引 INDEX(a, b, c)
-- ✅ 能走索引
WHERE a = 1
WHERE a = 1 AND b = 2
WHERE a = 1 AND b = 2 AND c = 3
WHERE a = 1 AND b > 2          -- a 走等值，b 走范围
WHERE a = 1 AND c = 3          -- 只有 a 走索引，c 跳过了 b

-- ❌ 不能走索引
WHERE b = 2                    -- 跳过了 a
WHERE b = 2 AND c = 3          -- 跳过了 a
WHERE c = 3                    -- 跳过了 a 和 b
```

### 列顺序设计规则
1. **等值查询列放前面**，范围查询列放后面
2. **区分度高的列放前面**（性别不适合放第一位）
3. **ORDER BY 列放最后**（消除 filesort）

```sql
-- 查询：WHERE status = ? AND create_time > ? ORDER BY id
-- ✅ 好的索引设计：(status, create_time, id)
-- status 等值在前，create_time 范围其次，id 排序在后
CREATE INDEX idx_status_time_id ON orders(status, create_time, id);
```

### 覆盖索引设计
```sql
-- 查询：SELECT id, status, amount FROM orders WHERE user_id = ? AND status = 'paid'
-- 把 SELECT 的列也加入索引，避免回表
CREATE INDEX idx_covering ON orders(user_id, status, amount, id);
-- Extra: Using index → 不需要回表，性能极佳
```

---

## 索引失效场景（必须记住）

```sql
-- 1. 对索引列使用函数
WHERE YEAR(create_time) = 2024          -- ❌
WHERE create_time >= '2024-01-01'       -- ✅

-- 2. 隐式类型转换（字符串 vs 数字）
WHERE user_id = '1001'   -- user_id 是 INT  ❌
WHERE user_id = 1001                    -- ✅

-- 3. LIKE 前缀通配符
WHERE name LIKE '%张%'                  -- ❌ 全表扫描
WHERE name LIKE '张%'                   -- ✅ 走索引

-- 4. OR 连接不同索引列
WHERE a = 1 OR b = 2                    -- ❌（除非两列都有索引且优化器选择 index merge）
-- 改写为 UNION ALL                     -- ✅

-- 5. NOT IN / != / NOT EXISTS
WHERE status != 'active'               -- ❌ 通常不走索引
-- 改写为 IN 正向过滤                   -- ✅

-- 6. 联合索引不满足最左前缀
-- 见上方最左前缀原则

-- 7. 索引列参与计算
WHERE id + 1 = 100                     -- ❌
WHERE id = 99                          -- ✅
```

---

## 索引选择性分析

```sql
-- 计算列的区分度（越接近 1 越好，建议 > 0.1）
SELECT
    COUNT(DISTINCT status) / COUNT(*) AS status_selectivity,
    COUNT(DISTINCT user_id) / COUNT(*) AS user_id_selectivity,
    COUNT(DISTINCT DATE(create_time)) / COUNT(*) AS date_selectivity
FROM orders;

-- 查看索引使用情况（MySQL）
SELECT
    index_name,
    stat_value AS cardinality
FROM mysql.innodb_index_stats
WHERE table_name = 'orders'
  AND stat_name = 'n_diff_pfx01';

-- 查看索引是否被使用（MySQL performance_schema）
SELECT
    object_name,
    index_name,
    count_read,
    count_write
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE object_schema = 'your_db'
  AND object_name = 'orders'
ORDER BY count_read DESC;
```

---

## 索引维护

### 查找冗余索引
```sql
-- MySQL：查找前缀相同的冗余索引
SELECT
    a.table_name,
    a.index_name AS redundant_index,
    a.column_name,
    b.index_name AS dominant_index
FROM information_schema.statistics a
JOIN information_schema.statistics b
    ON a.table_schema = b.table_schema
    AND a.table_name = b.table_name
    AND a.seq_in_index = b.seq_in_index
    AND a.column_name = b.column_name
    AND a.index_name != b.index_name
WHERE a.table_schema = 'your_db';
```

### 索引碎片整理
```sql
-- MySQL：重建索引（会锁表，生产环境用 pt-online-schema-change）
ALTER TABLE orders ENGINE=InnoDB;  -- 重建整张表
OPTIMIZE TABLE orders;             -- 等价

-- 在线 DDL（MySQL 5.6+，不锁表）
ALTER TABLE orders ADD INDEX idx_new(col), ALGORITHM=INPLACE, LOCK=NONE;
```

---

## 特殊场景索引

### 时间范围查询（分区 + 索引）
```sql
-- 大表按时间分区，配合索引效果最佳
CREATE TABLE logs (
    id          BIGINT AUTO_INCREMENT,
    user_id     INT NOT NULL,
    action      VARCHAR(50),
    create_time DATETIME NOT NULL,
    PRIMARY KEY (id, create_time),  -- 分区键必须在主键中
    INDEX idx_user_time (user_id, create_time)
) PARTITION BY RANGE (YEAR(create_time)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### JSON 列索引（MySQL 5.7+）
```sql
-- 对 JSON 字段的特定路径建虚拟列索引
ALTER TABLE users
    ADD COLUMN city VARCHAR(50) GENERATED ALWAYS AS (JSON_UNQUOTE(profile->'$.city')) VIRTUAL,
    ADD INDEX idx_city (city);

SELECT * FROM users WHERE city = '北京';  -- 走虚拟列索引
```

### PostgreSQL 部分索引
```sql
-- 只对满足条件的行建索引（节省空间，提升效率）
CREATE INDEX idx_active_users ON users(email)
WHERE status = 'active';  -- 只索引活跃用户

-- 查询时必须包含相同条件才能走此索引
SELECT * FROM users WHERE email = 'x@x.com' AND status = 'active';
```
