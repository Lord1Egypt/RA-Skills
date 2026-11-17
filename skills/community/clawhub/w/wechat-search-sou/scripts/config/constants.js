let version = "unknown";
try {
  const pkg = require("../../package.json");
  if (pkg && typeof pkg.version === "string" && pkg.version) {
    version = pkg.version;
  }
} catch (_) {
  // package.json 缺失时仍应能输出错误信封
}

module.exports = {
  /**
   * API 基础域名（可用环境变量 GUAIKEI_API_HOST 覆盖）
   */
  BASE_URL: process.env.GUAIKEI_API_HOST || "www.guaikei.com",

  /**
   * 请求超时时间 (毫秒)
   */
  REQUEST_TIMEOUT: 20000,

  /**
   * 创建任务最大重试次数
   */
  CREATE_MAX_ATTEMPTS: 3,

  /**
   * 查询任务最大轮询次数（与 douyin-search-claw / MCP 对齐量级）
   */
  QUERY_MAX_ATTEMPTS: 20,

  /**
   * 重试/轮询基础间隔 (毫秒)；轮询退避上限见 request.pollTaskResult
   */
  RETRY_INTERVAL: 2000,

  /**
   * 技能版本号
   */
  VERSION: version,
};
