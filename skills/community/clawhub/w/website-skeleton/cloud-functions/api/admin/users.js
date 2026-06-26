/**
 * 用户管理 API — 管理员查询用户列表
 *
 * GET /api/admin/users?page=&limit=
 *
 * - 需要 superadmin 角色
 * - 不返回 password_hash 字段
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

  // === 认证 + 角色校验（仅 superadmin） ===
  const user = await requireRole(request, env, ['superadmin']);
  if (user instanceof Response) return user;
  const { tenant } = user;

  try {
    const url = new URL(request.url);
    const { page, limit, offset } = parsePagination(url);

    // 查询总数
    const [{ total }] = query(
      env,
      'SELECT COUNT(*) as total FROM users WHERE tenant_id = {tenant}',
      [],
      tenant
    );

    // 查询列表（不返回 password_hash）
    const items = query(
      env,
      `SELECT id, email, name, role, tenant_id, created_at, updated_at
       FROM users WHERE tenant_id = {tenant}
       ORDER BY id DESC
       LIMIT ? OFFSET ?`,
      [limit, offset],
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
    console.error('[Admin Users] Error:', err);
    return internalError('查询用户列表失败');
  }
}
