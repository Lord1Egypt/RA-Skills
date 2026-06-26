# SQL 原理深度

## 目录
1. [事务 & ACID](#事务--acid)
2. [MVCC 多版本并发控制](#mvcc-多版本并发控制)
3. [锁机制](#锁机制)
4. [索引原理（B+树）](#索引原理b树)
5. [查询优化器](#查询优化器)
6. [Join 算法](#join-算法)
7. [WAL & 崩溃恢复](#wal--崩溃恢复)

---

## 事务 & ACID

### 四个特性
```
A - Atomicity（原子性）：事务要么全成功，要么全回滚
C - Consistency（一致性）：事务前后数据满足业务约束
I - Isolation（隔离性）：并发事务互不干扰
D - Durability（持久性）：提交后数据不丢失
```

### 隔离级别（从低到高）

| 级别 | 脏读 | 不可重复读 | 幻读 | 说明 |
|------|------|-----------|------|------|
| READ UNCOMMITTED | ✅ 会 | ✅ 会 | ✅ 会 | 几乎不用 |
| READ COMMITTED | ❌ 不会 | ✅ 会 | ✅ 会 | Oracle/PG 默认 |
| REPEATABLE READ | ❌ 不会 | ❌ 不会 | ⚠️ 部分 | MySQL 默认 |
| SERIALIZABLE | ❌ 不会 | ❌ 不会 | ❌ 不会 | 性能最差 |

**MySQL RR 级别下的幻读**：
- 快照读（普通 SELECT）：MVCC 解决，不会幻读
- 当前读（SELECT FOR UPDATE / UPDATE）：需要间隙锁（Gap Lock）解决

```sql
-- 查看/设置隔离级别
SELECT @@transaction_isolation;
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

---

## MVCC 多版本并发控制

### 核心思想
**读不加锁，写不阻塞读** — 通过保存数据的多个历史版本，让读写操作并发执行。

### InnoDB 实现原理

每行数据有两个隐藏字段：
- `trx_id`：最后修改该行的事务 ID
- `roll_pointer`：指向 undo log 中的上一个版本

```
当前行 [trx_id=100, data='B']
    ↓ roll_pointer
undo log [trx_id=50, data='A']
    ↓ roll_pointer
undo log [trx_id=10, data='初始值']
```

### Read View（快照）
事务开始时创建 Read View，记录：
- `m_ids`：当前活跃（未提交）的事务 ID 列表
- `min_trx_id`：活跃事务中最小的 ID
- `max_trx_id`：下一个将分配的事务 ID

**可见性判断**：
```
读取某行时，检查该行的 trx_id：
1. trx_id < min_trx_id → 该版本在快照前已提交 → 可见 ✅
2. trx_id >= max_trx_id → 该版本在快照后才开始 → 不可见 ❌
3. trx_id 在 m_ids 中 → 该版本是活跃事务，未提交 → 不可见 ❌
4. 其他 → 已提交 → 可见 ✅
如果不可见，沿 roll_pointer 找上一个版本，重复判断
```

**RC vs RR 的区别**：
- RC：每次 SELECT 都创建新的 Read View（所以能读到其他事务新提交的数据）
- RR：事务开始时创建一次 Read View，之后复用（所以同一事务内多次读结果一致）

---

## 锁机制

### InnoDB 锁类型

```
行锁：
  S Lock（共享锁）：读锁，多个事务可同时持有
  X Lock（排他锁）：写锁，独占

表锁：
  IS（意向共享锁）：表示事务想对某行加 S 锁
  IX（意向排他锁）：表示事务想对某行加 X 锁
  （意向锁是自动加的，用于快速判断表级锁冲突）

间隙锁（Gap Lock）：锁定索引记录之间的间隙，防止幻读
  例：锁定 (5, 10) 之间，阻止插入 id=7 的行

临键锁（Next-Key Lock）= 行锁 + 间隙锁
  例：锁定 (5, 10]，包含 id=10 的行和 (5,10) 的间隙
  MySQL RR 级别默认使用临键锁
```

### 加锁规则（MySQL RR）
```sql
-- 等值查询，命中记录 → 行锁
SELECT * FROM t WHERE id = 5 FOR UPDATE;  -- 锁 id=5 这一行

-- 等值查询，未命中 → 间隙锁
SELECT * FROM t WHERE id = 7 FOR UPDATE;  -- 锁 (5, 10) 间隙（假设没有 id=7）

-- 范围查询 → 临键锁
SELECT * FROM t WHERE id > 5 FOR UPDATE;  -- 锁 (5, +∞)

-- 非唯一索引等值查询 → 临键锁 + 间隙锁
SELECT * FROM t WHERE age = 25 FOR UPDATE;  -- 锁 age=25 的行 + 前后间隙
```

### 死锁预防
```sql
-- 原则：所有事务按相同顺序加锁
-- ❌ 死锁场景：
-- 事务A：UPDATE orders WHERE id=1; UPDATE orders WHERE id=2;
-- 事务B：UPDATE orders WHERE id=2; UPDATE orders WHERE id=1;

-- ✅ 解决：统一按 id 升序加锁
-- 事务A：UPDATE orders WHERE id IN (1,2) ORDER BY id;
-- 事务B：UPDATE orders WHERE id IN (1,2) ORDER BY id;

-- 设置死锁超时
SET innodb_lock_wait_timeout = 5;  -- 5秒超时
```

---

## 索引原理（B+树）

### 为什么用 B+树？
```
二叉树：高度太高，磁盘 IO 次数多
哈希表：不支持范围查询
B 树：叶子节点不连接，范围查询需要回溯
B+树：
  - 所有数据在叶子节点
  - 叶子节点用链表连接 → 范围查询只需遍历链表
  - 非叶子节点只存键值 → 单个节点能存更多键 → 树更矮
  - 3-4 层 B+树可以存储千万级数据，只需 3-4 次 IO
```

### 聚簇索引 vs 非聚簇索引
```
聚簇索引（主键索引）：
  叶子节点存储完整行数据
  一张表只有一个聚簇索引
  InnoDB 默认按主键建聚簇索引

非聚簇索引（二级索引）：
  叶子节点存储 [索引列值, 主键值]
  查询时先找到主键，再回表查完整数据（回表）
  覆盖索引可以避免回表
```

### 为什么主键推荐自增整数？
```
UUID 主键的问题：
  UUID 是随机的，新插入的行可能落在 B+树中间
  → 导致页分裂（Page Split）
  → 大量碎片，写性能下降

自增整数的优势：
  新行总是追加到最右边的叶子节点
  → 无页分裂，写性能好
  → 索引紧凑，空间利用率高
```

---

## 查询优化器

### CBO vs RBO
```
RBO（Rule-Based Optimizer）：基于规则，固定套路，已淘汰
CBO（Cost-Based Optimizer）：基于代价估算，现代数据库都用这个

代价 = CPU 代价 + IO 代价
优化器会估算不同执行计划的代价，选最小的
```

### 统计信息的重要性
```sql
-- 优化器依赖统计信息做决策
-- 统计信息过期 → 优化器做出错误决策 → 慢查询

-- MySQL：更新统计信息
ANALYZE TABLE orders;

-- PostgreSQL：更新统计信息
ANALYZE orders;
VACUUM ANALYZE orders;  -- 同时回收死元组

-- 查看统计信息
SHOW INDEX FROM orders;  -- MySQL，看 Cardinality（基数）
SELECT * FROM pg_stats WHERE tablename = 'orders';  -- PostgreSQL
```

### 优化器 Hint（强制指定执行计划）
```sql
-- MySQL：强制使用某个索引
SELECT * FROM orders USE INDEX (idx_user_id) WHERE user_id = 1001;
SELECT * FROM orders FORCE INDEX (idx_user_id) WHERE user_id = 1001;
SELECT * FROM orders IGNORE INDEX (idx_status) WHERE status = 'active';

-- MySQL 8.0+：Optimizer Hints
SELECT /*+ INDEX(orders idx_user_id) */ * FROM orders WHERE user_id = 1001;
SELECT /*+ NO_HASH_JOIN(orders, users) */ * FROM orders JOIN users ...;

-- PostgreSQL：关闭某种扫描方式（调试用）
SET enable_seqscan = OFF;
SET enable_hashjoin = OFF;
```

---

## Join 算法

### Nested Loop Join（嵌套循环）
```
适用：小表驱动大表，被驱动表有索引
复杂度：O(M * log N)（M 是驱动表行数，N 是被驱动表行数）

for each row in 驱动表:
    在被驱动表中用索引查找匹配行

优化：Block Nested Loop（BNL）
  把驱动表的一批行放入 join_buffer
  被驱动表每行只需扫描一次 join_buffer
  减少被驱动表的扫描次数
```

### Hash Join
```
适用：大表等值 JOIN，无索引
复杂度：O(M + N)

Build 阶段：把小表（Build 表）的数据装入哈希表（内存）
Probe 阶段：扫描大表（Probe 表），每行在哈希表中查找匹配

注意：如果 Build 表太大，哈希表溢出到磁盘，性能急剧下降
MySQL 8.0.18+ 支持 Hash Join
```

### Merge Join（归并连接）
```
适用：两个表在 JOIN 列上都已排序（或有索引）
复杂度：O(M + N)（已排序的情况下）

类似归并排序的合并步骤：
  两个指针分别扫描两个有序表
  找到相等的行就输出

PostgreSQL 常用，MySQL 不支持
```

### 实战：选择 Join 策略
```sql
-- 场景：users(100万行) JOIN orders(1000万行)，等值 JOIN

-- 方案 A：确保小表在前（Nested Loop）
SELECT /*+ LEADING(u) USE_NL(o) */ u.name, o.amount
FROM users u JOIN orders o ON u.id = o.user_id
WHERE u.vip_level = 'gold';  -- 先过滤 users，减小驱动表

-- 方案 B：大表 JOIN 大表，用 Hash Join（MySQL 8.0+）
SELECT /*+ HASH_JOIN(u, o) */ u.name, o.amount
FROM users u JOIN orders o ON u.id = o.user_id;

-- 数据倾斜处理（某些 user_id 有大量订单）
-- 方案：广播小表（Spark SQL / Hive）
SELECT /*+ BROADCAST(u) */ u.name, o.amount
FROM orders o JOIN users u ON o.user_id = u.id;
```

---

## WAL & 崩溃恢复

### WAL（Write-Ahead Logging）原理
```
核心思想：先写日志，再写数据
  1. 事务提交时，先把变更写入 redo log（顺序写，极快）
  2. 数据页的修改先在内存（Buffer Pool）中进行
  3. 后台线程异步将脏页刷到磁盘

崩溃恢复：
  重启时，读取 redo log，重放未刷盘的变更
  → 保证已提交事务不丢失（Durability）
```

### InnoDB 日志体系
```
redo log（重做日志）：
  固定大小，循环写入
  保证崩溃恢复（物理日志，记录页的修改）
  innodb_log_file_size 控制大小

undo log（回滚日志）：
  记录数据修改前的值
  用于事务回滚 + MVCC 历史版本

binlog（二进制日志）：
  MySQL Server 层的逻辑日志
  用于主从复制 + 数据恢复
  记录 SQL 语句或行变更

两阶段提交（2PC）：
  保证 redo log 和 binlog 的一致性
  1. Prepare：写 redo log，标记 prepare
  2. Commit：写 binlog，然后 redo log 标记 commit
```
