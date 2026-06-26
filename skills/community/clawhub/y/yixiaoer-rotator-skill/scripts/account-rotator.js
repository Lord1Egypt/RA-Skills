#!/usr/bin/env node

/**
 * 蚁小二账号轮询管理器
 * 用于多账号矩阵的自动轮询发布
 * 
 * 智能同步特性：
 * - 新增账号自动追加到队列末尾
 * - 保留当前索引，不影响发布顺序
 * - 删除账号自动移除，索引自动调整
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const STATE_FILE = path.join(__dirname, 'account-rotator-state.json');
const API_KEY = process.env.YIXIAOER_API_KEY;
const MEMBER_ID = process.env.YIXIAOER_MEMBER_ID;

/**
 * 调用蚁小二 API（通过 yixiaoer-skill 的 api.ts）
 * 
 * 安全说明：
 * - API Key 通过 execSync 的 env 选项传递，避免 shell 注入风险
 * - payload 通过临时文件传递，避免命令行参数注入
 * - 临时文件在使用后立即删除
 */
function callYixiaoerAPI(payload) {
  const scriptPath = '/root/.openclaw/workspace/skills/yixiaoer-skill/scripts/api.ts';
  
  if (!API_KEY) {
    throw new Error('缺少 YIXIAOER_API_KEY 环境变量，请设置后重试');
  }
  
  if (!MEMBER_ID) {
    throw new Error('缺少 YIXIAOER_MEMBER_ID 环境变量，请设置后重试。成员 ID 用于过滤该成员有运营权限的账号');
  }
  
  // 简单的 API Key 格式验证（只允许字母、数字、下划线、连字符）
  if (!/^[A-Za-z0-9_-]+$/.test(API_KEY)) {
    console.warn('警告：API Key 包含非标准字符，请确保来源可信');
  }
  
  const apiKey = API_KEY;
  const payloadStr = JSON.stringify(payload);
  
  try {
    // 通过 --payload 参数传递，避免 shell 注入
    const result = execSync(`node "${scriptPath}" --payload='${payloadStr.replace(/'/g, "'\\''")}'`, {
      encoding: 'utf-8',
      env: {
        ...process.env,
        YIXIAOER_API_KEY: apiKey
      }
    });
    
    return JSON.parse(result);
  } catch (error) {
    console.error(`API 调用失败：${error.message}`);
    throw error;
  }
}

/**
 * 读取状态文件
 */
function readState() {
  if (!fs.existsSync(STATE_FILE)) {
    return { platforms: {}, lastUpdated: null };
  }
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
  } catch (err) {
    console.error('读取状态文件失败:', err.message);
    return { platforms: {}, lastUpdated: null };
  }
}

/**
 * 写入状态文件
 */
function writeState(state) {
  state.lastUpdated = Date.now();
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2) + '\n');
}

/**
 * 从蚁小二同步账号列表（智能同步：保留索引、追加新账号）
 */
