/**
 * zhihu-signature.js — 知乎 API 签名头生成模块
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
 * ║                                                        ║
 * ║  原 Zse96Provider 已移除（含硬编码密钥）                   ║
 * ║  仅保留 MockProvider 作为 Plan B 默认降级                 ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * P0-2 (Hermes 评审): 删除硬编码签名密钥
 * C3b | I18 | I14 | I20
 *
 * @module zhihu-signature
 */

import { signatureLog } from './zhihu-logger.js';

/** @type {string} App 版本号 */
const APP_VERSION = '4.79.0';
/** @type {string} 平台标识 */
const PLATFORM = 'pc';

// ──────────────────────────────────────────
// MockProvider — Plan B 降级（默认）
// ──────────────────────────────────────────

/**
 * Mock 签名提供者
 * Plan B 默认降级：返回空签名头
 */
class MockProvider {
  /**
   * 生成签名头（空实现）
   * @param {string} [url] - 请求 URL
   * @param {string} [method] - HTTP 方法
   * @param {string} [body] - 请求体
   * @returns {Promise<Record<string,string>>} 签名头
   */
  async sign(url, method, body) {
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

/**
 * 签名管理器
 * 当前始终使用 MockProvider（HTTP 签名通道已放弃）
 */
class SignatureManager {
  /**
   * @param {MockProvider} [provider] - 签名提供者
   */
  constructor(provider = new MockProvider()) {
    /** @type {MockProvider} 签名提供者 */
    this.provider = provider;
    /** @type {boolean} Plan B 是否激活 */
    this._planBActive = true;
  }

  /**
   * 生成完整的请求头
   * 当前始终使用 MockProvider（HTTP 签名通道已放弃）
   *
   * @param {string} url - 请求 URL
   * @param {string} method - HTTP 方法
   * @param {string} [body] - 请求体
   * @returns {Promise<Record<string,string>>} 请求头对象
   */
  async getHeaders(url, method, body) {
    try {
      return await this.provider.sign(url, method, body);
    } catch (err) {
      signatureLog.warn('签名生成失败，返回基础头', err);
      return new MockProvider().sign(url, method, body);
    }
  }

  /**
   * Plan B 是否已激活（始终返回 true）
   * @returns {boolean}
   */
  isPlanBActive() {
    return this._planBActive;
  }
}

// ──────────────────────────────────────────
// 默认实例
// ──────────────────────────────────────────

/** @type {SignatureManager} 默认签名管理器 */
const defaultSignatureManager = new SignatureManager(new MockProvider());

// ──────────────────────────────────────────
// 导出
// ──────────────────────────────────────────

export {
  MockProvider,
  SignatureManager,
  defaultSignatureManager,
};
