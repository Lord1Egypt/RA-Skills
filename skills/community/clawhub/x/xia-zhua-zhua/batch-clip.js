#!/usr/bin/env node
/**
 * batch-clip - 并发批量网页转 Markdown（支持 clip log 去重）
 * 用法: node batch-clip.js <url文件> [并发数] [输出目录]
 *
 * 新增:
 * - 自动跳过已抓过的URL（读取 ~/.clips/clips.json）
 * - --force 强制重新抓取
 * - WeChat 专用内容提取（#js_content）
 */

const { chromium } = require('playwright');
const TurndownService = require('turndown');
const fs = require('fs');
const path = require('path');
const url = require('url');

const lib = require('./clip-lib');

const DESKTOP = path.join(process.env.USERPROFILE || '', 'Desktop');
const DEFAULT_CONCURRENCY = 3;
const DEFAULT_OUTPUT = DESKTOP;
const MIN_DELAY = 1000;
const MAX_DELAY = 3000;

// ─── 元数据提取（复用 markdown-clip 的逻辑）───────────────

async function extractMetadata(page) {
  const getMeta = async (selectors) => {
    for (const sel of selectors) {
      try {
        const el = await page.$(sel);
        if (el) { const c = await el.getAttribute('content'); if (c) return c; }
      } catch {}
    }
    return '';
  };
  const isWeChat = page.url().includes('mp.weixin.qq.com');
  if (isWeChat) {
    try {
      const wc = await page.evaluate(() => ({
        title: document.querySelector('meta[property="og:title"]')?.getAttribute('content')
             || document.querySelector('#activity-name')?.innerText?.trim(),
        author: document.querySelector('meta[name="author"]')?.getAttribute('content')
              || document.querySelector('#js_name')?.innerText?.trim(),
        description: document.querySelector('meta[name="description"]')?.getAttribute('content')
                  || document.querySelector('meta[property="og:description"]')?.getAttribute('content'),
        cover: document.querySelector('meta[property="og:image"]')?.getAttribute('content'),
      }));
      if (wc.title || wc.author) return wc;
    } catch {}
  }
  return {
    title: await getMeta(['meta[property="og:title"]']),
    author: await getMeta(['meta[name="author"]', 'meta[property="article:author"]']),
    description: await getMeta(['meta[property="og:description"]', 'meta[name="description"]']),
    cover: await getMeta(['meta[property="og:image"]', 'meta[name="twitter:image"]']),
  };
}

async function extractContent(page) {
  const selectors = [
    'article', '[role="main"]', 'main',
    '.article-content', '.article-body', '.post-content',
    '.entry-content', '.content', '#content', '.post-body',
    '#js_content',      // WeChat 专用
    '.article-cont', '.detail-content',
  ];
  for (const sel of selectors) {
    try {
      const el = await page.$(sel);
      if (el) {
        const html = await page.evaluate((element) => {
          const clone = element.cloneNode(true);
          ['script', 'style', 'nav', 'footer', 'aside', 'iframe', 'noscript',
           '[class*="login"]', '[class*="sidebar"]', '[class*="related"]',
           '[class*="recommend"]', '[class*="advertisement"]',
           '#js_pc_qr_code', '.qr_code', '.qrcode',
          ].forEach(sel => { try { clone.querySelectorAll(sel).forEach(n => n.remove()); } catch {} });
          clone.querySelectorAll('a[href=""], a[href="#"]').forEach(a => {
            a.replaceWith(document.createTextNode(a.textContent.trim()));
          });
          return clone.innerHTML;
        }, el);
        if (html && html.replace(/<[^>]+>/g, '').length > 200) return html;
      }
    } catch {}
  }
  // 找不到正文时返回 null，让 clipOneUrl 决定是否 fallback 到 page.content()
  return null;
}

function buildFrontmatter(metadata, pageUrl) {
  const lines = ['---'];
  if (metadata.title) lines.push(`title: "${metadata.title.replace(/"/g, '\\"')}"`);
  if (metadata.author) lines.push(`author: "${metadata.author.replace(/"/g, '\\"')}"`);
  if (metadata.description) lines.push(`description: "${metadata.description.replace(/"/g, '\\"')}"`);
  if (metadata.cover) lines.push(`cover: "${metadata.cover}"`);
  lines.push(`source: ${pageUrl}`);
  lines.push(`clipped: ${new Date().toISOString()}`);
  lines.push('---\n');
  return lines.join('\n') + '\n';
}

function buildTurndown() {
  const td = new TurndownService({
    headingStyle: 'atx', codeBlockStyle: 'fenced',
    bulletListMarker: '-', linkStyle: 'inlined',
  });
  td.addRule('images', {
    filter: 'img',
    replacement: (content, node) => {
      const src = node.src || node.getAttribute('data-src') || '';
      if (!src) return '';
      return `![${node.alt || ''}](${src})`;
    },
  });
  td.addRule('pre', {
    filter: 'pre',
    replacement: (content, node) => {
      const code = node.querySelector('code');
      const lang = code ? code.className.replace('language-', '') : '';
      return `\n\`\`\`${lang}\n${code ? code.innerText : node.innerText}\n\`\`\`\n`;
    },
  });
  td.keep(['table']);
  return td;
}

function cleanMarkdown(md) {
  return md
    .replace(/\n{3,}/g, '\n\n')
    .replace(/^\s*\|.*\|\s*$/gm, '')
    .replace(/\[MathJax\].*/gi, '')
    .replace(/^\[\]\([^)]*\?ad_trace=[^)]*\)/g, '')
    .replace(/\[[^\]]*\]\([^)]*utm_[^)]*\)/g, '')
    .replace(/^\[\]\(.*\)\s*$/gm, '')
    .replace(/^\[Login\/Register\].*/gm, '')
    .trim();
}

