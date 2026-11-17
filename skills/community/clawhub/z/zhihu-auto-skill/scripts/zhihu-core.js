/**
 * zhihu-core.js — 知乎自动化 Skill 核心模块
 *
 * 职责:
 * - Cookie 管理（加载/保存/AES-256-GCM 加密/解密）
 * - 浏览器初始化与持久化会话
 * - 通用错误重试 (withRetry)
 * - 登录状态检测
 * - 日志输出（统一通过 zhihu-logger）
 *
 * @module zhihu-core
 */

import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';
import { readFileSync, writeFileSync, existsSync, mkdirSync, chmodSync, renameSync } from 'fs';
import { homedir } from 'os';
import { resolve } from 'path';
import { chromium } from 'playwright';
import { coreLog, writeLog } from './zhihu-logger.js';

// ──────────────────────────────────────────
// 路径常量
// ──────────────────────────────────────────

/** @type {string} Cookie 加密存储目录 */
const COOKIE_DIR = resolve(homedir(), '.hermes', 'credentials');
/** @type {string} Cookie 加密文件路径 */
const COOKIE_PATH = resolve(COOKIE_DIR, 'zhihu-cookies.enc');
/** @type {string} 日志目录 */
const LOG_DIR = resolve(homedir(), '.hermes', 'logs', 'zhihu');
/** @type {string} 浏览器持久化数据目录 */
const BROWSER_DATA_DIR = resolve(homedir(), '.hermes', 'browser-data', 'zhihu');

// ──────────────────────────────────────────
// Cookie 管理
// ──────────────────────────────────────────

/** @type {string} 加密算法 */
const ALGORITHM = 'aes-256-gcm';
/** @type {number} IV 长度 */
const IV_LENGTH = 12;
/** @type {number} 认证标签长度 */
const AUTH_TAG_LENGTH = 16;

/**
 * 获取加密密钥（从环境变量）
 * @returns {Buffer} 32 字节密钥
 * @throws {Error} 当 ZHIHU_COOKIE_KEY 未设置或格式不正确时
 */
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

/**
 * 确保目录存在
 * @param {string} dirPath - 目录路径
 * @returns {void}
 */
