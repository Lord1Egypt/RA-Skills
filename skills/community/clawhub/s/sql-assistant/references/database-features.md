# SQL 数据库特性对比与最佳实践

## PostgreSQL vs MySQL vs SQLite 特性对比

| 特性 | PostgreSQL | MySQL 8+ | SQLite |
|------|-----------|----------|--------|
| 窗口函数 | ✅ 完整支持 | ✅ 完整支持 | ✅ 3.25+ |
| CTE (WITH) | ✅ 递归CTE | ✅ | ✅ |
| JSON 支持 | ✅ jsonb（高效） | ✅ | 有限 |
| 全文搜索 | ✅ 内置 | ✅ | 有限 |
| 并发控制 | MVCC（优秀） | MVCC | WAL模式 |
| 最大数据库大小 | 无限制 | 无限制 | 281TB |
| 适用场景 | 复杂查询/分析 | Web应用/OLTP | 嵌入式/移动端 |

---

## PostgreSQL 专属特性

### JSONB 操作
```sql
-- 创建带 JSONB 列的表
CREATE TABLE products (id SERIAL, attrs JSONB);

-- 查询 JSONB 字段
SELECT * FROM products WHERE attrs->>'color' = 'red';
SELECT * FROM products WHERE attrs @> '{"color": "red"}';

-- JSONB 聚合
SELECT attrs->>'category', COUNT(*) FROM products GROUP BY attrs->>'category';

-- 创建 JSONB 索引
CREATE INDEX idx_products_attrs ON products USING GIN(attrs);
```

### 数组类型
```sql
-- 数组列
CREATE TABLE users (tags TEXT[]);
INSERT INTO users VALUES (ARRAY['dev', 'python', 'sql']);

-- 数组查询（包含）
SELECT * FROM users WHERE 'python' = ANY(tags);
SELECT * FROM users WHERE tags @> ARRAY['dev', 'python'];

-- 数组展开
SELECT UNNEST(tags) AS tag FROM users;
```

### 全文搜索
```sql
-- 创建全文索引
CREATE INDEX idx_articles_fts ON articles USING GIN(to_tsvector('english', content));

-- 全文搜索查询
SELECT * FROM articles
WHERE to_tsvector('english', content) @@ plainto_tsquery('english', 'database optimization');
```

---

## MySQL 专属优化

### InnoDB 配置优化
```sql
-- 查看缓冲池大小（建议设为物理内存的70-80%）
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- 查看慢查询
SHOW VARIABLES LIKE 'slow_query_log%';
SHOW VARIABLES LIKE 'long_query_time';
```

### MySQL 特有 JSON 函数
```sql
-- 提取 JSON 值
SELECT JSON_EXTRACT(config, '$.theme') FROM settings;
SELECT config->>'$.theme' FROM settings;  -- 简写

-- JSON 数组操作
SELECT JSON_ARRAYAGG(name) FROM users WHERE active = 1;
SELECT JSON_OBJECTAGG(id, name) FROM users;
```

### 分区表（大表优化）
```sql
-- 按日期范围分区
CREATE TABLE orders (
  id BIGINT,
  created_at DATE,
  ...
) PARTITION BY RANGE (YEAR(created_at)) (
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p2025 VALUES LESS THAN (2026),
  PARTITION p2026 VALUES LESS THAN (2027)
);
```

---

## 事务与并发控制

### 事务隔离级别
| 级别 | 脏读 | 不可重复读 | 幻读 | 适用场景 |
|------|------|-----------|------|----------|
| READ UNCOMMITTED | ✅ | ✅ | ✅ | 极少使用 |
| READ COMMITTED | ❌ | ✅ | ✅ | 多数OLTP |
| REPEATABLE READ | ❌ | ❌ | ✅(MySQL) | MySQL默认 |
| SERIALIZABLE | ❌ | ❌ | ❌ | 高一致性需求 |

PostgreSQL 默认：READ COMMITTED
MySQL InnoDB 默认：REPEATABLE READ

### 乐观锁 vs 悲观锁
```sql
-- 悲观锁（SELECT FOR UPDATE）
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;

-- 乐观锁（版本号）
UPDATE accounts
SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = :expected_version;
-- 检查 affected rows = 1，否则重试
```

---

## 数据库设计规范

### 表设计规范
1. 主键：推荐使用 BIGINT SERIAL/AUTO_INCREMENT（非 UUID，避免索引碎片）
2. 时间戳：使用 `created_at TIMESTAMPTZ DEFAULT NOW()` 和 `updated_at`
3. 软删除：添加 `deleted_at TIMESTAMPTZ NULL`（而非物理删除）
4. 字符集：UTF8MB4（MySQL），UTF8（PostgreSQL）

### 命名规范
- 表名：蛇形命名，复数（`user_orders`）
- 列名：蛇形命名（`created_at`）
- 索引：`idx_{表名}_{列名}` 或 `idx_{表名}_{列名}_{列名}`
- 外键：`fk_{子表}_{父表}`

### 必备字段模板
```sql
CREATE TABLE example (
  id          BIGSERIAL PRIMARY KEY,
  -- 业务字段...
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at  TIMESTAMPTZ NULL  -- 软删除
);

-- 自动更新 updated_at（PostgreSQL）
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_updated_at
  BEFORE UPDATE ON example
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```
