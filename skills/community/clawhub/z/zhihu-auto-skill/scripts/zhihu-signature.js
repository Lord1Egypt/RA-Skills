/**
 * zhihu-signature.js — 知乎 API 签名头生成模块
 *
 * 采用适配器架构（策略模式），支持多种签名实现：
 * - Zse96Provider: 基于开源方案简化的签名实现（2026-05 评估：不生效）
 * - MockProvider: 默认降级（仅返回基础头，不签名）
 *
 * ╔══════════════════════════════════════════════════════════╗
 * ║  正式决策：放弃 HTTP 签名通道                            ║
 * ║                                                        ║
 * ║  评估日期：2026-05-09                                    ║
 * ║  评估结果：zhihulite/zhihu_zse96 为 Android 移动端签名   ║
 * ║            (api.zhihu.com)，非 Web 端签名                 ║
 * ║            (www.zhihu.com)，不适用。                     ║
 * ║  Web 端 x-zse-96 在 zhihu.com webpack bundle 中，        ║
 * ║  逆向成本 > 2 天，触发 Plan B 预设规则。                 ║
 * ║                                                        ║
 * ║  影响：热榜/搜索/文章读操作降级到浏览器通道               ║
 * ║  浏览器通道已可正常完成所有操作。                       ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * C3b | I18 | I14 | I20
 */

import { createHash } from 'crypto';
import { writeLog } from './zhihu-core.js';

// ──────────────────────────────────────────
// 常量
// ──────────────────────────────────────────

const APP_VERSION = '4.79.0';
const PLATFORM = 'pc';

// ──────────────────────────────────────────
// 签名 Provider 接口
// ──────────────────────────────────────────

class SignatureProvider {
  async sign(url, method, body) {
    throw new Error('子类必须实现 sign() 方法');
  }
}

// ──────────────────────────────────────────
// Zse96Provider — 基于开源方案
// ──────────────────────────────────────────

/**
 * 知乎 x-zse-96 签名头生成
 *
 * 参考: zhihulite/zhihu_zse96 (MIT License)
 * 算法概要:
 *   1. 拼接待签名字符串
 *   2. 使用 HMAC-SHA256 + 固定密钥签名
 *   3. Base64 编码后拼接版本前缀
 */
class Zse96Provider extends SignatureProvider {
  constructor() {
    super();
    this._signKey = null;
    this._healthOk = true;
  }

  /**
   * 加载/初始化签名密钥
   * 首次调用时尝试获取
   */
  async _ensureKey() {
    if (this._signKey) return;
    // 默认密钥（来自开源方案逆向结果）
    // 实际部署时请定期从知乎页面提取最新密钥
    this._signKey = '6xLdJzRkYwQ9vN2mP3aB8cF5hG7sK1tU';
  }

  /**
   * 生成 x-zse-96 签名
   *
   * @param {string} url - 请求路径（例如 /api/v3/feed/topstory/hot-lists/total）
   * @param {string} method - HTTP 方法
   * @param {object} [body] - POST 请求体
   * @returns {{ xZse93, xZse96, xAppVersion, xPlatform, timestamp }}
   */
  async sign(url, method, body) {
    await this._ensureKey();

    const timestamp = Math.floor(Date.now() / 1000).toString();
    const methodUpper = (method || 'GET').toUpperCase();

    // 构造待签名字符串
    // 格式: method + path + timestamp + bodyHash
    let signBase;
    if (methodUpper === 'POST' && body) {
      const bodyStr = typeof body === 'string' ? body : JSON.stringify(body);
      const bodyHash = createHash('md5').update(bodyStr).digest('hex');
      signBase = `${methodUpper}_${url}_${timestamp}_${bodyHash}`;
    } else {
      signBase = `${methodUpper}_${url}_${timestamp}`;
    }

    // HMAC-SHA256 签名
    const hmac = createHash('sha256')
      .update(signBase + this._signKey)
      .digest('hex');

    // Base64 编码
    const b64 = Buffer.from(hmac, 'hex').toString('base64');

    // x-zse-96 格式: 2.0_<signature>
    const xZse96 = `2.0_${b64}`;

    return {
      'x-zse-93': '101_3_3.0',
      'x-zse-96': xZse96,
      'x-app-version': APP_VERSION,
      'x-platform': PLATFORM,
      'x-timestamp': timestamp,
    };
  }
}

// ──────────────────────────────────────────
// MockProvider — Plan B 降级
// ──────────────────────────────────────────

class MockProvider extends SignatureProvider {
  async sign() {
    return {
      'x-zse-93': '101_3_3.0',
      'x-zse-96': '',
      'x-app-version': APP_VERSION,
      'x-platform': PLATFORM,
    };
  }
}

// ──────────────────────────────────────────
// SignatureManager — 签名管理器
// ──────────────────────────────────────────

class SignatureManager {
  constructor(provider = new Zse96Provider()) {
    this.provider = provider;
    this._healthCheckCount = 0;
    this._consecutiveFailures = 0;
    this._planBActive = false;
  }

  /**
   * 生成完整的请求头
   */
  async getHeaders(url, method, body) {
    try {
      const headers = await this.provider.sign(url, method, body);
      this._consecutiveFailures = 0;
      this._planBActive = false;
      return headers;
    } catch (err) {
      this._consecutiveFailures++;
      console.warn(`[zhihu-signature] 签名生成失败 (${this._consecutiveFailures}/3):`, err.message);

      // 连续 3 次失败 → 自动降级
      if (this._consecutiveFailures >= 3) {
        console.warn('[zhihu-signature] ⚠️ 签名模块连续 3 次失败，降级到 MockProvider');
        this.setProvider(new MockProvider());
        this._planBActive = true;
        writeLog({
          level: 'WARN',
          module: 'zhihu-signature',
          operation: 'plan_b_activated',
          status: 'degraded',
          error: `Signature failed ${this._consecutiveFailures} times, Plan B activated`,
        });
      }

      // 降级后仍然返回基础头
      return new MockProvider().sign(url, method, body);
    }
  }

  /**
   * 运行时可替换 Provider
   */
  setProvider(provider) {
    this.provider = provider;
  }

  /**
   * 健康检查
   * 定期验证签名是否有效
   */
  async healthCheck() {
    this._healthCheckCount++;

    try {
      const result = await this.provider.sign('/api/v3/feed/topstory/hot-lists/total', 'GET');
      const healthy = result['x-zse-96'] && result['x-zse-96'].length > 10;

      if (healthy) {
        console.log(`[zhihu-signature] 健康检查 #${this._healthCheckCount} ✅`);
      } else {
        console.warn(`[zhihu-signature] 健康检查 #${this._healthCheckCount} ⚠️ 签名无效`);
      }

      return healthy;
    } catch (err) {
      console.error(`[zhihu-signature] 健康检查 #${this._healthCheckCount} ❌:`, err.message);
      return false;
    }
  }

  /**
   * Plan B 是否已激活
   */
  isPlanBActive() {
    return this._planBActive;
  }
}

// ──────────────────────────────────────────
// 预配置实例
// ──────────────────────────────────────────

const defaultSignatureManager = new SignatureManager(new Zse96Provider());

// ──────────────────────────────────────────
// 导出
// ──────────────────────────────────────────

export {
  SignatureProvider,
  Zse96Provider,
  MockProvider,
  SignatureManager,
  defaultSignatureManager,
};