function ensureDir(dirPath) {
  if (!existsSync(dirPath)) {
    mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * @typedef {object} CookieCheckResult
 * @property {boolean} valid - 是否有效
 * @property {number|null} expiresInDays - 剩余天数
 * @property {string} [reason] - 无效原因
 */

/**
 * 解密保存的 Cookie 文件
 * 文件格式: [12 bytes IV][16 bytes authTag][加密负载]
 *
 * @returns {Array<object>|null} Cookie 数组，解密失败返回 null
 */
function decryptCookies() {
  if (!existsSync(COOKIE_PATH)) return null;

  try {
    const data = readFileSync(COOKIE_PATH);
    if (data.length < IV_LENGTH + AUTH_TAG_LENGTH + 1) {
      coreLog.warn('Cookie 文件损坏或为空，跳过解密');
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
    coreLog.error('Cookie 解密失败', err);
    coreLog.warn('请确认 ZHIHU_COOKIE_KEY 正确，或清除 Cookie 文件后重新登录');
    return null;
  }
}

/**
 * 加密并保存 Cookie 到文件
 * 权限设为 0600，仅当前用户可读
 *
 * @param {Array<object>} cookies - Playwright 格式的 Cookie 数组
 * @returns {void}
 */
function encryptAndSaveCookies(cookies) {
  ensureDir(COOKIE_DIR);

  const iv = randomBytes(IV_LENGTH);
  const cipher = createCipheriv(ALGORITHM, getEncryptionKey(), iv);

  const plaintext = Buffer.from(JSON.stringify(cookies), 'utf-8');
  const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const authTag = cipher.getAuthTag();

  const output = Buffer.concat([iv, authTag, encrypted]);

  // 原子写入：先写 tmp 文件，再 rename，防止写入崩溃导致文件损坏
  const tmpPath = COOKIE_PATH + '.tmp';
  writeFileSync(tmpPath, output);
  try {
    chmodSync(tmpPath, 0o600);
  } catch {
    // Windows 不支持 chmod，静默忽略
  }
  renameSync(tmpPath, COOKIE_PATH);

  coreLog.info('Cookie 已加密保存', { sizeKB: (output.length / 1024).toFixed(1) });
}

/**
 * Cookie 密钥轮换（底层）
 * @param {string} oldKeyHex - 旧密钥（hex）
 * @param {string} newKeyHex - 新密钥（hex）
 * @throws {Error} 当旧密钥解密失败时
 * @returns {void}
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
  coreLog.info('Cookie 密钥轮换成功');
}

// ──────────────────────────────────────────
// Cookie 有效期检测
// ──────────────────────────────────────────

/**
 * 检查 Cookie 中 z_c0 的过期时间
 *
 * @returns {CookieCheckResult} 检测结果
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
 *
 * @returns {boolean} 是否通过预检
 */
function preflightCookieCheck() {
  const { valid, expiresInDays, reason } = checkCookieExpiry();

  if (!valid) {
    if (reason === 'no_cookie_file') {
      coreLog.warn('⚠️ 未找到保存的 Cookie 文件。请先手动登录知乎并导出 Cookie：');
      coreLog.warn('   node scripts/zhihu-export-cookie.js');
      return false;
    }
    if (reason === 'expired' || reason === 'z_c0_missing') {
      coreLog.warn('⚠️ Cookie 已过期，请重新登录并导出 Cookie');
      return false;
    }
  }

  if (reason === 'expiring_soon') {
    coreLog.warn(`⚠️ Cookie 将在 ${expiresInDays} 天后过期，请提前重新登录`);
  }

  return true;
}

// ──────────────────────────────────────────
// 浏览器管理
// ──────────────────────────────────────────

/** @type {import('playwright').Browser|null} */
let browserInstance = null;
/** @type {import('playwright').BrowserContext|null} */
let browserContext = null;

/**
 * @typedef {object} BrowserSession
 * @property {import('playwright').Browser} browser - 浏览器实例
 * @property {import('playwright').BrowserContext} context - 浏览器上下文
 */

/**
 * @typedef {object} InitBrowserOptions
 * @property {boolean} [headless=false] - 是否无头模式
 * @property {string} [proxy] - 代理服务器地址
 * @property {string} [userDataDir] - 自定义用户数据目录
 */

/**
 * 初始化持久化浏览器会话
 * 使用原生 Playwright + addInitScript 绕过反爬
 *
 * @param {InitBrowserOptions} [options] - 初始化选项
 * @returns {Promise<BrowserSession>} 浏览器会话对象
 * @throws {Error} 浏览器启动失败时抛出
 */
async function initBrowser({ headless = false, proxy, userDataDir } = {}) {
  if (browserInstance && browserInstance.isConnected()) {
    coreLog.info('复用已有浏览器会话');
    return { browser: browserInstance, context: browserContext };
  }

  const browserPath = userDataDir || BROWSER_DATA_DIR;
  ensureDir(browserPath);

  const launchOptions = {
    headless,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--disable-features=IsolateOrigins,site-per-process',
      '--no-sandbox',
      '--disable-setuid-sandbox',
    ],
  };

  if (proxy) {
    launchOptions.args.push(`--proxy-server=${proxy}`);
  }

  try {
    const browser = await chromium.launch(launchOptions);

    const context = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
      viewport: { width: 1920, height: 1080 },
      locale: 'zh-CN',
      timezoneId: 'Asia/Shanghai',
      permissions: [],
    });

    // 设置浏览器环境：隐藏自动化特征（替代 stealth 插件）
    await context.addInitScript(() => {
      // 1. 隐藏 navigator.webdriver
      delete navigator.webdriver;
      Object.defineProperty(navigator, 'webdriver', { get: () => false });

      // 2. 设置 Chrome 属性
      window.chrome = { runtime: {} };

      // 3. 绕过 permissions 检测
      const originalQuery = window.navigator.permissions.query;
      window.navigator.permissions.query = (parameters) =>
        parameters.name === 'notifications'
          ? Promise.resolve({ state: Notification.permission })
          : originalQuery(parameters);

      // 4. 设置插件列表（模拟正常浏览器）
      Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5],
      });

      // 5. 语言一致性
      Object.defineProperty(navigator, 'languages', {
        get: () => ['zh-CN', 'zh', 'en'],
      });
    });

    // 加载已保存的 Cookie
    const cookies = decryptCookies();
    if (cookies) {
      await context.addCookies(cookies);
      coreLog.info('Cookie 已加载', { count: cookies.length });
    }

    browserInstance = browser;
    browserContext = context;

    coreLog.info('浏览器会话已初始化');
    return { browser, context };
  } catch (err) {
    coreLog.error('浏览器初始化失败', err);
    throw err;
  }
}

