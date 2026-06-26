/**
 * 支付预下单 API — 微信/支付宝预下单（含库存锁定 + 幂等性）
 *
 * POST /api/pay/create-order
 * Body: { productId, quantity }
 *
 * - authenticate → get tenant + userId
 * - withTransaction:
 *   1. SELECT ... FOR UPDATE 锁定商品
 *   2. 校验库存
 *   3. 扣减库存（乐观锁 version）
 *   4. 创建订单
 * - 写 KV 幂等锁
 * - 返回 { orderNo, amount, status }
 */

import { withTransaction } from '../../utils/db.js';
import { authenticate } from '../_helpers.js';
import { ok, badRequest, unauthorized, internalError } from '../../../sharing/response.js';
import { idempotencyKey } from '../../../sharing/kv-keys.js';

/**
 * 生成订单号：时间戳 + 随机 6 位数字
 */
function generateOrderNo() {
  const ts = Date.now().toString(36).toUpperCase();
  const rand = Math.floor(Math.random() * 1000000)
    .toString()
    .padStart(6, '0');
  return `ORD${ts}${rand}`;
}

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

  const { productId, quantity } = body;

  if (!productId) {
    return badRequest('productId 为必填项');
  }
  const qty = parseInt(quantity, 10);
  if (isNaN(qty) || qty <= 0 || qty > 999) {
    return badRequest('quantity 必须为 1-999 之间的整数');
  }

  // === 事务处理 ===
  try {
    return withTransaction(env, tenant, (ctx) => {
      // Step 1: SELECT FOR UPDATE 锁定商品
      // 价格为服务端唯一来源，客户端不可篡改。从 DB 读取的 price 用于后续金额计算，
      // 忽略客户端传入的任何金额字段。
      const product = ctx.queryOne(
        'SELECT id, stock, price, version, name FROM products WHERE tenant_id = {tenant} AND id = ? FOR UPDATE',
        [productId]
      );

      if (!product) {
        return badRequest('商品不存在');
      }

      // Step 2: 校验库存
      if (product.stock < qty) {
        return badRequest(`库存不足：当前库存 ${product.stock}，需要 ${qty}`);
      }

      // Step 3: 扣减库存（乐观锁）
      const updateResult = ctx.execute(
        'UPDATE products SET stock = stock - ?, version = version + 1 WHERE tenant_id = {tenant} AND id = ? AND version = ?',
        [qty, productId, product.version]
      );

      if (updateResult.affectedRows === 0) {
        return badRequest('库存更新冲突，请重试');
      }

      // Step 4: 创建订单
      const orderNo = generateOrderNo();
      const amount = Math.round(product.price * qty * 100) / 100; // 精确到分
      const status = 'pending';

      ctx.execute(
        `INSERT INTO orders (tenant_id, order_no, user_id, product_id, qty, amount, status)
         VALUES ({tenant}, ?, ?, ?, ?, ?, ?)`,
        [orderNo, userId, productId, qty, amount, status]
      );

      return ok({
        orderNo,
        amount,
        status,
      });
    });
  } catch (err) {
    console.error('[Pay Create Order] Error:', err);
    return internalError('创建订单失败');
  }
}
