/**
 * zhihu-browser.js — 知乎浏览器自动化核心模块
 *
 * 基于 Playwright 的浏览器自动化，处理知乎写操作。
 * 包含：
 * - 反爬策略（C1：stealth + 行为模拟 + 指纹伪装）
 * - 持久化浏览器会话（I1）
 * - 页面操作封装（导航、等待、点击、输入）
 * - 浏览器崩溃恢复（G5）
 *
 * C1 | I1 | G5
 */

import { initBrowser, persistCookies, closeBrowser, humanDelay, sleep, withRetry, writeLog } from './zhihu-core.js';
import { readFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SELECTORS_PATH = resolve(__dirname, '..', 'config', 'selectors.json');

// ──────────────────────────────────────────
// 选择器管理
// ──────────────────────────────────────────

let selectorsCache = null;

function getSelectors() {
  if (selectorsCache) return selectorsCache;
  try {
    const raw = readFileSync(SELECTORS_PATH, 'utf-8');
    selectorsCache = JSON.parse(raw);
    return selectorsCache;
  } catch (err) {
    console.error('[zhihu-browser] 选择器文件加载失败:', err.message);
    return null;
  }
}

/**
 * 尝试依次匹配 primary → fallbacks
 * @param {import('playwright').Page} page
 * @param {object} selectorDef - { primary, fallbacks? }
 * @param {number} [timeout=5000]
 * @returns {Promise<import('playwright').Locator|null>}
 */
async function findElement(page, selectorDef, timeout = 5000) {
  if (!selectorDef) return null;
  const candidates = [selectorDef.primary, ...(selectorDef.fallbacks || [])];
  for (const sel of candidates) {
    try {
      const loc = page.locator(sel).first();
      await loc.waitFor({ timeout, state: 'attached' });
      if (await loc.isVisible().catch(() => false)) {
        if (sel !== selectorDef.primary) {
          console.warn(`[zhihu-browser] 选择器降级: "${selectorDef.primary}" → "${sel}"`);
        }
        return loc;
      }
    } catch {
      // 继续尝试下一个
    }
  }
  return null;
}

// ──────────────────────────────────────────
// 反爬策略
// ──────────────────────────────────────────

/**
 * 贝塞尔曲线鼠标移动
 * 模拟人类鼠标轨迹（非瞬时跳转）
 */
async function bezierMove(page, fromX, fromY, toX, toY, steps = 20) {
  const points = [];
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    // 加入随机扰动
    const x = fromX + (toX - fromX) * t + (Math.random() - 0.5) * 3;
    const y = fromY + (toY - fromY) * t + (Math.random() - 0.5) * 3;
    points.push({ x, y });
  }
  for (const p of points) {
    await page.mouse.move(p.x, p.y);
    await sleep(10 + Math.random() * 20);
  }
}

/**
 * 逐字输入（模拟人类打字节奏）
 */
async function typeLikeHuman(page, selector, text, delayMin = 60, delayMax = 200) {
  await page.locator(selector).click();
  await humanDelay(200, 500);
  for (const char of text) {
    await page.keyboard.type(char, { delay: delayMin + Math.floor(Math.random() * (delayMax - delayMin)) });
    // 偶尔停顿（模拟思考）
    if (Math.random() < 0.05) {
      await sleep(500 + Math.random() * 1000);
    }
  }
}

/**
 * 插入富文本（替代逐字输入，适用于大段内容）
 */
async function insertRichHTML(page, html) {
  await page.evaluate((htmlContent) => {
    const sel = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(document.body);
    sel.removeAllRanges();
    sel.addRange(range);
    document.execCommand('insertHTML', false, htmlContent);
  }, html);
}

/**
 * 模拟人类滚动
 */
async function scrollLikeHuman(page, distance, duration = 1000) {
  const steps = 8;
  const stepSize = distance / steps;
  const stepDelay = duration / steps;
  for (let i = 0; i < steps; i++) {
    await page.mouse.wheel(0, stepSize + (Math.random() - 0.5) * 20);
    await sleep(stepDelay * (0.8 + Math.random() * 0.4));
  }
}

// ──────────────────────────────────────────
// 浏览器会话管理
// ──────────────────────────────────────────

let browserSession = null;

