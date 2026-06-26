/**
 * 关闭/取消支付订单 API
 *
 * POST /api/pay/close
 * Body: { orderNo }
 *
 * - authenticate
 * - withTransaction:
 *   1. 关闭订单（仅 pending 状态可关闭）
 *   2. 恢复库存
 * - 返回 200
 */

import { withTransaction } from '../../utils/db.js';
import { authenticate } from '../_helpers.js';
import { ok, badRequest, unauthorized, notFound, internalError } from '../../../sharing/response.js';

export async function onRequest(request, env) {
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // === 认证 ===
  const user = await authenticate(request, env);
  if (!user) {
    return unauthorized();
  }
  const { tenant } = user;

  // === 解析请求 ===
  let body;
  try {
    body = await request.json();
  } catch {
    return badRequest('Invalid JSON body');
  }

  const { orderNo } = body;
  if (!orderNo) {
    return badRequest('orderNo 为必填项');
  }

  // === 事务处理 ===
  try {
    return withTransaction(env, tenant, (ctx) => {
      // Step 1: 校验订单存在且为 pending 状态
      const order = ctx.queryOne(
        'SELECT id, status, product_id, qty FROM orders WHERE tenant_id = {tenant} AND order_no = ? FOR UPDATE',
        [orderNo]
      );

      if (!order) {
        return notFound('订单不存在');
      }

      if (order.status !== 'pending') {
        return badRequest(`订单状态为 ${order.status}，仅 pending 状态的订单可关闭`);
      }

      // Step 2: 更新订单状态为 cancelled
      ctx.execute(
        "UPDATE orders SET status = 'cancelled' WHERE tenant_id = {tenant} AND order_no = ? AND status = 'pending'",
        [orderNo]
      );

      // Step 3: 恢复库存
      ctx.execute(
        'UPDATE products SET stock = stock + ? WHERE tenant_id = {tenant} AND id = ?',
        [order.qty, order.product_id]
      );

      return ok({ orderNo, status: 'cancelled', message: '订单已关闭' });
    });
  } catch (err) {
    console.error('[Pay Close] Error:', err);
    return internalError('关闭订单失败');
  }
}
