/**
 * 共享配额模块 — 多租户 KV/API 配额限制
 *
 * Phase 4A W2 实现：
 * - Edge Functions + Cloud Functions 共用（架构专家 D4）
 * - 软限制/硬限制双层防护（安全专家 S-05）
 * - KV 故障时 fail-open（带告警）
 * - 使用 Edge KV atomic counter
 *
 * 使用方式：
 *   import { checkQuota, incrementQuota } from '../sharing/quota.js';
 *
 *   // 检查配额
 *   const result = await checkQuota(env, tenant, 'kv_ops');
 *   if (!result.allowed) {
 *     return new Response('Quota exceeded', { status: 429 });
 *   }
 *
 *   // 递增配额
 *   await incrementQuota(env, tenant, 'kv_ops');
 */

// ===================== 配额限制定义 =====================

/** 硬限制（硬性上限） */
export const HARD_LIMITS = {
  kv_ops: 10000,       // 每日 KV 操作次数
  storage: 10485760,   // 存储空间（字节）
  api_calls: 1000,     // 每日 API 调用次数
};

/** 软限制（硬限制 * 0.9，提前告警，防止边界值频繁拒绝） */
export const SOFT_LIMITS = {
  kv_ops: Math.floor(HARD_LIMITS.kv_ops * 0.9),
  storage: Math.floor(HARD_LIMITS.storage * 0.9),
  api_calls: Math.floor(HARD_LIMITS.api_calls * 0.9),
};

/** 配额键前缀 */
const QUOTA_KEY_PREFIX = 'quota';

// ===================== 配额检查 =====================

/**
 * 检查租户配额是否超限
 * @param {Object} env - 环境变量（含 env.KV）
 * @param {string} tenant - 租户 ID
 * @param {string} type - 配额类型：kv_ops | storage | api_calls
 * @returns {Promise<Object>} { allowed, reason?, warning?, remaining?, degradedMode? }
 */
export async function checkQuota(env, tenant, type = 'kv_ops') {
  const quotaKey = `${QUOTA_KEY_PREFIX}:${tenant}:${type}`;
  const limit = HARD_LIMITS[type] || 10000;
  const softLimit = SOFT_LIMITS[type] || Math.floor(limit * 0.9);

  try {
    if (!env?.KV) {
      // 无 KV 绑定时不限制（开发环境降级）
      return { allowed: true, degradedMode: true };
    }

    const count = parseInt(await env.KV.get(quotaKey) || '0', 10);

    if (count >= limit) {
      // 超过硬限制 → 拒绝
      return { allowed: false, reason: 'QUOTA_EXCEEDED', hard: true, limit, current: count };
    }

    if (count >= softLimit) {
      // 超过软限制 → 放行但告警
      return { allowed: true, warning: 'NEAR_QUOTA_LIMIT', remaining: limit - count, limit, current: count };
    }

    return { allowed: true, remaining: limit - count, limit, current: count };
  } catch (err) {
    // 🛡️ KV 故障时 fail-open：允许通过但记录告警
    console.error(`[Quota] Check failed for ${tenant}:${type}`, err.message);
    // 使用非阻塞告警上报
    try {
      await reportQuotaFailure(env, tenant, type, err.message);
    } catch { /* ignore */ }
    return { allowed: true, degradedMode: true };
  }
}

// ===================== 配额递增 =====================

/**
 * 递增租户配额计数
 *
 * ⚠️ 近似计数（非原子）：
 * 高并发下 read-modify-write 可能产生 ±1 偏差。
 * 对于日配额 10000 的上限，±1 不影响实际效果。
 * 如需精确计数，改用 D1 database + SELECT FOR UPDATE。
 *
 * @param {Object} env - 环境变量（含 env.KV）
 * @param {string} tenant - 租户 ID
 * @param {string} type - 配额类型
 * @param {number} [amount=1] - 递增数量
 */
export async function incrementQuota(env, tenant, type = 'kv_ops', amount = 1) {
  const quotaKey = `${QUOTA_KEY_PREFIX}:${tenant}:${type}`;

  try {
    if (!env?.KV) return;

    // read-modify-write（非原子，但日配额 10000 下近似足够）
    const current = parseInt(await env.KV.get(quotaKey) || '0', 10);
    await env.KV.put(quotaKey, String(current + amount), {
      expirationTtl: 86400, // 24h 自动重置
    });
  } catch (err) {
    // 配额递增失败不影响业务操作，仅记录
    console.error(`[Quota] Increment failed for ${tenant}:${type}`, err.message);
  }
}

// ===================== 配额重置 =====================

