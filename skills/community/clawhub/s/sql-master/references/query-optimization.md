# 慢查询诊断 & 执行计划分析

## 诊断流程

```
收到慢 SQL
    ↓
1. 读 EXPLAIN 输出（识别问题类型）
    ↓
2. 定位根因（全表扫描/索引失效/数据倾斜/...）
    ↓
3. 给出优化方案（改写 SQL / 加索引 / 改架构）
    ↓
4. 估算收益 + 提供验证方法
```

---

## MySQL EXPLAIN 解读

### 关键字段含义

| 字段 | 含义 | 危险信号 |
|------|------|---------|
| `type` | 访问类型 | `ALL`（全表扫描）、`index`（全索引扫描） |
| `key` | 实际使用的索引 | `NULL`（没用索引） |
| `rows` | 预估扫描行数 | 远大于实际返回行数 |
| `Extra` | 附加信息 | `Using filesort`、`Using temporary` |
| `filtered` | 过滤比例 | 很低说明索引选择性差 |

### type 访问类型（从好到差）
```
system > const > eq_ref > ref > range > index > ALL

const：主键或唯一索引等值查询，最快
eq_ref：JOIN 时被驱动表用主键/唯一索引，很快
ref：非唯一索引等值查询
range：索引范围扫描（BETWEEN, >, <, IN）
index：全索引扫描（比 ALL 好，但仍然慢）
ALL：全表扫描，必须优化
```

### Extra 字段解读
```
Using index          → 覆盖索引，不需要回表，很好 ✅
Using where          → 在 Server 层过滤，索引不够精确
Using filesort       → 需要额外排序，考虑加索引 ⚠️
Using temporary      → 使用临时表，GROUP BY/ORDER BY 列不一致 ⚠️
Using index condition → 索引下推（ICP），MySQL 5.6+，较好 ✅
Select tables optimized away → 直接从索引返回，最优 ✅
```

### 实战示例：读懂一个 EXPLAIN

```sql
EXPLAIN SELECT u.name, COUNT(o.id) AS order_cnt
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id
ORDER BY order_cnt DESC
LIMIT 10;
```

```
+----+-------------+-------+------+---------------+--------+---------+------------------+------+----------------------------------------------+
| id | select_type | table | type | possible_keys | key    | key_len | ref              | rows | Extra                                        |
+----+-------------+-------+------+---------------+--------+---------+------------------+------+----------------------------------------------+
|  1 | SIMPLE      | u     | ref  | idx_status    | idx_status | 1   | const            | 5000 | Using index condition; Using temporary; Using filesort |
|  1 | SIMPLE      | o     | ref  | idx_user_id   | idx_user_id | 4 | db.u.id          |   10 | NULL                                         |
+----+-------------+-------+------+---------------+--------+---------+------------------+------+----------------------------------------------+
```

**诊断**：
- `u` 表：`Using temporary; Using filesort` → GROUP BY + ORDER BY 触发了临时表和文件排序
- `u.rows = 5000` → status='active' 过滤后还有 5000 行，选择性不够好
- `o` 表：正常，走了 idx_user_id

**优化方向**：
1. 如果 active 用户占比很高，考虑去掉 status 过滤或换策略
2. 加 `(status, id)` 联合索引，让 GROUP BY 利用索引顺序消除 filesort

---

## PostgreSQL EXPLAIN ANALYZE 解读

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT ...;
```

### 关键指标
```
Seq Scan        → 全表扫描，需要索引
Index Scan      → 索引扫描 + 回表
Index Only Scan → 覆盖索引，最优
Bitmap Heap Scan → 批量回表，适合低选择性查询
Hash Join       → 哈希连接，适合大表等值 JOIN
Nested Loop     → 嵌套循环，适合小表驱动大表
Merge Join      → 归并连接，适合有序数据

actual time=X..Y → X 是第一行时间，Y 是最后一行时间
rows=N          → 实际返回行数
loops=N         → 执行次数（Nested Loop 内层会多次执行）
Buffers: shared hit=X read=Y → hit 是缓存命中，read 是磁盘读
```

### 实战：识别数据倾斜
```
Hash Join  (cost=... actual time=5000..5000 rows=1000000 loops=1)
  Hash Cond: (o.user_id = u.id)
  ->  Seq Scan on orders  (actual time=0.1..2000 rows=10000000 loops=1)
  ->  Hash  (actual time=100..100 rows=100 loops=1)
        Buckets: 1024  Batches: 8  Memory Usage: 4096kB  ← Batches>1 说明内存不够，溢出磁盘