// ─── 单条抓取 ──────────────────────────────────────────────

async function clipOneUrl(pageUrl, outputDir, force) {
  const timeout = 60000;
  const normalizedUrl = lib.normalizeUrl(pageUrl);

  // 去重检查
  if (!force) {
    const existing = lib.findClip(normalizedUrl);
    if (existing) {
      return { skipped: true, url: pageUrl, existing };
    }
  }

  const ua = lib.randomUA();
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox',
           '--disable-blink-features=AutomationControlled',
           '--no-first-run', '--no-zygote', '--disable-gpu'],
  });
  const context = await browser.newContext({
    userAgent: ua, viewport: { width: 1920, height: 1080 },
    locale: 'zh-CN', timezoneId: 'Asia/Shanghai',
  });
  // 反爬：仅隐藏 webdriver（最小化指纹伪造，避免触发 AV）
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
  });

  const page = await context.newPage();
  try {
    await page.goto(pageUrl, { waitUntil: 'domcontentloaded', timeout });
    await page.waitForTimeout(3000);
  } catch {
    await page.goto(pageUrl, { waitUntil: 'commit', timeout: 30000 });
    await page.waitForTimeout(5000);
  }

  const metadata = await extractMetadata(page);
  const htmlContent = await extractContent(page);

  // extractContent 找不到正文时用 page.content() 作为 fallback
  const rawHtml = htmlContent || await page.content();
  let markdown = buildTurndown().turndown(rawHtml);
  markdown = cleanMarkdown(markdown);
  markdown = buildFrontmatter(metadata, pageUrl) + markdown;

  const filename = lib.buildFilename(pageUrl, metadata.title, '.md');
  const outputPath = path.join(outputDir, filename);
  fs.writeFileSync(outputPath, markdown, 'utf8');

  lib.recordClip(pageUrl, { path: outputPath, metadata });
  await browser.close();
  return { success: true, url: pageUrl, path: outputPath, title: metadata.title };
}

// ─── 并发队列 ───────────────────────────────────────────────

function randomDelay() {
  return Math.floor(Math.random() * (MAX_DELAY - MIN_DELAY)) + MIN_DELAY;
}

async function worker(id, queue, results, outputDir, force, progress) {
  while (true) {
    const item = queue.shift();
    if (!item) break;

    const { url, index, total } = item;
    process.stdout.write(`\r  [${id}/${queue.length + progress.done + 1}] ${index}/${total}: ${url.substring(0, 50)}...`);

    try {
      const r = await clipOneUrl(url, outputDir, force);
      results.push(r);
    } catch (err) {
      results.push({ url, status: 'failed', error: err.message });
    }

    progress.done++;
    if (queue.length > 0) await new Promise(res => setTimeout(res, randomDelay()));
  }
}

// ─── 主入口 ────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log(`
📦 batch-clip - 并发批量网页转 Markdown（v2 去重版）

用法:
  node batch-clip.js <url文件> [并发数] [输出目录]

参数:
  url文件      每行一个URL，支持 # 注释
  并发数       同时浏览器数（默认 3，最大 10）
  输出目录     保存目录（默认桌面）

新功能:
  - 自动跳过已抓过的URL（clip log 去重）
  - 记录每次抓取到 ~/.clips/clips.json
  - WeChat 专用内容提取（#js_content）

示例:
  node batch-clip.js urls.txt
  node batch-clip.js urls.txt 5 ~/Desktop
`);
    process.exit(0);
  }

  const urlFile = args[0];
  const concurrency = Math.min(Math.max(parseInt(args[1]) || DEFAULT_CONCURRENCY, 1), 10);
  const outputDir = args[2] || DESKTOP;

  if (!fs.existsSync(urlFile)) {
    console.error(`❌ URL文件不存在: ${urlFile}`);
    process.exit(1);
  }

  const raw = fs.readFileSync(urlFile, 'utf-8');
  const urls = raw.split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#'));

  if (urls.length === 0) {
    console.error('❌ URL文件中没有有效URL');
    process.exit(1);
  }

  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  console.log(`\n📦 batch-clip 并发批量抓取`);
  console.log(`  URL数量: ${urls.length}  |  并发数: ${concurrency}  |  输出: ${outputDir}`);
  console.log('');

  const queue = urls.map((url, i) => ({ url, index: i + 1, total: urls.length }));
  const results = [];
  const progress = { done: 0 };

  await Promise.all(
    Array.from({ length: Math.min(concurrency, urls.length) }, (_, i) =>
      worker(i + 1, queue, results, outputDir, false, progress))
  );

  console.log('\n\n' + '─'.repeat(50));
  const success = results.filter(r => r.success);
  const skipped = results.filter(r => r.skipped);
  const failed = results.filter(r => r.status === 'failed');

  console.log(`\n📊 处理完成: ${results.length}/${urls.length}`);
  console.log(`  ✅ 成功: ${success.length}  |  ⏭️ 跳过(已存在): ${skipped.length}  |  ❌ 失败: ${failed.length}`);

  if (failed.length > 0) {
    console.log('\n失败列表:');
    failed.forEach(r => console.log(`  - ${r.url} (${r.error})`));
  }

  if (success.length > 0) {
    console.log('\n已保存文件:');
    success.forEach(r => console.log(`  ✅ ${path.basename(r.path)}`));
  }
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
