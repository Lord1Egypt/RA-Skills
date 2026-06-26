/**
 * 配置管理模块
 * 管理 TikTok Shop API 和飞书集成配置
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_DIR = path.join(
  process.env.HOME || process.env.USERPROFILE, 
  '.clawhub', 
  'tiktok-shop'
);
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');
const CREDENTIALS_FILE = path.join(CONFIG_DIR, 'credentials.json');

/**
 * 配置 schema
 */
const defaultConfig = {
  // TikTok Shop 配置
  tiktok: {
    apiKey: '',
    apiSecret: '',
    shopId: '',
    region: 'US',
    useMock: true // 默认使用 Mock API
  },
  
  // 飞书集成配置
  feishu: {
    enabled: false,
    appToken: '',
    tableId: '',
    webhookUrl: ''
  },
  
  // 账号管理
  accounts: [],
  currentAccount: null,
  
  // 通知配置
  notifications: {
    feishuWebhook: '',
    email: '',
    enabled: true
  },
  
  // 自动同步配置
  autoSync: {
    orders: {
      enabled: false,
      interval: 15 // 分钟
    },
    inventory: {
      enabled: false,
      interval: 60 // 分钟
    }
  },
  
  // 高级配置
  advanced: {
    apiTimeout: 30000,
    retryAttempts: 3,
    logLevel: 'info' // debug, info, warn, error
  }
};

/**
 * 初始化配置目录
 */
function initConfigDir() {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
    console.log(`✓ 配置目录已创建：${CONFIG_DIR}`);
  }
}

/**
 * 加载配置
 * @returns {Object} 配置对象
 */
export function loadConfig() {
  initConfigDir();
  
  if (!fs.existsSync(CONFIG_FILE)) {
    console.log('⚠️  配置文件不存在，将使用默认配置');
    return JSON.parse(JSON.stringify(defaultConfig));
  }
  
  try {
    const configContent = fs.readFileSync(CONFIG_FILE, 'utf-8');
    const config = JSON.parse(configContent);
    
    // 合并默认配置（确保新字段存在）
    return { ...defaultConfig, ...config, tiktok: { ...defaultConfig.tiktok, ...config.tiktok }, feishu: { ...defaultConfig.feishu, ...config.feishu } };
  } catch (error) {
    console.error('✗ 读取配置文件失败:', error.message);
    return JSON.parse(JSON.stringify(defaultConfig));
  }
}

/**
 * 保存配置
 * @param {Object} config - 配置对象
 */
export function saveConfig(config) {
  initConfigDir();
  
  try {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf-8');
    console.log(`✓ 配置已保存：${CONFIG_FILE}`);
    return true;
  } catch (error) {
    console.error('✗ 保存配置失败:', error.message);
    return false;
  }
}

/**
 * 加载敏感凭证（单独存储）
 * @returns {Object} 凭证对象
 */
