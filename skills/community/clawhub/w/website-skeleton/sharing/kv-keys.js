/**
 * KV Key 命名规范 — 多租户前缀支持
 *
 * Phase 3 L3-1 实现
 *
 * Phase 3: Key 前缀占位符 = "default"（向后兼容）
 * Phase 4: Key 前缀从 JWT payload.tenant 动态读取
 *
 * 使用方式：
 *   import { makeKey, getTenant } from './kv-keys.js';
 *
 *   // 当前租户
 *   const tenant = getTenant(payload); // 从 JWT 读取，默认 "default"
 *
 *   // Session key
 *   kv.get(makeKey(tenant, 'session', sessionId));
 *
 *   // Refresh Token key
 *   kv.get(makeKey(tenant, 'rt', userId, 'meta'));
 */

// ===================== 常量 =====================

/**
 * Phase 3 默认租户（向后兼容）
 * Phase 4 中替换为 JWT payload.tenant
 */
export const DEFAULT_TENANT = 'default';

/**
 * Key 前缀名称（用于 KV 命名约定）
 */
export const KEY_PREFIXES = {
  SESSION:         'session',
  REFRESH_TOKEN:   'rt',
  CART:            'cart',
  AI_SESSION:      'ai',
  IDEMPOTENCY:     'pay:idempotency',
  RATE_LIMIT:      'rl',
  ANALYTICS:       'analytics',
  PRODUCT_CACHE:   'product',
};

/**
 * Key TTL 定义（秒）
 */
export const KEY_TTL = {
  SESSION:         86400,     // 24h
  REFRESH_TOKEN:    604800,   // 7d
  CART:             2592000,  // 30d
  AI_SESSION:       86400,    // 24h
  IDEMPOTENCY:      86400,    // 24h（微信重试窗口内）
  RATE_LIMIT:       120,      // 2min（略超窗口宽）
  PRODUCT_CACHE:    300,      // 5min
  ANALYTICS:        7776000,  // 90d
};

// ===================== Key 生成 =====================

/**
 * 生成带租户前缀的 KV Key
 * @param {string} tenant - 租户 ID（从 JWT payload.tenant 获取）
 * @param {...string} parts - Key 组成部分
 * @returns {string} 完整 key，如 "default:session:abc123"
 * @throws {Error} 当 tenant 为空时抛出
 *
 * Phase 4A W2: 强制 tenant 非空检查（IMA S3：防止并发串租户）
 */
export function makeKey(tenant, ...parts) {
  if (!tenant || tenant === 'undefined' || tenant === 'null') {
    throw new Error(`tenant is required for KV key (got: ${JSON.stringify(tenant)})`);
  }
  return [tenant, ...parts].join(':');
}

/**
 * 从 JWT payload 中提取租户 ID
 * @param {Object} payload - JWT payload
 * @returns {string} 租户 ID，未设置时返回 DEFAULT_TENANT
 */
export function getTenant(payload) {
  return payload?.tenant || DEFAULT_TENANT;
}

// ===================== 便捷函数 =====================

/**
 * Session Key
 */
export function sessionKey(tenant, sessionId) {
  return makeKey(tenant, KEY_PREFIXES.SESSION, sessionId);
}

/**
 * Refresh Token Meta Key
 */
export function rtMetaKey(tenant, userId) {
  return makeKey(tenant, KEY_PREFIXES.REFRESH_TOKEN, String(userId), 'meta');
}

/**
 * Cart Key
 */
export function cartKey(tenant, userId) {
  return makeKey(tenant, KEY_PREFIXES.CART, String(userId));
}

/**
 * AI Session Key
 */
export function aiSessionKey(tenant, userId, sessionId) {
  return makeKey(tenant, KEY_PREFIXES.AI_SESSION, String(userId), sessionId);
}

/**
 * 支付幂等 Key
 */
export function idempotencyKey(tenant, outTradeNo) {
  return makeKey(tenant, KEY_PREFIXES.IDEMPOTENCY, outTradeNo);
}

/**
 * 限流 Key
 */
export function rateLimitKey(tenant, identifier, windowKey) {
  return makeKey(tenant, KEY_PREFIXES.RATE_LIMIT, identifier, windowKey);
}

/**
 * 产品缓存 Key
 */
export function productCacheKey(tenant, productId) {
  return makeKey(tenant, KEY_PREFIXES.PRODUCT_CACHE, String(productId));
}

// ===================== 导出 makeKey（默认） =====================
export { makeKey as key };

// ===================== KV 热 key 分散（Phase 4B5 — 待接入触发逻辑） =====================

/**
 * ⚠️ 预留函数：KV session 热 key 分片
 *
 * Phase 4B5 实现。当前未接入任何调用点（dead code），
 * 因为缺少自动监控 → 切换的触发逻辑。
 *
 * **接入条件：** 当 KV get/set 延迟 > 200ms 持续 5 分钟时，
 * 应将 sessionKey() 调用切换为 getShardSessionKey()。
 * 需实现 monitoring/metrics 模块检测延迟。
 *
 * FNV-1a 哈希（快速、低碰撞、确定性）
 * @param {string} str - 输入字符串
 * @returns {number} 32 位无符号整数哈希
 */
function fnv1a(str) {
  let hash = 2166136261;
  for (let i = 0; i < str.length; i++) {
    hash ^= str.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

/**
 * 获取分片的 session key（用于 KV 热 key 分散）
 *
 * Phase 4B5: 将单租户的 session key 分散到 64 个分区
 * 触发条件：KV get/set 延迟 > 200ms 持续 5 分钟（架构专家 O1+O3）
 *
 * @param {string} tenant - 租户 ID
 * @param {string} sessionId - Session ID
 * @param {number} [partitions=64] - 分区数
 * @returns {string} 分片后的 session key
 */
export function getShardSessionKey(tenant, sessionId, partitions = 64) {
  if (!tenant) throw new Error('tenant is required for shard session key');
  const shard = fnv1a(`${tenant}:session:${sessionId}`) % partitions;
  return `session_shard:${shard}:${sessionId}`;
}
