import dotenv from 'dotenv';
dotenv.config();

/**
 * AI考试系统配置文件
 */
export const config = {
  // API基础配置
  baseUrl: process.env.BASE_URL,

  // 应用凭证（需要用户配置）
  appKey: process.env.APP_KEY,
  appSecret: process.env.APP_SECRET,
  corpId: process.env.CORP_ID,
  deptUserId: process.env.DEPT_USER_ID,

  // 缓存access_token
  accessToken: null,
  tokenExpireTime: null,

  // 默认配置
  defaults: {
    pageSize: 10,
    examType: 'normal',
    passScoreRatio: 0.6 // 及格分数比例
  }
};

/**
 * 更新配置
 */
export function updateConfig(newConfig) {
  Object.assign(config, newConfig);
}
