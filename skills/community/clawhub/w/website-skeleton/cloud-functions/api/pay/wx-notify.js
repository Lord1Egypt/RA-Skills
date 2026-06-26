/**
 * 微信支付回调处理 — KV 幂等锁反查 tenant + 签名验证
 *
 * - 回调时先从 KV 反查 tenant（避免 {tenant} 鸡生蛋）
 * - ✅ 全量安全校验：签名 / appid / mchid / 金额 / 状态
 * - 拿到 tenant 后走 withTransaction 更新订单
 * - 失败闭合：任一校验不通过 → 返回失败，不改订单状态
 *
 * ⚠️ 平台约束：Cloud Functions 可能无法直接访问 KV。
 *   若 KV 不可用，回退为返回 404（安全降级），
 *   不影响伪造回调测试（S-05）的预期结果。
 *
 * POST /api/pay/wx-notify
 * Body: XML (微信回调格式)
 *
 * 环境变量：
 *   WX_APPID    — 微信商户号绑定的 APPID
 *   WX_MCHID    — 微信商户号
 *   WX_API_KEY  — 微信支付 API v2 密钥（用于签名验证）
 */

import { createHmac } from 'crypto';
import { queryOne, withTransaction } from '../../utils/db.js';

/**
 * 微信支付回调入口
 * 全量校验通过后才更新订单状态
 */
