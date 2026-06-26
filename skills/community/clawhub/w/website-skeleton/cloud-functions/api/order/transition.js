/**
 * 订单状态变更 API — 统一入口（Phase 4A W1 迁移版）
 *
 * POST /api/order/transition
 * Body: { orderId, toStatus, express_company?, express_no?, reason? }
 *
 * Phase 4A W1 变更：
 * - 从 mysql2/promise Pool 迁移到 db.js (D1) 接口
 * - 所有 SQL 增加 {tenant} 占位符
 * - 事务改用 withTransaction()
 */

import { canTransition, StateMachineError, OrderStatus } from '../../utils/order-state-machine.js';
import { query, queryOne, execute, withTransaction } from '../../utils/db.js';
import { withTenant } from '../../middleware/tenant-context.js';

// ===================== 库存回补 =====================

async function releaseStock(env, orderId, tenant) {
  const items = query(env, `
    SELECT oi.product_id, oi.qty, p.version
    FROM order_items oi
    JOIN products p ON p.id = oi.product_id
    WHERE oi.tenant_id = {tenant} AND oi.order_id = ?
  `, [orderId], tenant);

  for (const item of items) {
    const result = execute(env,
      'UPDATE products SET stock = stock + ?, version = version + 1 WHERE tenant_id = {tenant} AND id = ? AND version = ?',
      [item.qty, item.product_id, item.version], tenant
    );
    if (result.affectedRows === 0) {
      console.warn(`[StateMachine] Stock release conflict for product ${item.product_id}`);
    }
  }
}

// ===================== 审计日志写入 =====================

async function writeStatusLog(env, orderId, fromStatus, toStatus, operatorId, reason, tenant) {
  execute(env,
    `INSERT INTO order_status_logs (tenant_id, order_id, from_status, to_status, operator, reason)
     VALUES ({tenant}, ?, ?, ?, ?, ?)`,
    [orderId, fromStatus, toStatus, operatorId, reason || null], tenant
  );
}

// ===================== 主处理函数 =====================

export async function onRequest(request, env) {
  // === 认证 + 租户上下文 ===
  const ctx = await withTenant(request, env);
  if (ctx instanceof Response) return ctx;
  const { tenant, userId, role } = ctx;

  // === 解析请求 ===
  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
      status: 400, headers: { 'Content-Type': 'application/json' }
    });
  }

  const { orderId, toStatus, express_company, express_no, reason } = body;

  if (!orderId || !toStatus) {
    return new Response(JSON.stringify({ error: 'orderId 和 toStatus 为必填项' }), {
      status: 400, headers: { 'Content-Type': 'application/json' }
    });
  }

  // === SHIPPED 状态校验物流信息 ===
  if (toStatus === OrderStatus.SHIPPED) {
    if (!express_company || !express_no) {
      return new Response(JSON.stringify({
        error: '发货需要提供快递公司和运单号'
      }), { status: 400, headers: { 'Content-Type': 'application/json' } });
    }
  }

  try {
    // === 事务：锁定 → 校验 → 更新 → 日志 ===
    return withTransaction(env, tenant, (ctx) => {
      // Step 1: SELECT FOR UPDATE 锁行
      const order = ctx.queryOne(
        'SELECT id, status, user_id, version FROM orders WHERE tenant_id = {tenant} AND id = ? FOR UPDATE',
        [orderId]
      );

      if (!order) {
        return new Response(JSON.stringify({ error: '订单不存在' }), {
          status: 404, headers: { 'Content-Type': 'application/json' }
        });
      }

      const { id, status: fromStatus, user_id: orderUserId, version } = order;

      // Step 2: 状态机 + 权限校验
      try {
        canTransition(fromStatus, toStatus, { role, userId, orderUserId });
      } catch (e) {
        if (e instanceof StateMachineError) {
          return new Response(JSON.stringify({
            error: e.message,
            code: 'STATE_MACHINE_REJECTED'
          }), { status: 403, headers: { 'Content-Type': 'application/json' } });
        }
        throw e;
      }

      // Step 3: 库存回补（取消/退款时）
      if ([OrderStatus.CANCELLED, OrderStatus.REFUNDED].includes(toStatus)) {
        const items = ctx.query(
          'SELECT oi.product_id, oi.qty, p.version FROM order_items oi JOIN products p ON p.id = oi.product_id WHERE oi.tenant_id = {tenant} AND oi.order_id = ?',
          [orderId]
        );
        for (const item of items) {
          const result = ctx.execute(
            'UPDATE products SET stock = stock + ?, version = version + 1 WHERE tenant_id = {tenant} AND id = ? AND version = ?',
            [item.qty, item.product_id, item.version]
          );
          if (result.affectedRows === 0) {
            console.warn(`[StateMachine] Stock release conflict for product ${item.product_id}`);
          }
        }
      }

      // Step 4: 更新状态（含 version 乐观锁）
      const updateFields = ['status = ?', 'version = version + 1'];
      const updateParams = [toStatus];

      if (toStatus === OrderStatus.PAID) {
        updateFields.push('paid_at = NOW()');
      }
      if (toStatus === OrderStatus.SHIPPED) {
        updateFields.push('express_company = ?', 'express_no = ?');
        updateParams.push(express_company, express_no);
      }

      updateParams.push(orderId, version);

      const result = ctx.execute(
        `UPDATE orders SET ${updateFields.join(', ')} WHERE tenant_id = {tenant} AND id = ? AND version = ?`,
        updateParams
      );

      if (result.affectedRows === 0) {
        return new Response(JSON.stringify({
          error: '并发冲突，请重试',
          code: 'CONCURRENT_UPDATE'
        }), { status: 409, headers: { 'Content-Type': 'application/json' } });
      }

      // Step 5: 审计日志
      ctx.execute(
        `INSERT INTO order_status_logs (tenant_id, order_id, from_status, to_status, operator, reason)
         VALUES ({tenant}, ?, ?, ?, ?, ?)`,
        [orderId, fromStatus, toStatus, userId, reason || null]
      );

      return new Response(JSON.stringify({
        ok: true,
        orderId,
        fromStatus,
        toStatus,
        version: version + 1,
        message: `订单已变更为 ${toStatus}`
      }), { status: 200, headers: { 'Content-Type': 'application/json' } });
    });

  } catch (err) {
    console.error('[Order Transition] Error:', err);
    return new Response(JSON.stringify({ error: '服务器错误' }), {
      status: 500, headers: { 'Content-Type': 'application/json' }
    });
  }
}
