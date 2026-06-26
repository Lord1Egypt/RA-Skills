/**
 * OpenClaw / Agent 运行时环境加载
 *
 * 规则：
 * - 已在 process.env 中的键不覆盖（与 dotenv「不覆盖已存在变量」一致）
 * - 依次加载多个 .env，后加载的文件只补充尚未定义的键
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const _libDir = path.dirname(fileURLToPath(import.meta.url));

/**
 * @param {object} [opts]
 * @param {string} [opts.skillRoot] - 技能根目录（其下可有 .env）
 */
export function loadOpenClawEnv(opts = {}) {
  const skillRoot = opts.skillRoot || path.join(_libDir, '..', '..');
  /** @type {string[]} */
  const files = [];

  if (process.env.OPENCLAW_ENV_FILE) {
    files.push(process.env.OPENCLAW_ENV_FILE);
  }

  files.push(path.join(skillRoot, '.env'));

  const home = process.env.HOME || process.env.USERPROFILE || '';
  if (home) {
    files.push(path.join(home, '.openclaw', '.env'));
    files.push(path.join(home, '.workbuddy', '.env'));
  }

  const seen = new Set();
  for (const file of files) {
    if (!file || seen.has(file)) continue;
    seen.add(file);
    if (fs.existsSync(file)) {
      applyEnvFile(file);
    }
  }
}

/**
 * @param {string} filePath
 */
function applyEnvFile(filePath) {
  let raw;
  try {
    raw = fs.readFileSync(filePath, 'utf-8');
  } catch {
    return;
  }

  for (const line of raw.split(/\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;

    const eq = trimmed.indexOf('=');
    if (eq <= 0) continue;

    const key = trimmed.slice(0, eq).trim();
    let value = trimmed.slice(eq + 1).trim();
    if (!key || key.includes(' ')) continue;

    // 与 dotenv 一致：已存在于 process.env 则跳过
    if (Object.prototype.hasOwnProperty.call(process.env, key)) {
      continue;
    }

    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }

    process.env[key] = value;
  }
}

/** 阿里云 DashScope / 万相（封面等） */
export function resolveDashScopeKey() {
  return (
    process.env.DASHSCOPE_API_KEY ||
    process.env.QWEN_API_KEY ||
    process.env.ALIYUN_DASHSCOPE_API_KEY ||
    ''
  ).trim();
}

/** OpenAI 兼容 Chat Completions（含自建网关） */
export function resolveOpenAICompatibleKey() {
  return (
    process.env.OPENAI_API_KEY ||
    process.env.LLM_API_KEY ||
    process.env.OPENROUTER_API_KEY ||
    ''
  ).trim();
}

export function getOpenAICompatibleBaseUrl() {
  const base =
    process.env.OPENAI_BASE_URL ||
    process.env.LLM_BASE_URL ||
    'https://api.openai.com/v1';
  return base.replace(/\/$/, '');
}

export function getOpenAICompatibleModel() {
  return (
    process.env.OPENAI_MODEL ||
    process.env.LLM_MODEL ||
    'gpt-4o'
  ).trim();
}

export function getDashScopeChatModel() {
  return (
    process.env.DASHSCOPE_CHAT_MODEL ||
    process.env.QWEN_CHAT_MODEL ||
    'qwen-max'
  ).trim();
}

/** 微信公众号开发者 AppID（兼容多种命名） */
export function resolveWechatAppId() {
  return (
    process.env.WECHAT_APP_ID ||
    process.env.WECHAT_APPID ||
    ''
  ).trim();
}

export function resolveWechatAppSecret() {
  return (
    process.env.WECHAT_APP_SECRET ||
    process.env.WECHAT_SECRET ||
    ''
  ).trim();
}
