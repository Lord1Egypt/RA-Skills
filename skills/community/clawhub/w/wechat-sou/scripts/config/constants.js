/**
 * 应用常量配置
 */

module.exports = {
  /**
   * API 基础域名
   */
  BASE_URL: "www.guaikei.com",

  /**
   * 请求超时时间 (毫秒)
   */
  REQUEST_TIMEOUT: 20000,

  /**
   * 创建任务最大重试次数
   */
  CREATE_MAX_ATTEMPTS: 3,

  /**
   * 查询任务最大重试次数
   */
  QUERY_MAX_ATTEMPTS: 60,

  /**
   * 重试间隔时间 (毫秒)
   */
  RETRY_INTERVAL: 2000,

  /**
   * 技能版本号
   */
  VERSION: "1.0.0",
};