```

---

## 常见慢查询模式 & 修复

### 模式 1：索引失效（函数/类型转换）

```sql
-- ❌ 慢：对索引列使用函数，索引失效
SELECT * FROM orders WHERE DATE(create_time) = '2024-01-01';
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';
SELECT * FROM orders WHERE user_id = '1001';  -- user_id 是 INT，传了字符串

-- ✅ 快：改写为范围查询，保持索引列干净
SELECT * FROM orders
WHERE create_time >= '2024-01-01 00:00:00'
  AND create_time <  '2024-01-02 00:00:00';

-- ✅ 快：建函数索引（MySQL 8.0+ / PostgreSQL）
CREATE INDEX idx_email_lower ON users ((LOWER(email)));
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';
```

### 模式 2：深度分页

```sql
-- ❌ 慢：扫描 1000020 行，丢弃前 1000000 行
SELECT * FROM logs ORDER BY id LIMIT 1000000, 20;

-- ✅ 快：游标分页（业务上记录上次最大 id）
SELECT * FROM logs WHERE id > :cursor ORDER BY id LIMIT 20;

-- ✅ 快：延迟关联（必须分页时）
SELECT l.* FROM logs l
JOIN (SELECT id FROM logs ORDER BY id LIMIT 1000000, 20) t ON l.id = t.id;
```

### 模式 3：N+1 查询

```sql
-- ❌ 慢：查出 100 个用户，再循环查 100 次订单（N+1）
SELECT * FROM users WHERE status = 'active';
-- 然后对每个 user_id 执行：
SELECT * FROM orders WHERE user_id = ?;

-- ✅ 快：一次 JOIN 或 IN 查询
SELECT u.*, o.order_id, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';

-- 或者（当 JOIN 结果集太大时）
SELECT * FROM orders
WHERE user_id IN (
    SELECT id FROM users WHERE status = 'active'
);
```

### 模式 4：OR 导致索引失效

```sql
-- ❌ 慢：OR 连接不同列，无法走复合索引
SELECT * FROM orders WHERE user_id = 1001 OR product_id = 2002;

-- ✅ 快：改写为 UNION ALL（各自走各自的索引）
SELECT * FROM orders WHERE user_id = 1001
UNION ALL
SELECT * FROM orders WHERE product_id = 2002
  AND user_id != 1001;  -- 避免重复
```

### 模式 5：大 IN 列表

```sql
-- ❌ 慢：IN 列表超过几百个值，优化器可能放弃索引
SELECT * FROM products WHERE id IN (1,2,3,...,10000);

-- ✅ 快：改为临时表 JOIN
CREATE TEMPORARY TABLE tmp_ids (id INT PRIMARY KEY);
INSERT INTO tmp_ids VALUES (1),(2),(3),...;
SELECT p.* FROM products p JOIN tmp_ids t ON p.id = t.id;
```

### 模式 6：COUNT 优化

```sql
-- 场景：只需要知道是否存在，不需要精确数量
-- ❌ 慢：COUNT(*) 扫描所有行
SELECT COUNT(*) FROM orders WHERE user_id = 1001;

-- ✅ 快：EXISTS 找到第一条就停止
SELECT EXISTS(SELECT 1 FROM orders WHERE user_id = 1001);

-- 场景：需要精确总数（大表）
-- ✅ MySQL：information_schema 近似值（误差<5%）
SELECT table_rows FROM information_schema.tables
WHERE table_name = 'orders';

-- ✅ PostgreSQL：pg_class 近似值
SELECT reltuples::BIGINT FROM pg_class WHERE relname = 'orders';
```

---

## 锁分析

### MySQL 查看锁等待
```sql
-- 查看当前锁等待
SELECT
    r.trx_id                    AS waiting_trx_id,
    r.trx_mysql_thread_id       AS waiting_thread,
    r.trx_query                 AS waiting_query,
    b.trx_id                    AS blocking_trx_id,
    b.trx_mysql_thread_id       AS blocking_thread,
    b.trx_query                 AS blocking_query
FROM information_schema.innodb_lock_waits w
JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_trx_id
JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_trx_id;

-- MySQL 8.0+ 用 performance_schema
SELECT * FROM performance_schema.data_lock_waits;
```

### 死锁分析
```sql
-- 查看最近一次死锁信息
SHOW ENGINE INNODB STATUS\G
-- 找 LATEST DETECTED DEADLOCK 部分

-- 死锁常见原因：
-- 1. 两个事务以相反顺序锁定同一批行
-- 2. 解决：统一加锁顺序，或缩短事务
```
