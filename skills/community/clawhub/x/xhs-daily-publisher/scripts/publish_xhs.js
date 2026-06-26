/**
 * 小红书自动发布机器人 · 通用模板
 * 由 xhs-auto-publisher skill 生成
 *
 * 使用说明：
 *   1. 修改 CONFIG 里的 WORKSPACE / POST_TITLE / POST_BODY / IMAGES_DIR
 *   2. 运行：node publish_xhs.js
 *   3. 首次会打开浏览器让你扫码登录小红书创作者中心
 *   4. 之后免登，自动完成上传图+填文案，停在发布页等你点"发布"
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// ============ 配置区 ============
const CONFIG = {
  WORKSPACE: process.env.XHS_WORKSPACE || process.cwd(),
  // 图片目录（内含 01.jpg ~ 09.jpg，最多 18 张）
  IMAGES_DIR: process.env.XHS_IMAGES_DIR || path.join(process.cwd(), 'output/images'),
  IMAGE_COUNT: parseInt(process.env.XHS_IMAGE_COUNT || '9', 10),
  POST_TITLE: process.env.XHS_POST_TITLE || '【请在 publish_xhs.js 里设置标题】',
  POST_BODY: process.env.XHS_POST_BODY || '【请在 publish_xhs.js 里设置正文】',
};
// =============================

const STATE_FILE = path.join(CONFIG.WORKSPACE, '.auth/xhs_cookies.json');
const USER_DATA_DIR = path.join(CONFIG.WORKSPACE, '.auth/chrome_profile');
const IMAGES = Array.from({ length: CONFIG.IMAGE_COUNT }, (_, i) =>
  path.join(CONFIG.IMAGES_DIR, String(i + 1).padStart(2, '0') + '.jpg')
);

const sleep = ms => new Promise(r => setTimeout(r, ms));
const ensureDir = d => { if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true }); };

async function loadCookies(page) {
  if (!fs.existsSync(STATE_FILE)) return false;
  try {
    const cookies = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
    if (!cookies.length) return false;
    await page.setCookie(...cookies);
    return true;
  } catch (e) { return false; }
}

async function saveCookies(page) {
  ensureDir(path.dirname(STATE_FILE));
  const cookies = await page.cookies('https://creator.xiaohongshu.com', 'https://www.xiaohongshu.com');
  fs.writeFileSync(STATE_FILE, JSON.stringify(cookies, null, 2));
}

function registerGracefulShutdown(browser, page) {
  let closing = false;
  const shutdown = async (sig) => {
    if (closing) return; closing = true;
    console.log(`\n↩ 收到 ${sig}，优雅关闭...`);
    try { if (page && !page.isClosed()) await saveCookies(page); } catch {}
    try { if (browser && browser.isConnected()) await browser.close(); } catch {}
    process.exit(0);
  };
  ['SIGINT', 'SIGTERM', 'SIGHUP'].forEach(s => process.on(s, () => shutdown(s)));
}

(async () => {
  console.log('\n========== 小红书自动发布 ==========\n');
  console.log('标题：' + CONFIG.POST_TITLE);
  console.log('图片目录：' + CONFIG.IMAGES_DIR);
  console.log('图片数量：' + CONFIG.IMAGE_COUNT + '\n');

  // 校验图片存在
  for (const img of IMAGES) {
    if (!fs.existsSync(img)) {
      console.error('✗ 找不到图片:', img);
      process.exit(1);
    }
  }

  ensureDir(USER_DATA_DIR);
  ensureDir(path.dirname(STATE_FILE));

  const browser = await puppeteer.launch({
    headless: false,
    defaultViewport: null,
    userDataDir: USER_DATA_DIR,
    ignoreDefaultArgs: ['--enable-automation'],
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--disable-infobars',
      '--disable-notifications',
      '--disable-popup-blocking',
      '--disable-features=TranslateUI',
      '--disable-ipc-flooding-protection',
      '--disable-background-timer-throttling',
      '--disable-backgrounding-occluded-windows',
      '--disable-renderer-backgrounding',
      '--no-first-run',
      '--no-default-browser-check',
      '--window-size=1440,960',
    ],
  });

  const pages = await browser.pages();
  const page = pages[0] || await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  registerGracefulShutdown(browser, page);

  const ctx = browser.defaultBrowserContext();
  await ctx.overridePermissions('https://creator.xiaohongshu.com', ['notifications', 'clipboard-read', 'clipboard-write']);
  await ctx.overridePermissions('https://www.xiaohongshu.com', ['notifications', 'clipboard-read', 'clipboard-write']);

  await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36');

  await loadCookies(page);

  console.log('→ 打开发布页');
  await page.goto('https://creator.xiaohongshu.com/publish/publish?source=official', {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await sleep(3000);

  if (page.url().includes('/login')) {
    console.log('⚡ 请扫码登录小红书创作者中心（本次登录后永久免登）');
    try {
      await page.waitForFunction(() => !location.href.includes('/login'), { timeout: 300000 });
      console.log('✓ 登录成功');
      await saveCookies(page);
      await sleep(2000);
      if (!page.url().includes('/publish')) {
        await page.goto('https://creator.xiaohongshu.com/publish/publish?source=official', { waitUntil: 'domcontentloaded' });
        await sleep(3000);
      }
    } catch (e) {
      console.log('✗ 5 分钟内未完成登录，退出');
      await browser.close();
      process.exit(1);
    }
  } else {
    await saveCookies(page);
  }

  await sleep(4000);

  // 切图文 tab
  try {
    await page.evaluate(() => {
      const tab = Array.from(document.querySelectorAll('*'))
        .find(el => el.children.length === 0 && (el.innerText || '').trim() === '上传图文');
      if (tab) tab.click();
    });
    await sleep(1500);
  } catch {}

  console.log('→ 上传' + CONFIG.IMAGE_COUNT + '张图');
  let input = await page.$('input[type="file"]');
  if (!input) {
    await page.waitForSelector('input[type="file"]', { timeout: 20000 }).catch(() => {});
    input = await page.$('input[type="file"]');
  }
  if (!input) {
    console.log('✗ 找不到上传入口。浏览器保持打开，可手动操作。');
    await new Promise(() => {});
  }
  await input.uploadFile(...IMAGES);
  await sleep(12000);

  console.log('→ 填标题');
  await page.evaluate((title) => {
    const cand = document.querySelector('input[placeholder*="标题"]')
              || document.querySelector('textarea[placeholder*="标题"]')
              || document.querySelector('input[placeholder*="填写标题"]');
    if (!cand) return false;
    const nat = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')
             || Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value');
    nat.set.call(cand, title);
    cand.dispatchEvent(new Event('input', { bubbles: true }));
    cand.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  }, CONFIG.POST_TITLE);

  console.log('→ 填正文');
  await page.evaluate(() => {
    const ed = document.querySelector('div[contenteditable="true"]');
    if (ed) ed.focus();
  });
  await sleep(600);
  await page.keyboard.type(CONFIG.POST_BODY, { delay: 5 });

  console.log('\n✓ 全部填完！请在浏览器中点"发布"按钮，然后关闭窗口。\n');

  browser.on('disconnected', () => {
    console.log('↩ 浏览器已关闭，脚本退出');
    process.exit(0);
  });
  setInterval(() => {}, 30000);
})().catch(err => {
  console.error('\n✗ 错误：', err.message);
  console.error(err.stack);
  process.exit(1);
});
