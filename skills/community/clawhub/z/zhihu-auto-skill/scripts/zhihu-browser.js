/**
 * zhihu-browser.js — 知乎浏览器自动化核心模块
 *
 * 基于 Playwright 的浏览器自动化，处理知乎写操作。
 * 包含：
 * - 浏览器行为模拟策略（C1：行为模拟）
 * - 持久化浏览器会话（I1）
 * - 页面操作封装（导航、等待、点击、输入）
 * - 浏览器崩溃恢复（G5）
 *
 * C1 | I1 | G5
 *
 * @module zhihu-browser
 */

import { initBrowser, persistCookies, closeBrowser, humanDelay, sleep, withRetry } from './zhihu-core.js';
import { browserLog, writeLog } from './zhihu-logger.js';
import { readFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
/** @type {string} 选择器配置文件路径 */
const SELECTORS_PATH = resolve(__dirname, '..', 'config', 'selectors.json');

// ──────────────────────────────────────────
// 选择器管理
// ──────────────────────────────────────────

/** @type {object|null} 选择器缓存 */
let selectorsCache = null;

/**
 * @typedef {object} SelectorDef
 * @property {string} primary - 主选择器
 * @property {string[]} [fallbacks] - 降级选择器列表
 */

/**
 * 获取当前选择器配置（含缓存）
 * @returns {object|null} 选择器配置对象，加载失败返回 null
 */
function getSelectors() {
  if (selectorsCache) return selectorsCache;
  try {
    const raw = readFileSync(SELECTORS_PATH, 'utf-8');
    selectorsCache = JSON.parse(raw);
    return selectorsCache;
  } catch (err) {
    browserLog.error('选择器文件加载失败', err);
    return null;
  }
}

/**
 * 尝试依次匹配 primary → fallbacks
 *
 * @param {import('playwright').Page} page - Playwright 页面对象
 * @param {SelectorDef} selectorDef - 选择器定义 { primary, fallbacks? }
 * @param {number} [timeout=5000] - 每个选择器的等待超时（毫秒）
 * @returns {Promise<import('playwright').Locator|null>} 匹配到的 Locator，未找到返回 null
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
          browserLog.warn(`选择器降级: "${selectorDef.primary}" → "${sel}"`);
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
 *
 * @param {import('playwright').Page} page - Playwright 页面对象
 * @param {number} fromX - 起始 X 坐标
 * @param {number} fromY - 起始 Y 坐标
 * @param {number} toX - 目标 X 坐标
 * @param {number} toY - 目标 Y 坐标
 * @param {number} [steps=20] - 插值步数
 * @returns {Promise<void>}
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
 *
 * @param {import('playwright').Page} page - Playwright 页面对象
 * @param {string} selector - 输入框选择器
 * @param {string} text - 要输入的文本
 * @param {number} [delayMin=60] - 最小字符间延迟（毫秒）
 * @param {number} [delayMax=200] - 最大字符间延迟（毫秒）
 * @returns {Promise<void>}
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
 *
 * @param {import('playwright').Page} page - Playwright 页面对象
 * @param {string} html - HTML 富文本内容
 * @returns {Promise<void>}
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
 *
 * @param {import('playwright').Page} page - Playwright 页面对象
 * @param {number} distance - 滚动距离（像素）
 * @param {number} [duration=1000] - 滚动持续时间（毫秒）
 * @returns {Promise<void>}
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

/** @type {{ browser: import('playwright').Browser, context: import('playwright').BrowserContext, page: import('playwright').Page }|null} 浏览器会话 */
let browserSession = null;

/**
 * @typedef {object} SessionOptions
 * @property {boolean} [headless] - 是否无头模式
 * @property {string} [proxy] - 代理地址
 */

/**
 * 获取或创建浏览器会话
 *
 * @param {SessionOptions} [options] - 会话选项
 * @returns {Promise<{ browser: import('playwright').Browser, context: import('playwright').BrowserContext, page: import('playwright').Page }>} 浏览器会话
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
 *
 * @returns {Promise<void>}
 */
async function closeSession() {
  if (browserSession) {
    await persistCookies();
    await browserSession.browser.close();
    browserSession = null;
    browserLog.info('浏览器会话已关闭');
  }
}

/**
 * @typedef {object} CrashRecoveryOptions
 * @property {number} [maxRetries=2] - 最大重试次数
 */

/**
 * 浏览器崩溃恢复（G5）
 * 捕获浏览器崩溃异常并自动重建会话
 *
 * @template T
 * @param {() => Promise<T>} fn - 执行的异步函数
 * @param {string} context - 操作上下文名
 * @param {CrashRecoveryOptions} [options] - 恢复选项
 * @returns {Promise<T>} 函数执行结果
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
      browserLog.warn(`⚠️ 浏览器异常 (第 ${attempt}/${maxRetries} 次): ${err.message}`);
      // 关闭旧会话
      if (browserSession) {
        try { await browserSession.browser.close(); } catch {}
        browserSession = null;
      }
      // 重新初始化
      await getSession();
      browserLog.info('浏览器会话已恢复');
    }
  }
}

// ──────────────────────────────────────────
// 页面操作
// ──────────────────────────────────────────

/**
 * @typedef {object} NavigateOptions
 * @property {number} [timeout=30000] - 导航超时（毫秒）
 * @property {'load'|'domcontentloaded'|'networkidle'} [waitUntil='load'] - 等待策略
 */

/**
 * 安全导航到目标页面
 * 使用 load 而非 networkidle（Zhihu 有长轮询，networkidle 永不触发）
 *
 * @param {import('playwright').Page} page - Playwright 页面对象
 * @param {string} url - 目标 URL
 * @param {NavigateOptions} [options] - 导航选项
 * @returns {Promise<void>}
 */
async function navigateTo(page, url, options = {}) {
  const timeout = options.timeout ?? 30000;
  const waitUntil = options.waitUntil ?? 'load';
  await page.goto(url, { waitUntil, timeout });
  await humanDelay(1000, 2000);
}

/**
 * @typedef {object} ClickOptions
 * @property {number} [timeout=5000] - 元素查找超时（毫秒）
 */

/**
 * 通过选择器点击元素（含贝塞尔鼠标移动）
 *
 * @param {import('playwright').Page} page - Playwright 页面对象
 * @param {SelectorDef} selectorDef - 选择器定义
 * @param {ClickOptions} [options] - 点击选项
 * @returns {Promise<void>}
 * @throws {Error} 当元素未找到时
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
 *
 * @param {import('playwright').Page} page - Playwright 页面对象
 * @returns {Promise<boolean>} 是否已登录
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
 * 支持：标题、加粗、斜体、链接、无序列表、有序列表、任务列表、
 *       引用块、行内代码、删除线、图片、表格、代码块、段落
 *
 * @param {string} md - Markdown 文本
 * @returns {string} 知乎富文本 HTML
 */
function markdownToZhihuHTML(md) {
  let html = md

    // ── 代码块 (```) ── 优先处理，保护内容不被后续正则干扰
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')

    // ── 引用块 (> quote) ── 块级，带 <p> 保持段落结构
    .replace(/^> (.+)$/gm, '<blockquote><p>$1</p></blockquote>')

    // ── 任务列表 (- [x] / - [ ]) ── 用临时标记避免与无序列表混淆
    .replace(/^- \[x\] (.+)$/gim, '<tmp-task data-checked>$1</tmp-task>')
    .replace(/^- \[ \] (.+)$/gim, '<tmp-task>$1</tmp-task>')

    // ── 有序列表 (1. item) ── 用临时标记以便分组
    .replace(/^\d+\. (.+)$/gm, '<tmp-ol>$1</tmp-ol>')

    // ── 无序列表 (- item) ──
    .replace(/^- (.+)$/gm, '<tmp-ul>$1</tmp-ul>')

    // ── 标题 (## → <h2>)
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>');

  // ── 表格 (| col1 | col2 |) ── 整块处理，支持表头
  html = html.replace(/(^\|.+\|\n?)+/gm, (tableBlock) => {
    const lines = tableBlock.trim().split('\n');
    // 分隔行：每个单元格只包含 - : 空格
    const isSepRow = (line) => line.split('|').slice(1, -1).every(c => /^[\s:-]+$/.test(c.trim()));
    const hasHeader = lines.length > 1 && isSepRow(lines[1]);
    let tableHtml = '<table>';
    lines.forEach((line, idx) => {
      if (hasHeader && idx === 1) return; // 跳过分隔行
      const cells = line.split('|').slice(1, -1).map(s => s.trim());
      const tag = (hasHeader && idx === 0) ? 'th' : 'td';
      tableHtml += '<tr>';
      cells.forEach(c => { tableHtml += `<${tag}>${c}</${tag}>`; });
      tableHtml += '</tr>';
    });
    return tableHtml + '</table>';
  });

  // ── 合并相邻引用块 ── 需在段落处理之前
  html = html.replace(/<\/blockquote>\n?<blockquote>/g, '\n');

  // ── 包装有序列表 ── 先于无序列表，避免交叉匹配
  html = html.replace(/(<tmp-ol>.*?<\/tmp-ol>\n?)+/g, (match) => {
    return '<ol>' + match.replace(/tmp-ol>/g, 'li>') + '</ol>';
  });

  // ── 包装任务列表和无序列表 ── 用统一 <ul> 包裹
  html = html.replace(/(<(?:tmp-task|tmp-ul)[^>]*>.*?<\/(?:tmp-task|tmp-ul)>\n?)+/g, (match) => {
    let inner = match
      .replace(/<tmp-task data-checked>/g, '<li class="task-list-item"><input type="checkbox" checked="" disabled> ')
      .replace(/<tmp-task>/g, '<li class="task-list-item"><input type="checkbox" disabled> ')
      .replace(/<tmp-ul>/g, '<li>')
      .replace(/<\/(?:tmp-task|tmp-ul)>/g, '</li>');
    return '<ul>' + inner + '</ul>';
  });

  // ── 行内代码 (`code`)
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>')

  // ── 删除线 (~~text~~)
    .replace(/~~(.+?)~~/g, '<del>$1</del>')

  // ── 加粗 + 斜体
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')

  // ── 图片 (![alt](url)) ── 在链接之前，用 <figure> 包裹符合知乎编辑器结构
    .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<figure><img src="$2" alt="$1" referrerpolicy="no-referrer"></figure>')

  // ── 链接 ([text](url))
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')

  // ── 段落 ── 最后处理，跳过已标记的 HTML 块
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
