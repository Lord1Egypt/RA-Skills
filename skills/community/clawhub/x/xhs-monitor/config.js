/**
 * 模块0: 账号配置
 * 
 * 使用说明：
 * 1. 复制 config.example.js 为 config.js（如果不存在）
 * 2. 填入自己的账号
 * 
 * ⚠️ 重要：请勿将包含真实账号信息的 config.js 上传到公开仓库！
 */

// 竞品账号列表
// 从 https://www.xiaohongshu.com/user/profile/ 获取用户ID
const ACCOUNTS = [
  { name: '示例账号1', id: '用户ID1' },
  { name: '示例账号2', id: '用户ID2' },
];

// 账号主页URL映射（用于跳转链接）
const ACCOUNT_URLS = {
  '示例账号1': 'https://www.xiaohongshu.com/user/profile/用户ID1',
  '示例账号2': 'https://www.xiaohongshu.com/user/profile/用户ID2',
};

const fetchAccounts = () => Promise.resolve(ACCOUNTS);
const getAccountUrl = (name) => ACCOUNT_URLS[name] || null;

module.exports = { ACCOUNTS, fetchAccounts, getAccountUrl, ACCOUNT_URLS };
