/**
 * 账号配置模板
 * 
 * 使用方法：
 * 1. 复制此文件为 config.js
 * 2. 填入你的账号信息
 * 
 * ⚠️ 请勿将 config.js 上传到公开仓库！
 */

// 竞品账号列表
// 从小红书用户主页URL获取ID：xiaohongshu.com/user/profile/用户ID
const ACCOUNTS = [
  { name: '你的账号名', id: '小红书用户ID' },
  // 添加更多账号...
];

// 账号主页URL映射（用于跳转链接，可选）
const ACCOUNT_URLS = {
  '你的账号名': 'https://www.xiaohongshu.com/user/profile/小红书用户ID',
};

const fetchAccounts = () => Promise.resolve(ACCOUNTS);
const getAccountUrl = (name) => ACCOUNT_URLS[name] || null;

module.exports = { ACCOUNTS, fetchAccounts, getAccountUrl, ACCOUNT_URLS };
