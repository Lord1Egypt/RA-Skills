/**
 * 订单管理 API — 管理员查询所有订单
 *
 * GET /api/admin/orders?page=&limit=&status=
 *
 * - 需要 admin 角色 (superadmin / tenant_admin)
 * - 支持按状态过滤
 * - 分页返回
 */

import { query } from '../../utils/db.js';
import { requireRole, parsePagination } from '../_helpers.js';
import { ok, internalError } from '../../../sharing/response.js';

export async function onRequest(request, env) {
  if (request.method !== 'GET') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // === 认证 + 角色校验 ===
  const user = await requireRole(request, env, ['superadmin', 'tenant_admin']);
  if (user instanceof Response) return user;
  const { tenant } = user;

  try {
    const url = new URL(request.url);
    const { page, limit, offset } = parsePagination(url);
    const statusFilter = url.searchParams.get('status');

    // 构建查询条件
    let whereClause = 'WHERE o.tenant_id = {tenant}';
    const params = [];

    if (statusFilter) {
      whereClause += ' AND o.status = ?';
      params.push(statusFilter);
    }

    // 查询总数
    const [{ total }] = query(
      env,
      `SELECT COUNT(*) as total FROM orders o ${whereClause}`,
      params,
      tenant
    );

    // 查询列表
    const items = query(
      env,
      `SELECT o.id, o.order_no, o.user_id, o.product_id, o.qty, o.amount, o.status, o.paid_at, o.created_at, o.updated_at
       FROM orders o ${whereClause}
       ORDER BY o.created_at DESC
       LIMIT ? OFFSET ?`,
      [...params, limit, offset],
      tenant
    );

    return ok({
      items,
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit),
    });
  } catch (err) {
    console.error('[Admin Orders] Error:', err);
    return internalError('查询订单列表失败');
  }
}
