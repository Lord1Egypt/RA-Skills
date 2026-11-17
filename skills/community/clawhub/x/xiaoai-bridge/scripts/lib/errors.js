/**
 * 共享错误类型。
 *
 * 单独成文件是为了让 core.js 与 state.js 共用同一个 ConfigError，
 * 又不会形成 ESM 循环依赖（state.js 不依赖 core.js）。
 */

export class ConfigError extends Error {
  constructor(message) {
    super(message);
    this.name = "ConfigError";
    this.code = "CONFIG_ERROR";
  }
}

/**
 * Jev 判定服务错误。category 用于降级决策：
 * - auth：密钥无效/未获权限（401/403），属配置错误，进入长冷却；
 * - rate_limit：限流（429）；
 * - server：服务端故障（5xx）；
 * - request：请求被拒（4xx 其它，如 413/422）；
 * - network：网络不可达；
 * - timeout：请求超时；
 * - protocol：响应不符合约定（缺字段/非法 JSON）。
 */
export class JevError extends Error {
  constructor(message, { category = "network", status, traceId } = {}) {
    super(message);
    this.name = "JevError";
    this.code = "JEV_ERROR";
    this.category = category;
    this.status = status;
    this.traceId = traceId;
  }
}
