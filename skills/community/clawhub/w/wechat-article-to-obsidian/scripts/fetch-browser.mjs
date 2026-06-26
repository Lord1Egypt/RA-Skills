#!/usr/bin/env node
/**
 * Browser fallback fetcher for WeChat articles.
 * Usage: node fetch-browser.mjs <url> <output_html>
 */
import { writeFileSync } from 'fs';
import { createRequire } from 'module';

const url = process.argv[2];
const output = process.argv[3];

if (!url || !output) {
  console.error('Usage: node fetch-browser.mjs <url> <output_html>');
  process.exit(1);
}

const require = createRequire(import.meta.url);
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  try {
    ({ chromium } = require('/opt/homebrew/lib/node_modules/playwright'));
  } catch (err) {
    console.error('Cannot load playwright from local or global install');
    console.error(err?.stack || String(err));
    process.exit(1);
  }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch({
    channel: 'chrome',
    headless: true,
  });
  const page = await browser.newPage({
    userAgent:
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    locale: 'zh-CN',
  });

  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
    await sleep(2500);

    const data = await page.evaluate(() => {
      const qs = (sel) => document.querySelector(sel);
      const getText = (sel) => qs(sel)?.textContent?.trim() || '';
      const getHtml = (sel) => qs(sel)?.innerHTML || '';
      const meta = Array.from(document.querySelectorAll('meta')).reduce((acc, el) => {
        const k = el.getAttribute('property') || el.getAttribute('name');
        const v = el.getAttribute('content');
        if (k && v) acc[k] = v;
        return acc;
      }, {});

      return {
        title:
          window.msg_title ||
          meta['og:title'] ||
          getText('#activity-name') ||
          getText('.rich_media_title') ||
          document.title || '',
        author:
          window.nickname ||
          getText('#js_name') ||
          meta['author'] ||
          '',
        publishDate:
          getText('#publish_time') || '',
        contentHtml:
          getHtml('#js_content') ||
          getHtml('.rich_media_content') ||
          '',
      };
    });

    const escaped = (s) => String(s || '')
      .replace(/\\/g, '\\\\')
      .replace(/'/g, "\\'")
      .replace(/\n/g, ' ');

    const html = `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>${data.title || ''}</title>
<script>
function htmlDecode(s){return s;}
var msg_title = '${escaped(data.title)}';
var nickname = htmlDecode('${escaped(data.author)}');
var msg_link = '${escaped(url)}';
</script>
</head>
<body>
<h1 class="rich_media_title">${data.title || ''}</h1>
<div id="js_name">${data.author || ''}</div>
<div id="publish_time">${data.publishDate || ''}</div>
<div id="js_content">${data.contentHtml || ''}</div>
</body>
</html>`;

    writeFileSync(output, html, 'utf8');
    console.log(JSON.stringify({
      ok: true,
      title: data.title,
      author: data.author,
      publishDate: data.publishDate,
      contentLength: (data.contentHtml || '').length,
      output,
    }, null, 2));
  } finally {
    await page.close().catch(() => {});
    await browser.close().catch(() => {});
  }
})().catch((err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});
