/**
 * KV 滑动窗口限流
 *
 * Edge Functions（V8 + KV）专用。使用 KV 存储滑动窗口计数器。
 *
 * 策略：
 *   - 未登录（IP 级别）：10 次/分钟
 *   - 已登录（User ID 级别）：60 次/分钟
 *   - Admin：200 次/分钟
 */

/**
 * 检查是否超过限流阈值
 *
 * @param {object} context - Edge Function context（含 env.KV）
 * @param {string} key - 限流 key（如 `ai:user123`）
 * @param {number} limit - 窗口内允许的最大请求数
 * @returns {Promise<{allowed: boolean, remaining: number, resetMs: number}>}
 */
export async function checkRateLimit(context, key, limit) {
  const { KV } = context.env;
  if (!KV) {
    // KV 不可用时降级放行
    return { allowed: true, remaining: limit, resetMs: 60000 };
  }

  const now = Date.now();
  const windowMs = 60 * 1000; // 1 分钟滑动窗口
  const currentWindow = Math.floor(now / windowMs);
  const windowKey = `rl:${key}:${currentWindow}`;
  const prevKey = `rl:${key}:${currentWindow - 1}`;

  try {
    const current = parseInt(await KV.get(windowKey) || '0', 10);
    const prev = parseInt(await KV.get(prevKey) || '0', 10);

    // 滑动窗口：当前窗口占比 + 上一窗口剩余权重
    const elapsedMs = now % windowMs;
    const prevWeight = (windowMs - elapsedMs) / windowMs;
    const totalWeight = current + prev * prevWeight;

    if (totalWeight >= limit) {
      return {
        allowed: false,
        remaining: 0,
        resetMs: windowMs - elapsedMs,
      };
    }

    // 写入当前计数（TTL 120s，足够覆盖窗口）
    await KV.put(windowKey, String(current + 1), { expirationTtl: 120 });

    return {
      allowed: true,
      remaining: limit - Math.ceil(totalWeight) - 1,
      resetMs: windowMs - elapsedMs,
    };
  } catch (err) {
    // KV 写入失败时降级放行
    console.warn(`[RateLimit] KV operation failed: ${err.message}`);
    return { allowed: true, remaining: limit, resetMs: 60000 };
  }
}
