-- ============================================================
-- Phase 4A W3: 多租户隔离 — 回滚脚本（独立可执行文件）
-- ============================================================
-- 注意：
-- - MySQL 8.0.12+：ALGORITHM=INSTANT 零停机回滚
-- - MySQL 5.7：DROP COLUMN 对大表会重建（X-lock），必须使用 gh-ost
-- ============================================================

ALTER TABLE orders DROP COLUMN tenant_id, ALGORITHM=INSTANT, LOCK=NONE;
ALTER TABLE products DROP COLUMN tenant_id, ALGORITHM=INSTANT, LOCK=NONE;
ALTER TABLE users DROP COLUMN tenant_id, ALGORITHM=INSTANT, LOCK=NONE;
ALTER TABLE order_items DROP COLUMN tenant_id, ALGORITHM=INSTANT, LOCK=NONE;
ALTER TABLE order_status_logs DROP COLUMN tenant_id, ALGORITHM=INSTANT, LOCK=NONE;
ALTER TABLE carts DROP COLUMN tenant_id, ALGORITHM=INSTANT, LOCK=NONE;

-- 注意：索引会在 DROP COLUMN 时自动删除
