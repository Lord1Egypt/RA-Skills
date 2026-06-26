/**
 * 用户注册 API — bcrypt 密码哈希
 *
 * POST /api/auth/register
 * Body: { email, password, name }
 *
 * - 验证 email 格式，password >= 8 chars
 * - bcrypt hash password (cost=12)
 * - 处理重复 email → 409
 * - 返回 201 { user: { id, email, name, role, tenant } }
 */

import { execute, queryOne } from '../../utils/db.js';
import { created, badRequest, conflict, internalError } from '../../../sharing/response.js';

/**
 * 简单的邮箱格式验证
 */
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export async function onRequest(request, env) {
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return badRequest('Invalid JSON body');
  }

  const { email, password, name } = body;

  // === 参数校验 ===
  if (!email || !isValidEmail(email)) {
    return badRequest('邮箱格式不正确');
  }
  if (!password || password.length < 8) {
    return badRequest('密码长度至少 8 位');
  }
  if (!name || name.trim().length === 0) {
    return badRequest('姓名不能为空');
  }

  // === 检查邮箱是否已注册 ===
  try {
    const existing = queryOne(
      env,
      'SELECT id FROM users WHERE email = {tenant} AND email = ?',
      [email],
      'default'
    );
    if (existing) {
      return conflict('该邮箱已被注册');
    }
  } catch (err) {
    console.error('[Register] Check duplicate error:', err.message);
    return internalError('服务器错误');
  }

  // === bcrypt 哈希密码 ===
  let bcrypt;
  try {
    bcrypt = await import('bcryptjs');
  } catch {
    return internalError('加密模块加载失败');
  }
  const hash = await bcrypt.hash(password, 12);

  // === 写入数据库 ===
  try {
    // 新用户默认租户为 'default'，角色为 'user'
    const tenant = 'default';
    const role = 'user';

    const result = execute(
      env,
      `INSERT INTO users (tenant_id, email, password_hash, name, role)
       VALUES ({tenant}, ?, ?, ?, ?)`,
      [email, hash, name, role],
      tenant
    );

    if (!result || !result.meta || !result.meta.last_row_id) {
      throw new Error('Failed to insert user: no last_row_id returned');
    }

    const userId = result.meta.last_row_id;

    return created({
      user: {
        id: userId,
        email,
        name,
        role,
        tenant,
      },
    });
  } catch (err) {
    // 捕获 unique 约束违反（兜底）
    if (err.message && err.message.includes('UNIQUE')) {
      return conflict('该邮箱已被注册');
    }
    console.error('[Register] Insert error:', err.message);
    return internalError('注册失败，请稍后重试');
  }
}