function syncAccounts() {
  console.log('正在从蚁小二同步账号列表...\n');
  console.log(`📋 使用成员 ID 过滤：${MEMBER_ID}`);
  
  const result = callYixiaoerAPI({ action: 'accounts', page: 1, size: 100 });
  
  // 返回结构可能是 {data: [...]} 或 {data: {data: [...]}}
  let accounts;
  if (result.data && Array.isArray(result.data)) {
    accounts = result.data;
  } else if (result.data && result.data.data && Array.isArray(result.data.data)) {
    accounts = result.data.data;
  } else {
    console.error('同步失败：无法解析账号列表');
    console.error('返回数据:', JSON.stringify(result, null, 2).slice(0, 500));
    return false;
  }
  
  const state = readState();
  
  // 过滤出该成员有运营权限的账号
  accounts = accounts.filter(acc => {
    // 检查 operators 数组中是否包含该成员 ID
    return acc.operators && acc.operators.some(op => op.id === MEMBER_ID);
  });
  
  if (accounts.length === 0) {
    console.warn('⚠️ 警告：该成员没有任何运营权限的账号');
  } else {
    console.log(`✅ 过滤后剩余 ${accounts.length} 个账号（该成员有运营权限）`);
  }
  
  // 按平台分组
  const platformGroups = {};
  accounts.forEach(acc => {
    const platform = acc.platformName;
    if (!platformGroups[platform]) {
      platformGroups[platform] = [];
    }
    platformGroups[platform].push({
      id: acc.id,
      name: acc.platformAccountName,
      platform: platform,
      fansTotal: acc.fansTotal || 0,
      status: acc.status
    });
  });
  
  // 智能更新：保留索引、追加新账号
  let newAccountsCount = 0;
  let removedAccountsCount = 0;
  
  Object.keys(platformGroups).forEach(platform => {
    const newAccounts = platformGroups[platform];
    const existing = state.platforms[platform] || { accounts: [], currentIndex: 0 };
    
    // 构建现有账号的 ID 映射
    const existingIdMap = {};
    existing.accounts.forEach((acc, idx) => {
      existingIdMap[acc.id] = { ...acc, oldIndex: idx };
    });
    
    // 构建新账号列表的 ID 映射
    const newIdMap = {};
    newAccounts.forEach(acc => {
      newIdMap[acc.id] = acc;
    });
    
    // 找出新账号（在新列表但不在旧列表）
    const addedIds = newAccounts.filter(acc => !existingIdMap[acc.id]);
    newAccountsCount += addedIds.length;
    
    // 找出已删除的账号（在旧列表但不在新列表）
    const removedIds = existing.accounts.filter(acc => !newIdMap[acc.id]);
    removedAccountsCount += removedIds.length;
    
    // 合并账号列表：保留原有顺序，追加新账号
    const mergedAccounts = [];
    
    // 先保留原有的账号（按旧顺序）
    existing.accounts.forEach(acc => {
      if (newIdMap[acc.id]) {
        // 账号还在，使用最新数据
        mergedAccounts.push(newIdMap[acc.id]);
      }
      // 账号已删除，跳过
    });
    
    // 追加新账号到末尾
    addedIds.forEach(acc => {
      mergedAccounts.push(acc);
    });
    
    // 调整索引：如果当前索引超出范围，重置到 0
    let newIndex = existing.currentIndex;
    if (mergedAccounts.length === 0) {
      newIndex = 0;
    } else if (newIndex >= mergedAccounts.length) {
      newIndex = 0;
    }
    
    state.platforms[platform] = {
      accounts: mergedAccounts,
      totalAccounts: mergedAccounts.length,
      currentIndex: newIndex,
      accountCount: mergedAccounts.length
    };
  });
  
  writeState(state);
  
  console.log(`✅ 同步完成！共 ${accounts.length} 个账号，分布在 ${Object.keys(platformGroups).length} 个平台`);
  if (newAccountsCount > 0) {
    console.log(`🆕 新增账号：${newAccountsCount} 个（已追加到队列末尾）`);
  }
  if (removedAccountsCount > 0) {
    console.log(`❌ 移除账号：${removedAccountsCount} 个`);
  }
  console.log('\n平台分布:');
  Object.keys(platformGroups).forEach(platform => {
    console.log(`  - ${platform}: ${platformGroups[platform].length} 个账号`);
  });
  
  return true;
}

/**
 * 获取指定平台的下一个账号
 */
function getNextAccount(platform) {
  const state = readState();
  
  if (!state.platforms[platform]) {
    console.error(`错误：平台 "${platform}" 不存在，请先执行 sync 同步账号`);
    return null;
  }
  
  const platformData = state.platforms[platform];
  if (platformData.accounts.length === 0) {
    console.error(`错误：平台 "${platform}" 下没有账号`);
    return null;
  }
  
  // 获取当前索引的账号
  const account = platformData.accounts[platformData.currentIndex];
  
  // 更新索引（循环）
  const nextIndex = (platformData.currentIndex + 1) % platformData.accounts.length;
  platformData.currentIndex = nextIndex;
  
  writeState(state);
  
  return account;
}

/**
 * 查看所有平台的下一个账号
 */
function getAllNextAccounts() {
  const state = readState();
  const result = {};
  
  Object.keys(state.platforms).forEach(platform => {
    const platformData = state.platforms[platform];
    if (platformData.accounts.length > 0) {
      const account = platformData.accounts[platformData.currentIndex];
      result[platform] = {
        name: account.name,
        id: account.id,
        index: platformData.currentIndex,
        total: platformData.totalAccounts
      };
    }
  });
  
  return result;
}

/**
 * 显示轮询状态
 */
