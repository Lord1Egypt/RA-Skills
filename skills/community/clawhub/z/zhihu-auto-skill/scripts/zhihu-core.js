/**
 * zhihu-core.js — 知乎自动化 Skill 核心模块
 *
 * 职责:
 * - Cookie 管理（加载/保存/AES-256-GCM 加密/解密）
 * - 浏览器初始化与持久化会话
 * - 通用错误重试 (withRetry)
 * - 登录状态检测
 * - 日志输出
 */

import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';
import { readFileSync, writeFileSync, existsSync, mkdirSync, chmodSync } from 'fs';
import { homedir } from 'os';
import { resolve } from 'path';
import { chromium } from 'playwright';
import { addExtra } from 'playwright-extra';
import stealthPlugin from 'puppeteer-extra-plugin-stealth';

// ──────────────────────────────────────────
// 路径常量
// ──────────────────────────────────────────

const COOKIE_DIR = resolve(homedir(), '.hermes', 'credentials');
const COOKIE_PATH = resolve(COOKIE_DIR, 'zhihu-cookies.enc');
const LOG_DIR = resolve(homedir(), '.hermes', 'logs', 'zhihu');
const BROWSER_DATA_DIR = resolve(homedir(), '.hermes', 'browser-data', 'zhihu');

// ──────────────────────────────────────────
// Cookie 管理
// ──────────────────────────────────────────

const ALGORITHM = 'aes-256-gcm';
const IV_LENGTH = 12;
const AUTH_TAG_LENGTH = 16;

function getEncryptionKey() {
  const key = process.env.ZHIHU_COOKIE_KEY;
  if (!key || key.length !== 64) {
    throw new Error(
      '环境变量 ZHIHU_COOKIE_KEY 未设置或格式不正确。\n' +
      '请设置 32 字节 (64 位 hex) 的加密密钥：\n' +
      '  export ZHIHU_COOKIE_KEY="$(openssl rand -hex 32)"'
    );
  }
  return Buffer.from(key, 'hex');
}

