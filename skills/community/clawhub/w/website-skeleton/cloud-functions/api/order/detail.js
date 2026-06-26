/**
 * 订单详情 API
 *
 * GET /api/order/detail?orderNo=X
 *
 * - authenticate
 * - 返回订单详情（含订单项）
 */

import { query, queryOne } from '../../utils/db.js';
import { authenticate } from '../_helpers.js';
import { ok, badRequest, unauthorized, notFound, internalError } from '../../../sharing/response.js';

export async function onRequest(request, env) {
  if (request.method !== 'GET') {
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

  // === 解析参数 ===
  const url = new URL(request.url);
  const orderNo = url.searchParams.get('orderNo');

  if (!orderNo) {
    return badRequest('orderNo 为必填参数');
  }

  try {
    // Step 1: 查询订单
    const order = queryOne(
      env,
      'SELECT * FROM orders WHERE tenant_id = {tenant} AND order_no = ?',
      [orderNo],
      tenant
    );

    if (!order) {
      return notFound('订单不存在');
    }

    // 权限校验：只能查看自己的订单（管理员除外）
    if (user.role !== 'superadmin' && user.role !== 'tenant_admin' && String(order.user_id) !== String(userId)) {
      return unauthorized('无权查看该订单');
    }

    // Step 2: 查询订单项（如果有 order_items 表）
    let items = [];
    try {
      items = query(
        env,
        'SELECT oi.*, p.name as product_name FROM order_items oi LEFT JOIN products p ON p.id = oi.product_id WHERE oi.tenant_id = {tenant} AND oi.order_id = ?',
        [order.id],
        tenant
      );
    } catch {
      // order_items 表可能不存在，忽略
      items = [];
    }

    return ok({
      order: {
        id: order.id,
        orderNo: order.order_no,
        userId: order.user_id,
        productId: order.product_id,
        productName: order.product_name || null,
        qty: order.qty,
        amount: order.amount,
        status: order.status,
        paidAt: order.paid_at || null,
        createdAt: order.created_at,
        updatedAt: order.updated_at,
      },
      items,
    });
  } catch (err) {
    console.error('[Order Detail] Error:', err);
    return internalError('查询订单详情失败');
  }
}
