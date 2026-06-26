# SQL 开发规范与标准参考

## 目录

1. [SQL 编写规范](#sql-编写规范)
2. [数据库方言差异](#数据库方言差异)
3. [性能优化 checklist](#性能优化-checklist)
4. [常见反模式](#常见反模式)
5. [索引设计指南](#索引设计指南)

---

## SQL 编写规范

### 命名规范

| 对象 | 规范 | 示例 |
|------|------|------|
| 表名 | 小写下划线，复数形式 | `user_orders`, `product_categories` |
| 字段名 | 小写下划线 | `created_at`, `total_amount` |
| 索引名 | `idx_` + 表名 + 字段名 | `idx_orders_user_id` |
| 约束名 | `pk_`, `fk_`, `uq_` 前缀 | `pk_orders`, `fk_orders_user_id` |
| CTE名称 | 描述性名词 | `monthly_sales`, `active_users` |
| 临时表 | `tmp_` + 描述 + 日期 | `tmp_order_stats_20240317` |

### 代码格式

```sql
-- ✅ 推荐格式
SELECT
    o.order_id,o.user_id,
    u.username,
    SUM(oi.amount) AS total_amount
FROM orders o
INNER JOIN users u ON o.user_id = u.id
INNER JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.created_at >= '2024-01-01'
    AND o.status = 'completed'
GROUP BY o.order_id, o.user_id, u.username
HAVING SUM(oi.amount) > 1000
ORDER BY total_amount DESC
LIMIT 100;

-- ❌ 避免
select o.order_id, o.user_id, u.username, sum(oi.amount) as total_amount from orders o
inner join users u on o.user_id=u.id
inner join order_items oi on o.order_id=oi.order_id
where o.created_at>='2024-01-01' and o.status='completed'
group by o.order_id, o.user_id, u.username having sum(oi.amount)>1000
order by total_amount desc limit 100;
```

### 注释规范

```sql
-- ============================================
-- 查询目的：统计月度活跃用户
-- 业务场景：运营报表
-- 更新历史：
--   2024-03-01: 增加渠道筛选条件 (by zhangsan)
-- ============================================

/*
 * 临时解决方案：等待用户行为表分区改造完成后优化
 * TODO: 2024-06-01 前完成优化
 */
```

---

## 数据库方言差异

### 日期函数对比

| 功能 | MySQL | PostgreSQL | SQL Server | Oracle |
|------|-------|------------|------------|--------|
| 当前日期 | `CURDATE()` | `CURRENT_DATE` | `CAST(GETDATE() AS DATE)` | `SYSDATE` |
| 当前时间戳 | `NOW()` | `NOW()` / `CURRENT_TIMESTAMP` | `GETDATE()` | `SYSTIMESTAMP` |
| 日期加减 | `DATE_SUB(date, INTERVAL n DAY)` | `date - INTERVAL 'n days'` | `DATEADD(DAY, -n, date)` | `date - n` |
| 日期格式化 | `DATE_FORMAT(date, '%Y-%m-%d')` | `TO_CHAR(date, 'YYYY-MM-DD')` | `FORMAT(date, 'yyyy-MM-dd')` | `TO_CHAR(date, 'YYYY-MM-DD')` |
| 提取年月 | `YEAR(date)`, `MONTH(date)` | `EXTRACT(YEAR FROM date)` | `YEAR(date)`, `MONTH(date)` | `EXTRACT(YEAR FROM date)` |
| 月份第一天 | `DATE_FORMAT(date, '%Y-%m-01')` | `DATE_TRUNC('month', date)` | `DATEADD(DAY, 1, EOMONTH(date, -1))` | `TRUNC(date, 'MM')` |

### 字符串函数对比

| 功能 | MySQL | PostgreSQL | SQL Server | Oracle |
|------|-------|------------|------------|--------|
| 字符串拼接 | `CONCAT(s1, s2)` | `s1 \|\| s2` / `CONCAT(s1, s2)` | `s1 + s2` / `CONCAT(s1, s2)` | `s1 \|\| s2` / `CONCAT(s1, s2)` |
| 子串提取 | `SUBSTRING(s, start, len)` | `SUBSTRING(s FROM start FOR len)` | `SUBSTRING(s, start, len)` | `SUBSTR(s, start, len)` |
| 字符串长度 | `LENGTH(s)` / `CHAR_LENGTH(s)` | `LENGTH(s)` | `LEN(s)` / `DATALENGTH(s)` | `LENGTH(s)` |
| 去除空格 | `TRIM(s)` | `TRIM(s)` | `LTRIM(RTRIM(s))` | `TRIM(s)` |
| 替换 | `REPLACE(s, old, new)` | `REPLACE(s, old, new)` | `REPLACE(s, old, new)` | `REPLACE(s, old, new)` |
| 大小写转换 | `UPPER(s)`, `LOWER(s)` | `UPPER(s)`, `LOWER(s)` | `UPPER(s)`, `LOWER(s)` | `UPPER(s)`, `LOWER(s)` |

### 分页语法对比

```sql
-- MySQL / MariaDB
SELECT * FROM orders
ORDER BY created_at DESC
LIMIT 20 OFFSET 100;
-- 或
LIMIT 100, 20;

-- PostgreSQL
SELECT * FROM orders
ORDER BY created_at DESC
LIMIT 20 OFFSET 100;
-- 或 (PostgreSQL 13+)
SELECT * FROM orders
ORDER BY created_at DESC
FETCH FIRST 20 ROWS ONLY
OFFSET 100 ROWS;

-- SQL Server 2012+
SELECT * FROM orders
ORDER BY created_at DESC
OFFSET 100 ROWS
FETCH NEXT 20 ROWS ONLY;

-- Oracle 12c+
SELECT * FROM orders
ORDER BY created_at DESC
OFFSET 100 ROWS
FETCH NEXT 20 ROWS ONLY;

-- Oracle 11g 及更早版本
SELECT * FROM (
    SELECT a.*, ROWNUM rn FROM (
        SELECT * FROM orders ORDER BY created_at DESC
    ) a WHERE ROWNUM <= 120
) WHERE rn > 100;
```

### 类型转换对比

```sql
-- MySQL
CAST(expression AS CHAR) / CONVERT(expression, CHAR)
CAST(expression AS SIGNED) -- 转整数
CAST(expression AS DECIMAL(10,2)) -- 转小数

-- PostgreSQL
expression::text
expression::integer
expression::numeric(10,2)
CAST(expression AS text)

-- SQL Server
CAST(expression AS VARCHAR(100))
CONVERT(VARCHAR(100), expression, 120) -- 带样式

-- Oracle
TO_CHAR(expression)
TO_NUMBER(expression)
TO_DATE(expression, 'YYYY-MM-DD')
CAST(expression AS VARCHAR2(100))
```

---

## 性能优化 checklist

### 查询前检查

- [ ] 是否只查询需要的字段（避免 SELECT *）
- [ ] WHERE 条件是否使用了索引字段
- [ ] 日期范围是否使用闭开区间 `[start, end)`
- [ ] 大表查询是否添加了 LIMIT
- [ ] 是否可以使用覆盖索引

### JOIN 检查

- [ ] JOIN 条件是否完整（避免笛卡尔积）
- [ ] JOIN 字段是否有索引
- [ ] 小表是否作为驱动表
- [ ] 是否有多余的 JOIN

### 聚合检查

- [ ] GROUP BY 字段是否最小化
- [ ] HAVING 是否可以改为 WHERE
- [ ] 是否可以使用 ROLLUP/CUBE 替代多个查询

### 子查询检查

- [ ] 关联子查询是否可以改为 JOIN
- [ ] IN 子查询是否可以改为 EXISTS（大数据量时）
- [ ] 是否可以改为 CTE 提高可读性

---

## 常见反模式

### 反模式 1：SELECT *

```sql
-- ❌ 低效
SELECT * FROM orders WHERE user_id = 123;

-- ✅ 优化
SELECT order_id, order_no, total_amount, status, created_at
FROM orders
WHERE user_id = 123;
```

### 反模式 2：函数导致索引失效

```sql
-- ❌ 低效
SELECT * FROM orders
WHERE DATE(created_at) = '2024-01-01';

-- ✅ 优化
SELECT * FROM orders
WHERE created_at >= '2024-01-01'
    AND created_at < '2024-01-02';
```

### 反模式 3：大偏移分页

```sql
-- ❌ 低效
SELECT * FROM orders
ORDER BY created_at DESC
LIMIT 10 OFFSET 1000000;

-- ✅ 优化（游标分页）
SELECT * FROM orders
WHERE created_at < '2024-01-15 14:30:00' -- 上一页最后一条的时间
ORDER BY created_at DESC
LIMIT 10;
```

### 反模式 4：隐式类型转换

```sql
-- ❌ 低效（user_id 是 BIGINT）
SELECT * FROM orders WHERE user_id = '12345';

-- ✅ 优化
SELECT * FROM orders WHERE user_id = 12345;
```

### 反模式 5：NOT IN 子查询（含 NULL）

```sql
-- ❌ 危险（子查询含 NULL 时结果为空）
SELECT * FROM users
WHERE id NOT IN (SELECT user_id FROM banned_users);

-- ✅ 优化（使用 NOT EXISTS）
SELECT * FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM banned_users b WHERE b.user_id = u.id
);
```

### 反模式 6：UNION 去重（不需要时）

```sql
-- ❌ 低效（如果确定无重复）
SELECT user_id FROM orders_2023
UNION
SELECT user_id FROM orders_2024;

-- ✅ 优化
SELECT user_id FROM orders_2023
UNION ALL
SELECT user_id FROM orders_2024;
```

---

## 索引设计指南

### 索引类型选择

| 场景 | 推荐索引类型 | 示例 |
|------|-------------|------|
| 等值查询 | B-Tree 普通索引 | `CREATE INDEX idx ON table(col)` |
| 范围查询 | B-Tree 索引 | `CREATE INDEX idx ON table(date_col)` |
| 多条件查询 | 复合索引 | `CREATE INDEX idx ON table(col1, col2)` |
| 文本搜索 | 全文索引 | `CREATE FULLTEXT INDEX idx ON table(text_col)` |
| JSON 字段 | 函数索引 / GIN | `CREATE INDEX idx ON table((json_col->>'field'))` |
| 地理位置 | GiST / SP-GiST | `CREATE INDEX idx ON table USING GIST (geo_col)` |
| 数组类型 | GIN | `CREATE INDEX idx ON table USING GIN (array_col)` |

### 复合索引设计原则

**最左前缀原则**：
```sql
-- 索引 (a, b, c)
WHERE a = 1              -- ✅ 使用索引
WHERE a = 1 AND b = 2    -- ✅ 使用索引
WHERE a = 1 AND b = 2 AND c = 3  -- ✅ 使用索引
WHERE b = 2              -- ❌ 不使用索引
WHERE a = 1 AND c = 3    -- ✅ 使用索引（仅 a）
WHERE a = 1 AND b > 2 AND c = 3  -- ✅ 使用索引（a, b）
```

**列顺序建议**：
1. 等值查询条件列在前
2. 区分度高的列在前
3. 范围查询列在后（因为范围查询后的列不走索引）

### 覆盖索引

```sql
-- 查询
SELECT user_id, order_date, status FROM orders
WHERE user_id = 123 AND order_date >= '2024-01-01';

-- 覆盖索引（包含所有查询和返回字段）
CREATE INDEX idx_orders_covering
ON orders(user_id, order_date, status);
```

### 索引维护

```sql
-- PostgreSQL：更新统计信息
ANALYZE orders;

-- PostgreSQL：重建索引（释放空间）
REINDEX INDEX idx_orders_user_id;

-- MySQL：优化表（重建索引）
OPTIMIZE TABLE orders;

-- MySQL：更新统计信息
ANALYZE TABLE orders;

-- 查看索引使用情况（PostgreSQL）
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE tablename = 'orders';

-- 查看索引使用情况（MySQL 8.0）
SELECT
    OBJECT_NAME,
    INDEX_NAME,
    COUNT_FETCH,
    COUNT_INSERT,
    COUNT_UPDATE
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE OBJECT_NAME = 'orders';
```

---

## 参考资料

- [PostgreSQL 文档 - Query Planning](https://www.postgresql.org/docs/current/planner-optimizer.html)
- [MySQL 文档 - Optimization](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [SQL Server 查询优化指南](https://docs.microsoft.com/sql/relational-databases/query-processing-architecture-guide)
- [Oracle 性能调优指南](https://docs.oracle.com/en/database/oracle/oracle-database/tgsql/)
