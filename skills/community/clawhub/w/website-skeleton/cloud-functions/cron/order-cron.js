/**
 * 订单定时任务 — Cron Job（Phase 4A W1 迁移版）
 *
 * EdgeOne Pages Cron 触发器配置：每 5 分钟执行一次
 * 定时任务：
 * 1. PENDING 超时 30 分钟 → CANCELLED
 * 2. SHIPPED 超过 7 天无售后 → COMPLETED
 *
 * Phase 4A W1 变更：
 * - 从 mysql2/promise Pool 迁移到 db.js (D1) 接口
 * - 所有 SQL 增加 {tenant} 占位符
 * - 事务改用 withTransaction()
 */

import { withTransaction } from '../utils/db.js';

// ===================== 工具函数 =====================

function writeLog(env, orderId, from, to, tenant) {
  // 操作者为 null 表示系统操作（系统操作使用 'default' 租户）
  withTransaction(env, tenant, (ctx) => {
    ctx.execute(
      `INSERT INTO order_status_logs (tenant_id, order_id, from_status, to_status, operator, reason)
       VALUES ({tenant}, ?, ?, NULL, ?, ?)`,
      [orderId, from, to, 'System: auto-cron', tenant]
    );
  });
}

// ===================== 定时任务主入口 =====================

export async function scheduled(event, env) {
  console.log('[OrderCron] Starting scheduled job at', new Date().toISOString());

  // 系统 cron 使用 'default' 作为默认操作租户
  // 实际生产环境中，需要遍历所有活跃租户
  const tenants = ['default'];
  let totalCancelled = 0;
  let totalCompleted = 0;

  try {
    for (const tenant of tenants) {
      // === 任务 1：PENDING 超时 30 分钟 → CANCELLED ===
      const pendingOrders = env.DB.prepare(`
        SELECT id, user_id FROM orders
        WHERE tenant_id = ? AND status = 'PENDING'
          AND created_at < DATE_SUB(NOW(), INTERVAL 30 MINUTE)
      `).bind(tenant).all();

      if (pendingOrders.length > 0) {
        console.log(`[OrderCron][${tenant}] Found ${pendingOrders.length} expired PENDING orders`);

        for (const order of pendingOrders) {
          try {
            withTransaction(env, tenant, (ctx) => {
              const o = ctx.queryOne(
                'SELECT id, status, version FROM orders WHERE tenant_id = {tenant} AND id = ? FOR UPDATE',
                [order.id]
              );
              if (!o || o.status !== 'PENDING') return; // 已被其他进程处理

              // 回补库存
              const items = ctx.query(
                'SELECT oi.product_id, oi.qty, p.version FROM order_items oi JOIN products p ON p.id = oi.product_id WHERE oi.tenant_id = {tenant} AND oi.order_id = ?',
                [order.id]
              );
              for (const item of items) {
                ctx.execute(
                  'UPDATE products SET stock = stock + ?, version = version + 1 WHERE tenant_id = {tenant} AND id = ? AND version = ?',
                  [item.qty, item.product_id, item.version]
                );
              }

              // 更新状态
              ctx.execute(
                'UPDATE orders SET status = ?, version = version + 1 WHERE tenant_id = {tenant} AND id = ? AND version = ?',
                ['CANCELLED', order.id, o.version]
              );

              // 写日志
              ctx.execute(
                `INSERT INTO order_status_logs (tenant_id, order_id, from_status, to_status, operator, reason)
                 VALUES ({tenant}, ?, ?, NULL, ?, ?)`,
                [order.id, 'PENDING', 'CANCELLED', 'System: auto-cron', tenant]
              );
            });
            totalCancelled++;
            console.log(`[OrderCron] Order ${order.id} auto-cancelled`);
          } catch (err) {
            console.error(`[OrderCron] Failed to cancel order ${order.id}:`, err.message);
          }
        }
      }

      // === 任务 2：SHIPPED 超时 7 天 → COMPLETED ===
      const shippedOrders = env.DB.prepare(`
        SELECT id, user_id FROM orders
        WHERE tenant_id = ? AND status = 'SHIPPED'
          AND paid_at < DATE_SUB(NOW(), INTERVAL 7 DAY)
      `).bind(tenant).all();

      if (shippedOrders.length > 0) {
        console.log(`[OrderCron][${tenant}] Found ${shippedOrders.length} orders to auto-complete`);

        for (const order of shippedOrders) {
          try {
            withTransaction(env, tenant, (ctx) => {
              const o = ctx.queryOne(
                'SELECT id, status, version FROM orders WHERE tenant_id = {tenant} AND id = ? FOR UPDATE',
                [order.id]
              );
              if (!o || o.status !== 'SHIPPED') return;

              ctx.execute(
                'UPDATE orders SET status = ?, version = version + 1 WHERE tenant_id = {tenant} AND id = ? AND version = ?',
                ['COMPLETED', order.id, o.version]
              );

              ctx.execute(
                `INSERT INTO order_status_logs (tenant_id, order_id, from_status, to_status, operator, reason)
                 VALUES ({tenant}, ?, ?, NULL, ?, ?)`,
                [order.id, 'SHIPPED', 'COMPLETED', 'System: auto-cron', tenant]
              );
            });
            totalCompleted++;
            console.log(`[OrderCron] Order ${order.id} auto-completed`);
          } catch (err) {
            console.error(`[OrderCron] Failed to complete order ${order.id}:`, err.message);
          }
        }
      }
    }

    console.log(`[OrderCron] Job completed: ${totalCancelled} cancelled, ${totalCompleted} completed`);
  } catch (err) {
    console.error('[OrderCron] Job failed:', err);
    throw err;
  }
}