/**
 * 持久化当前浏览器 Cookie 到加密文件
 *
 * @returns {Promise<void>}
 */
async function persistCookies() {
  if (!browserContext) {
    coreLog.warn('无活跃浏览器会话，无法保存 Cookie');
    return;
  }
  try {
    const cookies = await browserContext.cookies();
    encryptAndSaveCookies(cookies);
  } catch (err) {
    coreLog.error('Cookie 持久化失败', err);
  }
}

/**
 * 关闭浏览器并保存状态
 *
 * @returns {Promise<void>}
 */
async function closeBrowser() {
  if (browserContext) {
    await persistCookies();
    browserContext = null;
  }
  if (browserInstance) {
    await browserInstance.close();
    browserInstance = null;
    coreLog.info('浏览器会话已关闭');
  }
}

/**
 * 检查页面登录状态
 * 通过检测用户头像 DOM 元素判断
 *
 * @param {import('playwright').Page} page - Playwright 页面对象
 * @returns {Promise<boolean>} 是否已登录
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
    coreLog.error('登录检测失败', err);
    return false;
  }
}

/**
 * 等待用户手动登录
 * 轮询检测登录状态，超时后返回 false
 *
 * @param {import('playwright').Page} page - Playwright 页面对象
 * @param {number} [timeout=300000] - 超时毫秒（默认 5 分钟）
 * @returns {Promise<boolean>} 是否登录成功
 */
async function waitForLogin(page, timeout = 5 * 60 * 1000) {
  const startTime = Date.now();
  let isLoggedIn = await checkPageLogin(page);

  while (!isLoggedIn && (Date.now() - startTime) < timeout) {
    coreLog.info('等待用户登录...');
    await sleep(3000);
    isLoggedIn = await checkPageLogin(page);
  }

  if (isLoggedIn) {
    coreLog.info('✅ 登录成功，正在保存 Cookie...');
    await persistCookies();
    return true;
  }

  coreLog.error('❌ 登录超时');
  return false;
}

// ──────────────────────────────────────────
// 通用工具
// ──────────────────────────────────────────

/**
 * 异步延迟
 * @param {number} ms - 毫秒数
 * @returns {Promise<void>}
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 人机延迟 - 模拟人类操作间隔
 *
 * @param {number} [min=500] - 最小延迟（毫秒）
 * @param {number} [max=2000] - 最大延迟（毫秒）
 * @returns {Promise<void>}
 */
function humanDelay(min = 500, max = 2000) {
  const ms = Math.floor(Math.random() * (max - min + 1)) + min;
  return sleep(ms);
}

/**
 * @typedef {object} RetryOptions
 * @property {number} [maxRetries=3] - 最大重试次数
 * @property {number} [baseDelay=1000] - 基础延迟（毫秒）
 * @property {number} [maxDelay=30000] - 最大延迟（毫秒）
 * @property {(err: Error) => boolean} [retryOn] - 自定义重试判定
 * @property {(attempt: number, err: Error, delay: number) => void} [onRetry] - 重试回调
 * @property {string} [context=''] - 上下文标签
 */

/**
 * 统一重试包装器
 * 支持指数退避 + 自定义重试判定
 *
 * @template T
 * @param {() => Promise<T>} fn - 异步函数
 * @param {RetryOptions} [options] - 重试选项
 * @returns {Promise<T>} 函数执行结果
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
        coreLog.warn(
          `${context ? context + ' ' : ''}` +
          `第 ${attempt}/${maxRetries} 次重试，等待 ${Math.round(totalDelay / 1000)}s: ${err.message}`
        );
      }

      await sleep(totalDelay);
    }
  }

  throw lastError;
}

// ──────────────────────────────────────────
// Cookie 密钥轮换（高层接口）
// ──────────────────────────────────────────

/**
 * Cookie 密钥轮换（高层接口）
 * 使用环境变量 ZHIHU_COOKIE_KEY_OLD 和 ZHIHU_COOKIE_KEY_NEW
 *
 * @returns {Promise<void>}
 * @throws {Error} 当环境变量未设置时
 */
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
  coreLog.info('✅ Cookie 密钥轮换完成');
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