function ensureDir(dirPath) {
  if (!existsSync(dirPath)) {
    mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * 解密保存的 Cookie 文件
 * 文件格式: [12 bytes IV][16 bytes authTag][加密负载]
 */
function decryptCookies() {
  if (!existsSync(COOKIE_PATH)) return null;

  try {
    const data = readFileSync(COOKIE_PATH);
    if (data.length < IV_LENGTH + AUTH_TAG_LENGTH + 1) {
      console.warn('[zhihu-core] Cookie 文件损坏或为空，跳过解密');
      return null;
    }

    const iv = data.subarray(0, IV_LENGTH);
    const authTag = data.subarray(IV_LENGTH, IV_LENGTH + AUTH_TAG_LENGTH);
    const ciphertext = data.subarray(IV_LENGTH + AUTH_TAG_LENGTH);

    const decipher = createDecipheriv(ALGORITHM, getEncryptionKey(), iv);
    decipher.setAuthTag(authTag);

    const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
    return JSON.parse(decrypted.toString('utf-8'));
  } catch (err) {
    console.error('[zhihu-core] Cookie 解密失败:', err.message);
    console.error('[zhihu-core] 请确认 ZHIHU_COOKIE_KEY 正确，或清除 Cookie 文件后重新登录');
    return null;
  }
}

/**
 * 加密并保存 Cookie 到文件
 * 权限设为 0600，仅当前用户可读
 */
function encryptAndSaveCookies(cookies) {
  ensureDir(COOKIE_DIR);

  const iv = randomBytes(IV_LENGTH);
  const cipher = createCipheriv(ALGORITHM, getEncryptionKey(), iv);

  const plaintext = Buffer.from(JSON.stringify(cookies), 'utf-8');
  const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const authTag = cipher.getAuthTag();

  const output = Buffer.concat([iv, authTag, encrypted]);
  writeFileSync(COOKIE_PATH, output);

  // 权限 0600
  try {
    chmodSync(COOKIE_PATH, 0o600);
  } catch {
    // Windows 不支持 chmod，静默忽略
  }

  console.log(`[zhihu-core] Cookie 已加密保存 (${(output.length / 1024).toFixed(1)} KB)`);
}

/**
 * Cookie 密钥轮换
 */
function rotateCookieKey(oldKeyHex, newKeyHex) {
  const envKey = process.env.ZHIHU_COOKIE_KEY;
  process.env.ZHIHU_COOKIE_KEY = oldKeyHex;
  const cookies = decryptCookies();
  if (!cookies) {
    process.env.ZHIHU_COOKIE_KEY = envKey;
    throw new Error('旧密钥解密失败，轮换中止');
  }
  process.env.ZHIHU_COOKIE_KEY = newKeyHex;
  encryptAndSaveCookies(cookies);
  process.env.ZHIHU_COOKIE_KEY = envKey;
  console.log('[zhihu-core] Cookie 密钥轮换成功');
}

// ──────────────────────────────────────────
// Cookie 有效期检测
// ──────────────────────────────────────────

/**
 * 检查 Cookie 中 z_c0 的过期时间
 * 返回: { valid, expiresInDays }
 */
function checkCookieExpiry() {
  const cookies = decryptCookies();
  if (!cookies) {
    return { valid: false, expiresInDays: null, reason: 'no_cookie_file' };
  }

  // 查找 z_c0 cookie
  const zc0 = cookies.find(c => c.name === 'z_c0');
  if (!zc0) {
    return { valid: false, expiresInDays: null, reason: 'z_c0_missing' };
  }

  // 某些 cookie 有 expires 字段（Unix 时间戳，秒）
  if (!zc0.expires) {
    return { valid: true, expiresInDays: 365, reason: 'session_cookie' };
  }

  const expiresDate = new Date(zc0.expires * 1000);
  const now = new Date();
  const diffMs = expiresDate.getTime() - now.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays <= 0) {
    return { valid: false, expiresInDays: 0, reason: 'expired' };
  }
  if (diffDays <= 7) {
    return { valid: true, expiresInDays: diffDays, reason: 'expiring_soon' };
  }
  return { valid: true, expiresInDays: diffDays, reason: 'valid' };
}

/**
 * Cookie 全生命周期检测
 * 在每次启动时调用
 */
function preflightCookieCheck() {
  const { valid, expiresInDays, reason } = checkCookieExpiry();

  if (!valid) {
    if (reason === 'no_cookie_file') {
      console.warn('[zhihu-core] ⚠️ 未找到保存的 Cookie 文件。请先手动登录知乎并导出 Cookie：');
      console.warn('   node scripts/zhihu-export-cookie.js');
      return false;
    }
    if (reason === 'expired' || reason === 'z_c0_missing') {
      console.warn('[zhihu-core] ⚠️ Cookie 已过期，请重新登录并导出 Cookie');
      return false;
    }
  }

  if (reason === 'expiring_soon') {
    console.warn(`[zhihu-core] ⚠️ Cookie 将在 ${expiresInDays} 天后过期，请提前重新登录`);
  }

  return true;
}

// ──────────────────────────────────────────
// 浏览器管理
// ──────────────────────────────────────────

let browserInstance = null;
let browserContext = null;

/**
 * 初始化持久化浏览器会话
 * 使用 playwright-extra + stealth 插件绕过反爬
 */
async function initBrowser({ headless = false, proxy, userDataDir } = {}) {
  if (browserInstance && browserInstance.isConnected()) {
    console.log('[zhihu-core] 复用已有浏览器会话');
    return { browser: browserInstance, context: browserContext };
  }

  const browserPath = userDataDir || BROWSER_DATA_DIR;
  ensureDir(browserPath);

  const launchOptions = {
    headless,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--disable-features=IsolateOrigins,site-per-process',
      '--disable-web-security',
      '--no-sandbox',
      '--disable-setuid-sandbox',
    ],
  };

  if (proxy) {
    launchOptions.args.push(`--proxy-server=${proxy}`);
  }

  try {
    // 如果有 stealth 插件则使用，否则回退到原生 Playwright
    let browser;
    try {
      const playwright = addExtra(chromium);
      playwright.use(stealthPlugin());
      browser = await playwright.launch(launchOptions);
    } catch {
      console.log('[zhihu-core] playwright-extra 不可用，回退到原生 Playwright');
      browser = await chromium.launch(launchOptions);
    }

    const context = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
      viewport: { width: 1920, height: 1080 },
      locale: 'zh-CN',
      timezoneId: 'Asia/Shanghai',
      permissions: [],
    });

    // 加载已保存的 Cookie
    const cookies = decryptCookies();
    if (cookies) {
      await context.addCookies(cookies);
      console.log(`[zhihu-core] Cookie 已加载 (${cookies.length} 条)`);
    }

    browserInstance = browser;
    browserContext = context;

    console.log('[zhihu-core] 浏览器会话已初始化');
    return { browser, context };
  } catch (err) {
    console.error('[zhihu-core] 浏览器初始化失败:', err.message);
    throw err;
  }
}

/**
 * 持久化当前浏览器 Cookie 到加密文件
 */
async function persistCookies() {
  if (!browserContext) {
    console.warn('[zhihu-core] 无活跃浏览器会话，无法保存 Cookie');
    return;
  }
  try {
    const cookies = await browserContext.cookies();
    encryptAndSaveCookies(cookies);
  } catch (err) {
    console.error('[zhihu-core] Cookie 持久化失败:', err.message);
  }
}

/**
 * 关闭浏览器并保存状态
 */
async function closeBrowser() {
  if (browserContext) {
    await persistCookies();
    browserContext = null;
  }
  if (browserInstance) {
    await browserInstance.close();
    browserInstance = null;
    console.log('[zhihu-core] 浏览器会话已关闭');
  }
}

/**
 * 检查页面登录状态
 * 通过检测用户头像 DOM 元素判断
 */
