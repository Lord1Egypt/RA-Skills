/**
 * xhs-core.js - 小红书 Windows 原生核心库
 * 基于 Playwright + XHS Web API，纯 Node.js，无需任何外部二进制
 *
 * 依赖: playwright (npm install)
 * 运行环境: Windows 10/11, Node.js 18+
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// ── 配置 ──────────────────────────────────────────────────────────────────
const DATA_DIR = path.join(process.env.USERPROFILE, '.xiaohongshu-win');
const COOKIE_FILE = path.join(DATA_DIR, 'cookies.json');
const STATE_FILE = path.join(DATA_DIR, 'browser-state.json');

const XHS_BASE = 'https://www.xiaohongshu.com';
const XHS_API  = 'https://edith.xiaohongshu.com';

if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

// ── Cookie 管理 ───────────────────────────────────────────────────────────
function loadCookies() {
  if (!fs.existsSync(COOKIE_FILE)) return null;
  try { return JSON.parse(fs.readFileSync(COOKIE_FILE, 'utf8')); }
  catch { return null; }
}

function saveCookies(cookies) {
  fs.writeFileSync(COOKIE_FILE, JSON.stringify(cookies, null, 2), 'utf8');
}

function isLoggedIn() {
  const cookies = loadCookies();
  if (!cookies) return false;
  const web_session = cookies.find(c => c.name === 'web_session');
  if (!web_session) return false;
  // 检查过期时间
  if (web_session.expires && web_session.expires < Date.now() / 1000) return false;
  return true;
}

// ── 浏览器启动 ────────────────────────────────────────────────────────────
async function launchBrowser(headless = true) {
  const opts = {
    headless,
    args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'],
  };
  // 使用持久化用户数据目录，保持登录状态
  const userDataDir = path.join(DATA_DIR, 'browser-profile');
  const context = await chromium.launchPersistentContext(userDataDir, {
    ...opts,
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    locale: 'zh-CN',
  });
  return context;
}

// ── 登录 ──────────────────────────────────────────────────────────────────
async function login() {
  console.log('[*] 启动浏览器，请扫码登录小红书...');
  const context = await launchBrowser(false); // 有头模式，用户可见
  const page = await context.newPage();

  await page.goto(`${XHS_BASE}/login`, { waitUntil: 'domcontentloaded' });
  console.log('[*] 浏览器已打开，请在窗口中扫码或账号密码登录');
  console.log('[*] 登录成功后会自动保存 Cookie，请勿关闭浏览器...');

  // 等待登录成功（检测到 web_session cookie）
  let loggedIn = false;
  const timeout = 120000; // 2分钟超时
  const start = Date.now();

  while (!loggedIn && Date.now() - start < timeout) {
    await page.waitForTimeout(2000);
    const cookies = await context.cookies();
    const session = cookies.find(c => c.name === 'web_session');
    if (session) {
      loggedIn = true;
      saveCookies(cookies);
      console.log('[OK] 登录成功！Cookie 已保存');
      console.log(`[*] 用户数据目录: ${path.join(DATA_DIR, 'browser-profile')}`);
    }
  }

  await context.close();
  if (!loggedIn) {
    console.error('[!] 登录超时（2分钟），请重试');
    process.exit(1);
  }
}

// ── HTTP 请求（带 Cookie）────────────────────────────────────────────────
function buildHeaders(cookies) {
  const cookieStr = cookies.map(c => `${c.name}=${c.value}`).join('; ');
  const webSession = cookies.find(c => c.name === 'web_session');
  const a1 = cookies.find(c => c.name === 'a1');
  const webId = cookies.find(c => c.name === 'webId');

  return {
    'Cookie': cookieStr,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.xiaohongshu.com/',
    'Origin': 'https://www.xiaohongshu.com',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'x-s': '',  // 签名（通过浏览器注入获取）
    'x-t': String(Date.now()),
  };
}

// 通过 Playwright 执行带签名的请求（绕过反爬）
async function apiRequest(endpoint, method = 'GET', body = null) {
  const cookies = loadCookies();
  if (!cookies) throw new Error('未登录，请先运行 login 命令');

  const context = await launchBrowser(true);
  const page = await context.newPage();

  // 注入 cookies
  await context.addCookies(cookies);
  await page.goto(XHS_BASE, { waitUntil: 'domcontentloaded' });

  // 在页面上下文中执行 fetch（自动携带签名和 cookie）
  const result = await page.evaluate(async ({ endpoint, method, body, apiBase }) => {
    const url = apiBase + endpoint;
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
    };
    if (body) opts.body = JSON.stringify(body);
    const resp = await fetch(url, opts);
    const data = await resp.json();
    return { status: resp.status, data };
  }, { endpoint, method, body, apiBase: XHS_API });

  // 保存最新 cookies
  const newCookies = await context.cookies();
  if (newCookies.length > 0) saveCookies(newCookies);

  await context.close();
  return result;
}

// ── 搜索 ──────────────────────────────────────────────────────────────────
async function search(keyword, limit = 20) {
  console.log(`[*] 搜索: ${keyword}`);

  const cookies = loadCookies();
  if (!cookies) { console.error('[!] 未登录'); process.exit(1); }

  const context = await launchBrowser(true);
  const page = await context.newPage();
  await context.addCookies(cookies);

  // 拦截 API 响应
  const results = [];
  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('/api/sns/web/v1/search/notes') || url.includes('/api/sns/web/v1/feed')) {
      try {
        const json = await response.json();
        if (json.data && json.data.items) {
          results.push(...json.data.items);
        }
      } catch {}
    }
  });

  // 导航到搜索页
  const searchUrl = `${XHS_BASE}/search_result?keyword=${encodeURIComponent(keyword)}&source=web_explore_feed`;
  await page.goto(searchUrl, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  // 保存最新 cookies
  const newCookies = await context.cookies();
  if (newCookies.length > 0) saveCookies(newCookies);

  await context.close();

  if (results.length === 0) {
    // 备用：直接解析页面 DOM
    console.log('[*] API 拦截无结果，尝试 DOM 解析...');
    return await searchViaDom(keyword, limit);
  }

  return results.slice(0, limit);
}

// DOM 解析备用方案
async function searchViaDom(keyword, limit = 20) {
  const cookies = loadCookies();
  const context = await launchBrowser(true);
  const page = await context.newPage();
  await context.addCookies(cookies);

  const searchUrl = `${XHS_BASE}/search_result?keyword=${encodeURIComponent(keyword)}&source=web_explore_feed`;
  await page.goto(searchUrl, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  const notes = await page.evaluate(() => {
    const items = [];
    // 小红书搜索结果卡片选择器
    const cards = document.querySelectorAll('[data-v-a264b01a] .note-item, .note-item, section.note-item');
    cards.forEach(card => {
      const titleEl = card.querySelector('.title, .footer .title span');
      const authorEl = card.querySelector('.author .name, .author-wrapper .name');
      const likeEl = card.querySelector('.like-wrapper .count, .interactions .like .count');
      const linkEl = card.querySelector('a[href*="/explore/"]');
      const imgEl = card.querySelector('img');

      if (titleEl || linkEl) {
        items.push({
          title: titleEl ? titleEl.textContent.trim() : '',
          author: authorEl ? authorEl.textContent.trim() : '',
          likes: likeEl ? likeEl.textContent.trim() : '0',
          url: linkEl ? linkEl.href : '',
          cover: imgEl ? imgEl.src : '',
        });
      }
    });
    return items;
  });

  const newCookies = await context.cookies();
  if (newCookies.length > 0) saveCookies(newCookies);
  await context.close();

  return notes.slice(0, limit);
}

// ── 获取帖子详情 ──────────────────────────────────────────────────────────
async function getNoteDetail(noteUrl) {
  console.log(`[*] 获取帖子详情: ${noteUrl}`);
  const cookies = loadCookies();
  if (!cookies) { console.error('[!] 未登录'); process.exit(1); }

  const context = await launchBrowser(true);
  const page = await context.newPage();
  await context.addCookies(cookies);

  let detail = null;

  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('/api/sns/web/v1/feed') || url.includes('/api/sns/web/v4/note/feed')) {
      try {
        const json = await response.json();
        if (json.data && json.data.items && json.data.items[0]) {
          detail = json.data.items[0];
        }
      } catch {}
    }
  });

  await page.goto(noteUrl, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  if (!detail) {
    // DOM 解析备用
    detail = await page.evaluate(() => {
      const title = document.querySelector('#detail-title')?.textContent?.trim() || '';
      const desc = document.querySelector('#detail-desc')?.textContent?.trim() || '';
      const author = document.querySelector('.author-wrapper .username')?.textContent?.trim() || '';
      const likes = document.querySelector('.like-wrapper .count')?.textContent?.trim() || '0';
      const collects = document.querySelector('.collect-wrapper .count')?.textContent?.trim() || '0';
      const comments = [];
      document.querySelectorAll('.comment-item').forEach(el => {
        const user = el.querySelector('.author .name')?.textContent?.trim() || '';
        const content = el.querySelector('.content')?.textContent?.trim() || '';
        const like = el.querySelector('.like .count')?.textContent?.trim() || '0';
        if (content) comments.push({ user, content, likes: like });
      });
      return { title, desc, author, likes, collects, comments };
    });
  }

  const newCookies = await context.cookies();
  if (newCookies.length > 0) saveCookies(newCookies);
  await context.close();

  return detail;
}

// ── 发布笔记 ──────────────────────────────────────────────────────────────
async function publishNote(title, content, imagePaths = []) {
  if (title.length > 20) { console.error('[!] 标题不能超过20字'); process.exit(1); }
  if (content.length > 1000) { console.error('[!] 正文不能超过1000字'); process.exit(1); }

  console.log(`[*] 准备发布笔记: ${title}`);
  const cookies = loadCookies();
  if (!cookies) { console.error('[!] 未登录'); process.exit(1); }

  const context = await launchBrowser(false); // 有头，方便观察
  const page = await context.newPage();
  await context.addCookies(cookies);

  await page.goto('https://creator.xiaohongshu.com/publish/publish', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);

  // 上传图片
  if (imagePaths.length > 0) {
    const uploadInput = await page.$('input[type="file"]');
    if (uploadInput) {
      await uploadInput.setInputFiles(imagePaths);
      await page.waitForTimeout(3000);
      console.log(`[*] 已上传 ${imagePaths.length} 张图片`);
    }
  }

  // 填写标题
  const titleInput = await page.$('[placeholder*="标题"], .title-input input, #title');
  if (titleInput) {
    await titleInput.click();
    await titleInput.fill(title);
  }

  // 填写正文
  const contentInput = await page.$('[placeholder*="正文"], .content-input, #content, .ql-editor');
  if (contentInput) {
    await contentInput.click();
    await contentInput.fill(content);
  }

  await page.waitForTimeout(1000);

  // 点击发布
  const publishBtn = await page.$('button:has-text("发布"), .publish-btn');
  if (publishBtn) {
    await publishBtn.click();
    await page.waitForTimeout(3000);
    console.log('[OK] 笔记已发布！');
  } else {
    console.log('[!] 未找到发布按钮，请手动点击发布');
    await page.waitForTimeout(10000); // 等待用户手动操作
  }

  const newCookies = await context.cookies();
  if (newCookies.length > 0) saveCookies(newCookies);
  await context.close();
}

// ── 检查状态 ──────────────────────────────────────────────────────────────
function checkStatus() {
  const cookies = loadCookies();
  if (!cookies) {
    console.log('Status: NOT_LOGGED_IN');
    console.log('Run: node xhs.js login');
    return;
  }
  const session = cookies.find(c => c.name === 'web_session');
  if (!session) {
    console.log('Status: NO_SESSION');
    return;
  }
  const expired = session.expires && session.expires < Date.now() / 1000;
  if (expired) {
    console.log('Status: SESSION_EXPIRED');
    console.log('Run: node xhs.js login');
    return;
  }
  console.log('Status: LOGGED_IN');
  console.log(`Cookie file: ${COOKIE_FILE}`);
  console.log(`Session expires: ${session.expires ? new Date(session.expires * 1000).toLocaleString('zh-CN') : 'session'}`);
}

module.exports = { login, search, getNoteDetail, publishNote, checkStatus, isLoggedIn, loadCookies };
