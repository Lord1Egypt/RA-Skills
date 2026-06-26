# CLI 实操速查

数据库命令行工具的常用操作速查，适合直接上手。

---

## SQLite

SQLite 内置于 Python，零配置，适合本地开发和原型验证。

### 连接与基本操作
```bash
# 打开/创建数据库
sqlite3 mydb.sqlite

# 单行查询（不进入交互模式）
sqlite3 mydb.sqlite "SELECT COUNT(*) FROM users;"

# 交互模式开启表头和列对齐
sqlite3 -header -column mydb.sqlite
```

### 数据导入导出
```bash
# 导入 CSV
sqlite3 mydb.sqlite ".mode csv" ".import data.csv mytable" "SELECT COUNT(*) FROM mytable;"

# 导出为 CSV
sqlite3 -header -csv mydb.sqlite "SELECT * FROM orders;" > orders.csv

# 导出整个数据库为 SQL
sqlite3 mydb.sqlite .dump > backup.sql

# 从 SQL 文件恢复
sqlite3 mydb.sqlite < backup.sql
```

### 常用 Meta 命令
```
.tables              -- 列出所有表
.schema users        -- 查看表结构
.indexes users       -- 查看索引
.mode column         -- 列对齐显示
.headers on          -- 显示列名
.quit                -- 退出
```

### 关键 PRAGMA
```sql
PRAGMA journal_mode = WAL;        -- 提升并发写入性能
PRAGMA synchronous = NORMAL;      -- 平衡安全与性能
PRAGMA foreign_keys = ON;         -- 启用外键约束（默认关闭！）
PRAGMA cache_size = -64000;       -- 设置缓存 64MB
PRAGMA temp_store = MEMORY;       -- 临时表放内存
PRAGMA integrity_check;           -- 数据库完整性检查
```

---

## PostgreSQL

### 连接
```bash
# 基本连接
psql -h localhost -U myuser -d mydb

# 连接字符串
psql "postgresql://user:pass@localhost:5432/mydb?sslmode=require"

# 单行查询
psql -h localhost -U myuser -d mydb -c "SELECT NOW();"

# 执行 SQL 文件
psql -h localhost -U myuser -d mydb -f migration.sql

# 列出所有数据库
psql -l
```

### 数据导入导出
```bash
# 导出整个数据库
pg_dump -h localhost -U myuser mydb > backup.sql

# 导出为自定义格式（推荐，支持并行恢复）
pg_dump -h localhost -U myuser -Fc mydb > backup.dump

# 恢复
psql -h localhost -U myuser mydb < backup.sql
pg_restore -h localhost -U myuser -d mydb backup.dump

# 导出单表为 CSV
psql -h localhost -U myuser -d mydb -c "\COPY orders TO 'orders.csv' CSV HEADER"

# 导入 CSV
psql -h localhost -U myuser -d mydb -c "\COPY orders FROM 'orders.csv' CSV HEADER"
```

### 常用 Meta 命令
```
\l                   -- 列出数据库
\c mydb              -- 切换数据库
\dt                  -- 列出表
\d users             -- 查看表结构（含索引）
\di                  -- 列出索引
\df                  -- 列出函数
\timing              -- 显示查询耗时
\x                   -- 切换扩展显示模式（宽表友好）
\e                   -- 用编辑器编辑查询
\q                   -- 退出
```

### 性能诊断
```sql
-- 查看慢查询（需开启 pg_stat_statements）
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- 查看表大小
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- 查看锁等待
SELECT pid, wait_event_type, wait_event, query
FROM pg_stat_activity
WHERE wait_event IS NOT NULL;

-- 终止慢查询
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE query_start < NOW() - INTERVAL '5 minutes'
  AND state = 'active';
```

---

## MySQL / MariaDB

### 连接
```bash
# 基本连接
mysql -h localhost -u myuser -p mydb

# 单行查询
mysql -h localhost -u myuser -p mydb -e "SELECT NOW();"

# 执行 SQL 文件
mysql -h localhost -u myuser -p mydb < migration.sql

# 不显示密码警告（脚本用）
mysql --defaults-extra-file=~/.my.cnf mydb -e "SELECT 1;"
```

### ~/.my.cnf 配置（避免明文密码）
```ini
[client]
host=localhost
user=myuser
password=mypassword
```

### 数据导入导出
```bash
# 导出整个数据库
mysqldump -h localhost -u myuser -p mydb > backup.sql

# 导出单表
mysqldump -h localhost -u myuser -p mydb orders > orders.sql

# 恢复
mysql -h localhost -u myuser -p mydb < backup.sql

# 导出为 CSV（需 FILE 权限）
mysql -h localhost -u myuser -p mydb -e \
  "SELECT * FROM orders INTO OUTFILE '/tmp/orders.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n';"
```

### 常用 Meta 命令
```sql
SHOW DATABASES;
USE mydb;
SHOW TABLES;
DESCRIBE users;           -- 查看表结构
SHOW CREATE TABLE users;  -- 查看建表语句（含索引）
SHOW INDEX FROM users;    -- 查看索引详情
SHOW PROCESSLIST;         -- 查看当前连接和查询
SHOW VARIABLES LIKE 'innodb%';  -- 查看 InnoDB 配置
```

### 性能诊断
```sql
-- 查看慢查询日志状态
SHOW VARIABLES LIKE 'slow_query%';
SHOW VARIABLES LIKE 'long_query_time';

-- 开启慢查询（临时）
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- 超过 1 秒记录

-- 查看 InnoDB 状态（锁、事务）
SHOW ENGINE INNODB STATUS\G

-- 查看当前锁等待
SELECT * FROM information_schema.INNODB_LOCK_WAITS;

-- 终止慢查询
KILL QUERY <pid>;
```

---

## 通用技巧

### EXPLAIN 快速解读
```sql
-- MySQL
EXPLAIN SELECT ...;
EXPLAIN FORMAT=JSON SELECT ...;   -- 更详细

-- PostgreSQL
EXPLAIN SELECT ...;
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;  -- 实际执行 + 缓存命中

-- 关注指标
-- type: ALL（全表扫描，危险）→ ref/eq_ref/const（索引，好）
-- rows: 预估扫描行数，越小越好
-- Extra: Using filesort / Using temporary（需优化）
```

### 快速生成测试数据
```sql
-- MySQL：生成 10000 行测试数据
INSERT INTO test_table (name, value, created_at)
SELECT
  CONCAT('user_', seq),
  FLOOR(RAND() * 1000),
  DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 365) DAY)
FROM (
  SELECT @row := @row + 1 AS seq
  FROM information_schema.columns, (SELECT @row := 0) r
  LIMIT 10000
) t;

-- PostgreSQL：generate_series
INSERT INTO test_table (name, value, created_at)
SELECT
  'user_' || i,
  (RANDOM() * 1000)::INT,
  NOW() - (RANDOM() * 365 || ' days')::INTERVAL
FROM generate_series(1, 10000) AS i;

-- SQLite
WITH RECURSIVE cnt(x) AS (
  SELECT 1 UNION ALL SELECT x+1 FROM cnt WHERE x < 10000
)
INSERT INTO test_table (name, value)
SELECT 'user_' || x, ABS(RANDOM() % 1000) FROM cnt;
```
