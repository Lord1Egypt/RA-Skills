/**
 * 运营统计 API — 管理员查看全局统计数据
 *
 * GET /api/admin/stats
 *
 * - 需要 admin 角色 (superadmin / tenant_admin)
 * - 返回: { totalOrders, revenue, activeUsers, productsCount, ordersTrend }
 */

import { query } from '../../utils/db.js';
import { requireRole } from '../_helpers.js';
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
    // 并行查询各个统计指标
    const [
      [{ totalOrders }],
      [{ revenue }],
      [{ activeUsers }],
      [{ productsCount }],
      ordersTrend,
    ] = await Promise.all([
      // 总订单数
      query(
        env,
        "SELECT COUNT(*) as totalOrders FROM orders WHERE tenant_id = {tenant} AND status != 'cancelled'",
        [],
        tenant
      ),
      // 总收入（仅已支付订单）
      query(
        env,
        "SELECT COALESCE(SUM(amount), 0) as revenue FROM orders WHERE tenant_id = {tenant} AND status = 'paid'",
        [],
        tenant
      ),
      // 活跃用户数
      query(
        env,
        'SELECT COUNT(DISTINCT user_id) as activeUsers FROM orders WHERE tenant_id = {tenant}',
        [],
        tenant
      ),
      // 商品总数
      query(
        env,
        "SELECT COUNT(*) as productsCount FROM products WHERE tenant_id = {tenant} AND status = 'active'",
        [],
        tenant
      ),
      // 近 7 天订单趋势
      query(
        env,
        `SELECT DATE(created_at) as date,
                COUNT(*) as count,
                COALESCE(SUM(amount), 0) as revenue
         FROM orders
         WHERE tenant_id = {tenant}
           AND created_at >= DATE('now', '-7 days')
         GROUP BY DATE(created_at)
         ORDER BY date ASC`,
        [],
        tenant
      ),
    ]);

    return ok({
      totalOrders: Number(totalOrders),
      revenue: Number(revenue),
      activeUsers: Number(activeUsers),
      productsCount: Number(productsCount),
      ordersTrend: ordersTrend.map((row) => ({
        date: row.date,
        count: row.count,
        revenue: Number(row.revenue),
      })),
    });
  } catch (err) {
    console.error('[Admin Stats] Error:', err);
    return internalError('获取统计数据失败');
  }
}
