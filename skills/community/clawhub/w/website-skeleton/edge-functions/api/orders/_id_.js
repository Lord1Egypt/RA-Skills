/**
 * Order Detail API — Edge Function
 *
 * GET /api/orders/:id
 * 单个订单详情（tenant 作用域）
 *
 * Phase 4A P0-4 实现
 */

import { verifyJWT } from '../../sharing/jwt-helper.js';
import { getTenant } from '../../sharing/kv-keys.js';
import { ok, unauthorized, notFound, internalError } from '../../sharing/response.js';

async function authenticate(request, env) {
  const auth = request.headers.get('Authorization');
  if (!auth?.startsWith('Bearer ')) return null;
  const token = auth.slice(7);
  try {
    return await verifyJWT(token, env);
  } catch {
    return null;
  }
}

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== 'GET') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    const payload = await authenticate(request, env);
    if (!payload) {
      return unauthorized('请先登录');
    }

    const tenant = getTenant(payload);
    const userId = String(payload.sub);

    const url = new URL(request.url);
    const pathParts = url.pathname.split('/').filter(Boolean);
    // pathParts = ['api', 'orders', '{id}']
    const orderId = pathParts[2];

    if (!orderId) {
      return notFound('缺少订单 ID');
    }

    if (!env.DB) {
      return internalError('数据库不可用');
    }

    // 查询订单 + 订单项（tenant 作用域）
    const order = await env.DB.prepare(
      `SELECT o.id, o.order_no, o.total_amount, o.status, o.currency,
              o.payment_method, o.shipping_address, o.billing_address,
              o.paid_at, o.created_at, o.updated_at
       FROM orders o
       WHERE o.id = ? AND o.tenant_id = ? AND o.user_id = ?`
    ).bind(orderId, tenant, userId).first();

    if (!order) {
      return notFound('订单不存在');
    }

    // 查询订单项
    const items = await env.DB.prepare(
      'SELECT id, product_id, product_name, quantity, unit_price, subtotal FROM order_items WHERE order_id = ? AND tenant_id = ?'
    ).bind(orderId, tenant).all();

    return ok({
      order: {
        ...order,
        items: items.results || [],
      },
    });
  } catch (err) {
    console.error('[Order Detail] Error:', err.message, err.stack);
    return internalError('获取订单详情失败');
  }
}
