/**
 * @website-skeleton/payment — 支付模块入口
 *
 * Cloud Functions 支付处理工具函数。
 *
 * 使用方式（Cloud Functions handler 中）：
 *   import { verifyPayment, createOrderRecord } from '@website-skeleton/payment';
 *   import { withTransaction } from '@website-skeleton/shared';
 *
 *   export async function onRequest(request, env) {
 *     // 1. 支付回调验证
 *     const { valid, orderId } = await verifyPayment(request, env);
 *     if (!valid) return new Response('Invalid', { status: 400 });
 *
 *     // 2. 更新订单状态
 *     withTransaction(env, tenant, (ctx) => {
 *       ctx.execute('UPDATE orders SET status = ? ...');
 *     });
 *   }
 */

/**
 * 验证支付回调签名（placeholder — 生产环境使用微信官方 SDK）
 * @param {Request} request
 * @param {Object} env
 * @returns {Promise<{valid: boolean, orderId: string|null}>}
 */
export async function verifyPayment(request, env) {
  // TODO: 实现微信/支付宝签名验证
  // 参考：references/payment-module.md
  try {
    const body = await request.text();
    const data = JSON.parse(body);
    return { valid: true, orderId: data.out_trade_no || null };
  } catch {
    return { valid: false, orderId: null };
  }
}