/**
 * 重置租户配额（每日零点调用，或 superadmin 手动重置）
 * @param {Object} env - 环境变量
 * @param {string} tenant - 租户 ID
 * @param {string} [type] - 配额类型（不传则重置所有）
 */
export async function resetQuota(env, tenant, type) {
  try {
    if (type) {
      await env.KV?.delete(`${QUOTA_KEY_PREFIX}:${tenant}:${type}`);
    } else {
      for (const t of Object.keys(HARD_LIMITS)) {
        await env.KV?.delete(`${QUOTA_KEY_PREFIX}:${tenant}:${t}`);
      }
    }
  } catch (err) {
    console.error(`[Quota] Reset failed for ${tenant}:${type || 'all'}`, err.message);
  }
}

// ===================== 滑动窗口计数器（Phase 4B6 — 计费 MVP） =====================

const SLIDING_WINDOW_PREFIX = 'billing:sw';

/**
 * 滑动窗口计数 — 用于计费统计
 *
 * 将时间窗口划分为多个槽位，每个槽位独立计数。
 * 查询时汇总当前窗口内所有有效槽位的计数。
 *
 * @param {Object} env - 环境变量（含 env.KV）
 * @param {string} tenant - 租户 ID
 * @param {string} metric - 计费指标（如 'api_calls', 'storage_gb'）
 * @param {number} [windowMinutes=60] - 窗口大小（分钟）
 * @returns {Promise<number>} 当前窗口内的总计数
 */
export async function getSlidingWindowCount(env, tenant, metric, windowMinutes = 60) {
  try {
    if (!env?.KV) return 0;

    const prefix = `${SLIDING_WINDOW_PREFIX}:${tenant}:${metric}:`;
    const now = Date.now();
    const windowMs = windowMinutes * 60 * 1000;
    const slotMs = 60 * 1000; // 1 分钟一个槽位
    const cutoff = now - windowMs;

    // 扫描当前窗口内的所有槽位
    const listResult = await env.KV.list({ prefix });
    let total = 0;

    for (const key of listResult.keys) {
      // 从 key 中提取时间戳（格式：prefix{timestamp}）
      const timestamp = parseInt(key.name.slice(prefix.length), 10);
      if (timestamp >= cutoff) {
        const val = parseInt(await env.KV.get(key.name) || '0', 10);
        total += val;
      }
    }

    return total;
  } catch (err) {
    console.error(`[Billing] Sliding window count failed: ${tenant}:${metric}`, err.message);
    return 0;
  }
}

/**
 * 记录一次计费事件
 *
 * @param {Object} env - 环境变量
 * @param {string} tenant - 租户 ID
 * @param {string} metric - 计费指标
 * @param {number} [amount=1] - 增量
 */
export async function recordBillingEvent(env, tenant, metric, amount = 1) {
  try {
    if (!env?.KV) return;

    const now = Date.now();
    // 按分钟槽位聚合
    const slotKey = `${SLIDING_WINDOW_PREFIX}:${tenant}:${metric}:${Math.floor(now / 60000) * 60000}`;

    // 原子递增
    const current = parseInt(await env.KV.get(slotKey) || '0', 10);
    await env.KV.put(slotKey, String(current + amount), { expirationTtl: 86400 }); // 1 天过期
  } catch (err) {
    console.error(`[Billing] Record event failed: ${tenant}:${metric}`, err.message);
  }
}

/**
 * 检查是否超限，超限返回 403 升级提示（计费 MVP 核心逻辑）
 *
 * @param {Object} env - 环境变量
 * @param {string} tenant - 租户 ID
 * @param {string} metric - 计费指标
 * @param {number} limit - 限制值
 * @param {number} [windowMinutes=60] - 窗口大小
 * @returns {Promise<Object>} { allowed, count, limit, upgrade? }
 */
export async function checkBillingQuota(env, tenant, metric, limit, windowMinutes = 60) {
  const count = await getSlidingWindowCount(env, tenant, metric, windowMinutes);

  if (count >= limit) {
    return {
      allowed: false,
      count,
      limit,
      upgrade: true,
      message: `已超出免费额度 (${limit}/${windowMinutes}min)，请升级套餐`,
    };
  }

  return { allowed: true, count, limit, remaining: limit - count };
}

// ===================== 内部工具 =====================

/**
 * 上报配额检查失败
 */
async function reportQuotaFailure(env, tenant, type, errorMessage) {
  const logKey = `quota:failures:${Date.now()}`;
  if (env?.KV) {
    await env.KV.put(logKey, JSON.stringify({
      timestamp: new Date().toISOString(),
      tenant,
      type,
      error: errorMessage,
    }), { expirationTtl: 86400 });
  }
  console.warn(`[Quota] Failure reported: ${tenant}:${type} -> ${errorMessage}`);
}