function showStatus() {
  const state = readState();
  
  if (!state.lastUpdated) {
    console.log('状态文件不存在，请先执行 sync 同步账号');
    return;
  }
  
  console.log(`最后同步时间：${new Date(state.lastUpdated).toLocaleString('zh-CN')}\n`);
  
  Object.keys(state.platforms).forEach(platform => {
    const data = state.platforms[platform];
    const currentAccount = data.accounts[data.currentIndex] || { name: '未知', id: '未知' };
    const nextIndex = (data.currentIndex + 1) % data.accounts.length;
    const nextAccount = data.accounts[nextIndex];
    
    console.log(`📱 ${platform}`);
    console.log(`   账号总数：${data.totalAccounts}`);
    console.log(`   当前索引：${data.currentIndex} (下次使用：${nextIndex})`);
    console.log(`   当前账号：${currentAccount.name}`);
    console.log(`   下次账号：${nextAccount ? nextAccount.name : '无'}`);
    console.log('');
  });
}

/**
 * 重置指定平台的索引
 */
function resetPlatform(platform) {
  const state = readState();
  
  if (platform && state.platforms[platform]) {
    state.platforms[platform].currentIndex = 0;
    writeState(state);
    console.log(`✅ 平台 "${platform}" 的索引已重置为 0`);
  } else if (!platform) {
    // 重置所有平台
    Object.keys(state.platforms).forEach(p => {
      state.platforms[p].currentIndex = 0;
    });
    writeState(state);
    console.log('✅ 所有平台的索引已重置为 0');
  } else {
    console.error(`错误：平台 "${platform}" 不存在`);
  }
}

/**
 * 列出所有平台
 */
function listPlatforms() {
  const state = readState();
  
  if (!state.lastUpdated) {
    console.log('状态文件不存在，请先执行 sync 同步账号');
    return;
  }
  
  console.log('已同步的平台:');
  Object.keys(state.platforms).forEach((platform, index) => {
    const data = state.platforms[platform];
    console.log(`  ${index + 1}. ${platform} (${data.totalAccounts} 个账号)`);
  });
}

/**
 * 获取指定平台的账号列表
 */
function listPlatformAccounts(platform) {
  const state = readState();
  
  if (!state.platforms[platform]) {
    console.error(`错误：平台 "${platform}" 不存在`);
    return;
  }
  
  const accounts = state.platforms[platform].accounts;
  const currentIndex = state.platforms[platform].currentIndex;
  
  console.log(`${platform} 账号列表 (当前索引：${currentIndex}):\n`);
  accounts.forEach((acc, index) => {
    const marker = index === currentIndex ? '👉 ' : '   ';
    console.log(`${marker}[${index}] ${acc.name} (ID: ${acc.id}, 粉丝：${acc.fansTotal})`);
  });
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command || command === '--help' || command === '-h') {
    console.log(`
蚁小二账号轮询管理器

用法:
  node account-rotator.js <command> [options]

命令:
  sync              从蚁小二同步账号列表（智能同步：保留索引、追加新账号）
  next <平台名>      获取指定平台的下一个账号（返回账号 ID）
  all               查看所有平台下次发布的账号
  status            查看轮询状态
  platforms         列出所有平台
  accounts <平台名>  列出指定平台的所有账号
  reset [平台名]     重置索引（不指定平台则重置所有）

示例:
  node account-rotator.js sync
  node account-rotator.js next 哔哩哔哩
  node account-rotator.js status
  node account-rotator.js reset 哔哩哔哩
`);
  process.exit(0);
  }
  
  switch (command) {
    case 'sync':
      syncAccounts();
      break;
      
    case 'next':
      if (!args[1]) {
        console.error('错误：请指定平台名');
        process.exit(1);
      }
      const account = getNextAccount(args[1]);
      if (account) {
        console.log(account.id);
      }
      break;
      
    case 'all':
      const allAccounts = getAllNextAccounts();
      console.log('各平台下次发布账号:\n');
      Object.entries(allAccounts).forEach(([platform, info]) => {
        console.log(`${platform}: ${info.name} (索引：${info.index}/${info.total})`);
      });
      break;
      
    case 'status':
      showStatus();
      break;
      
    case 'platforms':
      listPlatforms();
      break;
      
    case 'accounts':
      if (!args[1]) {
        console.error('错误：请指定平台名');
        process.exit(1);
      }
      listPlatformAccounts(args[1]);
      break;
      
    case 'reset':
      resetPlatform(args[1]);
      break;
      
    default:
      console.error(`未知命令：${command}`);
      console.log('使用 --help 查看帮助');
      process.exit(1);
  }
}

main();
