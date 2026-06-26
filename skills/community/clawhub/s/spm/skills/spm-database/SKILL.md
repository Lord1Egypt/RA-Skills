---
name: spm-database
version: 1.0.0
description: 数据库设计规范 — Schema设计/索引/迁移/N+1规避。Agent 常见错误：缺索引、用SELECT *、在循环里查库。SPM Phase 2 自动注入 Context Brief。
---

# SPM Database — 数据库规范

## 自动检测

SPM Phase 2 写 WBS 计划时，检测到数据库/schema/迁移相关任务 → 自动注入本技能的命名/索引/迁移规范。

## 独立使用

不走 SPM 也可以直接说："按 spm-database 规范设计用户表。"

---

## Schema 设计

### 命名

```sql
✅ 表名: 小写_复数     users, user_orders, order_items
✅ 主键: id            (UUID 或 bigserial)
✅ 外键: <表>_id       user_id, order_id
✅ 时间戳: created_at, updated_at (所有表)
✅ 布尔: is_active, has_paid (is_/has_ 前缀)
✅ 索引: idx_<表>_<列>  idx_users_email

❌ 表名: Users, User, tbl_users, t_user
❌ 列名: userId (驼峰), userID (混合), uid (太短)
```

### 字段类型

```sql
-- ✅ 字符串
VARCHAR(255)     -- 短字符串 (名字、邮箱、标题)
TEXT             -- 长文本 (描述、内容、JSON)
UUID             -- ID

-- ✅ 数值
INTEGER / BIGINT -- 计数、ID
DECIMAL(10,2)    -- 金额 (永远不用 FLOAT)

-- ✅ 时间
TIMESTAMPTZ      -- 时间戳 (永远不用 TIMESTAMP WITHOUT TZ)

-- ✅ 布尔
BOOLEAN         -- 是/否状态

-- ❌ 
FLOAT / DOUBLE  -- 金额 (精度丢失)
TIMESTAMP       -- 缺时区
ENUM            -- 用 VARCHAR + CHECK 约束替代
```

---

## 索引

```sql
-- ✅ 必建索引:
CREATE INDEX idx_users_email ON users(email);       -- WHERE 条件列
CREATE INDEX idx_orders_user_id ON orders(user_id);  -- 外键
CREATE INDEX idx_orders_created_at ON orders(created_at); -- 排序/范围查询列

-- ✅ 联合索引 (左前缀原则):
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- 这个索引覆盖: WHERE user_id = ? AND status = ?
-- 也覆盖:      WHERE user_id = ?  (左前缀)
-- 不覆盖:      WHERE status = ?   (跳过了左列)

-- ❌ 过度索引: 每个列都建
-- ❌ 缺索引: 外键列没索引 → 每次 JOIN 全表扫描
```

**规则：每个外键必须有索引。每个 WHERE/ORDER BY 高频列必须有索引。**

---

## Agent 常见 SQL 反模式

| # | 反模式 | 症状 | 修复 |
|---|--------|------|------|
| 1 | **SELECT \*** | 取回不需要的列，浪费内存和带宽 | 明确列名 |
| 2 | **N+1 查询** | 循环里 `SELECT * FROM items WHERE order_id = ?` | JOIN 或 WHERE id IN (...) |
| 3 | **缺 WHERE 的 UPDATE/DELETE** | 可能清空全表 | 事务 + WHERE + LIMIT |
| 4 | **应用层分页** | `SELECT *` → 在 JS 里 `.slice()` | SQL: `LIMIT 20 OFFSET 40` |
| 5 | **字符串拼接 SQL** | Bobby Tables 攻击 | 参数化查询 `$1, $2` |
| 6 | **无事务的多步写入** | 第一步成功、第二步失败 → 脏数据 | `BEGIN ... COMMIT / ROLLBACK` |
| 7 | **客户端排序** | 取 10000 行 → JS `.sort()` | `ORDER BY created_at DESC LIMIT 20` |

---

## 迁移

```sql
-- ✅ 迁移命名: 序号_动作_表名
-- 001_create_users.sql
-- 002_add_email_index.sql
-- 003_add_orders_table.sql

-- ✅ 每个迁移可回滚 (写在注释里):
-- UP:   CREATE TABLE users (...)
-- DOWN: DROP TABLE users

-- ❌ 手动改数据库 → 迁移脚本和实际 schema 不一致
-- ❌ 一个迁移文件做 5 件事 → 拆开
```

**规则：所有 schema 变更必须通过迁移脚本。禁止手动改库。**

---

## 查询优化

```sql
-- ✅ EXPLAIN 分析慢查询
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;

-- 关注:
-- Seq Scan → 缺索引，改
-- Index Scan → ✅
-- Nested Loop → 小表 OK，大表改 JOIN
```

---

## 安全

```
✅ 所有查询使用参数化 ($1, $2, :name)
✅ 数据库密码通过环境变量
✅ 生产环境限制连接数
✅ 敏感字段加密存储 (bcrypt for passwords)

❌ 拼接 SQL 字符串
❌ 密码明文存储
❌ 数据库端口暴露公网
```