async function checkPageLogin(page) {
  try {
    await page.goto('https://www.zhihu.com/', { waitUntil: 'domcontentloaded', timeout: 30000 });

    // 方法 1：检测用户头像
    const avatar = await page.$('.AppHeader-profileAvatar');
    if (avatar) return true;

    // 方法 2：检测登录按钮（未登录标志）
    const signinBtn = await page.$('.SignContainer-accountLogin');
    if (signinBtn) return false;

    // 方法 3：检测消息通知图标
    const notify = await page.$('.AppHeader-notifications');
    if (notify) return true;

    return false;
  } catch (err) {
    console.error('[zhihu-core] 登录检测失败:', err.message);
    return false;
  }
}

/**
 * 等待用户手动登录
 * 轮询检测登录状态，超时后返回 false
 */
async function waitForLogin(page, timeout = 5 * 60 * 1000) {
  const startTime = Date.now();
  let isLoggedIn = await checkPageLogin(page);

  while (!isLoggedIn && (Date.now() - startTime) < timeout) {
    console.log('[zhihu-core] 等待用户登录...');
    await sleep(3000);
    isLoggedIn = await checkPageLogin(page);
  }

  if (isLoggedIn) {
    console.log('[zhihu-core] ✅ 登录成功，正在保存 Cookie...');
    await persistCookies();
    return true;
  }

  console.error('[zhihu-core] ❌ 登录超时');
  return false;
}

// ──────────────────────────────────────────
// 通用工具
// ──────────────────────────────────────────

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 人机延迟 - 模拟人类操作间隔
 */
function humanDelay(min = 500, max = 2000) {
  const ms = Math.floor(Math.random() * (max - min + 1)) + min;
  return sleep(ms);
}

/**
 * 统一重试包装器
 * 支持指数退避 + 自定义重试判定
 */
async function withRetry(fn, options = {}) {
  const {
    maxRetries = 3,
    baseDelay = 1000,
    maxDelay = 30000,
    retryOn = (err) => true,
    onRetry = null,
    context = '',
  } = options;

  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;

      if (attempt === maxRetries || !retryOn(err)) {
        throw err;
      }

      const delay = Math.min(baseDelay * Math.pow(2, attempt - 1), maxDelay);
      const jitter = Math.floor(Math.random() * delay * 0.3);
      const totalDelay = delay + jitter;

      if (onRetry) {
        onRetry(attempt, err, totalDelay);
      } else {
        console.warn(
          `[zhihu-core]${context ? ` ${context}` : ''} ` +
          `第 ${attempt}/${maxRetries} 次重试，等待 ${Math.round(totalDelay / 1000)}s: ${err.message}`
        );
      }

      await sleep(totalDelay);
    }
  }

  throw lastError;
}

// ──────────────────────────────────────────
// 操作日志
// ──────────────────────────────────────────

/**
 * 写操作日志（JSONL 格式）
 * Schema: { timestamp, level, module, operation, status, duration_ms, cookie_status, error, details }
 */
function writeLog(entry) {
  ensureDir(LOG_DIR);

  const date = new Date().toISOString().slice(0, 10);
  const logFile = resolve(LOG_DIR, `${date}.jsonl`);

  const logEntry = {
    timestamp: entry.timestamp || new Date().toISOString(),
    level: entry.level || 'INFO',
    module: entry.module || 'zhihu-core',
    operation: entry.operation || 'unknown',
    status: entry.status || 'success',
    duration_ms: entry.duration_ms || 0,
    cookie_status: entry.cookie_status || 'unknown',
    error: entry.error || null,
    details: entry.details || {},
  };

  try {
    writeFileSync(logFile, JSON.stringify(logEntry) + '\n', { flag: 'a' });
  } catch (err) {
    console.error('[zhihu-core] 日志写入失败:', err.message);
  }
}

// ──────────────────────────────────────────
// Cookie 密钥轮换（高层接口）
// ──────────────────────────────────────────

async function rotateEncryptionKey() {
  const oldKey = process.env.ZHIHU_COOKIE_KEY_OLD;
  const newKey = process.env.ZHIHU_COOKIE_KEY_NEW;

  if (!oldKey || !newKey) {
    throw new Error(
      '密钥轮换需要设置环境变量:\n' +
      '  export ZHIHU_COOKIE_KEY_OLD="旧密钥"\n' +
      '  export ZHIHU_COOKIE_KEY_NEW="新密钥"'
    );
  }

  rotateCookieKey(oldKey, newKey);
  writeLog({
    level: 'INFO',
    module: 'zhihu-core',
    operation: 'rotate_cookie_key',
    status: 'success',
    details: { note: 'Cookie 加密密钥已轮换' },
  });
  console.log('[zhihu-core] ✅ Cookie 密钥轮换完成');
}

// ──────────────────────────────────────────
// 导出
// ──────────────────────────────────────────

export {
  // Cookie 管理
  decryptCookies,
  encryptAndSaveCookies,
  checkCookieExpiry,
  preflightCookieCheck,
  rotateCookieKey,
  rotateEncryptionKey,
  // 浏览器管理
  initBrowser,
  persistCookies,
  closeBrowser,
  checkPageLogin,
  waitForLogin,
  // 通用工具
  sleep,
  humanDelay,
  withRetry,
  writeLog,
  // 常量
  COOKIE_DIR,
  COOKIE_PATH,
  LOG_DIR,
};
