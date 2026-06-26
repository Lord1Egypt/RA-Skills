/**
 * 微信读书书架列表 — 列出书籍 + 阅读进度
 * 
 * 用法：
 *   node scripts/list-books.js
 * 
 * 依赖：profile/weread-cookies.json（由 login.js 生成）
 * 输出：JSON 格式的书籍列表（含阅读进度）
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SCRIPTS_DIR = __dirname;
const SKILL_DIR = path.resolve(SCRIPTS_DIR, '..');
const PROFILE_DIR = path.join(SKILL_DIR, 'profile');
const COOKIES_FILE = path.join(PROFILE_DIR, 'weread-cookies.json');
const OUTPUT_DIR = path.join(SKILL_DIR, 'output');

if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

async function loadCookies(context) {
  if (fs.existsSync(COOKIES_FILE)) {
    const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf-8'));
    await context.addCookies(cookies);
    return true;
  }
  return false;
}

async function listBooks() {
  if (!fs.existsSync(COOKIES_FILE)) {
    console.error('[weread] ❌ 未找到 cookies 文件，请先运行 login.js 登录');
    console.error('[weread]    运行: node scripts/login.js');
    process.exit(1);
  }

  console.log('[weread] 正在启动浏览器...');
  const browser = await chromium.launch({
    headless: true,
  });

  try {
    const context = await browser.newContext({
      viewport: { width: 1280, height: 800 },
      locale: 'zh-CN',
    });

    const page = await context.newPage();

    // 加载 cookies
    await loadCookies(context);

    // 拦截书架 API
    let shelfApiData = null;
    page.on('response', async (response) => {
      const url = response.url();
      try {
        if (url.includes('/web/shelf/sync') || url.includes('/web/book/shelf') || url.includes('/web/user/book/list')) {
          const body = await response.text();
          shelfApiData = { url, status: response.status(), body: body.substring(0, 10000) };
          console.log(`[weread] 📡 已拦截书架数据`);
        }
      } catch (e) {}
    });

    // 访问书架页
    console.log('[weread] 正在加载书架...');
    await page.goto('https://weread.qq.com/web/shelf', {
      waitUntil: 'networkidle',
      timeout: 20000,
    });

    // 检测是否登录成功
    const currentUrl = page.url();
    if (!currentUrl.includes('/web/shelf')) {
      console.error('[weread] ❌ 登录已过期，请重新运行 login.js 扫码登录');
      process.exit(1);
    }

    // 等待书架内容渲染
    await page.waitForTimeout(4000);

    // 从 DOM 中提取书籍和阅读进度
    const books = await page.evaluate(() => {
      const result = [];

      // 方法1: 查找所有书籍卡片
      const bookCards = document.querySelectorAll(
        '.bookList_item, ' +
        '[class*="bookItem"], ' +
        '[class*="shelfItem"], ' +
        'a[href*="/web/reader/"]:not([class*="nav"]):not([class*="header"])'
      );

      const seen = new Set();

      bookCards.forEach(card => {
        let link = card.getAttribute('href') || '';
        if (!link) {
          const a = card.querySelector('a[href*="/web/reader/"]');
          if (a) link = a.getAttribute('href') || '';
        }

        const match = link.match(/\/web\/reader\/([a-zA-Z0-9]+)/);
        const bookId = match ? match[1] : null;
        if (!bookId || seen.has(bookId)) return;
        seen.add(bookId);

        const titleEl = card.querySelector('[class*="title"], [class*="bookName"], [class*="name"]');
        const authorEl = card.querySelector('[class*="author"]');
        const coverEl = card.querySelector('img[src*="weread"]') || card.querySelector('img');
        const progressEl = card.querySelector('[class*="progress"], [class*="readPercent"], [class*="readInfo"]');

        result.push({
          bookId,
          title: titleEl ? titleEl.textContent.trim() : '未知书名',
          author: authorEl ? authorEl.textContent.trim() : '',
          cover: coverEl ? (coverEl.getAttribute('src') || '') : '',
          progress: progressEl ? progressEl.textContent.trim() : '',
          url: `https://weread.qq.com/web/reader/${bookId}`,
        });
      });

      // 方法2: 如果方法1没找到，尝试更广泛地扫描
      if (result.length === 0) {
        const allLinks = document.querySelectorAll('a');
        allLinks.forEach(a => {
          const href = a.getAttribute('href') || '';
          const match = href.match(/\/web\/reader\/([a-zA-Z0-9]+)/);
          if (match) {
            const id = match[1];
            if (seen.has(id)) return;
            seen.add(id);
            result.push({
              bookId: id,
              title: a.textContent?.trim()?.substring(0, 50) || '未知书名',
              author: '',
              cover: '',
              progress: '',
              url: `https://weread.qq.com/web/reader/${id}`,
            });
          }
        });
      }

      return result;
    });

    if (books.length === 0) {
      console.log('[weread] 书架为空或未检测到书籍');
      return [];
    }

    // 保存到文件
    const outputFile = path.join(OUTPUT_DIR, 'bookshelf.json');
    const outputData = {
      timestamp: new Date().toISOString(),
      total: books.length,
      books,
      shelfApiData: shelfApiData ? {
        captured: true,
        bodyLength: shelfApiData.body.length,
      } : { captured: false },
    };
    fs.writeFileSync(outputFile, JSON.stringify(outputData, null, 2), 'utf-8');

    // 打印结果
    console.log(`\n[weread] 📚 找到 ${books.length} 本书:\n`);
    books.forEach((book, i) => {
      console.log(`  ${i + 1}. ${book.title}`);
      if (book.author) console.log(`     作者: ${book.author}`);
      if (book.progress) console.log(`     进度: ${book.progress}`);
      console.log(`     ID: ${book.bookId}`);
      console.log(`     打开: weread open ${book.bookId}`);
      console.log();
    });

    // JSON 输出
    console.log('[weread] JSON 输出:');
    console.log(JSON.stringify(books, null, 2));

    return books;
  } finally {
    await browser.close();
    console.log('[weread] 浏览器已关闭');
  }
}

// 运行
listBooks()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error('[weread] 出错:', err.message);
    process.exit(1);
  });