export function loadCredentials() {
  if (!fs.existsSync(CREDENTIALS_FILE)) {
    return {};
  }
  
  try {
    const content = fs.readFileSync(CREDENTIALS_FILE, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error('✗ 读取凭证失败:', error.message);
    return {};
  }
}

/**
 * 保存敏感凭证
 * @param {Object} credentials - 凭证对象
 */
export function saveCredentials(credentials) {
  initConfigDir();
  
  try {
    fs.writeFileSync(CREDENTIALS_FILE, JSON.stringify(credentials, null, 2), 'utf-8');
    
    // 设置文件权限（仅所有者可读写）
    if (process.platform !== 'win32') {
      fs.chmodSync(CREDENTIALS_FILE, 0o600);
    }
    
    console.log(`✓ 凭证已保存：${CREDENTIALS_FILE}`);
    return true;
  } catch (error) {
    console.error('✗ 保存凭证失败:', error.message);
    return false;
  }
}

/**
 * 更新配置
 * @param {Object} updates - 配置更新
 */
export function updateConfig(updates) {
  const config = loadConfig();
  const newConfig = { ...config, ...updates };
  return saveConfig(newConfig);
}

/**
 * 验证配置
 * @param {Object} config - 配置对象
 * @returns {Object} 验证结果
 */
export function validateConfig(config) {
  const errors = [];
  const warnings = [];
  
  // TikTok 配置验证
  if (!config.tiktok.useMock) {
    if (!config.tiktok.apiKey) {
      errors.push('缺少 TikTok API Key');
    }
    if (!config.tiktok.apiSecret) {
      errors.push('缺少 TikTok API Secret');
    }
    if (!config.tiktok.shopId) {
      warnings.push('未设置 Shop ID，部分功能可能不可用');
    }
  }
  
  // 飞书配置验证
  if (config.feishu.enabled) {
    if (!config.feishu.appToken) {
      errors.push('飞书集成已启用但缺少 App Token');
    }
    if (!config.feishu.tableId) {
      errors.push('飞书集成已启用但缺少 Table ID');
    }
  }
  
  // 账号验证
  if (config.accounts.length === 0) {
    warnings.push('未添加任何 TikTok 账号');
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * 获取当前账号
 * @returns {Object|null} 当前账号信息
 */
export function getCurrentAccount() {
  const config = loadConfig();
  
  if (!config.currentAccount) {
    return null;
  }
  
  return config.accounts.find(acc => acc.username === config.currentAccount) || null;
}

/**
 * 设置当前账号
 * @param {string} username - 账号用户名
 */
export function setCurrentAccount(username) {
  const config = loadConfig();
  const account = config.accounts.find(acc => acc.username === username);
  
  if (!account) {
    throw new Error(`账号 ${username} 不存在`);
  }
  
  config.currentAccount = username;
  return saveConfig(config);
}

/**
 * 添加账号
 * @param {Object} account - 账号信息
 */
export function addAccount(account) {
  const config = loadConfig();
  
  // 检查是否已存在
  const exists = config.accounts.find(acc => acc.username === account.username);
  if (exists) {
    throw new Error(`账号 ${account.username} 已存在`);
  }
  
  config.accounts.push({
    ...account,
    addedAt: new Date().toISOString()
  });
  
  // 如果是第一个账号，自动设为当前账号
  if (config.accounts.length === 1) {
    config.currentAccount = account.username;
  }
  
  return saveConfig(config);
}

/**
 * 移除账号
 * @param {string} username - 账号用户名
 */
export function removeAccount(username) {
  const config = loadConfig();
  
  const index = config.accounts.findIndex(acc => acc.username === username);
  if (index === -1) {
    throw new Error(`账号 ${username} 不存在`);
  }
  
  config.accounts.splice(index, 1);
  
  // 如果移除的是当前账号，清空当前账号
  if (config.currentAccount === username) {
    config.currentAccount = config.accounts.length > 0 ? config.accounts[0].username : null;
  }
  
  return saveConfig(config);
}

/**
 * 列出所有账号
 * @returns {Array} 账号列表
 */
export function listAccounts() {
  const config = loadConfig();
  return config.accounts;
}

/**
 * 切换 Mock 模式
 * @param {boolean} useMock - 是否使用 Mock API
 */
export function toggleMockMode(useMock) {
  const config = loadConfig();
  config.tiktok.useMock = useMock;
  return saveConfig(config);
}

/**
 * 导出配置（用于备份）
 * @returns {string} 配置 JSON 字符串
 */
export function exportConfig() {
  const config = loadConfig();
  return JSON.stringify(config, null, 2);
}

/**
 * 导入配置（用于恢复）
 * @param {string} configJson - 配置 JSON 字符串
 */
export function importConfig(configJson) {
  try {
    const config = JSON.parse(configJson);
    return saveConfig(config);
  } catch (error) {
    throw new Error('配置格式错误: ' + error.message);
  }
}

export default {
  loadConfig,
  saveConfig,
  loadCredentials,
  saveCredentials,
  updateConfig,
  validateConfig,
  getCurrentAccount,
  setCurrentAccount,
  addAccount,
  removeAccount,
  listAccounts,
  toggleMockMode,
  exportConfig,
  importConfig
};
