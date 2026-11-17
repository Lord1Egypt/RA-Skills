'use strict';
/**
 * src/config.js — 配置读写 (与 xhs-dpt 采集 skill 单凭证共享)。
 *
 * 配置路径: ~/.xhs-platform/config.json (用户级, 升级/重装不丢; 与采集 skill 同一文件同一 token)。
 * 无 token 时直接 login --link 重新登录即可 (不做旧配置迁移)。
 * 优先级: --base-url/--token 参数 > 环境变量 > 配置文件 > 内置默认。
 */
const fs = require('fs');
const os = require('os');
const path = require('path');

const DEFAULT_BASE_URL = 'http://st.aidata366.com';
// 配置路径解析: XHS_CONFIG_PATH 环境变量 (完整文件路径) > ~/.xhs-platform/config.json。
// 用于测试隔离 / 多账号切换; 未设置时保持用户级默认路径 (升级/重装不丢)。
const CONFIG_PATH = process.env.XHS_CONFIG_PATH
  || path.join(os.homedir(), '.xhs-platform', 'config.json');
const CONFIG_DIR = path.dirname(CONFIG_PATH);

function ensureDir() {
  try {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  } catch { /* 目录已存在 */ }
  // 尽力收紧目录权限 (Windows 上 chmod 语义有限, 失败忽略, 不影响主流程)
  try {
    fs.chmodSync(CONFIG_DIR, 0o700);
  } catch { /* 不支持时忽略 */ }
}

/** 读取配置; 不存在/损坏按空配置。 */
function loadConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  } catch {
    return {};
  }
}

/** 合并写配置 (保留未涉及字段)。 */
function saveConfig(patch) {
  ensureDir();
  const next = { ...loadConfig(), ...patch };
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(next, null, 2) + '\n', 'utf8');
  // 配置文件含 token, 尽力收紧为仅本人可读写 (Windows 上 chmod 语义有限, 失败忽略)
  try {
    fs.chmodSync(CONFIG_PATH, 0o600);
  } catch { /* 不支持时忽略 */ }
  return next;
}

/** 解析生效配置。 */
function resolveConfig(overrides = {}) {
  const file = loadConfig();
  return {
    baseUrl: overrides.baseUrl || process.env.XHS_PLATFORM_BASE_URL || file.base_url || DEFAULT_BASE_URL,
    token: overrides.token !== undefined ? overrides.token : (file.token || ''),
    insecure: process.env.XHS_PLATFORM_INSECURE === '1' || file.insecure === true,
  };
}

/** token 脱敏。 */
function maskToken(token) {
  if (!token) return null;
  return token.length > 12 ? token.slice(0, 12) + '...' : token.slice(0, 4) + '...';
}

module.exports = {
  DEFAULT_BASE_URL, CONFIG_PATH, configPaths: { configPath: CONFIG_PATH },
  loadConfig, saveConfig, resolveConfig, maskToken,
};
