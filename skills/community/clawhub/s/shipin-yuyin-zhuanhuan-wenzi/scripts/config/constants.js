const pkg = require("../../package.json");
module.exports = {
  BASE_URL: "www.guaikei.com",
  REQUEST_TIMEOUT: 20000, // 接口请求超时（毫秒）
  UPLOAD_TIMEOUT: 120000, // 上传空闲超时（毫秒），数据持续发送时不会触发
  CREATE_MAX_ATTEMPTS: 3, // 创建操作最大重试次数
  UPLOAD_MAX_ATTEMPTS: 3, // 上传最大重试次数
  QUERY_MAX_ATTEMPTS: 30, // 查询视频文案最大轮询次数
  RETRY_INTERVAL: 2000, // 重试基础间隔（毫秒）
  RETRY_MAX_INTERVAL: 30000, // 重试与轮询间隔上限（毫秒）
  EXPIRE_TIME: 60 * 60 * 24, // 24 小时：tmp 清理和 pending 续传共用这一期限
  VERSION: pkg.version,
};
