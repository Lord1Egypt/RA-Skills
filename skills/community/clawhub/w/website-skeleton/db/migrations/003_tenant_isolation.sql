-- ============================================================
-- Phase 4A W3: 多租户隔离 — 数据库迁移
-- ============================================================
-- 迁移前必须执行 SQL 查询审计，为复合查询重建索引
-- 复合查询模式：
--   WHERE tenant_id = ? AND user_id = ?  → idx_orders_tenant_user(tenant_id, user_id)
--   WHERE tenant_id = ? AND status = ?   → idx_orders_tenant_status(tenant_id, status)
--   WHERE tenant_id = ? AND created_at   → idx_orders_tenant_created(tenant_id, created_at)
--
-- 最低 MySQL 版本：8.0.12+（支持 ALGORITHM=INSTANT 零停机 DDL）
-- MySQL 5.7 用户：必须使用 gh-ost 或 pt-online-schema-change
-- ============================================================

-- ---------------------------
-- 1. orders 表
-- ---------------------------
ALTER TABLE orders
  ADD COLUMN tenant_id VARCHAR(64) NOT NULL DEFAULT 'default'
  AFTER id,
  ALGORITHM=INSTANT, LOCK=NONE;

CREATE INDEX idx_orders_tenant ON orders (tenant_id);
CREATE INDEX idx_orders_tenant_user ON orders (tenant_id, user_id);
CREATE INDEX idx_orders_tenant_status ON orders (tenant_id, status);

-- ---------------------------
-- 2. products 表
-- ---------------------------
ALTER TABLE products
  ADD COLUMN tenant_id VARCHAR(64) NOT NULL DEFAULT 'default'
  AFTER id,
  ALGORITHM=INSTANT, LOCK=NONE;

CREATE INDEX idx_products_tenant ON products (tenant_id);
CREATE INDEX idx_products_tenant_status ON products (tenant_id, status);

-- ---------------------------
-- 3. users 表
-- ---------------------------
ALTER TABLE users
  ADD COLUMN tenant_id VARCHAR(64) NOT NULL DEFAULT 'default'
  AFTER id,
  ALGORITHM=INSTANT, LOCK=NONE;

CREATE INDEX idx_users_tenant ON users (tenant_id);
-- 用户登录查询路径：WHERE tenant_id = ? AND email = ?
CREATE INDEX idx_users_tenant_email ON users (tenant_id, email);

-- ---------------------------
-- 4. order_items 表
-- ---------------------------
ALTER TABLE order_items
  ADD COLUMN tenant_id VARCHAR(64) NOT NULL DEFAULT 'default'
  AFTER id,
  ALGORITHM=INSTANT, LOCK=NONE;

CREATE INDEX idx_order_items_tenant ON order_items (tenant_id);

-- ---------------------------
-- 5. order_status_logs 表
-- ---------------------------
ALTER TABLE order_status_logs
  ADD COLUMN tenant_id VARCHAR(64) NOT NULL DEFAULT 'default'
  AFTER id,
  ALGORITHM=INSTANT, LOCK=NONE;

CREATE INDEX idx_order_status_logs_tenant ON order_status_logs (tenant_id);

-- ---------------------------
-- 6. carts 表
-- ---------------------------
ALTER TABLE carts
  ADD COLUMN tenant_id VARCHAR(64) NOT NULL DEFAULT 'default'
  AFTER id,
  ALGORITHM=INSTANT, LOCK=NONE;

CREATE INDEX idx_carts_tenant ON carts (tenant_id);
CREATE INDEX idx_carts_tenant_user ON carts (tenant_id, user_id);

-- ============================================================
-- 迁移后数据一致性校验（手动执行）
-- ============================================================
-- SELECT COUNT(*) AS total_rows,
--        COUNT(DISTINCT tenant_id) AS tenant_count,
--        SUM(CASE WHEN tenant_id = 'default' THEN 1 ELSE 0 END) AS default_tenant_rows
-- FROM orders;
--
-- -- 抽查非 default 租户的数据
-- SELECT * FROM orders WHERE tenant_id != 'default' LIMIT 100;
