/**
 * Orders List API — Edge Function
 *
 * GET /api/orders/list
 * 查询 D1 用户订单列表（tenant 作用域），支持分页
 *
 * Phase 4A P0-4 实现
 */

import { verifyJWT } from '../../sharing/jwt-helper.js';
import { getTenant } from '../../sharing/kv-keys.js';
import { ok, badRequest, unauthorized, internalError } from '../../sharing/response.js';

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

    const page = Math.max(1, parseInt(url.searchParams.get('page') || '1'));
    const limit = Math.min(100, Math.max(1, parseInt(url.searchParams.get('limit') || '20')));
    const status = url.searchParams.get('status') || null;

    if (!env.DB) {
      return internalError('数据库不可用');
    }

    // 构建查询 — tenant 作用域
    let query = `
      SELECT o.id, o.order_no, o.total_amount, o.status, o.currency,
             o.payment_method, o.shipping_address, o.created_at, o.updated_at
      FROM orders o
      WHERE o.tenant_id = ? AND o.user_id = ?
    `;
    let countQuery = 'SELECT COUNT(*) as total FROM orders WHERE tenant_id = ? AND user_id = ?';
    const queryParams = [tenant, userId];
    const countParams = [tenant, userId];

    if (status) {
      query += ' AND o.status = ?';
      countQuery += ' AND status = ?';
      queryParams.push(status);
      countParams.push(status);
    }

    query += ' ORDER BY o.created_at DESC LIMIT ? OFFSET ?';
    const offset = (page - 1) * limit;
    queryParams.push(limit, offset);

    const [orders, countResult] = await Promise.all([
      env.DB.prepare(query).bind(...queryParams).all(),
      env.DB.prepare(countQuery).bind(...countParams).first(),
    ]);

    const total = countResult?.total || 0;

    return ok({
      orders: orders.results || [],
      total,
      page,
      limit,
    });
  } catch (err) {
    console.error('[Orders List] Error:', err.message, err.stack);
    return internalError('获取订单列表失败');
  }
}
