/**
 * 支付订单查询 API
 *
 * GET /api/pay/query?orderNo=X
 *
 * - authenticate
 * - query D1: SELECT * FROM orders WHERE order_no = {tenant} AND order_no = ?
 * - tenant 校验
 * - 返回 { orderNo, status, amount, paidAt, createdAt }
 */

import { queryOne } from '../../utils/db.js';
import { authenticate } from '../_helpers.js';
import { ok, unauthorized, notFound, internalError } from '../../../sharing/response.js';

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
  const { tenant } = user;

  // === 解析参数 ===
  const url = new URL(request.url);
  const orderNo = url.searchParams.get('orderNo');

  if (!orderNo) {
    return new Response(
      JSON.stringify({ error: 'orderNo 为必填参数' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // === 查询订单 ===
  try {
    const order = queryOne(
      env,
      'SELECT * FROM orders WHERE tenant_id = {tenant} AND order_no = ?',
      [orderNo],
      tenant
    );

    if (!order) {
      return notFound('订单不存在');
    }

    return ok({
      orderNo: order.order_no,
      status: order.status,
      amount: order.amount,
      paidAt: order.paid_at || null,
      createdAt: order.created_at || null,
    });
  } catch (err) {
    console.error('[Pay Query] Error:', err);
    return internalError('查询订单失败');
  }
}