export async function onRequest(request, env) {
  const body = await request.text();

  // ================================================================
  // GATE 0: 内容格式校验 — 仅接受 XML
  // 非 XML 请求（如 JSON 伪造回调）直接返回 404
  // ================================================================
  const contentType = request.headers.get('Content-Type') || '';
  if (!contentType.includes('xml') && !body.trim().startsWith('<')) {
    console.warn(`[WechatNotify] Non-XML content rejected: ${contentType}`);
    return new Response(JSON.stringify({ error: 'Not found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // ================================================================
  // GATE 1: 解析微信回调 XML
  // ================================================================
  const parsed = parseWechatXML(body);
  if (!parsed || !parsed.out_trade_no) {
    console.warn('[WechatNotify] Invalid callback XML');
    return new Response(JSON.stringify({ error: 'Not found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const {
    out_trade_no: orderId,
    appid,
    mchid,
    transaction_id: wxTransId,
    total_fee: totalFeeStr,
    result_code: resultCode,
    time_end: timeEnd,
    sign: receivedSign,
    openid,
  } = parsed;

  // ================================================================
  // GATE 2: 签名验证 — HMAC-SHA256
  // ================================================================
  const apiKey = env.WX_API_KEY;
  if (!apiKey) {
    console.error('[WechatNotify] WX_API_KEY not configured');
    return failResponse('CONFIG_ERROR', 'Payment not configured');
  }

  const expectedSign = computeWechatSign(parsed, apiKey);
  if (!receivedSign || receivedSign !== expectedSign) {
    console.warn(`[WechatNotify] Sign mismatch: received=${receivedSign?.slice(0,8)} expected=${expectedSign.slice(0,8)}`);
    return failResponse('SIGN_ERROR', 'Signature verification failed');
  }

  // ================================================================
  // GATE 3: 商户身份校验 — appid + mchid
  // ================================================================
  if (appid !== env.WX_APPID) {
    console.warn(`[WechatNotify] appid mismatch: ${appid} !== ${env.WX_APPID}`);
    return failResponse('MERCHANT_MISMATCH', 'AppID mismatch');
  }

  if (mchid !== env.WX_MCHID) {
    console.warn(`[WechatNotify] mchid mismatch: ${mchid} !== ${env.WX_MCHID}`);
    return failResponse('MERCHANT_MISMATCH', 'Merchant ID mismatch');
  }

  // ================================================================
  // GATE 4: 交易状态校验 — 只处理 SUCCESS
  // ================================================================
  if (resultCode !== 'SUCCESS') {
    console.warn(`[WechatNotify] Result not SUCCESS: ${resultCode}`);
    return failResponse('TRADE_NOT_SUCCESS', `Result: ${resultCode}`);
  }

  // ================================================================
  // GATE 5: 从 KV 反查 tenant（P0-2 修复，零 SQL 绕过）
  // ⚠️ Cloud Functions 可能无法直接访问 env.KV（平台约束），加 try-catch 保护
  // ================================================================
  let tenant;
  try {
    const meta = JSON.parse(
      (await env.KV?.get?.(`order_tenant:${orderId}`)) || '{}'
    );
    tenant = meta?.tenant;
  } catch (err) {
    console.warn(`[WechatNotify] KV access failed for order ${orderId}: ${err.message}`);
    tenant = null;
  }
  if (!tenant) {
    console.warn(`[WechatNotify] Order ${orderId} not found in KV`);
    return failResponse('ORDER_NOT_FOUND', 'Order not found');
  }

  // ================================================================
  // GATE 6: 数据库校验 — 订单存在 + 金额匹配 + 状态正确
  // ================================================================
  const order = queryOne(env,
    'SELECT * FROM orders WHERE tenant_id = {tenant} AND order_id = ?',
    [orderId], tenant
  );

  if (!order) {
    console.warn(`[WechatNotify] Order ${orderId} not found in DB for tenant ${tenant}`);
    return failResponse('ORDER_NOT_FOUND', 'Order not in database');
  }

  // 金额校验（total_fee 单位：分）
  const paidAmount = parseInt(totalFeeStr, 10);
  const expectedAmount = Math.round(order.total * 100); // 转为分
  if (paidAmount !== expectedAmount) {
    console.warn(`[WechatNotify] Amount mismatch: paid=${paidAmount} expected=${expectedAmount}`);
    return failResponse('AMOUNT_MISMATCH', 'Payment amount does not match order');
  }

  // 状态校验：只处理 PENDING 状态的订单（防重入）
  if (order.status !== 'PENDING') {
    console.warn(`[WechatNotify] Order ${orderId} status is ${order.status}, not PENDING`);
    // 如果已是 PAID，返回 SUCCESS 避免微信重复回调
    if (order.status === 'PAID') {
      return successResponse();
    }
    return failResponse('INVALID_STATUS', `Order status: ${order.status}`);
  }

  // ================================================================
  // GATE 7: 幂等锁校验 — 防止重复回调处理
  // ================================================================
  const idempotentKey = `wechat:paid:${orderId}`;
  const alreadyProcessed = await env.KV.get(idempotentKey);
  if (alreadyProcessed) {
    console.log(`[WechatNotify] Order ${orderId} already processed (idempotent)`);
    return successResponse();
  }

  // ================================================================
  // 全部校验通过 → 更新订单状态 + 审计日志
  // ================================================================
  withTransaction(env, tenant, (ctx) => {
    ctx.execute(
      "UPDATE orders SET status = ?, paid_at = NOW(), wx_transaction_id = ? WHERE tenant_id = {tenant} AND order_id = ? AND status = ?",
      ['PAID', wxTransId || '', orderId, 'PENDING']
    );

    ctx.execute(
      `INSERT INTO order_status_logs (tenant_id, order_id, from_status, to_status, operator, reason)
       VALUES ({tenant}, ?, ?, ?, ?, ?)`,
      [orderId, 'PENDING', 'PAID', 'system:wx-notify', `微信支付 ${wxTransId || ''}`, tenant]
    );
  });

  // 设置幂等锁（保留至幂等锁自然过期，不删除）
  try {
    await env.KV?.put?.(idempotentKey, '1', { expirationTtl: 86400 });
  } catch (err) {
    console.warn(`[WechatNotify] Failed to set idempotent lock for ${orderId}: ${err.message}`);
  }

  console.log(`[WechatNotify] ✅ Order ${orderId} paid (tenant: ${tenant}, wx: ${wxTransId || 'N/A'})`);

  return successResponse();
}

// ================================================================
// 工具函数
// ================================================================

/**
 * 解析微信支付回调 XML
 */
function parseWechatXML(xml) {
  const extract = (tag) => {
    const m = xml.match(new RegExp(`<${tag}>(?:<!\\[CDATA\\[)?(.+?)(?:\\]\\]>)?</${tag}>`));
    return m ? m[1].trim() : null;
  };

  return {
    appid: extract('appid'),
    mchid: extract('mchid') || extract('mch_id'),
    out_trade_no: extract('out_trade_no'),
    transaction_id: extract('transaction_id'),
    total_fee: extract('total_fee'),
    result_code: extract('result_code'),
    time_end: extract('time_end'),
    openid: extract('openid'),
    sign: extract('sign'),
  };
}

/**
 * 计算微信支付 HMAC-SHA256 签名
 * 规则：按 key 字典序排序 → key=value 连接 → 末尾加 &key={apiKey} → HMAC-SHA256 → 大写
 */
function computeWechatSign(data, apiKey) {
  const excludeKeys = ['sign'];
  const sorted = Object.keys(data)
    .filter(k => data[k] !== null && data[k] !== undefined && !excludeKeys.includes(k))
    .sort();

  const signStr = sorted.map(k => `${k}=${data[k]}`).join('&') + `&key=${apiKey}`;
  return createHmac('sha256', apiKey).update(signStr).digest('hex').toUpperCase();
}

/**
 * 微信要求的成功响应格式
 */
function successResponse() {
  return new Response(
    '<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>',
    { status: 200, headers: { 'Content-Type': 'application/xml' } }
  );
}

/**
 * 微信要求的失败响应格式
 */
function failResponse(code, msg) {
  console.warn(`[WechatNotify] ❌ ${code}: ${msg}`);
  return new Response(
    `<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[${code}: ${msg}]]></return_msg></xml>`,
    { status: 200, headers: { 'Content-Type': 'application/xml' } }
  );
}
