#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function cleanText(value = '') {
  return String(value).replace(/\s+/g, ' ').trim();
}

function truncateText(value = '', limit = 220) {
  const cleaned = cleanText(value);
  if (cleaned.length <= limit) return cleaned;
  return `${cleaned.slice(0, Math.max(limit - 1, 0)).trimEnd()}…`;
}

function resolvePlaywright(workspaceRoot) {
  const candidates = [
    'playwright',
    path.join(workspaceRoot, 'node_modules', 'playwright'),
    path.join(workspaceRoot, 'skills', 'wechat-studio', 'frontend', 'node_modules', 'playwright')
  ];

  for (const candidate of candidates) {
    try {
      return require(candidate);
    } catch (error) {
      continue;
    }
  }
  return null;
}

function classifyPage(html = '', finalUrl = '') {
  const body = cleanText(html);

  if (
    finalUrl.includes('wappoc_appmsgcaptcha') ||
    (body.includes('环境异常') && body.includes('完成验证后即可继续访问')) ||
    html.includes('id="js_verify"')
  ) {
    return {
      status: 'captcha_blocked',
      note: '浏览器仍停留在微信验证页，需要先完成验证后再继续抓取。',
      page_excerpt: truncateText(body, 220),
      content_found: false
    };
  }

  if (body.includes('参数错误') && body.includes('weui-msg__title')) {
    return {
      status: 'param_error',
      note: '浏览器打开后仍是参数错误页，当前链接不是可直接解析的标准文章页。',
      page_excerpt: truncateText(body, 220),
      content_found: false
    };
  }

  if (html.includes('id="js_content"') || html.includes('id=\\"js_content\\"') || html.includes('cover_url')) {
    return {
      status: 'article_page',
      note: '浏览器会话已经拿到文章正文 HTML。',
      page_excerpt: '',
      content_found: true
    };
  }

  return {
    status: 'unknown_extract_failure',
    note: '浏览器会话未命中文章正文，也未识别为已知验证或参数错误页。',
    page_excerpt: truncateText(body, 220),
    content_found: false
  };
}

function isRetryableNavigationError(error) {
  const message = cleanText(error && error.message ? error.message : error);
  return (
    message.includes('page is navigating and changing the content') ||
    message.includes('Execution context was destroyed') ||
    message.includes('Cannot find context with specified id') ||
    message.includes('Target page, context or browser has been closed')
  );
}

async function waitForStableSnapshot(page) {
  await page.waitForLoadState('domcontentloaded', { timeout: 3000 }).catch(() => {});
  const html = await page.content();
  const finalUrl = page.url();
  const pageTitle = cleanText(await page.title().catch(() => '')) || null;
  return { html, finalUrl, pageTitle };
}

async function main() {
  const [, , workspaceRoot, sourceUrl, profileDir, outputHtmlPath, headlessFlag] = process.argv;
  if (!workspaceRoot || !sourceUrl || !profileDir || !outputHtmlPath) {
    throw new Error('Usage: node fetch_article_html.js <workspaceRoot> <sourceUrl> <profileDir> <outputHtmlPath> [headlessFlag]');
  }

  const playwright = resolvePlaywright(workspaceRoot);
  if (!playwright) {
    throw new Error('Playwright dependency not found. Install playwright or reuse the existing frontend dependency first.');
  }

  fs.mkdirSync(profileDir, { recursive: true });
  fs.mkdirSync(path.dirname(outputHtmlPath), { recursive: true });

  const context = await playwright.chromium.launchPersistentContext(profileDir, {
    headless: headlessFlag === '1'
  });

  try {
    let page = context.pages()[0] || await context.newPage();
    await page.goto(sourceUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });

    const deadline = Date.now() + 90000;
    let html = '';
    let finalUrl = page.url();
    let pageTitle = null;
    let classification = { status: 'unknown_extract_failure', content_found: false, note: '', page_excerpt: '' };

    while (Date.now() < deadline) {
      await page.waitForTimeout(1500);
      const livePages = context.pages().filter((item) => !item.isClosed());
      if (livePages.length) {
        page = livePages[livePages.length - 1];
      }

      let snapshot;
      try {
        snapshot = await waitForStableSnapshot(page);
      } catch (error) {
        if (isRetryableNavigationError(error)) {
          continue;
        }
        throw error;
      }

      html = snapshot.html;
      finalUrl = snapshot.finalUrl;
      pageTitle = snapshot.pageTitle;
      classification = classifyPage(html, finalUrl);
      if (classification.content_found || classification.status === 'param_error') break;
      if (classification.status === 'captcha_blocked') {
        continue;
      }
    }

    if (classification.content_found) {
      fs.writeFileSync(outputHtmlPath, html, 'utf8');
    }

    process.stdout.write(JSON.stringify({
      done: classification.content_found,
      status: classification.status,
      note: classification.note,
      page_excerpt: classification.page_excerpt,
      final_url: finalUrl,
      page_title: pageTitle,
      output_html_path: classification.content_found ? outputHtmlPath : '',
      needs_manual_verification: classification.status === 'captcha_blocked'
    }));
  } finally {
    await context.close();
  }
}

main().catch((error) => {
  process.stderr.write(String(error && error.stack ? error.stack : error));
  process.exit(1);
});