/**
 * 获取或创建浏览器会话
 */
async function getSession(options = {}) {
  if (browserSession?.page?.isConnected?.()) {
    return browserSession;
  }

  const { browser, context } = await initBrowser({
    headless: options.headless ?? false,
    proxy: options.proxy,
  });

  const page = await context.newPage();

  // 设置 Cookie 持久化（页面关闭前自动保存）
  page.on('close', async () => {
    await persistCookies();
  });

  browserSession = { browser, context, page };
  return browserSession;
}

/**
 * 关闭浏览器会话
 */
async function closeSession() {
  if (browserSession) {
    await persistCookies();
    await browserSession.browser.close();
    browserSession = null;
    console.log('[zhihu-browser] 浏览器会话已关闭');
  }
}

/**
 * 浏览器崩溃恢复（G5）
 */
async function withCrashRecovery(fn, context, options = {}) {
  const maxRetries = options.maxRetries ?? 2;
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      const isCrash = err.message?.includes('crash') ||
                      err.message?.includes('closed') ||
                      err.message?.includes('detached') ||
                      err.message?.includes('Protocol error');
      if (!isCrash || attempt === maxRetries) {
        throw err;
      }
      console.warn(`[zhihu-browser] ⚠️ 浏览器异常 (第 ${attempt}/${maxRetries} 次): ${err.message}`);
      // 关闭旧会话
      if (browserSession) {
        try { await browserSession.browser.close(); } catch {}
        browserSession = null;
      }
      // 重新初始化
      await getSession();
      console.log('[zhihu-browser] 浏览器会话已恢复');
    }
  }
}

// ──────────────────────────────────────────
// 页面操作
// ──────────────────────────────────────────

/**
 * 安全导航到目标页面
 * 使用 load 而非 networkidle（Zhihu 有长轮询，networkidle 永不触发）
 */
async function navigateTo(page, url, options = {}) {
  const timeout = options.timeout ?? 30000;
  const waitUntil = options.waitUntil ?? 'load';
  await page.goto(url, { waitUntil, timeout });
  await humanDelay(1000, 2000);
}

/**
 * 通过选择器点击元素
 */
async function clickElement(page, selectorDef, options = {}) {
  const el = await findElement(page, selectorDef, options.timeout ?? 5000);
  if (!el) {
    throw new Error(`元素未找到: ${selectorDef?.primary}`);
  }
  // 获取元素中心位置用于贝塞尔鼠标移动
  const box = await el.boundingBox();
  if (box) {
    await bezierMove(page, 0, 0, box.x + box.width / 2, box.y + box.height / 2);
  }
  await el.click();
  await humanDelay(500, 1500);
}

/**
 * 检查登录状态
 */
async function checkLoginStatus(page) {
  const selectors = getSelectors();
  if (!selectors) return false;
  try {
    const avatar = await page.locator(selectors.login.avatar.primary).first().waitFor({ timeout: 3000 });
    return avatar !== null;
  } catch {
    return false;
  }
}

// ──────────────────────────────────────────
// Markdown → 知乎富文本（I2）
// ──────────────────────────────────────────

/**
 * 将 Markdown 转换为知乎可接受的 HTML 富文本
 * 支持：标题、列表、加粗、链接、代码块
 */
function markdownToZhihuHTML(md) {
  let html = md
    // 代码块 (```)
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    // 标题 (## → <h2>)
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // 加粗
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // 链接
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>')
    // 无序列表
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
    // 段落
    .replace(/\n\n/g, '</p><p>')
    .replace(/^(.+)$/gm, (match) => {
      if (match.startsWith('<')) return match;
      return `<p>${match}</p>`;
    });

  return html;
}

// ──────────────────────────────────────────
// 导出
// ──────────────────────────────────────────

export {
  // 选择器管理
  getSelectors,
  findElement,
  // 反爬策略
  bezierMove,
  typeLikeHuman,
  insertRichHTML,
  scrollLikeHuman,
  // 会话管理
  getSession,
  closeSession,
  withCrashRecovery,
  // 页面操作
  navigateTo,
  clickElement,
  checkLoginStatus,
  // 文本转换
  markdownToZhihuHTML,
  // 工具
  humanDelay,
  sleep,
  withRetry,
  writeLog,
};
