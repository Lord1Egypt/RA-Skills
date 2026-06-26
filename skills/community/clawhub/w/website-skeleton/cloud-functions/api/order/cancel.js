/**
 * 取消订单 API — 仅 pending 状态可取消，恢复库存
 *
 * POST /api/order/cancel
 * Body: { orderNo }
 *
 * - authenticate
 * - withTransaction:
 *   1. SELECT ... FOR UPDATE 锁定订单
 *   2. 校验状态为 pending
 *   3. 更新状态为 cancelled
 *   4. 恢复库存
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
  const { tenant, sub: userId } = user;

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
      // Step 1: SELECT FOR UPDATE 锁定订单
      const order = ctx.queryOne(
        'SELECT id, status, user_id, product_id, qty FROM orders WHERE tenant_id = {tenant} AND order_no = ? FOR UPDATE',
        [orderNo]
      );

      if (!order) {
        return notFound('订单不存在');
      }

      // 权限校验：只能取消自己的订单（管理员除外）
      if (user.role !== 'superadmin' && user.role !== 'tenant_admin' && String(order.user_id) !== String(userId)) {
        return unauthorized('无权取消该订单');
      }

      // Step 2: 校验状态
      if (order.status !== 'pending') {
        return badRequest(`订单状态为 ${order.status}，仅 pending 状态的订单可取消`);
      }

      // Step 3: 更新订单状态
      ctx.execute(
        "UPDATE orders SET status = 'cancelled' WHERE tenant_id = {tenant} AND order_no = ? AND status = 'pending'",
        [orderNo]
      );

      // Step 4: 恢复库存
      ctx.execute(
        'UPDATE products SET stock = stock + ? WHERE tenant_id = {tenant} AND id = ?',
        [order.qty, order.product_id]
      );

      return ok({
        orderNo,
        status: 'cancelled',
        message: '订单已取消',
      });
    });
  } catch (err) {
    console.error('[Order Cancel] Error:', err);
    return internalError('取消订单失败');
  }
}
