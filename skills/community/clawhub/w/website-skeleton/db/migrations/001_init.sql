-- ============================================================
-- Phase 1: 基础建表 — 网站骨架初始表结构
-- ============================================================
-- 迁移说明：
-- 001 → 002（订单审计日志）
-- 001 → 003（多租户：添加 tenant_id 列 + 复合索引）
--
-- 最低 MySQL 版本：8.0.12+（支持 ALGORITHM=INSTANT）
-- 使用 D1 (SQLite) 时自增语法为 AUTOINCREMENT
-- ============================================================

-- ---------------------------
-- 1. 用户表
-- ---------------------------
CREATE TABLE IF NOT EXISTS users (
  id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  email         VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name          VARCHAR(128) DEFAULT '',
  role          ENUM('user','admin','superadmin') DEFAULT 'user',
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_role ON users (role);

-- ---------------------------
-- 2. 商品分类表
-- ---------------------------
CREATE TABLE IF NOT EXISTS product_categories (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(128) NOT NULL,
  description TEXT,
  sort_order  INT UNSIGNED DEFAULT 0,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------
-- 3. 商品表
-- ---------------------------
CREATE TABLE IF NOT EXISTS products (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(255) NOT NULL,
  description TEXT,
  price       DECIMAL(10,2) NOT NULL,      -- 服务端唯一价格来源
  stock       INT UNSIGNED NOT NULL DEFAULT 0,
  category_id INT UNSIGNED,
  image_url   VARCHAR(512) DEFAULT '',
  status      ENUM('active','inactive') DEFAULT 'active',
  version     INT UNSIGNED DEFAULT 1,      -- 乐观锁版本号
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT chk_stock_positive CHECK (stock >= 0),
  FOREIGN KEY (category_id) REFERENCES product_categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_products_category ON products (category_id);
CREATE INDEX idx_products_status ON products (status);
CREATE INDEX idx_products_created ON products (created_at);

-- ---------------------------
-- 4. 订单表
-- ---------------------------
CREATE TABLE IF NOT EXISTS orders (
  id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  order_no      VARCHAR(64) UNIQUE NOT NULL,
  out_trade_no  VARCHAR(128) UNIQUE,
  user_id       BIGINT UNSIGNED NOT NULL,
  product_id    BIGINT UNSIGNED,
  qty           INT UNSIGNED DEFAULT 1,
  amount        DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  total         DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  status        ENUM('pending','paid','shipped','completed','cancelled','refunded') DEFAULT 'pending',
  paid_at       DATETIME,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_orders_order_no ON orders (order_no);
CREATE INDEX idx_orders_user ON orders (user_id);
CREATE INDEX idx_orders_status ON orders (status);
CREATE INDEX idx_orders_created ON orders (created_at);
CREATE INDEX idx_orders_paid_at ON orders (paid_at);

-- ---------------------------
-- 5. 订单项表（快照价格，历史追溯）
-- ---------------------------
CREATE TABLE IF NOT EXISTS order_items (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  order_id    BIGINT UNSIGNED NOT NULL,
  product_id  BIGINT UNSIGNED NOT NULL,
  product_name VARCHAR(255) DEFAULT '',
  qty         INT UNSIGNED NOT NULL DEFAULT 1,
  price       DECIMAL(10,2) NOT NULL,      -- 下单时快照价格
  subtotal    DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_order_items_order ON order_items (order_id);
CREATE INDEX idx_order_items_product ON order_items (product_id);

-- ---------------------------
-- 6. 管理操作审计日志
-- ---------------------------
CREATE TABLE IF NOT EXISTS admin_logs (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  admin_id    BIGINT UNSIGNED NOT NULL,
  action      VARCHAR(64) NOT NULL,         -- 如 'product.create', 'order.cancel'
  target_type VARCHAR(64) DEFAULT '',       -- 操作对象类型
  target_id   VARCHAR(128) DEFAULT '',      -- 操作对象 ID
  detail      JSON,                         -- 操作详情
  ip_address  VARCHAR(45) DEFAULT '',
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_admin_logs_admin ON admin_logs (admin_id);
CREATE INDEX idx_admin_logs_action ON admin_logs (action);
CREATE INDEX idx_admin_logs_created ON admin_logs (created_at);
