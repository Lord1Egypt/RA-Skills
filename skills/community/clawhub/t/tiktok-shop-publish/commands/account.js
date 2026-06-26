/**
 * 账号管理模块
 */

import { addAccount as addAccountConfig, listAccounts as listAccountsConfig, setCurrentAccount, getCurrentAccount, loadConfig } from './init.js';

/**
 * 添加账号
 */
export async function addAccount(options) {
  const config = loadConfig();

  console.log('👤 添加 TikTok 账号...');
  console.log(`  用户名：${options.username}`);
  console.log(`  地区：${options.region}`);

  try {
    addAccountConfig({
      username: options.username,
      region: options.region,
      cookie: options.cookie,
      addedAt: new Date().toISOString()
    });

    console.log(`✓ 账号 ${options.username} 添加成功`);

    return {
      success: true,
      username: options.username
    };
    
  } catch (error) {
    console.error('✗ 添加失败:', error.message);
    throw error;
  }
}

/**
 * 列出所有账号
 */
export async function listAccounts() {
  const config = loadConfig();
  const accounts = listAccountsConfig();
  const currentAccount = getCurrentAccount();

  console.log('📋 TikTok 账号列表:\n');

  if (accounts.length === 0) {
    console.log('  暂无账号，使用 add-account 命令添加');
    return { accounts: [] };
  }

  accounts.forEach((acc, index) => {
    const isCurrent = currentAccount?.username === acc.username;
    const marker = isCurrent ? '✓ ' : '  ';
    console.log(`${marker}${index + 1}. ${acc.username} (${acc.region})`);
    console.log(`   添加时间：${new Date(acc.addedAt).toLocaleString('zh-CN')}`);
  });

  return { accounts, current: currentAccount };
}

/**
 * 切换账号
 */
export async function switchAccount(username) {
  const config = loadConfig();

  console.log('🔄 切换账号...');
  console.log(`  目标账号：${username}`);

  try {
    setCurrentAccount(username);
    console.log(`✓ 已切换到账号 ${username}`);

    return {
      success: true,
      username
    };
    
  } catch (error) {
    console.error('✗ 切换失败:', error.message);
    throw error;
  }
}

/**
 * 获取当前账号（供其他模块使用）
 */
export function getCurrentAccount() {
  return getCurrentAccount();
}
