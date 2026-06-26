// scripts/config.mjs
// 共享配置模块 — 从环境变量或配置文件读取云效/飞书凭证
import { readFileSync, existsSync } from 'fs';
import { homedir } from 'os';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dir = dirname(fileURLToPath(import.meta.url));

function loadLocalEnv() {
  const envPath = join(__dir, '../.env.local');
  if (!existsSync(envPath)) return {};
  const content = readFileSync(envPath, 'utf8');
  const result = {};
  for (const line of content.split('\n')) {
    const m = line.match(/^([A-Z_]+)=(.*)/);
    if (m) result[m[1]] = m[2].trim().replace(/^["'`]|["'`]$/g, '');
  }
  return result;
}

function loadJsonConfig() {
  const configPath = join(homedir(), '.yunxiao-devops.json');
  if (!existsSync(configPath)) return {};
  try { return JSON.parse(readFileSync(configPath, 'utf8')); } catch { return {}; }
}

const localEnv = loadLocalEnv();
const jsonConfig = loadJsonConfig();

function get(envKey, jsonKey, fallback = '') {
  return process.env[envKey] || localEnv[envKey] || jsonConfig[jsonKey] || fallback;
}

export const TOKEN   = get('YUNXIAO_TOKEN',        'token');
export const ORG_ID  = get('YUNXIAO_ORG_ID',       'orgId');
export const USER_ID = get('YUNXIAO_USER_ID',      'userId');       // 云效用户 ID
export const OPEN_ID = get('FEISHU_USER_OPEN_ID',  'feishuOpenId'); // 飞书 open_id
export const DEFAULT_PROJECT_ID = get('YUNXIAO_PROJECT_ID', 'defaultProjectId');

export const YUNXIAO_TOKEN = TOKEN;

export function requireConfig() {
  if (!TOKEN)  throw new Error('缺少 YUNXIAO_TOKEN 配置。请设置环境变量或创建 .env.local 文件（参考 .env.local.example）。');
  if (!ORG_ID) throw new Error('缺少 YUNXIAO_ORG_ID 配置。请设置环境变量或创建 .env.local 文件（参考 .env.local.example）。');
}
