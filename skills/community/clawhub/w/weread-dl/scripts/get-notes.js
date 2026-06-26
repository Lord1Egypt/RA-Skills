/**
 * 微信读书标注/笔记拉取脚本
 *
 * 用法：
 *   node scripts/get-notes.js <bookId>
 *
 * 功能：
 * 1. 打开书籍阅读页，拦截 API 请求
 * 2. 获取全部书签（划线/高亮）和笔记
 * 3. 保存到 books/<书名>/notes.md（可读格式）
 *
 * 输出文件：
 *   - books/<书名>/notes.md        标注+笔记全文（Markdown 可读格式）
 *   - 更新 metadata.json 中的 notes/bookmarks 字段
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const COOKIES_FILE = path.join(__dirname, '..', 'profile', 'weread-cookies.json');
const BOOKS_DIR = path.join(__dirname, '..', 'books');

// 安全文件名
function safeName(s) { return s.replace(/[<>:"/\\|?*]/g, '_').replace(/_+/g,'_').replace(/^_|_$/g,''); }

// 解析 readInfo 拿到书名
function extractBookMeta(readInfo) {
  const info = readInfo?.bookInfo;
  if (!info) return null;
  return {
    bookId: info.bookId,
    title: info.title || '未知',
    author: info.author || '',
    url: `https://weread.qq.com/web/reader/${info.bookId}`,
  };
}

async function run() {
  const bidRaw = process.argv[2];
  if (!bidRaw) { console.error('Usage: node scripts/get-notes.js <bookId>'); process.exit(1); }
  // 从 URL 或纯 bookId 提取
  const m = bidRaw.match(/\/web\/reader\/([a-zA-Z0-9]+)/);
  const bid = m ? m[1] : bidRaw.replace(/[^a-zA-Z0-9]/g, '');
  if (!bid) { console.error('Invalid bookId'); process.exit(1); }

  if (!fs.existsSync(COOKIES_FILE)) { console.error('Not logged in, run login.js'); process.exit(1); }

  // 准备收集响应数据
  let bookmarkData = null;
  let reviewData = null;
  let readInfoData = null;

  const browser = await chromium.launch({ headless: true });
  try {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'zh-CN' });
    const page = await ctx.newPage();

    // API 拦截
    page.on('response', async resp => {
      const url = resp.url();
      try {
        // 注意：API 使用的 bookId 格式可能与阅读页 URL 不同（如带 CB_ 前缀）
        // 所以不按 bookId 过滤，只按 API 路径匹配
        if (url.includes('/web/book/bookmarklist')) {
          bookmarkData = await resp.json();
        }
        if (url.includes('/web/review/list')) {
          reviewData = await resp.json();
        }
        if (url.includes('/web/book/readInfo')) {
          readInfoData = await resp.json();
        }
      } catch(e) { /* ignore parse errors */ }
    });

    // 加载 cookies
    if (fs.existsSync(COOKIES_FILE)) {
      await ctx.addCookies(JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf-8')));
    }

    // 打开阅读页
    await page.goto(`https://weread.qq.com/web/reader/${bid}`, { waitUntil: 'networkidle', timeout: 25000 });
    await page.waitForTimeout(10000);

    // 从页面标题提取书名（兜底）
    const pageTitle = await page.title();
    const titleMatch = pageTitle.match(/^(.+?)\s*-\s*(.+?)\s*-\s*微信读书/);
    const fallbackTitle = titleMatch ? titleMatch[1].trim() : '未知';
    const fallbackAuthor = titleMatch ? titleMatch[2].trim() : '';

    // 确定书名
    const meta = extractBookMeta(readInfoData);
    const bookName = meta?.title || fallbackTitle;
    const author = meta?.author || fallbackAuthor;
    const slug = safeName(bookName);
    const bookDir = path.join(BOOKS_DIR, slug);
    if (!fs.existsSync(bookDir)) fs.mkdirSync(bookDir, { recursive: true });

    // ===== 整理标注（bookmarks） =====
    const bookmarks = [];
    if (bookmarkData?.updated) {
      for (const b of bookmarkData.updated) {
        bookmarks.push({
          chapterName: b.chapterName || '',
          chapterUid: b.chapterUid,
          text: b.markText || '',
          colorStyle: b.colorStyle,
          range: b.range,
          createTime: b.createTime ? new Date(b.createTime * 1000).toISOString() : '',
          bookmarkId: b.bookmarkId,
        });
      }
    }

    // ===== 整理笔记（reviews） =====
    const reviews = [];
    if (reviewData?.reviews) {
      for (const r of reviewData.reviews) {
        reviews.push({
          chapterName: r.review?.chapterName || '',
          chapterUid: r.review?.chapterUid,
          content: r.review?.content || '',
          abstract: r.review?.abstract || '',
          range: r.review?.range || '',
          createTime: r.review?.createTime ? new Date(r.review.createTime * 1000).toISOString() : '',
          reviewId: r.reviewId || '',
          type: r.review?.type,
        });
      }
    }

    // ===== 写入 notes.md =====
    const notesFile = path.join(bookDir, 'notes.md');
    let notesContent = `# 《${bookName}》标注与笔记\n\n`;
    notesContent += `> 作者：${author}\n> 更新：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n\n---\n\n`;

    if (bookmarks.length > 0) {
      notesContent += `## 📌 标注（共 ${bookmarks.length} 条）\n\n`;
      // 按章节分组
      const byChapter = {};
      for (const b of bookmarks) {
        const ch = b.chapterName || '(未知章节)';
        if (!byChapter[ch]) byChapter[ch] = [];
        byChapter[ch].push(b);
      }
      for (const [ch, items] of Object.entries(byChapter)) {
        notesContent += `### ${ch}\n\n`;
        for (const b of items) {
          notesContent += `> ${b.text}\n\n`;
        }
      }
    } else {
      notesContent += `## 📌 标注\n\n（暂无）\n\n`;
    }

    if (reviews.length > 0) {
      notesContent += `---\n\n## 📝 笔记（共 ${reviews.length} 条）\n\n`;
      for (const r of reviews) {
        notesContent += `### ${r.chapterName || '(未知章节)'}\n\n`;
        if (r.abstract) notesContent += `> ${r.abstract}\n\n`;
        notesContent += `${r.content}\n\n`;
      }
    } else {
      notesContent += `---\n\n## 📝 笔记\n\n（暂无）\n\n`;
    }

    fs.writeFileSync(notesFile, notesContent, 'utf-8');

    // ===== 更新 metadata.json =====
    const metaFile = path.join(bookDir, 'metadata.json');
    let metadata = {};
    if (fs.existsSync(metaFile)) {
      try { metadata = JSON.parse(fs.readFileSync(metaFile, 'utf-8')); } catch(e) {}
    }
    metadata.bookmarkCount = bookmarks.length;
    metadata.reviewCount = reviews.length;
    metadata.notesUpdatedAt = new Date().toISOString();
    if (meta) {
      metadata.bookId = meta.bookId || metadata.bookId || bid;
      metadata.title = meta.title || metadata.title || bookName;
      metadata.author = meta.author || metadata.author || author;
      metadata.url = meta.url || metadata.url || `https://weread.qq.com/web/reader/${bid}`;
    }
    fs.writeFileSync(metaFile, JSON.stringify(metadata, null, 2), 'utf-8');

    // ===== 输出统计 =====
    console.log(`\n📖 《${bookName}》`);
    console.log(`   作者: ${author}`);
    console.log(`   标注: ${bookmarks.length} 条`);
    console.log(`   笔记: ${reviews.length} 条`);
    console.log(`   已保存: ${notesFile}`);

    // 列出最新标注（最新的5条）
    const sorted = [...bookmarks].sort((a, b) => (b.createTime || '').localeCompare(a.createTime || ''));
    if (sorted.length > 0) {
      console.log(`\n📌 最新标注：`);
      for (const b of sorted.slice(0, 5)) {
        console.log(`   [${b.chapterName}] ${b.text.slice(0, 60)}${b.text.length > 60 ? '…' : ''}`);
      }
    }

  } finally {
    await browser.close();
  }
}

run().catch(e => { console.error(e); process.exit(1); });
